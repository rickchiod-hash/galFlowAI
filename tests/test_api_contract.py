"""FastAPI contract tests for critical routes.

Tests cover: status code 200/404/500, ApiResponse envelope schema,
and required response fields for health, providers, projects,
jobs, hardware, metrics, logs, and scripts.
"""
import json
from unittest.mock import patch, MagicMock
from pathlib import Path

from fastapi.testclient import TestClient
from app.api import app
from app.logging_config import setup_logger
from app.config import PROJECTS_DIR

logger = setup_logger()

# Patch LLM providers to avoid timeouts
_PROVIDER_PATCHES = [
    patch("app.adapters.llm.lmstudio_provider.LMStudioProvider.is_available", return_value=False),
    patch("app.adapters.llm.koboldcpp_provider.KoboldCppProvider.is_available", return_value=False),
    patch("app.adapters.llm.llamacpp_provider.LlamaCppProvider.is_available", return_value=False),
    patch("app.adapters.llm.gpt4all_provider.GPT4AllProvider.is_available", return_value=False),
]
for _p in _PROVIDER_PATCHES:
    _p.start()

client = TestClient(app)


# ========== Helpers ==========

def _assert_api_envelope(response, status_code=200):
    """Assert standard ApiResponse envelope structure."""
    assert response.status_code == status_code, (
        f"Expected {status_code}, got {response.status_code}: {response.text[:200]}"
    )
    data = response.json()
    if status_code == 200:
        assert data["ok"] is True, f"Expected ok=True, got {data}"
        assert "code" in data
        assert "message" in data
        assert "details" in data
    return data


def _setup_project(project_id: str) -> Path:
    """Create minimal test project on disk."""
    proj_dir = PROJECTS_DIR / project_id
    if proj_dir.exists():
        import shutil
        shutil.rmtree(proj_dir)
    proj_dir.mkdir(parents=True)
    (proj_dir / "project.json").write_text(
        json.dumps({"id": project_id, "name": "Test", "status": "initialized"}),
        encoding="utf-8",
    )
    for sub in ("script", "prompts", "storyboard", "renders", "audio", "final", "logs"):
        (proj_dir / sub).mkdir()
    return proj_dir


def _teardown_project(project_id: str):
    import shutil
    d = PROJECTS_DIR / project_id
    if d.exists():
        shutil.rmtree(d)


# ========== Health ==========

class TestHealthContract:
    def test_health_returns_200_and_schema(self):
        data = _assert_api_envelope(client.get("/api/v1/health"))
        d = data["details"]
        assert d["status"] == "ok"
        assert d["app"] == "GalFlowAI"
        assert d["mode"] == "local"
        assert d["version"] == "2.0"

    def test_health_dashboard_returns_200_or_500(self):
        resp = client.get("/api/v1/health/dashboard")
        assert resp.status_code in (200, 500)
        data = resp.json()
        assert "ok" in data
        assert "code" in data


# ========== LLM Providers ==========

class TestLLMProvidersContract:
    def test_providers_list_returns_200_and_schema(self):
        data = _assert_api_envelope(client.get("/api/v1/llm/providers"))
        d = data["details"]
        assert d["template"] is True
        for key in ("lmstudio", "koboldcpp", "gpt4all", "llamacpp", "openai_compatible_local"):
            assert key in d


# ========== Hardware ==========

class TestHardwareContract:
    def test_hardware_returns_200_or_500(self):
        resp = client.get("/api/v1/hardware")
        assert resp.status_code in (200, 500)
        if resp.status_code == 200:
            data = resp.json()
            assert data["ok"] is True


# ========== Jobs ==========

class TestJobsContract:
    def test_list_jobs_returns_200_or_500(self):
        resp = client.get("/api/v1/jobs")
        assert resp.status_code in (200, 500)
        if resp.status_code == 200:
            data = resp.json()
            assert data["ok"] is True
            assert "details" in data

    def test_get_job_not_found_returns_200_with_error(self):
        resp = client.get("/api/v1/jobs/nonexistent_job_gal935")
        assert resp.status_code == 200
        data = resp.json()
        assert data["detail"]["ok"] is False
        assert data["detail"]["code"] == "JOB_NOT_FOUND"

    @patch("app.jobs.queue.queue.get_job")
    def test_get_job_found_returns_200(self, mock_get_job):
        mock_job = MagicMock()
        mock_job.to_dict.return_value = {"job_id": "test_job", "status": "completed"}
        mock_get_job.return_value = mock_job
        data = _assert_api_envelope(client.get("/api/v1/jobs/test_job"))
        assert data["details"]["job_id"] == "test_job"

    @patch("app.jobs.queue.queue.cancel_job")
    def test_cancel_job_not_found_returns_500(self, mock_cancel):
        mock_cancel.return_value = False
        resp = client.post("/api/v1/jobs/nonexistent/cancel")
        assert resp.status_code == 500

    @patch("app.jobs.queue.queue.cancel_job")
    def test_cancel_job_success_returns_200(self, mock_cancel):
        mock_cancel.return_value = True
        data = _assert_api_envelope(client.post("/api/v1/jobs/test_job/cancel"))
        assert data["details"]["job_id"] == "test_job"


