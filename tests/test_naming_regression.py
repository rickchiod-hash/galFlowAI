import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logger

logger = setup_logger()

REPO_ROOT = Path(__file__).parent.parent

LEGACY_NAMES = [
    "FlowForgeAI",
    "flowforgeai",
    "flow_forge",
    "Gal AI",
    "gal ai",
    "AI Video Comercial Studio",
    "AI Video Commercial Studio",
]

ALLOWED_PATHS = [
    ".git",
    "__pycache__",
    ".pyc",
    "node_modules",
    ".github",
    "GalFlowAI_Governance_Backlog_Checkpoint_Pack_v2",
    "galflowai-go",
    ".opencode",
    "temp_backup",
    "session-ses",
    "test_naming_regression",
    "PROJECT_REFERENCE_CONTEXT",
    "project-control",
]

EXPECTED_CONSISTENT_NAMES = [
    "GalFlowAI",
    "galFlowAI",
    "galflowai",
]

PYTHON_FILES = list(REPO_ROOT.rglob("*.py"))
DOC_FILES = list(REPO_ROOT.rglob("*.md"))


def _should_skip(path: Path) -> bool:
    rel = str(path.relative_to(REPO_ROOT)).lower()
    for allowed in ALLOWED_PATHS:
        if allowed.lower() in rel:
            return True
    return False


def test_no_legacy_names_in_python_files():
    found = []
    for py_file in PYTHON_FILES:
        if _should_skip(py_file):
            continue
        try:
            content = py_file.read_text(encoding="utf-8", errors="ignore")
            for legacy in LEGACY_NAMES:
                if legacy in content:
                    found.append((str(py_file.relative_to(REPO_ROOT)), legacy))
        except Exception:
            continue
    assert not found, f"Nomes legados encontrados: {found}"
    logger.info("NENHUM NOME LEGADO EM .py: OK")
    return True


def test_no_legacy_names_in_doc_files():
    found = []
    for md_file in DOC_FILES:
        if _should_skip(md_file):
            continue
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            for legacy in LEGACY_NAMES:
                if legacy in content:
                    found.append((str(md_file.relative_to(REPO_ROOT)), legacy))
        except Exception:
            continue
    assert not found, f"Nomes legados em docs: {found}"
    logger.info("NENHUM NOME LEGADO EM .md: OK")
    return True


def test_project_uses_correct_name():
    key_files = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "app" / "main.py",
        REPO_ROOT / "app" / "api.py",
        REPO_ROOT / "AGENTS.md",
    ]
    for f in key_files:
        if not f.exists():
            continue
        content = f.read_text(encoding="utf-8", errors="ignore")
        has_correct = any(name in content for name in EXPECTED_CONSISTENT_NAMES)
        assert has_correct, f"{f.name} não contém nome correto (GalFlowAI)"
        logger.info(f"{f.name}: NOME CORRETO OK")
    return True


def test_git_log_shows_rename_commit():
    import subprocess
    result = subprocess.run(
        ["git", "log", "--oneline", "--grep=REF-01", "-10"],
        capture_output=True, text=True, cwd=REPO_ROOT
    )
    assert "ee05f5c" in result.stdout or "REF-01" in result.stdout, (
        "Commit de rename REF-01 não encontrado no git log"
    )
    logger.info("COMMIT RENAME REF-01: OK")
    return True


def test_no_flowforgeai_in_git_tracked_files():
    import subprocess
    result = subprocess.run(
        ["git", "grep", "-i", "FlowForgeAI", "--", "*.py", "*.md"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=REPO_ROOT
    )
    stdout = result.stdout or ""
    lines = stdout.strip().splitlines()
    non_history = [
        l for l in lines
            if not any(s in l.lower() for s in ["auditoria", "git log", "histórico", "historico", "legado", "session-ses", "backup", "project-control", "test_naming_regression"])
    ]
    assert len(non_history) == 0, f"FlowForgeAI encontrado em arquivos: {non_history}"
    logger.info("GIT GREP FLOWFORGEAI: OK (apenas em contexto histórico)")
    return True


if __name__ == "__main__":
    results = []
    for name, fn in [
        ("Nomes legados em .py", test_no_legacy_names_in_python_files),
        ("Nomes legados em .md", test_no_legacy_names_in_doc_files),
        ("Nome correto em arquivos chave", test_project_uses_correct_name),
        ("Commit rename existe", test_git_log_shows_rename_commit),
        ("FlowForgeAI em tracked", test_no_flowforgeai_in_git_tracked_files),
    ]:
        try:
            results.append((name, fn()))
        except Exception as e:
            logger.error(f"Falha em {name}: {e}")
            results.append((name, False))

    print("\n=== RESULTADOS DOS TESTES ===")
    for name, result in results:
        print(f"{name}: {'PASSOU' if result else 'FALHOU'}")
    print("==========================\n")
