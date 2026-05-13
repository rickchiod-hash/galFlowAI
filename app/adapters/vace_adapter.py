"""Adapter para Wan VACE 1.3B - Motor de video futuro opcional.

VACE (Video Editing, Mask, Compositing) e um modelo de edicao de video
(ref: mascara, keyframe, composicao). Nao implementado como adapter completo
- registrado como futuro opcional. EngineType.VACE NAO e selecionado
automaticamente pelo EngineRouter.
"""

import os
import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

import app.config as config
from app.core.app_error import AppError, Severity
from app.core.error_codes import ErrorCode
from app.domain.stage_logger import StageLogger

logger = logging.getLogger(__name__)

_VACE_DEFAULT = str(config.ENGINES_DIR / "VACE")


class VAceAdapter:
    """Adapter para Wan VACE 1.3B - Motor de video futuro opcional.

    Segue o mesmo padrao do WanGPAdapter (RND-600, RND-610).
    NAO e selecionado automaticamente - uso explicito.
    """

    @staticmethod
    def disponivel() -> bool:
        """Verifica se VACE esta disponivel (metodo estatico para testes)."""
        vace_path = _VACE_DEFAULT
        if not os.path.exists(vace_path):
            return False
        possible_main_files = ["main.py", "vace_interface.py", "inference.py"]
        for file in possible_main_files:
            if os.path.exists(os.path.join(vace_path, file)):
                return True
        return False

    def __init__(self, vace_path: Optional[str] = None, project_id: str = ""):
        self.vace_path = vace_path or _VACE_DEFAULT
        self._project_id = project_id
        self.available = self._check_availability()
        self.model_preset = "1.3B"
        self.resolution = "720p"
        self._stage_logger = StageLogger("VAceAdapter", project_id=project_id)
        self._error_writer = None
        self._render_count = 0
        self._render_success_count = 0
        self._render_fail_count = 0
        self._total_duration_ms = 0.0

    def _get_error_writer(self):
        if self._error_writer is None:
            from app.services.error_jsonl_writer import ErrorJsonlWriter
            self._error_writer = ErrorJsonlWriter()
        return self._error_writer

    def _check_availability(self) -> bool:
        """Verifica se VACE esta disponivel."""
        if not os.path.exists(self.vace_path):
            logger.info("VACE nao encontrado em: %s", self.vace_path)
            return False

        possible_main_files = ["main.py", "vace_interface.py", "inference.py"]
        main_found = False
        for file in possible_main_files:
            if os.path.exists(os.path.join(self.vace_path, file)):
                self.main_file = file
                main_found = True
                break

        if not main_found:
            logger.info("Arquivo principal do VACE nao encontrado em %s", self.vace_path)
            return False

        try:
            import torch
            return True
        except ImportError:
            logger.warning(
                "CAUSA: PyTorch nao encontrado no ambiente | "
                "CORRECAO: Instale PyTorch para usar VACE"
            )
            return False

    def is_available(self) -> bool:
        return self.available

    def render_scene(self, project_id: str, scene: dict, preset: dict = None) -> dict:
        """Render a single scene using generate_video().

        Called by RenderVideoUseCase with the scene dict format.
        Maps scene fields to generate_video parameters.
        """
        self._stage_logger.start(
            message="Renderizando cena %s com VACE" % scene.get("id", scene.get("scene_number", "?"))
        )
        prompt = scene.get("prompt", scene.get("description", "Cena sem descricao"))
        scene_id = scene.get("id", scene.get("scene_number", "000"))
        output_path = scene.get("output_path", "")
        if not output_path:
            from app.config import PROJECTS_DIR
            output_dir = Path(PROJECTS_DIR) / project_id / "renders"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(output_dir / ("scene_%s.mp4" % str(scene_id).zfill(3)))
        duration = scene.get("duration", scene.get("duration_estimate", 5))
        neg_prompt = scene.get("prompt_negative", scene.get("negative_prompt", ""))
        res = None
        if preset:
            res = preset.get("resolution")
        return self.generate_video(
            prompt=prompt,
            output_path=output_path,
            negative_prompt=neg_prompt,
            duration_seconds=int(duration),
            resolution=res,
        )

    def generate_video(
        self,
        prompt: str,
        output_path: str,
        negative_prompt: str = "",
        duration_seconds: int = 5,
        num_frames: int = 24,
        resolution: Optional[str] = None,
        progress_callback: Optional[callable] = None,
    ) -> Dict[str, Any]:
        """Gera video usando VACE.

        VACE e futuro opcional. Se nao estiver disponivel,
        retorna erro com fallback_suggested=True.
        """
        start_time = time.time()
        self._render_count += 1

        if not self.available:
            self._render_fail_count += 1
            err = AppError(
                code=ErrorCode.WANGP_UNAVAILABLE,
                severity=Severity.WARN,
                message="VACE nao esta disponivel",
                suggestion="Use FFmpeg fallback ou WanGP.",
                stage="render",
                retryable=True,
                project_id=self._project_id,
            )
            self._get_error_writer().write(err)
            self._stage_logger.warning(
                message="VACE nao disponivel para render",
                cause="VACE nao encontrado ou PyTorch ausente",
                correction="Use FFmpeg fallback ou WanGP",
            )
            elapsed_ms = (time.time() - start_time) * 1000
            return {
                "success": False,
                "error": "VACE nao esta disponivel",
                "fallback_suggested": True,
                "duration_ms": elapsed_ms,
            }

        resolution = resolution or self.resolution
        try:
            cmd = self._build_command(
                prompt=prompt,
                output_path=output_path,
                negative_prompt=negative_prompt,
                duration_seconds=duration_seconds,
                num_frames=num_frames,
                resolution=resolution,
            )

            import subprocess
            logger.info("Executando VACE: %s", " ".join(cmd))
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.vace_path,
            )
            stdout, stderr = process.communicate()
            elapsed_ms = (time.time() - start_time) * 1000
            self._total_duration_ms += elapsed_ms

            if process.returncode == 0:
                self._render_success_count += 1
                self._stage_logger.success(
                    message="Render VACE concluido",
                    duration_ms=elapsed_ms,
                )
                return {
                    "success": True,
                    "video_path": output_path,
                    "prompt": prompt,
                    "model": self.model_preset,
                    "resolution": resolution,
                    "duration": duration_seconds,
                    "provider": "VACE",
                    "duration_ms": elapsed_ms,
                }
            else:
                self._render_fail_count += 1
                err = AppError(
                    code=ErrorCode.UNKNOWN_ERROR,
                    severity=Severity.ERROR,
                    message="VACE falhou ao gerar video",
                    suggestion="Verifique se VACE esta instalado e configurado.",
                    stage="render",
                    retryable=True,
                    project_id=self._project_id,
                    details={"stderr": stderr[:500]},
                )
                self._get_error_writer().write(err)
                self._stage_logger.failure(
                    message="Erro VACE: %s" % stderr[:200],
                    cause="Processo VACE retornou codigo %d" % process.returncode,
                    correction="Verifique se VACE esta instalado e configurado",
                )
                return {
                    "success": False,
                    "error": stderr,
                    "fallback_suggested": True,
                    "duration_ms": elapsed_ms,
                }

        except Exception as e:
            elapsed_ms = (time.time() - start_time) * 1000
            self._total_duration_ms += elapsed_ms
            self._render_fail_count += 1
            err = AppError(
                code=ErrorCode.UNKNOWN_ERROR,
                severity=Severity.ERROR,
                message="Excecao ao executar VACE: %s" % e,
                suggestion="Verifique ambiente e dependencias.",
                stage="render",
                retryable=True,
                project_id=self._project_id,
            )
            self._get_error_writer().write(err)
            self._stage_logger.failure(
                message="Excecao VACE: %s" % e,
                cause="Excecao nao tratada no adapter VACE",
                correction="Verifique ambiente e dependencias",
            )
            return {
                "success": False,
                "error": str(e),
                "fallback_suggested": True,
                "duration_ms": elapsed_ms,
            }

    def _build_command(self, **kwargs) -> List[str]:
        """Converte comando para execucao do VACE."""
        python_exe = self._get_python_executable()
        cmd = [
            python_exe,
            "main.py",
            "--prompt", kwargs["prompt"],
            "--output", kwargs["output_path"],
            "--model", kwargs.get("model_preset", "1.3B"),
            "--resolution", kwargs.get("resolution", "720p"),
            "--frames", str(kwargs.get("num_frames", 24)),
            "--duration", str(kwargs.get("duration_seconds", 5)),
        ]
        if kwargs.get("negative_prompt"):
            cmd.extend(["--negative_prompt", kwargs["negative_prompt"]])
        return cmd

    def _get_python_executable(self) -> str:
        """Retorna caminho do Python para executar VACE."""
        studio_python = str(config.BASE_DIR / "envs" / "studio" / "Scripts" / "python.exe")
        if os.path.exists(studio_python):
            return studio_python
        return "python"

    def get_status(self) -> Dict[str, Any]:
        """Retorna status do adapter."""
        return {
            "available": self.available,
            "path": self.vace_path,
            "model_preset": self.model_preset,
            "resolution": self.resolution,
        }

    def get_metrics(self) -> Dict[str, Any]:
        """Retorna metricas de telemetria do adapter."""
        return {
            "render_count": self._render_count,
            "render_success_count": self._render_success_count,
            "render_fail_count": self._render_fail_count,
            "total_duration_ms": self._total_duration_ms,
            "avg_duration_ms": (
                self._total_duration_ms / self._render_count
                if self._render_count > 0 else 0.0
            ),
        }

    def get_stage_events(self) -> List[Dict[str, Any]]:
        """Retorna eventos estruturados do StageLogger."""
        return [
            {
                "stage": e.stage,
                "event_type": e.event_type,
                "message": e.message,
                "cause": e.cause,
                "correction": e.correction,
                "duration_ms": e.duration_ms,
                "timestamp": e.timestamp,
            }
            for e in self._stage_logger.events
        ]
