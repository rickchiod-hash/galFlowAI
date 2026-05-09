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
from app.application.use_cases.render_video_use_case import RenderVideoUseCase
from app.application.use_cases.create_static_video_use_case import CreateStaticVideoUseCase
from app.application.use_cases.concat_videos_use_case import ConcatVideosUseCase
from app.adapters.wangp_adapter import WanGPAdapter
from app.adapters.tts_adapter import TTSAdapter
from app.adapters.ffmpeg_adapter import FFmpegAdapter
from app.config import BASE_DIR, PROJECTS_DIR

logger = logging.getLogger(__name__)

# TODO_TECNICO(VIDEO_PIPELINE):
# 1) Quebrar etapas em casos de uso independentes (gerar roteiro/cenas/prompts/render).
# 2) Padronizar estado de job (queued/running/succeeded/failed/canceled).
# 3) Adicionar testes e2e com mocks para fallback WanGP -> FFmpeg.
# 4) Isolar operações de filesystem em helpers para facilitar testes.


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
        # Initialize use cases for main pipeline logic
        self.generate_script_use_case = GenerateScriptUseCase()
        self.split_scenes_use_case = SplitScenesUseCase()
        self.build_prompts_use_case = BuildPromptsUseCase()
        self.generate_audio_use_case = GenerateAudioUseCase()
        self.render_video_use_case = RenderVideoUseCase()
        self.create_static_video_use_case = CreateStaticVideoUseCase()
        self.concat_videos_use_case = ConcatVideosUseCase()
        
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
            
            # 1. Gerar roteiro
            self._report_progress(progress_callback, 10, "Gerando roteiro...")
            script_result = self.generate_script_use_case.execute(
                briefing=f"{product}. {target_audience}",
                project_id=project_id
            )
            
            if not script_result.get("ok"):
                return {"success": False, "error": script_result.get("error", "Falha ao gerar roteiro")}
            
            script_text = script_result.get("data", {}).get("script", "")
            
            # Salva roteiro
            script_path = project_dir / "script" / "script_approved.md"
            script_path.parent.mkdir(exist_ok=True)
            script_path.write_text(script_text, encoding="utf-8")
            
            # 2. Dividir em cenas
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
            # Note: build_prompts_for_scenes is still used, but we can refactor later.
            from app.pipeline.prompt_builder import build_prompts_for_scenes
            scene_prompts = build_prompts_for_scenes(
                scenes=scenes,
                project_id=project_id
            )
            
            # Salva prompts
            prompts_path = project_dir / "prompts" / "prompts.json"
            prompts_path.parent.mkdir(exist_ok=True)
            prompts_path.write_text(
                json.dumps(scene_prompts, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            
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
            rendered_scenes = []
            
            for i, scene_prompt in enumerate(scene_prompts):
                self._report_progress(
                    progress_callback,
                    50 + (i / len(scene_prompts)) * 30,
                    f"Gerando cena {i+1}/{len(scene_prompts)}..."
                )
                
                scene_output = project_dir / "renders" / f"scene_{i:03d}.mp4"
                scene_output.parent.mkdir(exist_ok=True)
                
                # Try WanGP first
                render_result = self.render_video_use_case.execute(
                    project_id=project_id,
                    scene=scene_prompt
                )
                
                if render_result.get("ok"):
                    # WanGP succeeded
                    scene_prompt["status"] = "completed"
                    scene_prompt["video_path"] = render_result.get("data", {}).get("video_path")
                    rendered_scenes.append(scene_prompt)
                    continue
                
                # Fallback: FFmpeg (vídeo estático com texto)
                logger.info(f"WanGP não disponível, usando FFmpeg para cena {i}")
                # Usa scene_text ou prompt como texto
                text_for_video = scene_prompt.get("scene_text") or scene_prompt.get("prompt") or "Cena"
                static_video_result = self.create_static_video_use_case.execute(
                    project_id=project_id,
                    text=text_for_video,
                    output_name=f"scene_{i:03d}.mp4",
                    duration=scene_prompt.get("duration", 5)
                )
                
                if static_video_result.get("ok"):
                    scene_prompt["status"] = "completed"
                    scene_prompt["video_path"] = static_video_result.get("data", {}).get("video_path")
                    rendered_scenes.append(scene_prompt)
                    continue
                else:
                    scene_prompt["status"] = "failed"
                    scene_prompt["error"] = static_video_result.get("error", "Erro desconhecido")
            
            # Atualiza prompts com status
            prompts_path.write_text(
                json.dumps(scene_prompts, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            
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
