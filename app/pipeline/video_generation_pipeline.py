"""Pipeline de geração de vídeo completo - Refatorado para usar use cases"""

import os
import sys
import logging
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.application.use_cases.generate_script_use_case import GenerateScriptUseCase
from app.application.use_cases.split_scenes_use_case import SplitScenesUseCase
from app.application.use_cases.build_prompts_use_case import BuildPromptsUseCase
from app.application.use_cases.generate_audio_use_case import GenerateAudioUseCase
from app.application.use_cases.concat_videos_use_case import ConcatVideosUseCase
from app.application.use_cases.render_all_scenes_use_case import RenderAllScenesUseCase
from app.adapters.wangp_adapter import WanGPAdapter
from app.adapters.tts_adapter import TTSAdapter
from app.adapters.ffmpeg_adapter import FFmpegAdapter
from app.config import BASE_DIR, PROJECTS_DIR
from app.core.app_error import AppError, Severity
from app.core.error_codes import ErrorCode
from app.domain.stage_logger import StageLogger
from app.pipeline.stage_gate import PipelineStage, get_failed_gates

logger = logging.getLogger(__name__)

# TODO(GAL-933, type=completed): Pipeline delega render de cenas a RenderAllScenesUseCase
# Contexto: Pipeline era monolithic — agora delega cada etapa a use case
# Dependência: ARCH-320 — concluída
# Critério de aceite: Pipeline delega cada etapa a use case com contrato definido
# Backlog: docs/project-control/05_BACKLOG_PRIORIZADO.md
#
# TODO(GAL-934, type=debt): Adicionar testes e2e com mocks para fallback WanGP -> FFmpeg
# Contexto: Sem teste pipeline que valide fallback chain
# Dependência: GAL-933
# Critério de aceite: Teste mockado cobre fallback WanGP falha → FFmpeg com logging
# Backlog: docs/project-control/05_BACKLOG_PRIORIZADO.md


