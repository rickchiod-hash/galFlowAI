"""Text optimization stage"""

from app.pipeline.stages.base_stage import BaseStage
from app.pipeline.voice_script_optimizer import VoiceScriptOptimizer
import logging

logger = logging.getLogger(__name__)


class TextOptimizationStage(BaseStage):
    """Stage for optimizing scene texts for TTS"""
    
    def __init__(self, max_chars_per_scene: int = 150):
        super().__init__()
        self.optimizer = VoiceScriptOptimizer(max_chars_per_scene=max_chars_per_scene)
    
    def execute(self, scene_prompts: list, **kwargs) -> dict:
        """
        Optimize texts in scene prompts for TTS
        
        Args:
            scene_prompts: List of scene prompt dictionaries
            **kwargs: Additional parameters (can include max_chars_per_scene)
            
        Returns:
            Dict with text optimization results
        """
        try:
            logger.info(f"Optimizing texts for {len(scene_prompts)} scenes")
            
            # Allow overriding max_chars_per_scene from kwargs
            max_chars = kwargs.get('max_chars_per_scene', 150)
            if max_chars != self.optimizer.max_chars_per_scene:
                self.optimizer = VoiceScriptOptimizer(max_chars_per_scene=max_chars)
            
            optimized_scenes = self.optimizer.optimize_scenes_batch(scene_prompts)
            
            return self._create_result(True, {
                "optimized_scenes": optimized_scenes
            })
            
        except Exception as e:
            logger.error(f"Error in text optimization: {e}")
            return self._create_result(False, error=str(e))