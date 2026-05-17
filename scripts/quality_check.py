"""Quality check CLI — run stage gates and prompt reviews on a project.

Usage:
    py scripts/quality_check.py <project_id> [--review-prompts]
    py scripts/quality_check.py <project_id> [--gate <stage>]

Examples:
    py scripts/quality_check.py meu_projeto
    py scripts/quality_check.py meu_projeto --gate scenes
    py scripts/quality_check.py meu_projeto --review-prompts
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

from app.config import PROJECTS_DIR
from app.pipeline.stage_gate import (
    PipelineStage, check_gates, STAGE_GATES, GateResult
)
from app.domain.prompt_reviewer import review_scene_prompts


def list_gates() -> None:
    """Print all registered gates."""
    print("=== Stage Gate Registry ===")
    for stage, gates in STAGE_GATES.items():
        if gates:
            print(f"  {stage.value}:")
            for g in gates:
                print(f"    - {g.name}")
        else:
            print(f"  {stage.value}: (no gates)")


def run_gate(stage_name: str, project_id: str) -> None:
    """Run gates for a specific stage."""
    try:
        stage = PipelineStage(stage_name)
    except ValueError:
        valid = [s.value for s in PipelineStage]
        print(f"Invalid stage '{stage_name}'. Valid: {', '.join(valid)}")
        return

    project_dir = Path(PROJECTS_DIR) / project_id
    if not project_dir.is_dir():
        print(f"Project '{project_id}' not found at {project_dir}")
        return

    results = check_gates(stage, project_id)
    gate_names = [g.name for g in STAGE_GATES.get(stage, [])]

    if not gate_names:
        print(f"No gates registered for stage '{stage_name}'")
        return

    print(f"\n=== Stage: {stage_name} ===")
    all_pass = True
    for result in results:
        status = "✅ PASS" if result.ok else "❌ FAIL"
        print(f"  {status} | {result.gate}")
        if result.error:
            print(f"         └─ {result.error}")
        if not result.ok:
            all_pass = False

    if all_pass:
        print(f"\n  Result: ✅ All gates pass — stage '{stage_name}' is clear to proceed.")
    else:
        print(f"\n  Result: ❌ Some gates blocked — stage '{stage_name}' cannot proceed.")


def run_all_gates(project_id: str) -> Dict[str, Any]:
    """Run all gates for a project and return summary."""
    from app.pipeline.stage_gate import check_gates

    results = {}
    all_pass = True
    print(f"\n=== Gate Report: project '{project_id}' ===\n")

    for stage in PipelineStage:
        gates = STAGE_GATES.get(stage, [])
        if not gates:
            continue

        stage_results = check_gates(stage, project_id)
        stage_ok = all(r.ok for r in stage_results)
        if not stage_ok:
            all_pass = False

        icon = "✅" if stage_ok else "❌"
        print(f"  {icon} {stage.value}:")
        for r in stage_results:
            print(f"       {'✅' if r.ok else '❌'} {r.gate}")
            if r.error:
                print(f"           └─ {r.error}")

        results[stage.value] = {
            "pass": stage_ok,
            "gates": [{"name": r.gate, "ok": r.ok, "error": r.error} for r in stage_results],
        }

    print(f"\n  Overall: {'✅ ALL GATES PASS' if all_pass else '❌ SOME GATES BLOCKED'}")
    return {"project_id": project_id, "overall_pass": all_pass, "stages": results}


def review_prompts(project_id: str) -> Dict[str, Any]:
    """Review prompts for a project."""
    scenes_file = Path(PROJECTS_DIR) / project_id / "storyboard" / "scenes.json"
    if not scenes_file.is_file():
        print(f"No scenes file found at {scenes_file}")
        return {"error": "No scenes file found"}

    try:
        scenes = json.loads(scenes_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Failed to read scenes: {e}")
        return {"error": str(e)}

    if not scenes:
        print("No scenes to review.")
        return {"error": "No scenes"}

    result = review_scene_prompts(scenes)

    print(f"\n=== Prompt Review Report: project '{project_id}' ===\n")
    print(f"  Scenes reviewed: {result['scene_count']}")
    print(f"  Average score:   {result['average_score']}")
    print(f"  Total violations: {result['total_violations']}")
    print()

    for scene_review in result["scene_reviews"]:
        score = scene_review["score"]
        icon = "✅" if score >= 0.8 else ("⚠️" if score >= 0.5 else "❌")
        violations = scene_review["violations"]
        print(f"  {icon} {scene_review['target']} (score: {score:.2f}, violations: {len(violations)})")
        for v in violations:
            sev_icon = {"error": "🔴", "warning": "🟡", "info": "🔵"}.get(v["severity"], "⚪")
            print(f"       {sev_icon} [{v['severity']}] {v['rule']}: {v['message']}")
            print(f"           💡 {v['suggestion']}")

    return result


def export_report(project_id: str) -> None:
    """Export full quality report to project directory."""
    gates = run_all_gates(project_id)
    prompts = review_prompts(project_id)

    report = {
        "project_id": project_id,
        "gates": gates,
        "prompts": prompts,
    }
    report_dir = Path(PROJECTS_DIR) / project_id / "quality"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "quality_report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nReport exported to {report_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="GalFlowAI Quality Check CLI")
    parser.add_argument("project_id", help="Project ID to check")
    parser.add_argument("--gate", "-g", help="Check specific stage gate", default=None)
    parser.add_argument("--review-prompts", "-p", action="store_true", help="Review scene prompts")
    parser.add_argument("--list-gates", "-l", action="store_true", help="List all registered gates")
    parser.add_argument("--export", "-e", action="store_true", help="Export full report")

    args = parser.parse_args()

    if args.list_gates:
        list_gates()
        return

    if args.gate:
        run_gate(args.gate, args.project_id)
        return

    if args.review_prompts:
        review_prompts(args.project_id)
        return

    if args.export:
        export_report(args.project_id)
        return

    run_all_gates(args.project_id)


if __name__ == "__main__":
    main()
