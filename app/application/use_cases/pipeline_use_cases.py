"""Use cases for pipeline operations (scenes, prompts, storyboard).
3-point standard: Validate -> Execute -> Return result.
"""
from typing import Dict, Any, List
from app.application.use_cases.base import UseCase, UseCaseError
from app.domain.scene_parser import split_script_into_scenes
from app.repositories.scene_repository import SceneRepository
from app.domain.prompt_builder_service import build_prompts_for_scenes
from app.repositories.prompt_repository import PromptRepository
from app.adapters.ffmpeg_adapter import create_storyboard_video
from app.hardware import get_gpu_info, get_recommended_preset

class SplitScenesUseCase(UseCase):
    """Split script into scenes.
    
    3-point standard:
    1. Validate script and project_id
    2. Split script into scenes
    3. Save scenes and return result
    """
    
    def execute(self, script: str, project_id: str) -> Dict[str, Any]:
        """Execute scene splitting use case."""
        try:
            # 1. Validate input
            if not self._validate(script=script, project_id=project_id):
                return self._build_error("Invalid script or project_id")
            
            # 2. Execute business logic
            scenes = split_script_into_scenes(script, project_id)
            SceneRepository(project_id).save_scenes(scenes)
            
            # 3. Return result with status
            return self._build_success(
                data={"scenes": scenes, "count": len(scenes)},
                project_id=project_id
            )
        except Exception as e:
            return self._build_error(str(e), project_id=project_id)
    
    def _validate(self, **kwargs) -> bool:
        """Validate script and project_id."""
        script = kwargs.get("script", "")
        project_id = kwargs.get("project_id", "")
        return bool(script and project_id)


class BuildPromptsUseCase(UseCase):
    """Build prompts for video scenes.
    
    3-point standard:
    1. Validate scenes and style
    2. Build prompts for each scene
    3. Save prompts and return result
    """
    
    def execute(self, scenes: List[Dict], style: str, project_id: str) -> Dict[str, Any]:
        """Execute prompt building use case."""
        try:
            # 1. Validate input
            if not self._validate(scenes=scenes, style=style, project_id=project_id):
                return self._build_error("Invalid scenes, style or project_id")
            
            # 2. Execute business logic
            scenes_with_prompts = build_prompts_for_scenes(scenes, project_id)
            PromptRepository(project_id).save_prompts(scenes_with_prompts)
            
            # 3. Return result with status
            return self._build_success(
                data={"scenes": scenes_with_prompts, "count": len(scenes_with_prompts)},
                project_id=project_id
            )
        except Exception as e:
            return self._build_error(str(e), project_id=project_id)
    
    def _validate(self, **kwargs) -> bool:
        """Validate scenes, style and project_id."""
        scenes = kwargs.get("scenes", [])
        style = kwargs.get("style", "")
        project_id = kwargs.get("project_id", "")
        return bool(scenes and style and project_id)


class CreateStoryboardUseCase(UseCase):
    """Create storyboard video from scenes.
    
    3-point standard:
    1. Validate project_id and scenes
    2. Generate storyboard using FFmpeg
    3. Return video path
    """
    
    def execute(self, project_id: str, scenes: List[Dict]) -> Dict[str, Any]:
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
