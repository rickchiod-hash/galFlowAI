"""Use case for script approval."""
from typing import Dict, Any
from app.application.use_cases.base_use_case import BaseUseCase
from app.services.script_service import approve_script as approve_script_service

class ApproveScriptUseCase(BaseUseCase):
    """Approve script for production.
    
    3-point standard:
    1. Validate project_id
    2. Approve current script
    3. Return approval status
    """
    
    def execute(self, project_id: str) -> Dict[str, Any]:
        """Execute script approval use case."""
        try:
            # 1. Validate input
            if not self._validate(project_id=project_id):
                return self._build_error("Invalid project_id")
            
            # 2. Execute business logic
            result = approve_script_service(project_id)
            
            # 3. Return result with status
            if result.get("ok"):
                return self._build_success(
                    data={"script": result.get("script"), "status": result.get("status")},
                    project_id=project_id
                )
            else:
                return self._build_error(result.get("error", "Approval failed"), project_id=project_id)
        except Exception as e:
            return self._build_error(str(e), project_id=project_id)
    
    def _validate(self, **kwargs) -> bool:
        """Validate project_id."""
        project_id = kwargs.get("project_id", "")
        return bool(project_id)
