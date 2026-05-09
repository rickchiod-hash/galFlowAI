"""Scene splitting stage"""

from app.pipeline.stages.base_stage import BaseStage
from app.pipeline.scene_splitter import split_script_into_scenes
import logging

logger = logging.getLogger(__name__)


class SceneSplittingStage(BaseStage):
    """Stage for splitting script into scenes"""
    
    def execute(self, script_text: str, project_id: str, **kwargs) -> dict:
        """
        Split script into scenes
        
        Args:
            script_text: The script text to split
            project_id: Project identifier (for logging)
            **kwargs: Additional parameters
            
        Returns:
            Dict with scene splitting results
        """
        try:
            logger.info(f"Splitting script into scenes for project {project_id}")
            scenes = split_script_into_scenes(
                script_text=script_text,
                project_id=project_id
            )
            
            if not scenes:
                return self._create_result(False, error="Falha ao dividir em cenas")
            
            return self._create_result(True, {
                "scenes": scenes
            })
            
        except Exception as e:
            logger.error(f"Error in scene splitting: {e}")
            return self._create_result(False, error=str(e))