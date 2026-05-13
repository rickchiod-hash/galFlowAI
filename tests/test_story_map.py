import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logger

logger = setup_logger()

REPO_ROOT = Path(__file__).parent.parent
MAP_FILE = REPO_ROOT / "docs" / "project-control" / "19_STORY_MAP.md"

REQUIRED_SECTIONS = [
    "Fluxo por etapas validáveis",
    "Story map por atividade",
    "Regras do fluxo",
]

REQUIRED_STEPS = [
    "BRIEFING",
    "ROTEIRO",
    "CENAS",
    "PROMPTS",
    "NARRAÇÃO",
    "VÍDEO",
    "MONTAGEM FINAL",
]

REQUIRED_GATES = [
    "Briefing preenchido",
    "Roteiro aprovado",
    "MP4 gerado",
]

REQUIRED_RULES = [
    "aprovado antes de gerar cenas",
    "TTS falha não quebra vídeo",
    "WanGP falha",
]


def test_story_map_file_exists():
    assert MAP_FILE.exists(), f"19_STORY_MAP.md ausente em {MAP_FILE}"
    logger.info("19_STORY_MAP.md: OK")



def test_story_map_has_step_flow():
    content = MAP_FILE.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        assert section in content, f"Seção obrigatória ausente: '{section}'"
        logger.info(f"SEÇÃO {section}: OK")



def test_story_map_lists_all_steps():
    content = MAP_FILE.read_text(encoding="utf-8")
    for step in REQUIRED_STEPS:
        assert step in content, f"Etapa obrigatória ausente: '{step}'"
        logger.info(f"ETAPA {step}: OK")



def test_story_map_has_validation_gates():
    content = MAP_FILE.read_text(encoding="utf-8")
    for gate in REQUIRED_GATES:
        assert gate in content, f"Gate de validação ausente: '{gate}'"
        logger.info(f"GATE {gate}: OK")



def test_story_map_has_flow_rules():
    content = MAP_FILE.read_text(encoding="utf-8")
    for rule in REQUIRED_RULES:
        assert rule in content, f"Regra de fluxo ausente: '{rule}'"
        logger.info(f"RULE {rule}: OK")



if __name__ == "__main__":
    results = []
    for name, fn in [
        ("Arquivo existe", test_story_map_file_exists),
        ("Fluxo por etapas", test_story_map_has_step_flow),
        ("Etapas listadas", test_story_map_lists_all_steps),
        ("Gates de validação", test_story_map_has_validation_gates),
        ("Regras de fluxo", test_story_map_has_flow_rules),
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
