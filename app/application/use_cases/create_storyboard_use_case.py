"""Use case for creating storyboard video."""
from typing import Dict, Any
from app.application.use_cases.base_use_case import BaseUseCase
from app.adapters.ffmpeg_adapter import create_storyboard_video
from app.hardware import get_gpu_info, get_recommended_preset

class CreateStoryboardUseCase(BaseUseCase):
    """Create storyboard video from scenes.
    
    3-point standard:
    1. Validate project_id and scenes
    2. Generate storyboard using FFmpeg
    3. Return video path
    """
    
    def execute(self, project_id: str, scenes: list) -> Dict[str, Any]:
        """Execute storyboard creation use case."""
        try:
            # 1. Validate input
            if not self._validate(project_id=project_id, scenes=scenes):
                return self._build_error("Invalid project_id or scenes")
            
            # 2. Execute business logic
            gpu = get_gpu_info()
            preset = get_recommended_preset(gpu["vram_gb"], gpu["name"])
            video_path = create_storyboard_video(project_id, scenes)
            
            # 3. Return result with status
            return self._build_success(
                data={
                    "video_path": str(video_path) if video_path else None,
                    "preset": preset["model"]
                },
                project_id=project_id
            )
        except Exception as e:
            return self._build_error(str(e), project_id=project_id)
    
    def _validate(self, **kwargs) -> bool:
        """Validate project_id and scenes."""
        project_id = kwargs.get("project_id", "")
        scenes = kwargs.get("scenes", [])
        return bool(project_id and scenes)