class VideoGenerationPipeline:
    """Pipeline completo: Briefing -> Roteiro -> Cenas -> Vídeo -> Final"""
    
    def __init__(self, llm_provider=None):
        """
        Inicializa o pipeline.
        
        Args:
            llm_provider: Provider LLM para geração de roteiro (opcional)
        """
        self.llm_provider = llm_provider
        # Keep adapters for status checking
        self.wangp_adapter = WanGPAdapter()
        self.tts_adapter = TTSAdapter()
        self.ffmpeg_adapter = FFmpegAdapter()
        self._stage_logger = StageLogger("VideoGenerationPipeline")
        self._error_writer = None
        # Initialize use cases for main pipeline logic
        self.generate_script_use_case = GenerateScriptUseCase()
        self.split_scenes_use_case = SplitScenesUseCase()
        self.build_prompts_use_case = BuildPromptsUseCase()
        self.generate_audio_use_case = GenerateAudioUseCase()
        self.render_all_scenes_uc = RenderAllScenesUseCase()
        self.concat_videos_use_case = ConcatVideosUseCase()
        
    def _get_error_writer(self):
        if self._error_writer is None:
            from app.services.error_jsonl_writer import ErrorJsonlWriter
            self._error_writer = ErrorJsonlWriter()
        return self._error_writer

    def _check_stage_gate(self, stage: PipelineStage, project_id: str, context: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Check stage gates. Returns error dict if any gate fails, else None."""
        failed = get_failed_gates(stage, project_id, context)
        if failed:
            errors = [f.error for f in failed]
            gates = [f.gate for f in failed]
            logger.warning("Gate(s) blocked stage '%s': %s", stage.value, "; ".join(gates))
            return {
                "success": False,
                "gate": "; ".join(gates),
                "stage": stage.value,
                "error": "; ".join(errors),
            }
        return None

    def generate_commercial(
        self,
        project_id: str,
        product: str,
        target_audience: str,
        duration_seconds: int = 30,
        style: str = "viral",
        keywords: Optional[List[str]] = None,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Gera um comercial completo.
        
        Args:
            project_id: ID do projeto
            product: Nome do produto
            target_audience: Público-alvo
            duration_seconds: Duração total em segundos
            style: Estilo (viral, premium, direct)
            keywords: Palavras-chave
            progress_callback: Função de callback para progresso
            
        Returns:
            Dict com status e caminhos dos arquivos gerados
        """
        try:
            project_dir = Path(PROJECTS_DIR) / project_id
            project_dir.mkdir(parents=True, exist_ok=True)

            # [GATE] SCRIPT: project exists + briefing not empty
            briefing = f"{product}. {target_audience}"
            script_gate_err = self._check_stage_gate(
                PipelineStage.SCRIPT, project_id,
                {"briefing": briefing}
            )
            if script_gate_err:
                return script_gate_err

            # 1. Gerar roteiro (draft)
            self._report_progress(progress_callback, 10, "Gerando roteiro...")
            script_result = self.generate_script_use_case.execute(
                briefing=briefing,
                project_id=project_id
            )
            
            if not script_result.get("ok"):
                return {"success": False, "error": script_result.get("error", "Falha ao gerar roteiro")}
            
            script_text = script_result.get("data", {}).get("script", "")
            
            # Salva como draft (não approved — aprovação é manual)
            script_path = project_dir / "script" / "script_draft.md"
            script_path.parent.mkdir(exist_ok=True)
            script_path.write_text(script_text, encoding="utf-8")
            
            # Verifica se o roteiro foi aprovado antes de prosseguir
            approved_path = project_dir / "script" / "script_approved.md"
            if not approved_path.exists():
                script_draft_path = project_dir / "script" / "script_draft.md"
                return {
                    "success": False,
                    "error": "Roteiro não aprovado. Revise e aprove o roteiro em script_draft.md antes de gerar cenas.",
                    "script_draft": str(script_draft_path),
                    "script_preview": script_text[:500]
                }
            
            # Usa o texto aprovado (pode ter sido editado)
            script_text = approved_path.read_text(encoding="utf-8")
            
            # 2. Dividir em cenas (somente com roteiro aprovado)
            self._report_progress(progress_callback, 20, "Dividindo em cenas...")
            scenes_result = self.split_scenes_use_case.execute(
                script=script_text,
                project_id=project_id
            )
            
            if not scenes_result.get("ok"):
                return {"success": False, "error": scenes_result.get("error", "Falha ao dividir em cenas")}
                
            scenes = scenes_result.get("data", {}).get("scenes", [])
            
            if not scenes:
                return {"success": False, "error": "Falha ao dividir em cenas"}
            
            # Salva cenas
            scenes_path = project_dir / "storyboard" / "scenes.json"
            scenes_path.parent.mkdir(exist_ok=True)
            scenes_path.write_text(
                json.dumps(scenes, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            
            # 3. Gerar prompts para cada cena
            self._report_progress(progress_callback, 30, "Gerando prompts de vídeo...")
            prompts_result = self.build_prompts_use_case.execute(
                scenes=scenes,
                style=style,
                project_id=project_id
            )
            scene_prompts = prompts_result.get("data", {}).get("scenes", [])
            
            # 4. Gerar narração (TTS)
            self._report_progress(progress_callback, 40, "Gerando narração...")
            audio_result = self.generate_audio_use_case.execute(
                project_id=project_id,
                text=script_text,
                output_name="narration.wav"
            )
            
            audio_path = None
            if audio_result.get("ok"):
                audio_path = Path(audio_result.get("data", {}).get("audio_path", ""))
            
            # 5. Gerar vídeos das cenas (WanGP ou FFmpeg fallback)
            self._report_progress(progress_callback, 50, "Gerando vídeos das cenas...")
            render_all_result = self.render_all_scenes_uc.execute(
                project_id=project_id,
                scene_prompts=scene_prompts,
            )

            if not render_all_result.get("ok"):
                return {"success": False, "error": render_all_result.get("error", "Falha ao renderizar cenas")}

            rendered_scenes = render_all_result.get("data", {}).get("rendered_scenes", [])

            # Atualiza prompts com status
            prompts_path = project_dir / "prompts" / "scene_prompts.json"
            prompts_path.parent.mkdir(parents=True, exist_ok=True)
            prompts_path.write_text(
                json.dumps(scene_prompts, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            
            # [GATE] CONCAT: at least one rendered scene before concat
            concat_gate_err = self._check_stage_gate(
                PipelineStage.CONCAT, project_id,
                {"rendered_scenes": rendered_scenes}
            )
            if concat_gate_err:
                return concat_gate_err

            # 6. Montar vídeo final com FFmpeg
            self._report_progress(progress_callback, 85, "Montando vídeo final...")
            final_video_path = project_dir / "final" / "commercial.mp4"
            final_video_path.parent.mkdir(exist_ok=True)
            
            # Concatena todos os vídeos das cenas
            video_files = [s["video_path"] for s in rendered_scenes if s.get("video_path")]
            
            if not video_files:
                return {"success": False, "error": "Nenhum vídeo de cena foi gerado"}
            
            # Concatena vídeos (áudio é opcional)
            audio_for_concat = str(audio_path) if audio_path is not None and audio_path.exists() else None
            concat_result = self.concat_videos_use_case.execute(
                project_id=project_id,
                video_paths=video_files,
                output_name="commercial.mp4",
                audio_path=audio_for_concat
            )
            
            if not concat_result.get("ok"):
                err = AppError(
                    code=ErrorCode.FFMPEG_CONCAT_FAILED,
                    severity=Severity.ERROR,
                    message="Falha ao montar vídeo final: %s" % concat_result.get("error", ""),
                    suggestion="Valide o arquivo inputs.txt e verifique se todos os vídeos existem.",
                    stage="render",
                    retryable=True,
                    project_id=project_id,
                )
                self._get_error_writer().write(err)
                self._stage_logger.failure(
                    message="FFmpeg concat falhou",
                    cause=concat_result.get("error", "Erro desconhecido"),
                    correction="Valide inputs.txt e verifique ausência de arquivos corrompidos",
                )
                return {
                    "success": False,
                    "error": f"Falha ao montar vídeo final: {concat_result.get('error')}"
                }
            
            # 7. Finalizado
            self._report_progress(progress_callback, 100, "Comercial gerado com sucesso!")
            
            return {
                "success": True,
                "project_id": project_id,
                "final_video": str(final_video_path),
                "script_path": str(script_path),
                "scenes_count": len(rendered_scenes),
                "scenes_succeeded": len([s for s in rendered_scenes if s.get("status") == "completed"]),
                "narration_path": str(audio_path) if audio_path is not None and audio_path.exists() else None,
                "provider_used": "WanGP" if self.wangp_adapter.is_available() else "FFmpeg Fallback"
            }
            
        except Exception as e:
            logger.error(f"Erro no pipeline: {e}", exc_info=True)
            err = AppError(
                code=ErrorCode.UNKNOWN_ERROR,
                severity=Severity.ERROR,
                message="Erro no pipeline: %s" % e,
                suggestion="Consulte os logs técnicos para mais detalhes.",
                stage="render",
                retryable=True,
                project_id=project_id,
            )
            self._get_error_writer().write(err)
            self._stage_logger.failure(
                message="Pipeline abortado",
                cause=str(e),
                correction="Consulte os logs técnicos",
            )
            return {"success": False, "error": str(e)}
    
    def _report_progress(
        self,
        callback: Optional[callable],
        progress: int,
        message: str
    ):
        """Reporta progresso se callback fornecido"""
        if callback:
            callback(progress, message)
        logger.info(f"Progresso: {progress}% - {message}")
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Retorna status dos componentes do pipeline"""
        return {
            "llm_available": self.llm_provider is not None,
            "wangp_available": self.wangp_adapter.is_available(),
            "tts_available": self.tts_adapter.is_available(),
            "ffmpeg_available": self.ffmpeg_adapter.is_available(),
            "selected_tts_engine": self.tts_adapter.selected_engine
        }
