"""
Use case for script generation.
"""
from typing import Dict, Any
from app.application.use_cases.base import UseCase, UseCaseError
from app.services.script_service import generate_script_with_llm


class GenerateScriptUseCase(UseCase):
    """Use case for generating scripts with LLM providers."""
    
    def execute(self, briefing: str, provider: str = "auto") -> Dict[str, Any]:
        """
        Generate script using LLM providers.
        
        Args:
            briefing: Text briefing for the commercial
            provider: Provider name or 'auto'
            
        Returns:
            Dictionary with script and metadata
        """
        try:
            result = generate_script_with_llm(briefing, provider)
            return {
                "success": True,
                "script": result.get("script", ""),
                "provider_used": result.get("provider", "Unknown"),
                "fallback_used": result.get("quality", "fallback") == "fallback",
                "response_time_seconds": result.get("time", 0),
                "quality_score": 0,
                "script_markdown": result.get("script", ""),
                "script_json": {},
                "logs": []
            }
        except Exception as e:
            raise UseCaseError("SCRIPT_GENERATION_FAILED", str(e))


class SaveManualEditUseCase(UseCase):
    """Use case for saving manual script edits."""
    
    def execute(self, project_id: str, script_markdown: str, version_note: str = None) -> Dict[str, Any]:
        """Save manually edited script."""
        from app.services.script_service import save_manual_edit
        try:
            result = save_manual_edit(project_id, script_markdown, version_note)
            return {
                "success": True,
                "version": result.get("version")
            }
        except Exception as e:
            raise UseCaseError("SAVE_EDIT_FAILED", str(e))


class ImproveScriptUseCase(UseCase):
    """Use case for improving existing script."""
    
    def execute(self, project_id: str, briefing: str = "") -> Dict[str, Any]:
        """Improve existing script."""
        from app.services.script_service import improve_script
        try:
            result = improve_script(project_id, briefing)
            return {
                "success": True,
                "script": result.get("script")
            }
        except Exception as e:
            raise UseCaseError("IMPROVE_FAILED", str(e))


class ApproveScriptUseCase(UseCase):
    """Use case for approving script."""
    
    def execute(self, project_id: str) -> Dict[str, Any]:
        """Approve script for production."""
        from app.services.script_service import approve_script
        try:
            result = approve_script(project_id)
            return {
                "success": True,
                "script": result.get("script")
            }
        except Exception as e:
            raise UseCaseError("APPROVE_FAILED", str(e))
