import json
from datetime import date
from pathlib import Path

from app.config import LOGS_DIR
from app.core.app_error import AppError


ERRORS_DIR = LOGS_DIR / "errors"


class ErrorJsonlWriter:

    def __init__(self, errors_dir: Path | None = None):
        self.errors_dir = errors_dir or ERRORS_DIR

    def _ensure_dir(self) -> None:
        self.errors_dir.mkdir(parents=True, exist_ok=True)

    def _file_path(self, dt: date | None = None) -> Path:
        dt = dt or date.today()
        return self.errors_dir / f"errors-{dt.isoformat()}.jsonl"

    def write(self, error: AppError) -> bool:
        try:
            self._ensure_dir()
            line = error.to_json_line()
            path = self._file_path()
            with open(path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
            return True
        except Exception:
            return False

    def read_recent(self, limit: int = 50) -> list[dict]:
        try:
            path = self._file_path()
            if not path.exists():
                return []
            lines = path.read_text(encoding="utf-8").strip().splitlines()
            results = []
            for line in lines[-limit:]:
                try:
                    results.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
            return results
        except Exception:
            return []
