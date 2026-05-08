import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logger

logger = setup_logger()

REPO_ROOT = Path(__file__).parent.parent
CONTEXT_FILE = REPO_ROOT / "docs" / "reference" / "PROJECT_REFERENCE_CONTEXT.md"

REQUIRED_SECTIONS = [
    "Identidade oficial",
    "Escopo do produto",
    "Regra de ouro",
    "Fallbacks invioláveis",
    "Providers obrigatórios a preservar",
    "Itens que não podem ser removidos silenciosamente",
    "Política de remoção",
    "Filosofia de evolução",
]

REQUIRED_KEYWORDS = [
    "GalFlowAI",
    "local-first",
    "TemplateProvider",
    "FFmpeg",
    "WanGP",
    "pyttsx3",
    "ADR",
    "Feature Preservation Matrix",
]


def test_context_file_exists():
    assert CONTEXT_FILE.exists(), f"PROJECT_REFERENCE_CONTEXT.md ausente em {CONTEXT_FILE}"
    logger.info(f"PROJECT_REFERENCE_CONTEXT.md: OK")
    return True


def test_context_has_required_sections():
    content = CONTEXT_FILE.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        assert section in content, f"Seção ausente: '{section}'"
        logger.info(f"SEÇÃO {section}: OK")
    return True


def test_context_has_required_keywords():
    content = CONTEXT_FILE.read_text(encoding="utf-8")
    for kw in REQUIRED_KEYWORDS:
        assert kw in content, f"Palavra-chave ausente: '{kw}'"
        logger.info(f"KEYWORD {kw}: OK")
    return True


def test_context_is_truth_source():
    content = CONTEXT_FILE.read_text(encoding="utf-8")
    assert "FONTE DE VERDADE DO PRODUTO" in content
    assert "Alteração permitida somente com ADR" in content
    logger.info("STATUS FONTE DE VERDADE: OK")
    return True


if __name__ == "__main__":
    results = []
    for name, fn in [
        ("Arquivo existe", test_context_file_exists),
        ("Seções obrigatórias", test_context_has_required_sections),
        ("Palavras-chave", test_context_has_required_keywords),
        ("Status fonte de verdade", test_context_is_truth_source),
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
