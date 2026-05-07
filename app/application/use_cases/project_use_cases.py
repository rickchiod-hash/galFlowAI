"""Use cases for project management.
3-point standard: Validate -> Execute -> Return result.
"""
from typing import Dict, Any
from app.application.use_cases.base import UseCase, UseCaseError
from app.project_manager import create_project

class CreateProjectUseCase(UseCase):
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


class LoadProjectUseCase(UseCase):
    """Load existing project data.
    
    3-point standard:
    1. Validate project_id
    2. Load project from disk
    3. Return project data
    """
    
    def execute(self, project_id: str) -> Dict[str, Any]:
        """Execute project loading use case."""
        try:
            # 1. Validate input
            if not self._validate(project_id=project_id):
                return self._build_error("Invalid project_id")
            
            # 2. Execute business logic
            from app.project_manager import load_project
            project_data = load_project(project_id)
            
            if not project_data:
                return self._build_error("Project not found", project_id=project_id)
            
            # 3. Return result with status
            return self._build_success(
                data=project_data,
                project_id=project_id
            )
        except Exception as e:
            return self._build_error(str(e), project_id=project_id)
    
    def _validate(self, **kwargs) -> bool:
        """Validate project_id."""
        project_id = kwargs.get("project_id", "")
        return bool(project_id)
