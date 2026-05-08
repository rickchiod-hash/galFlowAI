"""Template Provider - fallback that generates minimal script without external dependencies."""

from app.application.result import Result


class TemplateProvider:
    """Generates minimal script template when no LLM is available."""
    
    def generate(self, briefing: str, **kwargs) -> Result:
        """Generate a minimal script from briefing."""
        try:
            # Generate a simple 2-scene script
            lines = []
            lines.append("Cena 1: " + briefing[:50])
            lines.append("Cena 2: Continuação da história")
            
            script = "\n".join(lines)
            
            return Result.success(
                data={
                    "script": script,
                    "provider": "TemplateProvider",
                    "time": 0.01,
                    "quality": "template"
                }
            )
        except Exception as e:
            return Result.failure(error=str(e))