"""Audio generation stage with artifact caching (PIPE-402)."""

from app.pipeline.stages.base_stage import BaseStage
import logging
from pathlib import Path
from app.application.use_cases.artifact_cache_use_cases import (
    CheckArtifactCacheUseCase,
    StoreArtifactUseCase
)

logger = logging.getLogger(__name__)


class AudioGenerationStage(BaseStage):
    """Stage for generating audio for scenes with artifact caching.
    
    3-point standard with caching:
    1. Validate scene_prompts input
    2. Check artifact cache for existing audio files
    3. If cached: return cached audio paths
       If not cached: generate audio, save, cache, and return result
    """
    
    def __init__(self, tts_adapter):
        super().__init__()
        self.tts_adapter = tts_adapter
        self.check_cache_use_case = CheckArtifactCacheUseCase()
        self.store_cache_use_case = StoreArtifactUseCase()

    def execute(self, scene_prompts: list, project_id: str, **kwargs) -> dict:
        """
        Generate audio for each scene with artifact caching.
        
        Args:
            scene_prompts: List of scene prompt dictionaries
            project_id: Project identifier (for file paths)
            **kwargs: Additional parameters
            
        Returns:
            Dict with audio generation results
        """
        try:
            # 1. Validate input
            if not self._validate(scene_prompts=scene_prompts, project_id=project_id):
                return self._create_result(False, error="Invalid scene prompts or project ID")
            
            # Create audio directory
            audio_dir = Path(kwargs.get('projects_dir', '')) / project_id / "audio"
            audio_dir.mkdir(parents=True, exist_ok=True)
            
            # Process each scene
            updated_scenes = []
            cache_hits = 0
            total_scenes = len([s for s in scene_prompts if s.get("scene_text")])
            
            for i, scene_prompt in enumerate(scene_prompts):
                scene_text = scene_prompt.get("scene_text", "")
                
                # Create a copy of the scene to avoid modifying original
                updated_scene = scene_prompt.copy()
                
                if scene_text:
                    # 2. Check artifact cache for existing audio
                    artifact_key = self._generate_artifact_key(scene_text, project_id)
                    cache_result = self.check_cache_use_case.execute(
                        artifact_key=artifact_key,
                        content=None,  # Just check existence
                        artifact_type="file"
                    )
                    
                    if cache_result["ok"] and cache_result["data"].get("cached"):
                        # Return cached audio path
                        cached_audio_path = cache_result["data"]["content"]
                        updated_scene["audio_path"] = str(cached_audio_path)
                        updated_scene["audio_success"] = True
                        updated_scene["cache_hit"] = True
                        cache_hits += 1
                        logger.info("Using cached audio for scene %s (key: %s...)", 
                                   i, artifact_key[:12])
                    else:
                        # 3. Not cached - generate audio
                        scene_audio_path = audio_dir / f"scene_{i:03d}.wav"
                        
                        tts_result = self.tts_adapter.generate_audio(
                            text=scene_text,
                            output_path=str(scene_audio_path)
                        )
                        
                        if tts_result.get("success"):
                            updated_scene["audio_path"] = str(scene_audio_path)
                            updated_scene["audio_success"] = True
                            
                            # Cache the generated audio file
                            store_result = self.store_cache_use_case.execute(
                                artifact_key=artifact_key,
                                content=scene_audio_path,
                                artifact_type="file"
                            )
                            
                            if not store_result["ok"]:
                                logger.warning("Failed to cache audio: %s", 
                                             store_result.get("error", "Unknown error"))
                            
                            logger.info("Generated and cached audio for scene %s: %s", 
                                       i, scene_audio_path)
                        else:
                            updated_scene["audio_success"] = False
                            updated_scene["audio_error"] = tts_result.get("error", "Erro desconhecido")
                            logger.warning(f"Falha ao gerar áudio para cena {i}: {tts_result.get('error')}")
                else:
                    updated_scene["audio_success"] = False
                    updated_scene["audio_error"] = "Texto da cena vazio"
                    logger.warning(f"Texto vazio para cena {i}, pulando geração de áudio")
                
                updated_scenes.append(updated_scene)
            
            # 4. Return result with status
            return self._create_result(True, {
                "scenes_with_audio": updated_scenes,
                "audio_dir": str(audio_dir),
                "cache_hits": cache_hits,
                "total_scenes": total_scenes,
                "cache_hit_rate": cache_hits / max(total_scenes, 1)
            })
            
        except Exception as e:
            logger.error(f"Error in audio generation: {e}")
            return self._create_result(False, error=str(e))
    
    def _generate_artifact_key(self, scene_text: str, project_id: str) -> str:
        """Generate a unique artifact key for audio generation caching.
        
        Includes: scene text content and project_id.
        """
        import hashlib
        import json
        
        # Create deterministic representation of inputs
        key_data = {
            "scene_text": scene_text,
            "project_id": project_id
        }
        canonical = json.dumps(key_data, sort_keys=True)
        return f"audio_gen:{hashlib.sha256(canonical.encode('utf-8')).hexdigest()}"
    
    def _validate(self, **kwargs) -> bool:
        """Validate scene_prompts and project_id."""
        scene_prompts = kwargs.get("scene_prompts", [])
        project_id = kwargs.get("project_id", "")
        
        if not isinstance(scene_prompts, list):
            return False
        if not project_id:
            return False
            
        # Validate each scene_prompt has required fields
        for scene_prompt in scene_prompts:
            if not isinstance(scene_prompt, dict):
                return False
                
        return True