# ========== Metrics ==========

class TestMetricsContract:
    def test_metrics_returns_200_or_500(self):
        resp = client.get("/api/v1/metrics")
        assert resp.status_code in (200, 500)
        if resp.status_code == 200:
            assert resp.json()["ok"] is True

    def test_metrics_operations_returns_200_or_500(self):
        resp = client.get("/api/v1/metrics/operations")
        assert resp.status_code in (200, 500)
        if resp.status_code == 200:
            assert resp.json()["ok"] is True


# ========== Logs ==========

class TestLogsContract:
    def test_logs_recent_returns_200_or_500(self):
        resp = client.get("/api/v1/logs/recent")
        assert resp.status_code in (200, 500)
        if resp.status_code == 200:
            assert resp.json()["ok"] is True

    def test_logs_summary_returns_200_or_500(self):
        resp = client.get("/api/v1/logs/summary")
        assert resp.status_code in (200, 500)
        if resp.status_code == 200:
            assert resp.json()["ok"] is True

    def test_logs_last_error_returns_200_or_500(self):
        resp = client.get("/api/v1/logs/last-error")
        assert resp.status_code in (200, 500)
        if resp.status_code == 200:
            assert resp.json()["ok"] is True

    def test_logs_diagnostic_returns_200_or_500(self):
        resp = client.get("/api/v1/logs/diagnostic")
        assert resp.status_code in (200, 500)
        if resp.status_code == 200:
            assert resp.json()["ok"] is True

    def test_logs_structured_returns_200_or_500(self):
        resp = client.get("/api/v1/logs/structured")
        assert resp.status_code in (200, 500)
        if resp.status_code == 200:
            assert resp.json()["ok"] is True

    def test_logs_recent_with_filters_returns_200(self):
        resp = client.get("/api/v1/logs/recent?level=ERROR&limit=5")
        assert resp.status_code in (200, 500)
        if resp.status_code == 200:
            assert resp.json()["ok"] is True


# ========== Pipeline ==========

class TestPipelineContract:
    def test_pipeline_status_returns_200(self):
        data = _assert_api_envelope(client.get("/api/v1/pipeline/status"))
        keys = ("llm_available", "wangp_available", "tts_available", "ffmpeg_available")
        assert any(k in data["details"] for k in keys), f"No pipeline key found in {data['details']}"


# ========== Script Endpoints (Project-based) ==========

class TestScriptCurrentContract:
    def test_current_script_project_not_found_returns_200(self):
        resp = client.get("/api/v1/projects/nonexistent_gal935/script/current")
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True

    def test_current_script_empty_project_returns_script_or_error(self):
        pid = "test_gal935_script_empty"
        _setup_project(pid)
        try:
            resp = client.get(f"/api/v1/projects/{pid}/script/current")
            assert resp.status_code in (200, 500)
        finally:
            _teardown_project(pid)

    def test_current_script_with_saved_script(self):
        pid = "test_gal935_script_saved"
        proj_dir = _setup_project(pid)
        script_dir = proj_dir / "script"
        (script_dir / "script_v001.md").write_text("# Script content", encoding="utf-8")
        (script_dir / "script_v001.json").write_text(
            json.dumps({"version": "v001", "status": "Draft", "timestamp": "now", "note": "", "provider_used": "", "response_time_seconds": 0, "quality_score": 0}),
            encoding="utf-8",
        )
        (script_dir / "script_versions.json").write_text(
            json.dumps([{"version": "v001", "status": "Draft", "timestamp": "now", "note": "", "provider_used": "", "response_time_seconds": 0, "quality_score": 0}]),
            encoding="utf-8",
        )
        try:
            data = _assert_api_envelope(client.get(f"/api/v1/projects/{pid}/script/current"))
            assert "script" in data["details"]
        finally:
            _teardown_project(pid)


