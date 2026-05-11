"""StageLogger (OBS-900).

Logs estruturados por etapa do pipeline com CAUSA e CORRECAO.
Cada evento registra: stage, event_type, message, cause, correction.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class StageEvent:
    """Evento unico de uma etapa do pipeline."""
    stage: str
    event_type: str
    message: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    cause: str = ""
    correction: str = ""
    project_id: str = ""
    duration_ms: float = 0.0


class StageLogger:
    """Logger estruturado por etapa do pipeline.

    Uso:
        logger = StageLogger("SceneSplittingStage", project_id="proj_123")
        logger.start("Iniciando separacao de cenas")
        # ... work ...
        logger.success("10 cenas criadas")
        # or on failure:
        logger.failure("Falha ao separar cenas", cause="LLM indisponivel", correction="Verifique provider LLM")
    """

    def __init__(self, stage: str, project_id: str = "", log_corrections: bool = True):
        self._stage = stage
        self._project_id = project_id
        self._log_corrections = log_corrections
        self._py_logger = logging.getLogger(f"stage.{stage}")
        self._events: List[StageEvent] = []

    @property
    def stage(self) -> str:
        return self._stage

    @property
    def events(self) -> List[StageEvent]:
        return list(self._events)

    @property
    def project_id(self) -> str:
        return self._project_id

    def _log(self, event: StageEvent) -> None:
        self._events.append(event)
        base = f"[{event.stage}] {event.event_type}: {event.message}"
        if event.cause:
            base += f" | CAUSA: {event.cause}"
        if event.correction:
            base += f" | CORRECAO: {event.correction}"

        if event.event_type == "failure":
            self._py_logger.error(base)
        elif event.event_type == "warning":
            self._py_logger.warning(base)
        else:
            self._py_logger.info(base)

    def start(self, message: str) -> StageEvent:
        event = StageEvent(
            stage=self._stage,
            event_type="start",
            message=message,
            project_id=self._project_id,
        )
        self._log(event)
        return event

    def success(self, message: str, duration_ms: float = 0.0) -> StageEvent:
        event = StageEvent(
            stage=self._stage,
            event_type="success",
            message=message,
            project_id=self._project_id,
            duration_ms=duration_ms,
        )
        self._log(event)
        return event

    def failure(self, message: str, cause: str = "", correction: str = "") -> StageEvent:
        event = StageEvent(
            stage=self._stage,
            event_type="failure",
            message=message,
            cause=cause,
            correction=correction,
            project_id=self._project_id,
        )
        self._log(event)
        return event

    def warning(self, message: str, cause: str = "", correction: str = "") -> StageEvent:
        event = StageEvent(
            stage=self._stage,
            event_type="warning",
            message=message,
            cause=cause,
            correction=correction,
            project_id=self._project_id,
        )
        self._log(event)
        return event

    def get_summary(self) -> Dict[str, Any]:
        total = len(self._events)
        by_type: Dict[str, int] = {}
        for e in self._events:
            by_type[e.event_type] = by_type.get(e.event_type, 0) + 1
        failures = [e for e in self._events if e.event_type == "failure"]
        return {
            "stage": self._stage,
            "total_events": total,
            "by_type": by_type,
            "failures": len(failures),
            "last_failure": failures[-1].message if failures else "",
        }
