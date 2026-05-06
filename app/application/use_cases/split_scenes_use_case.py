"""Use case for splitting script into scenes."""
from typing import Dict, Any
from app.application.use_cases.base_use_case import BaseUseCase
from app.pipeline.scene_splitter import split_script_into_scenes, save_scenes

class SplitScenesUseCase(BaseUseCase):
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
            save_scenes(project_id, scenes)
            
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
