"""Idempotency service for pipeline stages (PIPE-401).

Generates content-hash keys from stage inputs and persists completed keys
to avoid duplicate rendering of the same stage with identical inputs.
"""
import json
import hashlib
import time as time_module
from pathlib import Path
from typing import Optional, Dict, Any, List
from app.logging_config import setup_logger

logger = setup_logger()

# Use monotonic clock for higher precision on Windows
_get_time = time_module.monotonic

STATE_DIR = Path(__file__).parent.parent.parent / "state"
REGISTRY_FILE = STATE_DIR / "idempotency_registry.json"


def generate_key(stage: str, params: Dict[str, Any]) -> str:
    """Generate a deterministic hash key from stage name and input parameters.

    The hash is SHA-256 of the stage name plus canonical JSON of params.
    """
    canonical = json.dumps(params, sort_keys=True, ensure_ascii=False)
    raw = f"{stage}:{canonical}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


class IdempotencyRegistry:
    """Persistent registry of completed pipeline stage keys.

    Stores {hash_key: {stage, output, timestamp}} in a JSON file.
    """

    def __init__(self, registry_file: Optional[Path] = None):
        self.registry_file = registry_file or REGISTRY_FILE
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        self._entries: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self):
        """Load registry from JSON file."""
        if not self.registry_file.exists():
            self._entries = {}
            return
        try:
            data = json.loads(self.registry_file.read_text(encoding="utf-8"))
            self._entries = data.get("entries", {})
            logger.info("Idempotency registry loaded: %d entries", len(self._entries))
        except Exception as e:
            logger.warning("Failed to load idempotency registry: %s", e)
            self._entries = {}

    def _save(self):
        """Persist registry to JSON file."""
        data = {
            "entries": self._entries,
            "updated_at": _get_time()
        }
        try:
            self.registry_file.write_text(
                json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
            )
        except Exception as e:
            logger.error("Failed to save idempotency registry: %s", e)

    def check(self, key: str) -> Optional[Dict[str, Any]]:
        """Check if a key exists in the registry. Returns the entry or None."""
        return self._entries.get(key)

    def register(self, key: str, stage: str, output: Dict[str, Any],
                 ttl_seconds: Optional[int] = None):
        """Register a completed stage with its output key.

        Args:
            key: The idempotency hash key.
            stage: Stage name (e.g. 'script_generation', 'scene_splitting').
            output: The output data to cache.
            ttl_seconds: Optional TTL for cache expiration.
        """
        entry = {
            "stage": stage,
            "output": output,
            "timestamp": _get_time()
        }
        if ttl_seconds is not None:
            entry["ttl"] = ttl_seconds
        self._entries[key] = entry
        self._save()
        logger.info("Registered idempotency key for stage '%s': %s...", stage, key[:12])

    def is_completed(self, key: str) -> bool:
        """Check if a key is registered and not expired."""
        entry = self._entries.get(key)
        if not entry:
            return False
        ttl = entry.get("ttl")
        if ttl is not None and _get_time() - entry["timestamp"] >= ttl:
            del self._entries[key]
            self._save()
            return False
        return True

    def clear(self):
        """Clear all entries (for tests)."""
        self._entries.clear()
        if self.registry_file.exists():
            self.registry_file.unlink()

    def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        return {
            "total_entries": len(self._entries),
            "stages": list(set(e["stage"] for e in self._entries.values())),
            "registry_file": str(self.registry_file)
        }


# Singleton for app-wide use
registry = IdempotencyRegistry()
