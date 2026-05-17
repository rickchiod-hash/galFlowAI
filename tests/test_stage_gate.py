"""Tests for stage gate system (PIPE-400)."""

from pathlib import Path
from unittest.mock import patch

import pytest

from app.pipeline.stage_gate import (
    PipelineStage,
    GateResult,
    ProjectExistsGate,
    BriefingNotEmptyGate,
    ScriptGeneratedGate,
    ScriptApprovedGate,
    ScenesExistGate,
    PromptsExistGate,
    RenderedScenesGate,
    check_gates,
    all_gates_pass,
    get_failed_gates,
    STAGE_GATES,
)


# ---------------------------------------------------------------------------
# Gate unit tests
# ---------------------------------------------------------------------------


def test_pipeline_stage_enum_values():
    assert PipelineStage.SCRIPT.value == "script"
    assert PipelineStage.APPROVAL.value == "approval"
    assert PipelineStage.SCENES.value == "scenes"
    assert PipelineStage.PROMPTS.value == "prompts"
    assert PipelineStage.AUDIO.value == "audio"
    assert PipelineStage.RENDER.value == "render"
    assert PipelineStage.CONCAT.value == "concat"
    assert PipelineStage.COMPLETE.value == "complete"


def test_gate_result_defaults():
    r = GateResult(ok=True, gate="test_gate")
    assert r.ok is True
    assert r.gate == "test_gate"
    assert r.stage is None
    assert r.error is None
    assert r.details is None


class TestProjectExistsGate:
    def test_passes_when_project_exists(self, tmp_path: Path):
        (tmp_path / "my_project").mkdir()
        gate = ProjectExistsGate()
        with patch("app.pipeline.stage_gate.PROJECTS_DIR", tmp_path):
            result = gate.check("my_project")
            assert result.ok is True

    def test_fails_when_project_missing(self, tmp_path: Path):
        gate = ProjectExistsGate()
        with patch("app.pipeline.stage_gate.PROJECTS_DIR", tmp_path):
            result = gate.check("nonexistent")
            assert result.ok is False
            assert "not found" in (result.error or "")


class TestBriefingNotEmptyGate:
    def test_passes_with_content(self):
        gate = BriefingNotEmptyGate()
        result = gate.check("proj", {"briefing": "Produto X para público Y"})
        assert result.ok is True

    def test_fails_on_empty(self):
        gate = BriefingNotEmptyGate()
        result = gate.check("proj", {"briefing": ""})
        assert result.ok is False
        assert "empty" in (result.error or "")

    def test_fails_on_whitespace(self):
        gate = BriefingNotEmptyGate()
        result = gate.check("proj", {"briefing": "   "})
        assert result.ok is False

    def test_fails_when_missing(self):
        gate = BriefingNotEmptyGate()
        result = gate.check("proj", {})
        assert result.ok is False


class TestScenesExistGate:
    def test_passes_when_scenes_file_exists(self, tmp_path: Path):
        proj_dir = tmp_path / "proj" / "storyboard"
        proj_dir.mkdir(parents=True)
        (proj_dir / "scenes.json").write_text("[]")
        gate = ScenesExistGate()
        with patch("app.pipeline.stage_gate.PROJECTS_DIR", tmp_path):
            result = gate.check("proj")
            assert result.ok is True

    def test_fails_when_scenes_file_missing(self, tmp_path: Path):
        gate = ScenesExistGate()
        with patch("app.pipeline.stage_gate.PROJECTS_DIR", tmp_path):
            result = gate.check("proj")
            assert result.ok is False
            assert "not found" in (result.error or "")


class TestPromptsExistGate:
    def test_passes_when_prompt_files_exist(self, tmp_path: Path):
        prompts_dir = tmp_path / "proj" / "prompts"
        prompts_dir.mkdir(parents=True)
        (prompts_dir / "scene_0.md").write_text("test prompt")
        gate = PromptsExistGate()
        with patch("app.pipeline.stage_gate.PROJECTS_DIR", tmp_path):
            result = gate.check("proj")
            assert result.ok is True

    def test_fails_when_no_prompt_files(self, tmp_path: Path):
        gate = PromptsExistGate()
        with patch("app.pipeline.stage_gate.PROJECTS_DIR", tmp_path):
            result = gate.check("proj")
            assert result.ok is False

    def test_fails_when_prompts_dir_missing(self, tmp_path: Path):
        gate = PromptsExistGate()
        with patch("app.pipeline.stage_gate.PROJECTS_DIR", tmp_path):
            result = gate.check("proj")
            assert result.ok is False


