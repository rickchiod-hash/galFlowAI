"""Use case for concatenating videos using FFmpeg."""
from typing import Dict, Any, List, Optional
from app.application.use_cases.base_use_case import BaseUseCase
from app.adapters.ffmpeg_adapter import FFmpegAdapter


class ConcatVideosUseCase(BaseUseCase):
    """Concatenate videos using FFmpeg adapter.
    
    3-point standard:
    1. Validate input parameters
    2. Concatenate videos using FFmpeg
    3. Return final video path and metadata
    """

    def execute(self, project_id: str, video_paths: List[str], 
                output_name: str = "commercial.mp4",
                audio_path: Optional[str] = None) -> Dict[str, Any]:
        """Execute video concatenation use case."""
        try:
            # 1. Validate input
            if not self._validate(project_id=project_id, video_paths=video_paths):
                return self._build_error("Invalid project_id or video_paths")

            # 2. Execute business logic
            adapter = FFmpegAdapter()
            if not adapter.is_available():
                return self._build_error("FFmpeg not available", project_id=project_id)

            # Create output directory
            from app.config import PROJECTS_DIR
            from pathlib import Path
            project_dir = Path(PROJECTS_DIR) / project_id
            output_dir = project_dir / "final"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = str(output_dir / output_name)

            # Concatenate videos
            result = adapter.concat_videos(
                video_paths=video_paths,
                output_path=output_path,
                audio_path=audio_path
            )

            # 3. Return result with status
            if result.get("success"):
                return self._build_success(
                    data={
                        "video_path": output_path,
                        "input_count": len(video_paths),
                        "has_audio": audio_path is not None
                    },
                    project_id=project_id
                )
            else:
                return self._build_error(
                    f"FFmpeg failed to concatenate videos: {result.get('error')}",
                    project_id=project_id
                )
        except Exception as e:
            return self._build_error(str(e), project_id=project_id)

    def _validate(self, **kwargs) -> bool:
        """Validate project_id and video_paths."""
        project_id = kwargs.get("project_id", "")
        video_paths = kwargs.get("video_paths", [])
        return bool(project_id and isinstance(video_paths, list) and len(video_paths) > 0)