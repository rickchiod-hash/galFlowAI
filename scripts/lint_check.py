"""Run lint checks (ruff) across the codebase.

Usage:
    py scripts/lint_check.py          # check all
    py scripts/lint_check.py --fix    # auto-fix safe issues
"""

import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="GalFlowAI Lint Check")
    parser.add_argument("--fix", action="store_true", help="Auto-fix safe issues")
    parser.add_argument("--format", action="store_true", help="Check formatting only")
    parser.add_argument("--lint", action="store_true", help="Check lint only")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    targets = ["app/", "tests/"]

    if args.fix:
        print("=== Ruff: checking + fixing ===")
        cmd = ["py", "-m", "ruff", "check", "--fix"] + targets
    elif args.format:
        print("=== Ruff: format check ===")
        cmd = ["py", "-m", "ruff", "format", "--check"] + targets
    elif args.lint:
        print("=== Ruff: lint check ===")
        cmd = ["py", "-m", "ruff", "check"] + targets
    else:
        print("=== Ruff: lint check ===")
        result = subprocess.run(
            ["py", "-m", "ruff", "check"] + targets,
            capture_output=True, text=True, cwd=root
        )
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)
        print(f"\nExit code: {result.returncode}")
        print("=== Ruff: format check ===")
        result2 = subprocess.run(
            ["py", "-m", "ruff", "format", "--check"] + targets,
            capture_output=True, text=True, cwd=root
        )
        print(result2.stdout)
        if result2.returncode != 0:
            print(result2.stderr)
        print(f"\nExit code: {result2.returncode}")
        sys.exit(result.returncode or result2.returncode)
        return

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=root)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
    print(f"\nExit code: {result.returncode}")
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
