from dataclasses import dataclass, field, asdict
from typing import Any

from app.core.error_codes import ErrorCode


class Severity:
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


@dataclass
class AppError:
    code: str | ErrorCode
    severity: str
    message: str
    suggestion: str
    stage: str
    retryable: bool
    project_id: str | None = None
    job_id: str | None = None
    provider: str | None = None
    fallback_used: bool = False
    details: dict | None = None

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}

    def to_json_line(self) -> str:
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False)
