"""Prompt building stage"""

from app.pipeline.stages.base_stage import BaseStage
from app.pipeline.prompt_builder import build_prompts_for_scenes
import logging

logger = logging.getLogger(__name__)


class PromptBuildingStage(BaseStage):
    """Stage for building video prompts for scenes"""
    
    def execute(self, scenes: list, project_id: str, **kwargs) -> dict:
        """
        Build prompts for scenes
        
        Args:
            scenes: List of scene dictionaries
            project_id: Project identifier (for logging)
            **kwargs: Additional parameters
            
        Returns:
            Dict with prompt building results
        """
        try:
            logger.info(f"Building prompts for {len(scenes)} scenes for project {project_id}")
            scene_prompts = build_prompts_for_scenes(
                scenes=scenes,
                project_id=project_id
            )
            
            return self._create_result(True, {
                "scene_prompts": scene_prompts
            })
            
        except Exception as e:
            logger.error(f"Error in prompt building: {e}")
            return self._create_result(False, error=str(e))