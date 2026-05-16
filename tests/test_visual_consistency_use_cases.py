import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import patch, MagicMock, ANY
from app.application.use_cases.visual_consistency_use_cases import (
    CreateVisualBibleUseCase,
    GenerateScenePromptsUseCase,
    ValidateVisualConsistencyUseCase,
)


class TestCreateVisualBibleUseCase:
    def test_execute_defaults(self):
        uc = CreateVisualBibleUseCase()
        with patch.object(uc, "_save_bible"):
            result = uc.execute(project_id="proj_1")
        assert result["ok"] is True
        bible = result["data"]
        assert bible["project_id"] == "proj_1"
        assert bible["color_palette"] == ["#FFFFFF", "#000000"]
        assert bible["style_keywords"] == ["cinematic", "modern"]

    def test_execute_custom(self):
        uc = CreateVisualBibleUseCase()
        with patch.object(uc, "_save_bible"):
            result = uc.execute(
                project_id="proj_1",
                color_palette=["#FF0000", "#00FF00"],
                style_keywords=["vibrant"],
                logo_path="/path/logo.png",
            )
        assert result["ok"] is True
        assert result["data"]["color_palette"] == ["#FF0000", "#00FF00"]
        assert result["data"]["logo_path"] == "/path/logo.png"

    def test_invalid_project_id(self):
        uc = CreateVisualBibleUseCase()
        result = uc.execute(project_id="")
        assert result["ok"] is False

    def test_exception(self):
        uc = CreateVisualBibleUseCase()
        with patch.object(uc, "_save_bible") as mock:
            mock.side_effect = OSError("permission denied")
            result = uc.execute(project_id="proj_1")
        assert result["ok"] is False


class TestGenerateScenePromptsUseCase:
    def test_execute_with_bible(self):
        uc = GenerateScenePromptsUseCase()
        bible = {
            "version": "1.0",
            "style_keywords": ["dark", "cinematic"],
            "color_palette": ["#000000", "#FFFFFF"],
            "negative_prompt_base": "blurry, low quality",
        }
        scenes = [
            {"id": "s1", "description": "Hero shot", "duration": 3},
            {"id": "s2", "description": "Product closeup", "duration": 5},
        ]
        with patch.object(uc, "_save_contracts"):
            result = uc.execute(
                project_id="proj_1",
                script="Script text",
                scenes=scenes,
                visual_bible=bible,
            )
        assert result["ok"] is True
        assert result["data"]["count"] == 2
        assert "colors: #000000, #FFFFFF" in result["data"]["scene_contracts"][0]["prompt_pos"]

    def test_execute_without_bible(self):
        uc = GenerateScenePromptsUseCase()
        scenes = [{"id": "s1", "description": "Hero shot"}]
        with patch.object(uc, "_load_bible", return_value=None), patch.object(uc, "_save_contracts"):
            result = uc.execute(project_id="proj_1", script="Script", scenes=scenes)
        assert result["ok"] is True
        assert "visual_bible_version" in result["data"]

    def test_invalid_params(self):
        uc = GenerateScenePromptsUseCase()
        result = uc.execute(project_id="", script="", scenes=[])
        assert result["ok"] is False

    def test_exception(self):
        uc = GenerateScenePromptsUseCase()
        with patch.object(uc, "_validate") as mock:
            mock.side_effect = ValueError("unexpected")
            result = uc.execute(project_id="proj_1", script="s", scenes=[{"id": "s1"}])
        assert result["ok"] is False


class TestValidateVisualConsistencyUseCase:
    def test_valid_contracts(self):
        uc = ValidateVisualConsistencyUseCase()
        contracts = [
            {"prompt_pos": "p1", "prompt_neg": "n1", "style": "cinematic"},
            {"prompt_pos": "p2", "prompt_neg": "n2", "style": "cinematic"},
        ]
        result = uc.execute(contracts=contracts)
        assert result["ok"] is True
        assert result["data"]["valid"] is True
        assert len(result["data"]["issues"]) == 0

    def test_missing_fields(self):
        uc = ValidateVisualConsistencyUseCase()
        contracts = [{"prompt_pos": "", "prompt_neg": "", "style": ""}]
        result = uc.execute(contracts=contracts)
        assert result["ok"] is True
        assert result["data"]["valid"] is False
        assert len(result["data"]["issues"]) >= 3

    def test_multiple_styles(self):
        uc = ValidateVisualConsistencyUseCase()
        contracts = [
            {"prompt_pos": "p1", "prompt_neg": "n1", "style": "dark"},
            {"prompt_pos": "p2", "prompt_neg": "n2", "style": "bright"},
        ]
        result = uc.execute(contracts=contracts)
        assert result["ok"] is True
        assert result["data"]["valid"] is False
        assert any("Multiple styles" in i for i in result["data"]["issues"])

    def test_empty_contracts(self):
        uc = ValidateVisualConsistencyUseCase()
        result = uc.execute(contracts=[])
        assert result["ok"] is False

    def test_exception(self):
        uc = ValidateVisualConsistencyUseCase()
        result = uc.execute(contracts=None)
        assert result["ok"] is False
