"""Use case for splitting script into scenes."""
from typing import Dict, Any, Optional
from pathlib import Path
from app.application.use_cases.base_use_case import BaseUseCase
from app.pipeline.scene_splitter import split_script_into_scenes, save_scenes
from app.config import PROJECTS_DIR

class SplitScenesUseCase(BaseUseCase):
    """Split script into scenes.
    
    UI-202: Blocks scene splitting if script is not approved.
    
    3-point standard:
    1. Validate script and project_id; check script approval
    2. Split script into scenes
    3. Save scenes and return result
    """
    
    def execute(self, script: str, project_id: str) -> Dict[str, Any]:
        """Execute scene splitting use case."""
        try:
            # 1. Validate input
            if not self._validate(script=script, project_id=project_id):
                return self._build_error("Invalid script or project_id")
            
            # 2. Check script approval (UI-202 gate)
            if not self._is_script_approved(project_id):
                return self._build_error(
                    "Script not approved. Approve script before splitting into scenes.",
                    project_id=project_id
                )
            
            # 3. Execute business logic
            scenes = split_script_into_scenes(script, project_id)
            save_scenes(project_id, scenes)
            
            # 4. Return result with status
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
    
    def _is_script_approved(self, project_id: str) -> bool:
        """Check if script is approved by verifying script_approved.md exists."""
        project_dir = Path(PROJECTS_DIR) / project_id
        approved_file = project_dir / "script" / "script_approved.md"
        return approved_file.exists()
