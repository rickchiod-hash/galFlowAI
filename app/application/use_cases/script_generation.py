"""
Use case for script generation.
3-point standard: Validate -> Execute -> Return result.
"""
from typing import Dict, Any
from app.application.use_cases.base import UseCase, UseCaseError
from app.services.script_service import generate_script_with_llm, generate_script_with_provider
from app.pipeline.script_generator import save_script


class GenerateScriptUseCase(UseCase):
    """Use case for generating scripts with LLM providers.
    
    3-point standard:
    1. Validate briefing and provider
    2. Generate script using LLM providers
    3. Save script and return result with status
    """
    
    def execute(self, briefing: str, project_id: str = "", provider: str = "auto") -> Dict[str, Any]:
        """
        Generate script using LLM providers.
        
        Args:
            briefing: Text briefing for the commercial
            project_id: Project identifier for saving script
            provider: Provider name or 'auto'
            
        Returns:
            Dictionary with script and metadata
        """
        try:
            # 1. Validate input
            if not self._validate(briefing=briefing, project_id=project_id):
                return self._build_error("Invalid briefing or project_id")
            
            # 2. Execute business logic
            if provider and provider != "auto":
                result = generate_script_with_provider(briefing, provider)
            else:
                result = generate_script_with_llm(briefing, "auto")
            if project_id:
                save_script(project_id, result.get("script", ""))
            
            # 3. Return result with status
            return self._build_success(
                data={
                    "script": result.get("script", ""),
                    "provider_used": result.get("provider", "Unknown"),
                    "fallback_used": result.get("quality", "fallback") == "fallback",
                    "response_time_seconds": result.get("time", 0),
                    "quality_score": 0
                },
                project_id=project_id
            )
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        """Validate briefing and project_id."""
        briefing = kwargs.get("briefing", "")
        project_id = kwargs.get("project_id", "")
        # briefing is required, project_id is optional (for saving)
        return bool(briefing and len(briefing.strip()) >= 10)


class SaveManualEditUseCase(UseCase):
    """Use case for saving manual script edits.
    
    3-point standard:
    1. Validate project_id and script_markdown
    2. Save manual edit as new version
    3. Return version info
    """
    
    def execute(self, project_id: str, script_markdown: str, version_note: str = None) -> Dict[str, Any]:
        """Save manually edited script."""
        try:
            # 1. Validate input
            if not self._validate(project_id=project_id, script_markdown=script_markdown):
                return self._build_error("Invalid project_id or script_markdown")
            
            # 2. Execute business logic
            from app.services.script_service import save_manual_edit
            result = save_manual_edit(project_id, script_markdown, version_note)
            
            # 3. Return result with status
            return self._build_success(
                data={"version": result.get("version")},
                project_id=project_id
            )
        except Exception as e:
            return self._build_error(str(e), project_id=project_id)
    
    def _validate(self, **kwargs) -> bool:
        """Validate project_id and script_markdown."""
        project_id = kwargs.get("project_id", "")
        script_markdown = kwargs.get("script_markdown", "")
        return bool(project_id and script_markdown)


class ImproveScriptUseCase(UseCase):
    """Use case for improving existing script.
    
    3-point standard:
    1. Validate project_id
    2. Improve existing script using LLM
    3. Return improved script
    """
    
    def execute(self, project_id: str, briefing: str = "") -> Dict[str, Any]:
        """Improve existing script."""
        try:
            # 1. Validate input
            if not self._validate(project_id=project_id):
                return self._build_error("Invalid project_id")
            
            # 2. Execute business logic
            from app.services.script_service import improve_script
            result = improve_script(project_id, briefing)
            
            # 3. Return result with status
            return self._build_success(
                data={"script": result.get("script")},
                project_id=project_id
            )
        except Exception as e:
            return self._build_error(str(e), project_id=project_id)
    
    def _validate(self, **kwargs) -> bool:
        """Validate project_id."""
        project_id = kwargs.get("project_id", "")
        return bool(project_id)


class ApproveScriptUseCase(UseCase):
    """Use case for approving script.
    
    3-point standard:
    1. Validate project_id
    2. Approve script for production
    3. Return approval status
    """
    
    def execute(self, project_id: str) -> Dict[str, Any]:
        """Approve script for production."""
        try:
            # 1. Validate input
            if not self._validate(project_id=project_id):
                return self._build_error("Invalid project_id")
            
            # 2. Execute business logic
            from app.services.script_service import approve_script
            result = approve_script(project_id)
            
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
