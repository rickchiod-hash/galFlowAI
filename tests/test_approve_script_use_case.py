import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import patch, MagicMock
from app.application.use_cases.approve_script_use_case import ApproveScriptUseCase


class TestApproveScriptUseCase:
    def test_execute_success(self):
        uc = ApproveScriptUseCase()
        with patch("app.application.use_cases.approve_script_use_case.approve_script_service") as mock_svc:
            mock_svc.return_value = {"ok": True, "script": "test", "status": "approved"}
            result = uc.execute(project_id="proj_1")
        assert result.ok is True
        assert result.data["status"] == "approved"

    def test_execute_invalid_project_id(self):
        uc = ApproveScriptUseCase()
        result = uc.execute(project_id="")
        assert result.ok is False
        assert "Invalid" in result.error

    def test_execute_service_failure(self):
        uc = ApproveScriptUseCase()
        with patch("app.application.use_cases.approve_script_use_case.approve_script_service") as mock_svc:
            mock_svc.return_value = {"ok": False, "error": "not found"}
            result = uc.execute(project_id="proj_1")
        assert result.ok is False
        assert "not found" in result.error

    def test_execute_exception(self):
        uc = ApproveScriptUseCase()
        with patch("app.application.use_cases.approve_script_use_case.approve_script_service") as mock_svc:
            mock_svc.side_effect = ValueError("engine error")
            result = uc.execute(project_id="proj_1")
        assert result.ok is False
        assert "engine error" in result.error
