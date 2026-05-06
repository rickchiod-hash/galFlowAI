"""Use case for script generation."""
from typing import Dict, Any
from app.application.use_cases.base_use_case import BaseUseCase
from app.services.script_service import generate_script_with_llm
from app.pipeline.script_generator import save_script

class GenerateScriptUseCase(BaseUseCase):
    """Generate commercial script from briefing.
    
    3-point standard:
    1. Validate briefing input
    2. Generate script using LLM providers
    3. Save script and return result
    """
    
    def execute(self, briefing: str, project_id: str, mode: str = "auto") -> Dict[str, Any]:
        """Execute script generation use case."""
        try:
            # 1. Validate input
            if not self._validate(briefing=briefing, project_id=project_id):
                return self._build_error("Invalid input parameters")
            
            # 2. Execute business logic
            result = generate_script_with_llm(briefing, mode)
            save_script(project_id, result["script"])
            
            # 3. Return result with status
            return self._build_success(
                data={
                    "script": result["script"],
                    "provider": result["provider"],
                    "time": result["time"],
                    "quality": result["quality"]
                },
                project_id=project_id
            )
        except Exception as e:
            return self._build_error(str(e), project_id=project_id)
    
    def _validate(self, **kwargs) -> bool:
        """Validate briefing and project_id."""
        briefing = kwargs.get("briefing", "")
        project_id = kwargs.get("project_id", "")
        return bool(briefing and len(briefing.strip()) >= 10 and project_id)
