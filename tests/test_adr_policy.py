import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logger

logger = setup_logger()

REPO_ROOT = Path(__file__).parent.parent
ADR_FILE = REPO_ROOT / "docs" / "project-control" / "11_DECISOES_TECNICAS_ADR.md"

ADR_TEMPLATE_FIELDS = [
    "Data:",
    "Status:",
    "Contexto:",
    "Decisão:",
    "Alternativas consideradas:",
    "Consequências positivas:",
    "Consequências negativas:",
    "Arquivos afetados:",
    "Testes obrigatórios:",
    "Plano de rollback:",
]

ADR_REFERENCES = [
    "ADR-000",
    "ADR-001",
    "ADR-002",
    "ADR-003",
    "ADR-004",
    "ADR-005",
    "TemplateProvider",
    "FFmpeg",
    "AGENTS.md",
    "MCP desabilitado",
]


def test_adr_file_exists():
    assert ADR_FILE.exists(), f"11_DECISOES_TECNICAS_ADR.md ausente em {ADR_FILE}"
    logger.info("11_DECISOES_TECNICAS_ADR.md: OK")



def test_adr_template_has_all_fields():
    content = ADR_FILE.read_text(encoding="utf-8")
    for field in ADR_TEMPLATE_FIELDS:
        assert field in content, f"Campo obrigatório do template ADR ausente: '{field}'"
        logger.info(f"CAMPO {field}: OK")



def test_adr_references_present():
    content = ADR_FILE.read_text(encoding="utf-8")
    for ref in ADR_REFERENCES:
        assert ref in content, f"Referência ADR ausente: '{ref}'"
        logger.info(f"ADR {ref}: OK")



if __name__ == "__main__":
    results = []
    for name, fn in [
        ("Arquivo existe", test_adr_file_exists),
        ("Template ADR completo", test_adr_template_has_all_fields),
        ("Referências ADR", test_adr_references_present),
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
