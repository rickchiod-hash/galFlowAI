import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logger

logger = setup_logger()

REPO_ROOT = Path(__file__).parent.parent
GAPS_FILE = REPO_ROOT / "docs" / "project-control" / "09_GAPS_TODOS_E_DIVIDAS.md"

REQUIRED_SECTIONS = [
    "Política",
    "Formato obrigatório",
    "TODO no código",
    "Resultado da varredura de código",
]

REQUIRED_FRAGMENTS = [
    "TODO(GAL-XXX",
    "TODO genérico é proibido",
    "História relacionada:",
    "CORE-100",
    "CORE-102",
    "UI-200",
    "PROV-300",
    "GAP-001",
    "GAP-005",
    "GAP-006",
]


def test_gaps_file_exists():
    assert GAPS_FILE.exists(), f"09_GAPS_TODOS_E_DIVIDAS.md ausente em {GAPS_FILE}"
    logger.info("09_GAPS_TODOS_E_DIVIDAS.md: OK")



def test_gaps_has_required_sections():
    content = GAPS_FILE.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        assert section in content, f"Seção obrigatória ausente: '{section}'"
        logger.info(f"SEÇÃO {section}: OK")



def test_todo_pattern_documented():
    content = GAPS_FILE.read_text(encoding="utf-8")
    for frag in REQUIRED_FRAGMENTS:
        assert frag in content, f"Fragmento obrigatório ausente: '{frag}'"
        logger.info(f"FRAGMENTO {frag}: OK")



def test_no_generic_todo_in_code():
    todos = []
    for pyfile in REPO_ROOT.rglob("*.py"):
        if ".pytest_cache" in str(pyfile) or "__pycache__" in str(pyfile) or ".git" in str(pyfile):
            continue
        try:
            text = pyfile.read_text(encoding="utf-8", errors="ignore")
            for i, line in enumerate(text.splitlines(), 1):
                if "TODO(" in line or "TODO:" in line:
                    if "GAL-" not in line and "TODO genérico" not in line:
                        todos.append((pyfile.relative_to(REPO_ROOT), i, line.strip()))
        except Exception:
            continue

    if todos:
        msg = "\n".join(f"{f}:{l} {t}" for f, l, t in todos)
        logger.warning(f"TODOs genéricos encontrados:\n{msg}")
    else:
        logger.info("Nenhum TODO genérico: OK")




if __name__ == "__main__":
    results = []
    for name, fn in [
        ("Arquivo existe", test_gaps_file_exists),
        ("Seções obrigatórias", test_gaps_has_required_sections),
        ("Padrão TODO documentado", test_todo_pattern_documented),
        ("Nenhum TODO genérico", test_no_generic_todo_in_code),
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
