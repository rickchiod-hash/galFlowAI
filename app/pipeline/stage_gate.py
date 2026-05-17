"""Stage gate system for pipeline validation (PIPE-400 formal)."""

from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path
import logging

from app.config import PROJECTS_DIR

logger = logging.getLogger(__name__)


class PipelineStage(str, Enum):
    """Formal pipeline stages in execution order."""
    SCRIPT = "script"
    APPROVAL = "approval"
    SCENES = "scenes"
    PROMPTS = "prompts"
    AUDIO = "audio"
    RENDER = "render"
    CONCAT = "concat"
    COMPLETE = "complete"


@dataclass
class GateResult:
    """Result of a single stage gate check."""
    ok: bool
    gate: str
    stage: Optional[str] = None
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class StageGate:
    """Base class for a stage gate that validates a pre-condition."""

    def __init__(self, name: str, stage: PipelineStage):
        self.name = name
        self.stage = stage

    def check(self, project_id: str, context: Optional[Dict[str, Any]] = None) -> GateResult:
        """Check if the gate passes. Override in subclasses."""
        return GateResult(ok=True, gate=self.name, stage=self.stage.value)

    def __repr__(self) -> str:
        return f"StageGate({self.name}, stage={self.stage.value})"


class ProjectExistsGate(StageGate):
    """Pre-condition: project directory must exist."""

    def __init__(self):
        super().__init__("project_exists", PipelineStage.SCRIPT)

    def check(self, project_id: str, context: Optional[Dict[str, Any]] = None) -> GateResult:
        project_dir = Path(PROJECTS_DIR) / project_id
        if not project_dir.is_dir():
            return GateResult(
                ok=False,
                gate=self.name,
                stage=self.stage.value,
                error=f"Project '{project_id}' not found at {project_dir}",
            )
        return GateResult(ok=True, gate=self.name, stage=self.stage.value)


class BriefingNotEmptyGate(StageGate):
    """Pre-condition: briefing must have content."""

    def __init__(self):
        super().__init__("briefing_not_empty", PipelineStage.SCRIPT)

    def check(self, project_id: str, context: Optional[Dict[str, Any]] = None) -> GateResult:
        briefing = (context or {}).get("briefing", "")
        if not briefing or not briefing.strip():
            return GateResult(
                ok=False,
                gate=self.name,
                stage=self.stage.value,
                error="Briefing is empty — provide product and target_audience",
            )
        return GateResult(ok=True, gate=self.name, stage=self.stage.value)


class ScriptGeneratedGate(StageGate):
    """Pre-condition: script draft must exist on disk."""

    def __init__(self):
        super().__init__("script_generated", PipelineStage.APPROVAL)

    def check(self, project_id: str, context: Optional[Dict[str, Any]] = None) -> GateResult:
        script_draft = Path(PROJECTS_DIR) / project_id / "script" / "script_draft.md"
        if not script_draft.is_file():
            return GateResult(
                ok=False,
                gate=self.name,
                stage=self.stage.value,
                error=f"Script draft not found at {script_draft}",
            )
        return GateResult(ok=True, gate=self.name, stage=self.stage.value)


class ScriptApprovedGate(StageGate):
    """Pre-condition: script must be approved before splitting scenes."""

    def __init__(self):
        super().__init__("script_approved", PipelineStage.SCENES)

    def check(self, project_id: str, context: Optional[Dict[str, Any]] = None) -> GateResult:
        approval_file = Path(PROJECTS_DIR) / project_id / "script" / "script_approved.md"
        if not approval_file.is_file():
            return GateResult(
                ok=False,
                gate=self.name,
                stage=self.stage.value,
                error="Script not approved — approve script/script_draft.md before generating scenes",
            )
        return GateResult(ok=True, gate=self.name, stage=self.stage.value)


