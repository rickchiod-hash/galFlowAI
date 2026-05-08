import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logger

logger = setup_logger()
REPO_ROOT = Path(__file__).parent.parent

UI_FILES = {
    "Gradio UI (gradio_app.py)": "app/ui/gradio_app.py",
    "Gradio legacy (main.py)": "app/main.py",
    "FastAPI (api.py)": "app/api.py",
}

ADAPTER_IMPORT_PATTERNS = [
    "from app.adapters",
    "import app.adapters",
    "from app.adapters.llm",
    "import app.adapters.llm",
]

ALLOWED_VIOLATIONS = {
    "app/api.py": [
        "from app.adapters.llm import ProviderRouter  # API->adapter direto (gap G4 conhecido, documentado em 03_ARQUITETURA_ATUAL.md)",
    ],
}


def _get_adapter_imports(rel_path: str) -> list[dict]:
    full = REPO_ROOT / rel_path
    if not full.exists():
        return []
    lines = full.read_text(encoding="utf-8", errors="ignore").splitlines()
    found = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        for pattern in ADAPTER_IMPORT_PATTERNS:
            if stripped.startswith(pattern):
                found.append({"line": i, "text": stripped})
                break
    return found


def _is_allowed(rel_path: str, import_text: str) -> bool:
    allowed = ALLOWED_VIOLATIONS.get(rel_path, [])
    for allowed_text in allowed:
        if import_text == allowed_text.split("  #")[0].strip():
            return True
        if import_text in allowed_text:
            return True
    return False


def _test_file_no_direct_adapter_imports(rel_path: str, label: str) -> bool:
    imports = _get_adapter_imports(rel_path)
    violations = [imp for imp in imports if not _is_allowed(rel_path, imp["text"])]
    if violations:
        details = "; ".join(f"L{imp['line']}: {imp['text']}" for imp in violations)
        logger.error(f"{label}: VIOLACOES nao permitidas -> {details}")
        return False
    if imports:
        allowed_count = len(imports) - len(violations)
        logger.info(f"{label}: {allowed_count} import(s) permitido(s) de adapter(s) (gap conhecido)")
    else:
        logger.info(f"{label}: OK - nenhum import de adapter")
    return True


def test_gradio_ui_no_adapter_imports():
    rel_path = UI_FILES["Gradio UI (gradio_app.py)"]
    result = _test_file_no_direct_adapter_imports(rel_path, "Gradio UI (gradio_app.py)")
    assert result, f"{rel_path} contem imports nao permitidos de app.adapters"
    logger.info("GRADIO UI: NENHUM IMPORT DE ADAPTER (OK)")


def test_gradio_legacy_no_adapter_imports():
    rel_path = UI_FILES["Gradio legacy (main.py)"]
    result = _test_file_no_direct_adapter_imports(rel_path, "Gradio legacy (main.py)")
    assert result, f"{rel_path} contem imports nao permitidos de app.adapters"
    logger.info("GRADIO LEGACY: NENHUM IMPORT DE ADAPTER (OK)")


def test_fastapi_known_violation_only():
    rel_path = UI_FILES["FastAPI (api.py)"]
    imports = _get_adapter_imports(rel_path)
    violations = [imp for imp in imports if not _is_allowed(rel_path, imp["text"])]
    assert not violations, (
        f"Novas violacoes nao documentadas em {rel_path}: "
        + "; ".join(f"L{imp['line']}: {imp['text']}" for imp in violations)
    )
    if imports:
        logger.info(f"FASTAPI API: {len(imports)} import(s) conhecido(s) de adapter (gap G4, ARCH-300)")
    else:
        logger.info("FASTAPI API: NENHUM IMPORT DE ADAPTER (OK)")


def test_all_ui_files_scanned():
    for label, rel_path in UI_FILES.items():
        full = REPO_ROOT / rel_path
        assert full.exists(), f"Arquivo UI nao encontrado: {rel_path}"
        logger.info(f"{label}: {rel_path} presente")
    logger.info("TODOS OS ARQUIVOS UI: OK")


if __name__ == "__main__":
    results = []
    for name, fn in [
        ("Gradio UI sem adapter", test_gradio_ui_no_adapter_imports),
        ("Gradio legacy sem adapter", test_gradio_legacy_no_adapter_imports),
        ("FastAPI violacao conhecida", test_fastapi_known_violation_only),
        ("Todos arquivos UI existem", test_all_ui_files_scanned),
    ]:
        try:
            fn()
            results.append((name, True))
        except Exception as e:
            logger.error(f"Falha em {name}: {e}")
            results.append((name, False))

    print("\n=== RESULTADOS QA-1002 ===")
    for name, result in results:
        print(f"{name}: {'PASSOU' if result else 'FALHOU'}")
    print("==========================\n")
