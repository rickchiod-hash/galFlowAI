"""Use case for rendering all scenes with WanGP -> FFmpeg fallback."""
from typing import Dict, Any, List, Optional
from app.application.use_cases.base_use_case import BaseUseCase
from app.application.use_cases.render_video_use_case import RenderVideoUseCase
from app.application.use_cases.create_static_video_use_case import CreateStaticVideoUseCase
from app.domain.stage_logger import StageLogger
from app.core.app_error import AppError, Severity
from app.core.error_codes import ErrorCode
from app.logging_config import setup_logger

logger = setup_logger()


class RenderAllScenesUseCase(BaseUseCase):
    """Render all scenes with automatic WanGP -> FFmpeg fallback per scene.

    3-point standard:
    1. Validate project_id and scene_prompts
    2. Render each scene (WanGP first, FFmpeg static fallback)
    3. Return rendered scenes list with status per scene
    """

    def __init__(self, render_video_uc=None, create_static_video_uc=None):
        self._render_video_uc = render_video_uc or RenderVideoUseCase()
        self._create_static_video_uc = create_static_video_uc or CreateStaticVideoUseCase()
        self._stage_logger = StageLogger("RenderAllScenes")
        self._error_writer = None

    def _get_error_writer(self):
        if self._error_writer is None:
            from app.services.error_jsonl_writer import ErrorJsonlWriter
            self._error_writer = ErrorJsonlWriter()
        return self._error_writer

    def execute(self, project_id: str, scene_prompts: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            if not self._validate(project_id=project_id, scene_prompts=scene_prompts):
                return self._build_error("Invalid project_id or scene_prompts")

            rendered_scenes = []

            for i, scene_prompt in enumerate(scene_prompts):
                render_result = self._render_video_uc.execute(
                    project_id=project_id,
                    scene=scene_prompt
                )

                if render_result.get("ok"):
                    scene_prompt["status"] = "completed"
                    scene_prompt["video_path"] = render_result.get("data", {}).get("video_path")
                    rendered_scenes.append(scene_prompt)
                    continue

                logger.info("WanGP nao disponivel, usando FFmpeg para cena %d", i)
                err = AppError(
                    code=ErrorCode.WANGP_UNAVAILABLE,
                    severity=Severity.WARN,
                    message="WanGP indisponivel para cena %d" % i,
                    suggestion="FFmpeg fallback usado automaticamente.",
                    stage="render",
                    retryable=True,
                    project_id=project_id,
                    fallback_used=True,
                )
                self._get_error_writer().write(err)
                self._stage_logger.warning(
                    message="WanGP falhou para cena %d, usando FFmpeg" % i,
                    cause="WanGP nao disponivel ou retornou erro",
                    correction="FFmpeg fallback ativado automaticamente",
                )

                text_for_video = (
                    scene_prompt.get("scene_text")
                    or scene_prompt.get("prompt")
                    or "Cena"
                )
                static_result = self._create_static_video_uc.execute(
                    project_id=project_id,
                    text=text_for_video,
                    output_name="scene_%03d.mp4" % i,
                    duration=scene_prompt.get("duration", 5),
                )

                if static_result.get("ok"):
                    scene_prompt["status"] = "completed"
                    scene_prompt["video_path"] = static_result.get("data", {}).get("video_path")
                    rendered_scenes.append(scene_prompt)
                else:
                    scene_prompt["status"] = "failed"
                    scene_prompt["error"] = static_result.get("error", "Erro desconhecido")
                    err2 = AppError(
                        code=ErrorCode.FFMPEG_NOT_FOUND,
                        severity=Severity.ERROR,
                        message="FFmpeg fallback tambem falhou para cena %d" % i,
                        suggestion="Verifique se FFmpeg esta instalado.",
                        stage="render",
                        retryable=True,
                        project_id=project_id,
                        fallback_used=True,
                    )
                    self._get_error_writer().write(err2)
                    self._stage_logger.failure(
                        message="FFmpeg fallback falhou para cena %d" % i,
                        cause="FFmpeg nao disponivel ou erro ao gerar video estatico",
                        correction="Verifique instalacao do FFmpeg",
                    )

            return self._build_success(
                data={"rendered_scenes": rendered_scenes, "count": len(rendered_scenes)},
                project_id=project_id
            )
        except Exception as e:
            logger.error("Erro ao renderizar cenas: %s", e, exc_info=True)
            return self._build_error(str(e), project_id=project_id)

    def _validate(self, **kwargs) -> bool:
        project_id = kwargs.get("project_id", "")
        scene_prompts = kwargs.get("scene_prompts", [])
        return bool(project_id and scene_prompts)