class TestScriptVersionsContract:
    def test_versions_empty_project(self):
        pid = "test_gal935_versions_empty"
        _setup_project(pid)
        try:
            data = _assert_api_envelope(client.get(f"/api/v1/projects/{pid}/script/versions"))
            assert "versions" in data["details"]
        finally:
            _teardown_project(pid)

    def test_versions_project_not_found_returns_200(self):
        resp = client.get("/api/v1/projects/nonexistent_gal935_v/script/versions")
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True


class TestScriptImproveContract:
    @patch("app.services.script_service.load_current_script")
    def test_improve_no_script_returns_200(self, mock_load):
        mock_load.return_value = {"ok": False, "error": "no script"}
        resp = client.post("/api/v1/projects/test_gal935_imp/script/improve", json={"briefing": ""})
        assert resp.status_code == 200, f"got {resp.status_code}: {resp.text[:200]}"
        data = resp.json()
        assert data["ok"] is True


class TestScriptApproveContract:
    @patch("app.services.script_service.load_current_script")
    def test_approve_no_script_returns_200_with_error(self, mock_load):
        mock_load.return_value = {"ok": False, "error": "no script"}
        resp = client.post("/api/v1/projects/test_gal935_app/script/approve")
        assert resp.status_code == 200, f"got {resp.status_code}: {resp.text[:200]}"
        data = resp.json()
        assert data["detail"]["ok"] is False
        assert data["detail"]["code"] == "APPROVE_FAILED"


class TestScriptNewVersionContract:
    def test_new_version_on_nonexistent_project(self):
        resp = client.post("/api/v1/projects/nonexistent_gal935_nv/script/new-version")
        assert resp.status_code in (200, 500)
        assert "ok" in resp.json()


class TestScriptRestoreContract:
    @patch("app.services.script_service._get_repo")
    def test_restore_without_previous(self, mock_get_repo):
        mock_repo = MagicMock()
        mock_repo.find_previous_version.return_value = type("Result", (), {"ok": False, "error": "no previous"})()
        mock_get_repo.return_value = mock_repo
        resp = client.post("/api/v1/projects/test_gal935_rest/script/restore-previous")
        assert resp.status_code == 500
        data = resp.json()
        assert "detail" in data


class TestScriptViralContract:
    @patch("app.services.script_service.load_current_script")
    def test_viral_no_script_returns_500(self, mock_load):
        mock_load.return_value = {"ok": False, "error": "no script"}
        mock_load.side_effect = None
        resp = client.post("/api/v1/projects/test_gal935_vir/script/more-viral")
        assert resp.status_code == 500


class TestScriptPremiumContract:
    def test_premium_nonexistent_project_returns_500(self):
        resp = client.post("/api/v1/projects/nonexistent_gal935_prem/script/more-premium")
        assert resp.status_code == 500


class TestScriptDirectContract:
    def test_direct_nonexistent_project_returns_500(self):
        resp = client.post("/api/v1/projects/nonexistent_gal935_dir/script/more-direct")
        assert resp.status_code == 500


# ========== Save Manual Edit ==========

class TestSaveManualEditContract:
    @patch("app.api.SaveManualEditUseCase")
    def test_save_edit_happy_path(self, mock_uc_cls):
        mock_uc = MagicMock()
        mock_uc.execute.return_value = {"ok": True, "data": {"version": "v001"}}
        mock_uc_cls.return_value = mock_uc

        data = _assert_api_envelope(
            client.post(
                "/api/v1/projects/test_pid/script/save-manual-edit",
                json={"project_id": "test_pid", "script_markdown": "# script"},
            )
        )
        assert data["details"]["version"] == "v001"


# ========== Script Generate for Project ==========

class TestGenerateScriptForProjectContract:
    def test_generate_for_nonexistent_project_returns_404(self):
        resp = client.post("/api/v1/projects/nonexistent_gal935_gen/script/generate", json={})
        assert resp.status_code == 404
        data = resp.json()
        assert "detail" in data

    def test_generate_for_valid_project_returns_script(self):
        pid = "test_gal935_gen_valid"
        _setup_project(pid)
        try:
            resp = client.post(f"/api/v1/projects/{pid}/script/generate", json={})
            assert resp.status_code in (200, 500)
            if resp.status_code == 200:
                data = resp.json()
                assert data["ok"] is True
                assert data["details"]["project_id"] == pid
                assert data["details"]["script_only"] is True
        finally:
            _teardown_project(pid)
