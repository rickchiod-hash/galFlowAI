import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import patch, MagicMock, ANY
from app.application.use_cases.script_improvement_use_cases import (
    ImproveScriptUseCase,
    ApproveScriptUseCase,
    GetScriptVersionsUseCase,
)


class TestImproveScriptUseCase:
    def test_viral_improvement(self):
        uc = ImproveScriptUseCase()
        with patch.object(uc, "_save_version"):
            result = uc.execute(project_id="proj_1", script="Hello world", improvement_type="viral")
        assert result["ok"] is True
        assert "!" in result["data"]["improved"]
        assert result["data"]["improvement_type"] == "viral"

    def test_premium_improvement(self):
        uc = ImproveScriptUseCase()
        with patch.object(uc, "_save_version"):
            result = uc.execute(project_id="proj_1", script="Este é bom grande", improvement_type="premium")
        assert result["ok"] is True
        improved = result["data"]["improved"]
        assert "excelente" in improved
        assert "extraordinário" in improved
        assert "exclusiva" in improved

    def test_direct_improvement(self):
        uc = ImproveScriptUseCase()
        with patch.object(uc, "_save_version"):
            result = uc.execute(project_id="proj_1", script="Frase um. Frase dois. Frase três.", improvement_type="direct")
        assert result["ok"] is True
        assert "Frase um" in result["data"]["improved"]

    def test_general_improvement(self):
        uc = ImproveScriptUseCase()
        with patch.object(uc, "_save_version"):
            result = uc.execute(project_id="proj_1", script="Meu roteiro", improvement_type="general")
        assert result["ok"] is True
        assert "Crie agora" in result["data"]["improved"]

    def test_invalid_project_id(self):
        uc = ImproveScriptUseCase()
        result = uc.execute(project_id="", script="text")
        assert result["ok"] is False

    def test_invalid_script(self):
        uc = ImproveScriptUseCase()
        result = uc.execute(project_id="proj_1", script="")
        assert result["ok"] is False

    def test_exception(self):
        uc = ImproveScriptUseCase()
        with patch.object(uc, "_apply_improvement") as mock:
            mock.side_effect = ValueError("fail")
            result = uc.execute(project_id="proj_1", script="text")
        assert result["ok"] is False

    def test_save_version_called(self):
        uc = ImproveScriptUseCase()
        with patch.object(uc, "_save_version") as mock_save:
            uc.execute(project_id="proj_1", script="text", improvement_type="viral")
            mock_save.assert_called_once()


class TestImprovementApproveScriptUseCase:
    def test_approve(self):
        uc = ApproveScriptUseCase()
        with patch.object(uc, "_save_approval"):
            result = uc.execute(project_id="proj_1", script="Script content", approved=True)
        assert result["ok"] is True
        assert result["data"]["approved"] is True

    def test_reject(self):
        uc = ApproveScriptUseCase()
        with patch.object(uc, "_save_approval"):
            result = uc.execute(project_id="proj_1", script="Script content", approved=False)
        assert result["ok"] is True
        assert result["data"]["approved"] is False

    def test_invalid_project_id(self):
        uc = ApproveScriptUseCase()
        result = uc.execute(project_id="", script="text")
        assert result["ok"] is False

    def test_invalid_script(self):
        uc = ApproveScriptUseCase()
        result = uc.execute(project_id="proj_1", script="")
        assert result["ok"] is False

    def test_save_approval_called(self):
        uc = ApproveScriptUseCase()
        with patch.object(uc, "_save_approval") as mock_save:
            uc.execute(project_id="proj_1", script="text")
            mock_save.assert_called_once()


class TestGetScriptVersionsUseCase:
    def test_execute_no_versions(self):
        uc = GetScriptVersionsUseCase()
        with patch.object(uc, "_load_versions", return_value=[]):
            result = uc.execute(project_id="proj_1")
        assert result["ok"] is True
        assert result["data"]["count"] == 0

    def test_execute_with_versions(self):
        uc = GetScriptVersionsUseCase()
        versions = [{"timestamp": "2024-01-01", "improvement_type": "viral"}]
        with patch.object(uc, "_load_versions", return_value=versions):
            result = uc.execute(project_id="proj_1")
        assert result["ok"] is True
        assert result["data"]["count"] == 1

    def test_invalid_project_id(self):
        uc = GetScriptVersionsUseCase()
        result = uc.execute(project_id="")
        assert result["ok"] is False

    def test_exception(self):
        uc = GetScriptVersionsUseCase()
        with patch.object(uc, "_load_versions") as mock:
            mock.side_effect = RuntimeError("disk error")
            result = uc.execute(project_id="proj_1")
        assert result["ok"] is False

    def test_load_versions_returns_sorted(self):
        uc = GetScriptVersionsUseCase()
        with patch.object(uc, "_load_versions") as mock:
            mock.return_value = [{"timestamp": "2"}, {"timestamp": "1"}]
            result = uc.execute(project_id="proj_1")
        assert result["ok"] is True
        assert result["data"]["versions"][0]["timestamp"] == "2"
