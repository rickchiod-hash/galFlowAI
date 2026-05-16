"""Scene splitting stage with artifact caching (PIPE-402)."""

from app.pipeline.stages.base_stage import BaseStage
from app.domain.scene_parser import split_script_into_scenes
from app.repositories.scene_repository import SceneRepository
from app.application.use_cases.artifact_cache_use_cases import (
    CheckArtifactCacheUseCase,
    StoreArtifactUseCase
)
import logging
import json

logger = logging.getLogger(__name__)


class SceneSplittingStage(BaseStage):
    """Stage for splitting script into scenes with artifact caching.
    
    3-point standard with caching:
    1. Validate script_text input
    2. Check artifact cache for existing scenes
    3. If cached: return cached scenes
       If not cached: split script, save, cache, and return result
    """
    
    def __init__(self):
        super().__init__()
        self.check_cache_use_case = CheckArtifactCacheUseCase()
        self.store_cache_use_case = StoreArtifactUseCase()

    def execute(self, script_text: str, project_id: str, **kwargs) -> dict:
        """
        Split script into scenes with artifact caching.
        
        Args:
            script_text: The script text to split
            project_id: Project identifier (for logging)
            **kwargs: Additional parameters
            
        Returns:
            Dict with scene splitting results
        """
        try:
            # 1. Validate input
            if not self._validate(script_text=script_text, project_id=project_id):
                return self._create_result(False, error="Invalid script text or project ID")
            
            # 2. Check artifact cache for existing scenes
            artifact_key = self._generate_artifact_key(script_text, project_id)
            cache_result = self.check_cache_use_case.execute(
                artifact_key=artifact_key,
                content=None,  # Just check existence
                artifact_type="string"
            )
            
            if cache_result["ok"] and cache_result["data"].get("cached"):
                # Return cached scenes
                cached_scenes_json = cache_result["data"]["content"]
                logger.info("Returning cached scenes for key: %s...", artifact_key[:12])
                try:
                    scenes = json.loads(cached_scenes_json)
                    return self._create_result(True, {
                        "scenes": scenes,
                        "cache_hit": True
                    })
                except json.JSONDecodeError as e:
                    logger.warning("Failed to parse cached scenes JSON: %s", e)
                    # Fall through to regenerate if cache is corrupt
            
            # 3. Not cached or cache invalid - split script
            logger.info("Splitting script into scenes for project %s", project_id)
            scenes = split_script_into_scenes(
                script_text=script_text,
                project_id=project_id
            )
            
            if not scenes:
                return self._create_result(False, error="Falha ao dividir em cenas")
            
            # Save scenes to disk
            SceneRepository(project_id).save_scenes(scenes)
            
            # Cache the scenes content for future use
            scenes_json = json.dumps(scenes, ensure_ascii=False, indent=2)
            store_result = self.store_cache_use_case.execute(
                artifact_key=artifact_key,
                content=scenes_json,
                artifact_type="string"
            )
            
            if not store_result["ok"]:
                logger.warning("Failed to cache scenes: %s", store_result.get("error", "Unknown error"))
                # Continue anyway - caching failure shouldn't break the pipeline
            
            # 4. Return result with status
            return self._create_result(True, {
                "scenes": scenes,
                "cache_hit": False
            })
            
        except Exception as e:
            logger.error(f"Error in scene splitting: {e}")
            return self._create_result(False, error=str(e))
    
    def _generate_artifact_key(self, script_text: str, project_id: str) -> str:
        """Generate a unique artifact key for scene splitting caching.
        
        Includes: script content and project_id.
        """
        import hashlib
        import json
        
        # Create deterministic representation of inputs
        key_data = {
            "script_text": script_text,
            "project_id": project_id
        }
        canonical = json.dumps(key_data, sort_keys=True)
        return f"scene_split:{hashlib.sha256(canonical.encode('utf-8')).hexdigest()}"
    
    def _validate(self, **kwargs) -> bool:
        """Validate script_text and project_id."""
        script_text = kwargs.get("script_text", "")
        project_id = kwargs.get("project_id", "")
        
        if not script_text or len(script_text.strip()) < 10:
            return False
        if not project_id:
            return False
            
        return True