import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logger

logger = setup_logger()

REPO_ROOT = Path(__file__).parent.parent
ARCH_FILE = REPO_ROOT / "docs" / "project-control" / "03_ARQUITETURA_ATUAL.md"

REQUIRED_SECTIONS = [
    "Arquitetura validada",
    "Acoplamentos encontrados",
    "Fluxo atual de execução",
    "Gaps encontrados",
    "Riscos atuais",
]

REQUIRED_PROVIDERS = [
    "TemplateProvider",
    "LM Studio",
    "GPT4All",
    "KoboldCpp",
    "llama.cpp",
    "Ollama",
]

REQUIRED_GAPS = [
    "GPT-compatible endpoint",
    "Piper pt-BR",
    "Fluxo completo",
    "API",
    "docs/reference",
]

GAP_PATTERNS = [
    "Doc desatualizada",
    "Provider não implementado",
    "Escopo superdimensionado",
    "Violação arquitetural",
]


def test_architecture_file_exists():
    assert ARCH_FILE.exists(), f"03_ARQUITETURA_ATUAL.md ausente em {ARCH_FILE}"
    logger.info("03_ARQUITETURA_ATUAL.md: OK")
    return True


def test_architecture_has_required_sections():
    content = ARCH_FILE.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        assert section in content, f"Seção obrigatória ausente: '{section}'"
        logger.info(f"SEÇÃO {section}: OK")
    return True


def test_architecture_lists_providers():
    content = ARCH_FILE.read_text(encoding="utf-8")
    for provider in REQUIRED_PROVIDERS:
        assert provider in content, f"Provider obrigatório ausente: '{provider}'"
        logger.info(f"PROVIDER {provider}: OK")
    return True


def test_architecture_documents_gaps():
    content = ARCH_FILE.read_text(encoding="utf-8")
    for gap in REQUIRED_GAPS:
        assert gap in content, f"Gap obrigatório ausente: '{gap}'"
        logger.info(f"GAP {gap}: OK")
    return True


def test_architecture_has_gap_patterns():
    content = ARCH_FILE.read_text(encoding="utf-8")
    for pattern in GAP_PATTERNS:
        assert pattern in content, f"Padrão de gap ausente: '{pattern}'"
        logger.info(f"PATTERN {pattern}: OK")
    return True


if __name__ == "__main__":
    results = []
    for name, fn in [
        ("Arquivo existe", test_architecture_file_exists),
        ("Seções obrigatórias", test_architecture_has_required_sections),
        ("Providers listados", test_architecture_lists_providers),
        ("Gaps documentados", test_architecture_documents_gaps),
        ("Padrões de gap", test_architecture_has_gap_patterns),
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
