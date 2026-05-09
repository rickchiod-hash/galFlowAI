"""Script generation stage"""

from app.pipeline.stages.base_stage import BaseStage
from app.services.script_service import generate_script_with_llm
import logging

logger = logging.getLogger(__name__)


class ScriptGenerationStage(BaseStage):
    """Stage for generating video script from briefing"""
    
    def execute(self, briefing: str, mode: str = "safe", **kwargs) -> dict:
        """
        Generate script from briefing
        
        Args:
            briefing: Product description and target audience
            mode: Generation mode (safe, creative, etc.)
            **kwargs: Additional parameters
            
        Returns:
            Dict with script generation results
        """
        try:
            logger.info("Generating script...")
            script_result = generate_script_with_llm(
                briefing=briefing,
                mode=mode
            )
            
            if not script_result or "script" not in script_result:
                return self._create_result(False, error="Falha ao gerar roteiro")
            
            return self._create_result(True, {
                "script": script_result["script"],
                "raw_result": script_result
            })
            
        except Exception as e:
            logger.error(f"Error in script generation: {e}")
            return self._create_result(False, error=str(e))