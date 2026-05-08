import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logger

logger = setup_logger()

REPO_ROOT = Path(__file__).parent.parent
AGENTS_FILE = REPO_ROOT / "AGENTS.md"
SKILL_FILE = REPO_ROOT / ".opencode" / "skills" / "galflowai" / "SKILL.md"

AGENTS_REQUIRED_FRAGMENTS = [
    "GalFlowAI",
    "Regra máxima",
    "Antes de qualquer alteração",
    "Política de escopo",
    "Como trabalhar",
    "Padrão de resposta final",
    "Padrão de TODO",
    "TODO(GAL-XXX, type=",
    "TODO genérico é proibido",
]

SKILL_REQUIRED_FRAGMENTS = [
    "GalFlowAI",
    "Documentos obrigatórios antes de codar",
    "Ordem de execução",
    "Guardrails",
    "Não remover fallbacks",
    "Não trocar stack sem ADR",
    "docs/reference/PROJECT_REFERENCE_CONTEXT.md",
    "docs/reference/FEATURE_PRESERVATION_MATRIX.md",
    "docs/project-control/00_STATUS_EXECUTIVO.md",
]


def test_agents_file_exists():
    assert AGENTS_FILE.exists(), f"AGENTS.md ausente em {AGENTS_FILE}"
    logger.info("AGENTS.md: OK")
    return True


def test_agents_has_required_content():
    content = AGENTS_FILE.read_text(encoding="utf-8")
    for frag in AGENTS_REQUIRED_FRAGMENTS:
        assert frag in content, f"Fragmento obrigatório ausente no AGENTS.md: '{frag}'"
        logger.info(f"AGENTS {frag}: OK")
    return True


def test_skill_file_exists():
    assert SKILL_FILE.exists(), f"SKILL.md ausente em {SKILL_FILE}"
    logger.info("SKILL.md: OK")
    return True


def test_skill_has_required_content():
    content = SKILL_FILE.read_text(encoding="utf-8")
    for frag in SKILL_REQUIRED_FRAGMENTS:
        assert frag in content, f"Fragmento obrigatório ausente no SKILL.md: '{frag}'"
        logger.info(f"SKILL {frag}: OK")
    return True


if __name__ == "__main__":
    results = []
    for name, fn in [
        ("AGENTS.md existe", test_agents_file_exists),
        ("AGENTS.md conteúdo", test_agents_has_required_content),
        ("SKILL.md existe", test_skill_file_exists),
        ("SKILL.md conteúdo", test_skill_has_required_content),
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
