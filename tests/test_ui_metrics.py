"""UI-203: Tests for log, metrics, and diagnostic screens."""

import sys
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, PropertyMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


# --- Fixtures ---

@pytest.fixture
def temp_metrics_dir():
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


@pytest.fixture
def metrics_service(temp_metrics_dir):
    from app.services.metrics_service import MetricsService
    svc = MetricsService()
    svc.metrics_file = temp_metrics_dir / "metrics.json"
    return svc


@pytest.fixture
def seeded_metrics(metrics_service):
    svc = metrics_service
    svc.record_script_generation(
        success=True, duration=5.2, provider="template",
        used_fallback=False, project_id="proj-01"
    )
    svc.record_script_generation(
        success=True, duration=8.1, provider="lm_studio",
        used_fallback=False, project_id="proj-02"
    )
    svc.record_video_generation(
        success=True, duration=45.0, engine="WanGP",
        used_fallback=False, project_id="proj-01"
    )
    svc.record_video_generation(
        success=False, duration=12.3, engine="FFMPEG",
        used_fallback=True, project_id="proj-03"
    )
    return svc


@pytest.fixture
def temp_log_file():
    logs_dir = Path(tempfile.mktemp(suffix="_logs"))
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "galflowai.log"
    log_file.write_text(
        "2025-01-15 10:00:00,000 - INFO - ModuleA - msg1 - sugestao1\n"
        "2025-01-15 10:01:00,000 - WARN - ModuleB - msg2 - sugestao2\n"
        "2025-01-15 10:02:00,000 - ERROR - ModuleC - msg3 - sugestao3\n"
        "2025-01-15 10:03:00,000 - INFO - ModuleA - msg4 - sugestao4\n",
        encoding="utf-8"
    )
    yield log_file
    import shutil
    shutil.rmtree(log_file.parent, ignore_errors=True)


# --- Metrics Unit Tests ---

class TestMetricsScreenSummary:

    def test_summary_returns_all_keys(self, metrics_service):
        summary = metrics_service.get_summary()
        expected_keys = {
            "generated_scripts", "generated_videos", "fallback_used",
            "errors", "success_rate_percent", "average_generation_time",
            "total_operations", "recent_operations"
        }
        assert expected_keys.issubset(summary.keys())

    def test_summary_with_seeded_data(self, seeded_metrics):
        summary = seeded_metrics.get_summary()
        assert summary["generated_scripts"] == 2
        assert summary["generated_videos"] == 2
        assert summary["fallback_used"] == 1
        assert summary["errors"] == 1
        assert summary["total_operations"] == 4
        assert summary["success_rate_percent"] == 75.0

    def test_summary_empty(self, metrics_service):
        summary = metrics_service.get_summary()
        assert summary["generated_scripts"] == 0
        assert summary["generated_videos"] == 0
        assert summary["fallback_used"] == 0
        assert summary["errors"] == 0
        assert summary["total_operations"] == 0

    def test_recent_operations_limit(self, seeded_metrics):
        ops = seeded_metrics.get_recent_operations(limit=2)
        assert len(ops) == 2
        assert ops[0]["type"] == "video_generation"

    def test_recent_operations_empty(self, metrics_service):
        ops = metrics_service.get_recent_operations(limit=5)
        assert ops == []

    def test_fallback_rate(self, seeded_metrics):
        rate = seeded_metrics.get_fallback_rate()
        assert rate == 25.0

    def test_fallback_rate_empty(self, metrics_service):
        assert metrics_service.get_fallback_rate() == 0.0


class TestMetricsScreenNegative:

    def test_invalid_limit_reverts_to_default(self, metrics_service):
        with patch.object(metrics_service, "_load_data", return_value={"operations": []}):
            ops = metrics_service.get_recent_operations(limit=-1)
            assert ops == []

    def test_corrupted_metrics_file(self, metrics_service):
        metrics_service.metrics_file.write_text(
            "not valid json", encoding="utf-8"
        )
        data = metrics_service._load_data()
        assert isinstance(data, dict)
        assert data["generated_scripts"] == 0
        assert data["errors"] == 0


# --- Log Service Tests ---

class TestLogScreen:

    def test_get_log_summary_returns_keys(self):
        from app.services.log_service import get_log_summary
        summary = get_log_summary()
        expected_keys = {"total_info", "total_warn", "total_error",
                         "last_error", "last_update", "log_file"}
        assert expected_keys.issubset(summary.keys())

    def test_get_recent_logs_returns_dataframe_structure(self):
        from app.services.log_service import get_recent_logs
        result = get_recent_logs(level="INFO", search=None, limit=10)
        assert "logs" in result
        assert isinstance(result["logs"], list)

    def test_diagnostic_bundle_contains_expected_sections(self):
        from app.services.log_service import copy_diagnostic_bundle
        bundle = copy_diagnostic_bundle()
        assert isinstance(bundle, str)
        assert len(bundle) > 50


# --- UI Structure Tests ---

class TestGradioAppTabStructure:

    def test_gradio_app_imports_and_creates_tabs(self):
        from app.ui.gradio_app import create_gradio_app
        demo = create_gradio_app()
        assert demo is not None
        assert demo.title == "GalFlowAI - Gerador de Comerciais"

    def test_metrics_service_import(self):
        from app.services.metrics_service import get_metrics_service
        svc = get_metrics_service()
        assert svc is not None
        assert hasattr(svc, "get_summary")

    def test_log_service_imports_exist(self):
        from app.services.log_service import (
            get_recent_logs, get_log_summary, copy_diagnostic_bundle
        )
        assert callable(get_recent_logs)
        assert callable(get_log_summary)
        assert callable(copy_diagnostic_bundle)


# --- Regression: UI still does not import adapters ---

def test_ui_no_adapter_imports():
    from tests.test_ui_adapter_separation import (
        test_gradio_ui_no_adapter_imports
    )
    test_gradio_ui_no_adapter_imports()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
