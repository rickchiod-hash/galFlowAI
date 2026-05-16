"""ConfigService (UI-204).

Gerenciamento de configuracoes da UI.
Persiste preferencias do usuario em JSON.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

from app.config import LOGS_DIR, PROJECTS_DIR
CONFIG_DIR = LOGS_DIR
CONFIG_FILE = CONFIG_DIR / "settings.json"

DEFAULT_CONFIG: Dict[str, Any] = {
    "default_llm_provider": "auto",
    "default_quality": "STANDARD",
    "default_duration_sec": 30,
    "logs_dir": str(CONFIG_DIR),
    "projects_dir": str(PROJECTS_DIR),
    "theme": "default",
}


class ConfigService:
    def __init__(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self._config: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if CONFIG_FILE.exists():
            try:
                data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
                self._config = {**DEFAULT_CONFIG, **data}
            except Exception:
                self._config = dict(DEFAULT_CONFIG)
        else:
            self._config = dict(DEFAULT_CONFIG)
            self._save()

    def _save(self) -> None:
        CONFIG_FILE.write_text(
            json.dumps(self._config, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._config[key] = value
        self._save()

    def set_multi(self, updates: Dict[str, Any]) -> None:
        self._config.update(updates)
        self._save()

    def get_all(self) -> Dict[str, Any]:
        return dict(self._config)

    def reset(self) -> None:
        self._config = dict(DEFAULT_CONFIG)
        self._save()


_config_instance: Optional[ConfigService] = None


def get_config_service() -> ConfigService:
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigService()
    return _config_instance