class TestRenderedScenesGate:
    def test_passes_with_rendered_scenes(self):
        gate = RenderedScenesGate()
        result = gate.check("proj", {
            "rendered_scenes": [
                {"status": "completed", "video_path": "out.mp4"},
                {"status": "completed", "video_path": "out2.mp4"},
            ]
        })
        assert result.ok is True
        assert result.details == {"rendered_count": 2, "total": 2}

    def test_fails_when_no_scenes(self):
        gate = RenderedScenesGate()
        result = gate.check("proj", {"rendered_scenes": []})
        assert result.ok is False
        assert "No scenes" in (result.error or "")

    def test_fails_when_all_failed(self):
        gate = RenderedScenesGate()
        result = gate.check("proj", {
            "rendered_scenes": [
                {"status": "failed"},
                {"status": "failed"},
            ]
        })
        assert result.ok is False


# ---------------------------------------------------------------------------
# Gate registry tests
# ---------------------------------------------------------------------------


class TestGateRegistry:
    def test_all_stages_have_registry_entry(self):
        for stage in PipelineStage:
            assert stage in STAGE_GATES, f"Missing STAGE_GATES entry for {stage}"

    def test_script_gates(self):
        gates = STAGE_GATES[PipelineStage.SCRIPT]
        names = [g.name for g in gates]
        assert "project_exists" in names
        assert "briefing_not_empty" in names

    def test_concat_gate(self):
        gates = STAGE_GATES[PipelineStage.CONCAT]
        names = [g.name for g in gates]
        assert "rendered_scenes" in names

    def test_empty_gate_stages(self):
        for stage in [PipelineStage.AUDIO, PipelineStage.COMPLETE]:
            assert STAGE_GATES[stage] == []


# ---------------------------------------------------------------------------
# check_gates / all_gates_pass / get_failed_gates
# ---------------------------------------------------------------------------


def test_check_gates_returns_list(tmp_path: Path):
    with patch("app.pipeline.stage_gate.PROJECTS_DIR", tmp_path):
        results = check_gates(PipelineStage.SCRIPT, "nonexistent_proj",
                              {"briefing": "test"})
        assert isinstance(results, list)
        assert len(results) >= 1
        assert isinstance(results[0], GateResult)


def test_all_gates_pass_true_with_fixture(tmp_path: Path):
    (tmp_path / "proj").mkdir()
    with patch("app.pipeline.stage_gate.PROJECTS_DIR", tmp_path):
        ok = all_gates_pass(PipelineStage.SCRIPT, "proj",
                            {"briefing": "Produto X para público Y"})
        assert ok is True


def test_all_gates_pass_false_on_empty_briefing(tmp_path: Path):
    (tmp_path / "proj_empty").mkdir()
    with patch("app.pipeline.stage_gate.PROJECTS_DIR", tmp_path):
        ok = all_gates_pass(PipelineStage.SCRIPT, "proj_empty",
                            {"briefing": ""})
        assert ok is False


def test_get_failed_gates_returns_only_failures(tmp_path: Path):
    with patch("app.pipeline.stage_gate.PROJECTS_DIR", tmp_path):
        failed = get_failed_gates(PipelineStage.SCRIPT, "missing_proj",
                                  {"briefing": "test"})
        assert all(not r.ok for r in failed)
        names = [r.gate for r in failed]
        assert "project_exists" in names


def test_check_gates_exception_handling(tmp_path: Path):
    class BrokenGate(RenderedScenesGate):
        def check(self, pid, ctx=None):
            raise RuntimeError("oh no")

    original = STAGE_GATES[PipelineStage.CONCAT]
    try:
        STAGE_GATES[PipelineStage.CONCAT] = [BrokenGate()]
        results = check_gates(PipelineStage.CONCAT, "proj", {})
        assert len(results) == 1
        assert results[0].ok is False
        assert "oh no" in (results[0].error or "")
    finally:
        STAGE_GATES[PipelineStage.CONCAT] = original


# ---------------------------------------------------------------------------
# Pipeline integration smoke test
# ---------------------------------------------------------------------------


def test_check_stage_gate_method_contract(tmp_path: Path):
    (tmp_path / "test_proj").mkdir()
    with patch("app.pipeline.stage_gate.PROJECTS_DIR", tmp_path):
        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
        pipeline = VideoGenerationPipeline(llm_provider=None)

        result = pipeline._check_stage_gate(
            PipelineStage.SCRIPT, "test_proj",
            {"briefing": "Produto Y"}
        )
        assert result is None

        result = pipeline._check_stage_gate(
            PipelineStage.SCRIPT, "missing_proj",
            {"briefing": "Produto Y"}
        )
        assert result is not None
        assert result.get("success") is False
        assert "gate" in result
        assert "stage" in result
        assert result["stage"] == "script"
        assert "error" in result
