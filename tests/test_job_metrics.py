"""Tests for JobMetrics (OBS-901)."""
import pytest

from app.domain.job_metrics import JobStageMetric, JobMetrics


class TestJobStageMetric:
    def test_default_values(self):
        m = JobStageMetric(stage="Test")
        assert m.stage == "Test"
        assert m.duration_ms == 0.0
        assert m.success is True
        assert m.fallback_count == 0
        assert m.error_count == 0


class TestJobMetrics:
    def test_initial_state(self):
        jm = JobMetrics(project_id="proj_001", job_type="render")
        assert jm.project_id == "proj_001"
        assert jm.job_type == "render"
        summary = jm.get_summary()
        assert summary["total_stages"] == 0
        assert summary["success_rate"] == 100.0

    def test_add_single_stage_start_success(self):
        jm = JobMetrics(project_id="proj_001")
        jm.add_stage_event(stage="SceneSplit", event_type="start")
        jm.add_stage_event(stage="SceneSplit", event_type="success", duration_ms=1500.0)
        summary = jm.get_summary()
        assert summary["total_stages"] == 1
        assert summary["total_duration_ms"] == 1500.0
        assert summary["failed_stages"] == 0

    def test_add_stage_failure(self):
        jm = JobMetrics(project_id="proj_002")
        jm.add_stage_event(stage="Render", event_type="start")
        jm.add_stage_event(stage="Render", event_type="failure", cause="GPU OOM")
        summary = jm.get_summary()
        assert summary["failed_stages"] == 1
        assert summary["success_rate"] == 0.0

    def test_add_stage_warning_is_fallback(self):
        jm = JobMetrics(project_id="proj_003")
        jm.add_stage_event(stage="Audio", event_type="warning", cause="TTS indisponivel")
        summary = jm.get_summary()
        assert summary["total_fallbacks"] == 1
        assert summary["total_errors"] == 0

    def test_multiple_stages_accumulate(self):
        jm = JobMetrics(project_id="proj_004")
        jm.add_stage_event(stage="Script", event_type="success", duration_ms=500.0)
        jm.add_stage_event(stage="Split", event_type="success", duration_ms=300.0)
        jm.add_stage_event(stage="Render", event_type="failure", cause="OOM")
        jm.add_stage_event(stage="Render", event_type="warning", cause="Fallback FFmpeg")
        summary = jm.get_summary()
        assert summary["total_stages"] == 3
        assert summary["total_duration_ms"] == 800.0
        assert summary["failed_stages"] == 1
        assert summary["total_fallbacks"] == 1
        assert summary["success_rate"] == 66.7

    def test_success_rate_100_when_no_failures(self):
        jm = JobMetrics(project_id="proj_005")
        jm.add_stage_event(stage="A", event_type="success")
        jm.add_stage_event(stage="B", event_type="success")
        assert jm.get_summary()["success_rate"] == 100.0

    def test_get_stage_metrics_returns_list(self):
        jm = JobMetrics(project_id="proj_006")
        jm.add_stage_event(stage="Stage1", event_type="success", duration_ms=100.0)
        stages = jm.get_stage_metrics()
        assert len(stages) == 1
        assert stages[0]["stage"] == "Stage1"
        assert stages[0]["duration_ms"] == 100.0

    def test_job_type_default(self):
        jm = JobMetrics(project_id="proj_007")
        assert jm.job_type == "video_render"

    def test_custom_job_type(self):
        jm = JobMetrics(project_id="proj_008", job_type="audio_only")
        assert jm.job_type == "audio_only"
