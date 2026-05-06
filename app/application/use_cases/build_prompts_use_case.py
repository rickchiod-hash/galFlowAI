"""Use case for building scene prompts."""
from typing import Dict, Any
from app.application.use_cases.base_use_case import BaseUseCase
from app.pipeline.prompt_builder import build_prompts_for_scenes, save_prompts

class BuildPromptsUseCase(BaseUseCase):
    """Build prompts for video scenes.
    
    3-point standard:
    1. Validate scenes and style
    2. Build prompts for each scene
    3. Save prompts and return result
    """
    
    def execute(self, scenes: list, style: str, project_id: str) -> Dict[str, Any]:
        """Execute prompt building use case."""
        try:
            # 1. Validate input
            if not self._validate(scenes=scenes, style=style, project_id=project_id):
                return self._build_error("Invalid scenes, style or project_id")
            
            # 2. Execute business logic
            scenes_with_prompts = build_prompts_for_scenes(scenes, style)
            save_prompts(project_id, scenes_with_prompts)
            
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
