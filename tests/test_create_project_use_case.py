import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import patch
from app.application.use_cases.create_project_use_case import CreateProjectUseCase


class TestCreateProjectUseCase:
    def test_execute_success(self):
        uc = CreateProjectUseCase()
        with patch("app.application.use_cases.create_project_use_case.create_project") as mock_cp:
            mock_cp.return_value = {"id": "proj_1", "name": "Test"}
            result = uc.execute(project_name="Test Project")
        assert result.ok is True
        assert result.data["id"] == "proj_1"

    def test_execute_invalid_name_empty(self):
        uc = CreateProjectUseCase()
        result = uc.execute(project_name="")
        assert result.ok is False
        assert "Invalid" in result.error

    def test_execute_invalid_name_blank(self):
        uc = CreateProjectUseCase()
        result = uc.execute(project_name="   ")
        assert result.ok is False
        assert "Invalid" in result.error

    def test_execute_exception(self):
        uc = CreateProjectUseCase()
        with patch("app.application.use_cases.create_project_use_case.create_project") as mock_cp:
            mock_cp.side_effect = RuntimeError("disk full")
            result = uc.execute(project_name="Test")
        assert result.ok is False
        assert "disk full" in result.error
