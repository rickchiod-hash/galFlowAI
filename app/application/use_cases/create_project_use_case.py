"""Use case for project creation."""
from typing import Dict, Any
from app.application.use_cases.base_use_case import BaseUseCase
from app.project_manager import create_project

class CreateProjectUseCase(BaseUseCase):
    """Create new video commercial project.
    
    3-point standard:
    1. Validate project name
    2. Create project structure
    3. Return project data
    """
    
    def execute(self, project_name: str) -> Dict[str, Any]:
        """Execute project creation use case."""
        try:
            # 1. Validate input
            if not self._validate(project_name=project_name):
                return self._build_error("Invalid project name")
            
            # 2. Execute business logic
            project_data = create_project(project_name)
            
            # 3. Return result with status
            return self._build_success(
                data=project_data,
                project_id=project_data.get("id")
            )
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        """Validate project name."""
        project_name = kwargs.get("project_name", "")
        return bool(project_name and len(project_name.strip()) > 0)
