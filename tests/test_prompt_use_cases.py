import sys
import json
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import patch, MagicMock, ANY
from app.application.use_cases.prompt_use_cases import (
    CreatePromptPackUseCase,
    LoadPromptPackUseCase,
    ValidatePromptConsistencyUseCase,
)


class TestCreatePromptPackUseCase:
    def test_execute_minimal(self):
        uc = CreatePromptPackUseCase()
        with patch.object(uc, "_save_pack"):
            result = uc.execute(project_id="proj_1", script="Test script")
        assert result["ok"] is True
        assert result["data"]["project_id"] == "proj_1"
        assert result["data"]["script_summary"] == "Test script"

    def test_execute_with_scenes(self):
        uc = CreatePromptPackUseCase()
        scenes = [
            {"id": "s1", "prompt": "a cat", "duration": 5},
            {"id": "s2", "prompt": "a dog", "duration": 3},
        ]
        with patch.object(uc, "_save_pack"):
            result = uc.execute(project_id="proj_1", script="Test", scenes=scenes)
        assert result["ok"] is True
        assert len(result["data"]["scene_prompts"]) == 2

    def test_execute_with_style(self):
        uc = CreatePromptPackUseCase()
        with patch.object(uc, "_save_pack"):
            result = uc.execute(project_id="proj_1", script="Test", visual_style="dark")
        assert result["ok"] is True
        assert result["data"]["visual_style"] == "dark"

    def test_invalid_project_id(self):
        uc = CreatePromptPackUseCase()
        result = uc.execute(project_id="", script="text")
        assert result["ok"] is False

    def test_exception(self):
        uc = CreatePromptPackUseCase()
        with patch.object(uc, "_save_pack") as mock:
            mock.side_effect = OSError("disk full")
            result = uc.execute(project_id="proj_1", script="text")
        assert result["ok"] is False


class TestLoadPromptPackUseCase:
    def test_execute_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            uc = LoadPromptPackUseCase()
            uc.packs_dir = Path(tmp)
            prompt_dir = Path(tmp) / "proj_1" / "prompts"
            prompt_dir.mkdir(parents=True)
            (prompt_dir / "prompt_pack.json").write_text(
                json.dumps({"project_id": "proj_1", "version": "1.0"}), encoding="utf-8"
            )
            result = uc.execute(project_id="proj_1")
        assert result["ok"] is True
        assert result["data"]["project_id"] == "proj_1"

    def test_execute_not_found(self):
        with tempfile.TemporaryDirectory() as tmp:
            uc = LoadPromptPackUseCase()
            uc.packs_dir = Path(tmp)
            result = uc.execute(project_id="proj_1")
        assert result["ok"] is False
        assert "not found" in result["error"]

    def test_invalid_project_id(self):
        uc = LoadPromptPackUseCase()
        result = uc.execute(project_id="")
        assert result["ok"] is False

    def test_exception(self):
        with tempfile.TemporaryDirectory() as tmp:
            uc = LoadPromptPackUseCase()
            uc.packs_dir = Path(tmp)
            prompt_dir = Path(tmp) / "proj_1" / "prompts"
            prompt_dir.mkdir(parents=True)
            (prompt_dir / "prompt_pack.json").write_text("not json", encoding="utf-8")
            result = uc.execute(project_id="proj_1")
        assert result["ok"] is False


class TestValidatePromptConsistencyUseCase:
    def test_valid_pack(self):
        uc = ValidatePromptConsistencyUseCase()
        pack = {
            "project_id": "proj_1",
            "scene_prompts": [
                {"prompt_pos": "p1", "duration": 5},
                {"prompt_pos": "p2", "duration": 3},
            ],
            "negative_prompt_base": "blurry",
        }
        result = uc.execute(pack_data=pack)
        assert result["ok"] is True
        assert result["data"]["valid"] is True

    def test_no_scene_prompts(self):
        uc = ValidatePromptConsistencyUseCase()
        pack = {"project_id": "proj_1", "negative_prompt_base": "blurry"}
        result = uc.execute(pack_data=pack)
        assert result["ok"] is True
        assert result["data"]["valid"] is False
        assert any("No scene prompts" in i for i in result["data"]["issues"])

    def test_missing_fields_in_scenes(self):
        uc = ValidatePromptConsistencyUseCase()
        pack = {
            "project_id": "proj_1",
            "scene_prompts": [{"prompt_pos": "", "duration": 0}],
            "negative_prompt_base": "blurry",
        }
        result = uc.execute(pack_data=pack)
        assert result["ok"] is True
        assert result["data"]["valid"] is False

    def test_missing_negative_prompt(self):
        uc = ValidatePromptConsistencyUseCase()
        pack = {"project_id": "proj_1", "scene_prompts": [{"prompt_pos": "p1", "duration": 5}]}
        result = uc.execute(pack_data=pack)
        assert result["ok"] is True
        assert result["data"]["valid"] is False
        assert any("negative" in i.lower() for i in result["data"]["issues"])

    def test_invalid_pack_data(self):
        uc = ValidatePromptConsistencyUseCase()
        result = uc.execute(pack_data={})
        assert result["ok"] is False

    def test_exception(self):
        uc = ValidatePromptConsistencyUseCase()
        result = uc.execute(pack_data=None)
        assert result["ok"] is False
