"""Use case for creating static video using FFmpeg (fallback)."""
from typing import Dict, Any
from app.application.use_cases.base_use_case import BaseUseCase
from app.adapters.ffmpeg_adapter import FFmpegAdapter


class CreateStaticVideoUseCase(BaseUseCase):
    """Create static video using FFmpeg adapter (fallback when WanGP not available).
    
    3-point standard:
    1. Validate input parameters
    2. Create static video using FFmpeg
    3. Return video path and metadata
    """

    def execute(self, project_id: str, text: str, output_name: str = "scene.mp4",
                duration: int = 5, width: int = 854, height: int = 480,
                bg_color: str = "303030", text_color: str = "FFFFFF") -> Dict[str, Any]:
        """Execute static video creation use case."""
        try:
            # 1. Validate input
            if not self._validate(project_id=project_id, text=text):
                return self._build_error("Invalid project_id or text")

            # 2. Execute business logic
            adapter = FFmpegAdapter()
            if not adapter.is_available():
                return self._build_error("FFmpeg not available", project_id=project_id)

            # Create output directory
            from app.config import PROJECTS_DIR
            from pathlib import Path
            project_dir = Path(PROJECTS_DIR) / project_id
            output_dir = project_dir / "renders"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = str(output_dir / output_name)

            # Create static video
            result = adapter.create_static_video(
                text=text,
                output_path=output_path,
                duration=duration,
                width=width,
                height=height,
                bg_color=bg_color,
                text_color=text_color
            )

            # 3. Return result with status
            if result.get("success"):
                return self._build_success(
                    data={
                        "video_path": output_path,
                        "text": text,
                        "duration": duration
                    },
                    project_id=project_id
                )
            else:
                return self._build_error(
                    f"FFmpeg failed to create static video: {result.get('error')}",
                    project_id=project_id
                )
        except Exception as e:
            return self._build_error(str(e), project_id=project_id)

    def _validate(self, **kwargs) -> bool:
        """Validate project_id and text."""
        project_id = kwargs.get("project_id", "")
        text = kwargs.get("text", "")
        return bool(project_id and text and len(text.strip()) > 0)