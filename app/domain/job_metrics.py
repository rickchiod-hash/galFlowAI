"""JobMetrics (OBS-901).

Metricas minimas por job do pipeline.
Agrega eventos do StageLogger em metricas por etapa:
tempo, fallback e erro.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class JobStageMetric:
    """Metrica de uma etapa do job."""
    stage: str
    duration_ms: float = 0.0
    success: bool = True
    fallback_count: int = 0
    error_count: int = 0
    warnings: List[str] = field(default_factory=list)


@dataclass
class JobMetrics:
    """Metricas agregadas de um job do pipeline.

    Uso:
        metrics = JobMetrics(project_id="proj_123", job_type="video_render")
        metrics.add_stage_event(stage="SceneSplittingStage", event_type="start")
        metrics.add_stage_event(stage="SceneSplittingStage", event_type="success", duration_ms=1200.0)
        metrics.add_stage_event(stage="RenderStage", event_type="failure", cause="OOM")
        summary = metrics.get_summary()
    """

    project_id: str
    job_type: str = "video_render"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    _stages: Dict[str, JobStageMetric] = field(default_factory=dict, repr=False)

    def add_stage_event(
        self,
        stage: str,
        event_type: str,
        duration_ms: float = 0.0,
        cause: str = "",
        correction: str = "",
    ) -> None:
        if stage not in self._stages:
            self._stages[stage] = JobStageMetric(stage=stage)

        metric = self._stages[stage]

        if event_type == "start":
            pass
        elif event_type == "success":
            metric.success = True
            metric.duration_ms = duration_ms if duration_ms > 0 else metric.duration_ms
        elif event_type == "failure":
            metric.success = False
            metric.error_count += 1
            if cause:
                metric.warnings.append(f"ERRO: {cause}")
        elif event_type == "warning":
            metric.fallback_count += 1
            if cause:
                metric.warnings.append(f"FALLBACK: {cause}")

    def get_stage_metrics(self) -> List[Dict[str, Any]]:
        return [
            {
                "stage": s.stage,
                "duration_ms": s.duration_ms,
                "success": s.success,
                "fallback_count": s.fallback_count,
                "error_count": s.error_count,
                "warnings": s.warnings,
            }
            for s in self._stages.values()
        ]

    def get_summary(self) -> Dict[str, Any]:
        stages = self.get_stage_metrics()
        total_duration = sum(s["duration_ms"] for s in stages)
        total_stages = len(stages)
        failed_stages = sum(1 for s in stages if not s["success"])
        total_fallbacks = sum(s["fallback_count"] for s in stages)
        total_errors = sum(s["error_count"] for s in stages)

        return {
            "project_id": self.project_id,
            "job_type": self.job_type,
            "created_at": self.created_at,
            "total_stages": total_stages,
            "total_duration_ms": total_duration,
            "total_duration_sec": round(total_duration / 1000, 2),
            "failed_stages": failed_stages,
            "success_rate": round(
                ((total_stages - failed_stages) / total_stages * 100) if total_stages > 0 else 100, 1
            ),
            "total_fallbacks": total_fallbacks,
            "total_errors": total_errors,
            "stages": stages,
        }
