"""Audio generation stage"""

from app.pipeline.stages.base_stage import BaseStage
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class AudioGenerationStage(BaseStage):
    """Stage for generating audio for scenes"""
    
    def __init__(self, tts_adapter):
        super().__init__()
        self.tts_adapter = tts_adapter
    
    def execute(self, scene_prompts: list, project_id: str, **kwargs) -> dict:
        """
        Generate audio for each scene
        
        Args:
            scene_prompts: List of scene prompt dictionaries
            project_id: Project identifier (for file paths)
            **kwargs: Additional parameters
            
        Returns:
            Dict with audio generation results
        """
        try:
            logger.info(f"Generating audio for {len(scene_prompts)} scenes")
            
            # Create audio directory
            audio_dir = Path(kwargs.get('projects_dir', '')) / project_id / "audio"
            audio_dir.mkdir(parents=True, exist_ok=True)
            
            # Process each scene
            updated_scenes = []
            for i, scene_prompt in enumerate(scene_prompts):
                scene_audio_path = audio_dir / f"scene_{i:03d}.wav"
                scene_text = scene_prompt.get("scene_text", "")
                
                # Create a copy of the scene to avoid modifying original
                updated_scene = scene_prompt.copy()
                
                if scene_text:
                    tts_result = self.tts_adapter.generate_audio(
                        text=scene_text,
                        output_path=str(scene_audio_path)
                    )
                    
                    if tts_result.get("success"):
                        updated_scene["audio_path"] = str(scene_audio_path)
                        updated_scene["audio_success"] = True
                        logger.info(f"Áudio gerado para cena {i}: {scene_audio_path}")
                    else:
                        updated_scene["audio_success"] = False
                        updated_scene["audio_error"] = tts_result.get("error", "Erro desconhecido")
                        logger.warning(f"Falha ao gerar áudio para cena {i}: {tts_result.get('error')}")
                else:
                    updated_scene["audio_success"] = False
                    updated_scene["audio_error"] = "Texto da cena vazio"
                    logger.warning(f"Texto vazio para cena {i}, pulando geração de áudio")
                
                updated_scenes.append(updated_scene)
            
            return self._create_result(True, {
                "scenes_with_audio": updated_scenes,
                "audio_dir": str(audio_dir)
            })
            
        except Exception as e:
            logger.error(f"Error in audio generation: {e}")
            return self._create_result(False, error=str(e))