"""Artifact cache service for PIPE-402 (Cache por hash de artefatos).

Caches pipeline artifacts by content hash to avoid recomputation of identical results.
"""

import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, Union
from app.logging_config import setup_logger

logger = setup_logger()

# Cache directory from config
try:
    from app.config import CACHE_DIR
except ImportError:
    # Fallback if config not available during testing
    CACHE_DIR = Path(__file__).parent.parent.parent / "cache"

# Metadata file to track cached artifacts
CACHE_METADATA_FILE = CACHE_DIR / "artifact_cache_metadata.json"


def _hash_file(file_path: Union[str, Path]) -> str:
    """Calculate SHA-256 hash of a file's content.
    
    Args:
        file_path: Path to the file to hash
        
    Returns:
        Hexadecimal SHA-256 hash string
    """
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def _hash_content(content: Union[str, bytes]) -> str:
    """Calculate SHA-256 hash of content.
    
    Args:
        content: String or bytes content to hash
        
    Returns:
        Hexadecimal SHA-256 hash string
    """
    if isinstance(content, str):
        content = content.encode('utf-8')
    hash_sha256 = hashlib.sha256()
    hash_sha256.update(content)
    return hash_sha256.hexdigest()


class ArtifactCache:
    """Manages caching of pipeline artifacts by content hash.
    
    The cache stores:
    1. The actual artifact files in content-addressable storage (CAS)
    2. Metadata mapping artifact keys to their cached file paths
    
    CAS structure:
        CACHE_DIR/
            artifacts/          # Content-addressable storage
                <hash>/         # First 2 chars of hash as subdir
                    <full_hash> # Actual file content
            metadata.json       # Tracks artifact_key -> cached_file_path mappings
    """
    
    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or CACHE_DIR
        self.artifacts_dir = self.cache_dir / "artifacts"
        self.metadata_file = self.cache_dir / "artifact_cache_metadata.json"
        
        # Ensure directories exist
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing metadata
        self._metadata: Dict[str, Dict[str, Any]] = self._load_metadata()
    
    def _load_metadata(self) -> Dict[str, Dict[str, Any]]:
        """Load cache metadata from JSON file."""
        if not self.metadata_file.exists():
            return {}
        try:
            data = json.loads(self.metadata_file.read_text(encoding="utf-8"))
            return data.get("entries", {})
        except Exception as e:
            logger.warning("Failed to load artifact cache metadata: %s", e)
            return {}
    
    def _save_metadata(self):
        """Persist cache metadata to JSON file."""
        try:
            data = {
                "entries": self._metadata,
                "updated_at": self._get_time()
            }
            self.metadata_file.write_text(
                json.dumps(data, indent=2, ensure_ascii=False), 
                encoding="utf-8"
            )
        except Exception as e:
            logger.error("Failed to save artifact cache metadata: %s", e)
    
    def _get_time(self):
        """Get monotonic time for consistency with idempotency service."""
        import time as time_module
        return time_module.monotonic()
    
    def _get_artifact_path(self, content_hash: str) -> Path:
        """Get the path where an artifact with given hash should be stored.
        
    Uses first 2 characters of hash as subdirectory to avoid too many files in one directory.
        """
        if len(content_hash) < 2:
            raise ValueError(f"Hash too short: {content_hash}")
        subdir = self.artifacts_dir / content_hash[:2]
        subdir.mkdir(exist_ok=True)
        return subdir / content_hash
    
    def store_artifact(self, 
                      artifact_key: str, 
                      content: Union[str, bytes, Path],
                      artifact_type: str = "file") -> Tuple[bool, str]:
        """Store an artifact in the cache.
        
        Args:
            artifact_key: Unique identifier for this artifact (e.g., "script_gen:abc123")
            content: The artifact content (string, bytes, or path to file)
            artifact_type: Type of artifact ("file", "string", "bytes")
            
        Returns:
            Tuple of (success, message_or_hash)
        """
        try:
            # Calculate content hash
            if isinstance(content, (str, bytes)):
                content_hash = _hash_content(content)
                is_file = False
            else:
                # Assume it's a Path to a file
                content_hash = _hash_file(content)
                is_file = True
            
            # Get target path in cache
            target_path = self._get_artifact_path(content_hash)
            
            # If file doesn't exist in cache, store it
            if not target_path.exists():
                if is_file:
                    # Copy file to cache
                    shutil.copy2(content, target_path)
                    logger.info("Cached file artifact: %s -> %s", artifact_key, content_hash[:12])
                else:
                    # Write content to cache
                    if isinstance(content, str):
                        target_path.write_text(content, encoding="utf-8")
                    else:
                        target_path.write_bytes(content)
                    logger.info("Cached content artifact: %s -> %s", artifact_key, content_hash[:12])
            else:
                logger.debug("Artifact already in cache: %s -> %s", artifact_key, content_hash[:12])
            
            # Update metadata
            self._metadata[artifact_key] = {
                "content_hash": content_hash,
                "artifact_type": artifact_type,
                "cached_at": self._get_time(),
                "size": target_path.stat().st_size if target_path.exists() else 0
            }
            self._save_metadata()
            
            return True, content_hash
            
        except Exception as e:
            logger.error("Failed to store artifact %s: %s", artifact_key, e)
            return False, str(e)
    
    def retrieve_artifact(self, artifact_key: str) -> Tuple[bool, Optional[Union[str, bytes, Path]]]:
        """Retrieve an artifact from the cache by its key.
        
        Args:
            artifact_key: The artifact key used when storing
            
        Returns:
            Tuple of (found, content_or_none)
            If found, content is returned as string for text artifacts, 
            or Path to cached file for file artifacts
        """
        try:
            if artifact_key not in self._metadata:
                return False, None
            
            entry = self._metadata[artifact_key]
            content_hash = entry["content_hash"]
            artifact_type = entry["artifact_type"]
            
            # Get path to cached artifact
            cached_path = self._get_artifact_path(content_hash)
            
            if not cached_path.exists():
                # Clean up missing entry
                del self._metadata[artifact_key]
                self._save_metadata()
                return False, None
            
            # Return content based on artifact type
            if artifact_type == "file":
                return True, cached_path
            elif artifact_type == "string":
                return True, cached_path.read_text(encoding="utf-8")
            else:  # bytes
                return True, cached_path.read_bytes()
                
        except Exception as e:
            logger.error("Failed to retrieve artifact %s: %s", artifact_key, e)
            return False, None
    
    def contains(self, artifact_key: str) -> bool:
        """Check if an artifact exists in the cache.
        
        Args:
            artifact_key: The artifact key to check
            
        Returns:
            True if artifact exists and is valid, False otherwise
        """
        if artifact_key not in self._metadata:
            return False
        
        entry = self._metadata[artifact_key]
        content_hash = entry["content_hash"]
        cached_path = self._get_artifact_path(content_hash)
        
        return cached_path.exists()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        total_size = sum(
            entry.get("size", 0) 
            for entry in self._metadata.values()
        )
        
        return {
            "total_artifacts": len(self._metadata),
            "total_size_bytes": total_size,
            "cache_dir": str(self.cache_dir),
            "artifacts_dir": str(self.artifacts_dir)
        }
    
    def clear(self):
        """Clear all cached artifacts (for testing)."""
        try:
            # Remove all artifact files
            if self.artifacts_dir.exists():
                shutil.rmtree(self.artifacts_dir)
                self.artifacts_dir.mkdir(parents=True)
            
            # Clear metadata
            self._metadata = {}
            self._save_metadata()
            
            logger.info("Artifact cache cleared")
        except Exception as e:
            logger.error("Failed to clear artifact cache: %s", e)


# Singleton for app-wide use
artifact_cache = ArtifactCache()