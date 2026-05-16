"""Use case for script generation with artifact caching (PIPE-402)."""

from typing import Dict, Any
import logging
from app.application.use_cases.base_use_case import BaseUseCase
from app.services.script_service import generate_script_with_llm, generate_script_with_provider
from app.repositories.script_repository import ScriptRepository
from app.application.use_cases.artifact_cache_use_cases import (
    CheckArtifactCacheUseCase,
    StoreArtifactUseCase
)

logger = logging.getLogger(__name__)

class GenerateScriptUseCase(BaseUseCase):
    """Generate commercial script from briefing with artifact caching.
    
    3-point standard with caching:
    1. Validate briefing input
    2. Check artifact cache for existing script
    3. If cached: return cached script
       If not cached: generate script using LLM, save, cache, and return result
    """
    
    def __init__(self):
        super().__init__()
        self.check_cache_use_case = CheckArtifactCacheUseCase()
        self.store_cache_use_case = StoreArtifactUseCase()

    def execute(self, briefing: str, project_id: str, mode: str = "auto", provider: str = "auto") -> Dict[str, Any]:
        """Execute script generation use case with artifact caching."""
        try:
            # 1. Validate input
            if not self._validate(briefing=briefing, project_id=project_id):
                return self._build_error("Invalid input parameters")
            
            # 2. Check artifact cache for existing script
            artifact_key = self._generate_artifact_key(briefing, project_id, mode if provider == "auto" else provider)
            cache_result = self.check_cache_use_case.execute(
                artifact_key=artifact_key,
                content=None,  # Just check existence
                artifact_type="string"
            )
            
            if cache_result["ok"] and cache_result["data"].get("cached"):
                # Return cached script
                cached_script = cache_result["data"]["content"]
                logger.info("Returning cached script for key: %s...", artifact_key[:12])
                return self._build_success(
                    data={
                        "script": cached_script,
                        "provider": "CACHE",  # Indicate it came from cache
                        "time": 0.0,  # No time spent generating
                        "quality": "cached",
                        "cache_hit": True
                    },
                    project_id=project_id
                )
            
            # 3. Not cached - generate script using LLM
            if provider != "auto":
                result = generate_script_with_provider(briefing, provider)
            else:
                result = generate_script_with_llm(briefing, mode)
            
            if not result.get("ok", False):
                return self._build_error(
                    f"Script generation failed: {result.get('error', 'Unknown error')}",
                    project_id=project_id
                )
            
            # Save script to disk
            ScriptRepository(project_id).save_script(result["script"])
            
            # Cache the script content for future use
            store_result = self.store_cache_use_case.execute(
                artifact_key=artifact_key,
                content=result["script"],
                artifact_type="string"
            )
            
            if not store_result["ok"]:
                logger.warning("Failed to cache script: %s", store_result.get("error", "Unknown error"))
                # Continue anyway - caching failure shouldn't break the pipeline
            
            # 4. Return result with status
            return self._build_success(
                data={
                    "script": result["script"],
                    "provider": result.get("provider", "Unknown"),
                    "time": result.get("time", 0),
                    "quality": result.get("quality", "fallback"),
                    "cache_hit": False
                },
                project_id=project_id
            )
        except Exception as e:
            return self._build_error(str(e), project_id=project_id)
    
    def _generate_artifact_key(self, briefing: str, project_id: str, mode: str) -> str:
        """Generate a unique artifact key for script caching.
        
        Includes: briefing content, project_id, and generation mode.
        """
        import hashlib
        import json
        
        # Create deterministic representation of inputs
        key_data = {
            "briefing": briefing,
            "project_id": project_id,
            "mode": mode
        }
        canonical = json.dumps(key_data, sort_keys=True)
        return f"script_gen:{hashlib.sha256(canonical.encode('utf-8')).hexdigest()}"
    
    def _validate(self, **kwargs) -> bool:
        """Validate briefing and project_id."""
        briefing = kwargs.get("briefing", "")
        project_id = kwargs.get("project_id", "")
        mode = kwargs.get("mode", "auto")
        provider = kwargs.get("provider", "auto")
        
        if not briefing or len(briefing.strip()) < 10:
            return False
        if not project_id:
            return False
        if mode not in ("auto", "fast", "quality", "safe", "template"):
            return False
        if provider not in ("auto", "template", "lm_studio", "koboldcpp", "llamacpp", "gpt4all"):
            return False
            
        return True