class ScenesExistGate(StageGate):
    """Pre-condition: scenes must exist before building prompts."""

    def __init__(self):
        super().__init__("scenes_exist", PipelineStage.PROMPTS)

    def check(self, project_id: str, context: Optional[Dict[str, Any]] = None) -> GateResult:
        scenes_file = Path(PROJECTS_DIR) / project_id / "storyboard" / "scenes.json"
        if not scenes_file.is_file():
            return GateResult(
                ok=False,
                gate=self.name,
                stage=self.stage.value,
                error=f"Scenes not found at {scenes_file}",
            )
        return GateResult(ok=True, gate=self.name, stage=self.stage.value)


class PromptsExistGate(StageGate):
    """Pre-condition: prompt files must exist before rendering."""

    def __init__(self):
        super().__init__("prompts_exist", PipelineStage.RENDER)

    def check(self, project_id: str, context: Optional[Dict[str, Any]] = None) -> GateResult:
        prompts_dir = Path(PROJECTS_DIR) / project_id / "prompts"
        if not prompts_dir.is_dir():
            return GateResult(
                ok=False,
                gate=self.name,
                stage=self.stage.value,
                error=f"Prompts directory not found at {prompts_dir}",
            )
        prompt_files = list(prompts_dir.iterdir())
        if not prompt_files:
            return GateResult(
                ok=False,
                gate=self.name,
                stage=self.stage.value,
                error=f"No prompt files found in {prompts_dir}",
            )
        return GateResult(ok=True, gate=self.name, stage=self.stage.value)


class RenderedScenesGate(StageGate):
    """Pre-condition: at least one scene rendered before concat."""

    def __init__(self):
        super().__init__("rendered_scenes", PipelineStage.CONCAT)

    def check(self, project_id: str, context: Optional[Dict[str, Any]] = None) -> GateResult:
        rendered = (context or {}).get("rendered_scenes", [])
        successful = [s for s in rendered if s.get("status") == "completed"]
        if not successful:
            return GateResult(
                ok=False,
                gate=self.name,
                stage=self.stage.value,
                error="No scenes rendered successfully — cannot concatenate",
            )
        return GateResult(
            ok=True,
            gate=self.name,
            stage=self.stage.value,
            details={"rendered_count": len(successful), "total": len(rendered)},
        )


STAGE_GATES: Dict[PipelineStage, List[StageGate]] = {
    PipelineStage.SCRIPT: [ProjectExistsGate(), BriefingNotEmptyGate()],
    PipelineStage.APPROVAL: [ScriptGeneratedGate()],
    PipelineStage.SCENES: [ScriptApprovedGate()],
    PipelineStage.PROMPTS: [ScenesExistGate()],
    PipelineStage.AUDIO: [],
    PipelineStage.RENDER: [PromptsExistGate()],
    PipelineStage.CONCAT: [RenderedScenesGate()],
    PipelineStage.COMPLETE: [],
}


def check_gates(
    stage: PipelineStage,
    project_id: str,
    context: Optional[Dict[str, Any]] = None,
) -> List[GateResult]:
    """Check all gates for a given pipeline stage."""
    results: List[GateResult] = []
    for gate in STAGE_GATES.get(stage, []):
        try:
            result = gate.check(project_id, context)
            results.append(result)
        except Exception as e:
            logger.exception("Gate check error: %s.%s", gate.name, e)
            results.append(GateResult(
                ok=False,
                gate=gate.name,
                stage=stage.value,
                error=f"Gate check error: {e}",
            ))
    return results


def all_gates_pass(
    stage: PipelineStage,
    project_id: str,
    context: Optional[Dict[str, Any]] = None,
) -> bool:
    """Check if all gates pass for a given stage."""
    return all(r.ok for r in check_gates(stage, project_id, context))


def get_failed_gates(
    stage: PipelineStage,
    project_id: str,
    context: Optional[Dict[str, Any]] = None,
) -> List[GateResult]:
    """Return only the failed gates for a given stage."""
    return [r for r in check_gates(stage, project_id, context) if not r.ok]
