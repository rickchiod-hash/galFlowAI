"""Prompt building stage with artifact caching (PIPE-402)."""

from app.pipeline.stages.base_stage import BaseStage
from app.pipeline.prompt_builder import build_prompts_for_scenes, save_prompts
from app.application.use_cases.artifact_cache_use_cases import (
    CheckArtifactCacheUseCase,
    StoreArtifactUseCase
)
import logging
import json

logger = logging.getLogger(__name__)


class PromptBuildingStage(BaseStage):
    """Stage for building video prompts for scenes with artifact caching.
    
    3-point standard with caching:
    1. Validate scenes input
    2. Check artifact cache for existing prompts
    3. If cached: return cached prompts
       If not cached: build prompts, save, cache, and return result
    """
    
    def __init__(self):
        super().__init__()
        self.check_cache_use_case = CheckArtifactCacheUseCase()
        self.store_cache_use_case = StoreArtifactUseCase()

    def execute(self, scenes: list, project_id: str, **kwargs) -> dict:
        """
        Build prompts for scenes with artifact caching.
        
        Args:
            scenes: List of scene dictionaries
            project_id: Project identifier (for logging)
            **kwargs: Additional parameters
            
        Returns:
            Dict with prompt building results
        """
        try:
            # 1. Validate input
            if not self._validate(scenes=scenes, project_id=project_id):
                return self._create_result(False, error="Invalid scenes or project ID")
            
            # 2. Check artifact cache for existing prompts
            artifact_key = self._generate_artifact_key(scenes, project_id)
            cache_result = self.check_cache_use_case.execute(
                artifact_key=artifact_key,
                content=None,  # Just check existence
                artifact_type="string"
            )
            
            if cache_result["ok"] and cache_result["data"].get("cached"):
                # Return cached prompts
                cached_prompts_json = cache_result["data"]["content"]
                logger.info("Returning cached prompts for key: %s...", artifact_key[:12])
                try:
                    scene_prompts = json.loads(cached_prompts_json)
                    return self._create_result(True, {
                        "scene_prompts": scene_prompts,
                        "cache_hit": True
                    })
                except json.JSONDecodeError as e:
                    logger.warning("Failed to parse cached prompts JSON: %s", e)
                    # Fall through to regenerate if cache is corrupt
            
            # 3. Not cached or cache invalid - build prompts
            logger.info("Building prompts for %d scenes for project %s", 
                       len(scenes), project_id)
            scene_prompts = build_prompts_for_scenes(
                scenes=scenes,
                project_id=project_id
            )
            
            # Save prompts to disk
            save_prompts(project_id, scene_prompts)
            
            # Cache the prompts content for future use
            prompts_json = json.dumps(scene_prompts, ensure_ascii=False, indent=2)
            store_result = self.store_cache_use_case.execute(
                artifact_key=artifact_key,
                content=prompts_json,
                artifact_type="string"
            )
            
            if not store_result["ok"]:
                logger.warning("Failed to cache prompts: %s", store_result.get("error", "Unknown error"))
                # Continue anyway - caching failure shouldn't break the pipeline
            
            # 4. Return result with status
            return self._create_result(True, {
                "scene_prompts": scene_prompts,
                "cache_hit": False
            })
            
        except Exception as e:
            logger.error(f"Error in prompt building: {e}")
            return self._create_result(False, error=str(e))
    
    def _generate_artifact_key(self, scenes: list, project_id: str) -> str:
        """Generate a unique artifact key for prompt building caching.
        
        Includes: scenes content and project_id.
        """
        import hashlib
        import json
        
        # Create deterministic representation of inputs
        # Sort scenes by id to ensure consistent ordering
        sorted_scenes = sorted(scenes, key=lambda s: s.get("id", ""))
        key_data = {
            "scenes": sorted_scenes,
            "project_id": project_id
        }
        canonical = json.dumps(key_data, sort_keys=True)
        return f"prompt_build:{hashlib.sha256(canonical.encode('utf-8')).hexdigest()}"
    
    def _validate(self, **kwargs) -> bool:
        """Validate scenes and project_id."""
        scenes = kwargs.get("scenes", [])
        project_id = kwargs.get("project_id", "")
        
        if not isinstance(scenes, list) or len(scenes) == 0:
            return False
        if not project_id:
            return False
            
        # Validate each scene has required fields
        for scene in scenes:
            if not isinstance(scene, dict):
                return False
            if "id" not in scene:
                return False
                
        return True