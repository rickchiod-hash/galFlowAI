"""Use cases for artifact cache (PIPE-402)."""

from typing import Dict, Any, Optional, Union
from pathlib import Path
from app.application.use_cases.base_use_case import BaseUseCase
from app.services.artifact_cache_service import artifact_cache


class CheckArtifactCacheUseCase(BaseUseCase):
    """Check if an artifact exists in the cache.
    
    3-point standard:
    1. Validate artifact key and content
    2. Check artifact cache
    3. Return cached artifact if found, or indicate not cached
    """

    def execute(self, 
                artifact_key: str, 
                content: Optional[Union[str, bytes]] = None,
                artifact_type: str = "file") -> Dict[str, Any]:
        """Execute artifact cache check use case."""
        try:
            if not self._validate(artifact_key=artifact_key, 
                                 content=content, 
                                 artifact_type=artifact_type):
                return self._build_error("Invalid artifact key or content")

            # If content provided, verify it matches cache (optional validation)
            if content is not None:
                found, cached_content = artifact_cache.retrieve_artifact(artifact_key)
                if found:
                    # For simplicity, we assume content matches if key exists
                    # In a more strict implementation, we could hash content and compare
                    return self._build_success(data={
                        "cached": True,
                        "artifact_key": artifact_key,
                        "content": cached_content,
                        "artifact_type": artifact_type
                    })
                else:
                    return self._build_success(data={
                        "cached": False,
                        "artifact_key": artifact_key
                    })
            else:
                # Just check if exists - if found, return the cached content
                found, cached_content = artifact_cache.retrieve_artifact(artifact_key)
                return self._build_success(data={
                    "cached": found,
                    "artifact_key": artifact_key,
                    "content": cached_content,
                    "artifact_type": artifact_type
                })
                
        except Exception as e:
            return self._build_error(str(e))

    def _validate(self, **kwargs) -> bool:
        artifact_key = kwargs.get("artifact_key", "")
        content = kwargs.get("content")
        artifact_type = kwargs.get("artifact_type", "file")
        
        if not artifact_key or not isinstance(artifact_key, str):
            return False
            
        if content is not None:
            if not isinstance(content, (str, bytes)):
                return False
                
        if artifact_type not in ("file", "string", "bytes"):
            return False
            
        return True


class StoreArtifactUseCase(BaseUseCase):
    """Store an artifact in the cache.
    
    3-point standard:
    1. Validate artifact key and content
    2. Store artifact in cache
    3. Return storage status
    """

    def execute(self, 
                artifact_key: str, 
                content: Union[str, bytes, Path],
                artifact_type: str = "file") -> Dict[str, Any]:
        """Execute artifact storage use case."""
        try:
            if not self._validate(artifact_key=artifact_key, 
                                 content=content, 
                                 artifact_type=artifact_type):
                return self._build_error("Invalid artifact key or content")

            success, message_or_hash = artifact_cache.store_artifact(
                artifact_key=artifact_key,
                content=content,
                artifact_type=artifact_type
            )
            
            if success:
                return self._build_success(data={
                    "stored": True,
                    "artifact_key": artifact_key,
                    "content_hash": message_or_hash,
                    "artifact_type": artifact_type
                })
            else:
                return self._build_error(f"Failed to store artifact: {message_or_hash}")
                
        except Exception as e:
            return self._build_error(str(e))

    def _validate(self, **kwargs) -> bool:
        artifact_key = kwargs.get("artifact_key", "")
        content = kwargs.get("content")
        artifact_type = kwargs.get("artifact_type", "file")
        
        if not artifact_key or not isinstance(artifact_key, str):
            return False
            
        if content is None:
            return False
            
        if artifact_type not in ("file", "string", "bytes"):
            return False
            
        return True