import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logger

logger = setup_logger()

REPO_ROOT = Path(__file__).parent.parent
MAP_FILE = REPO_ROOT / "docs" / "project-control" / "02_MAPA_ATUAL_DO_PROJETO.md"

REQUIRED_SECTIONS = [
    "Raiz real do projeto",
    "Tecnologias detectadas",
    "Estrutura de diretórios",
    "Entrypoints",
    "Estado das features obrigatórias",
    "Riscos identificados",
]

REQUIRED_TECHS = [
    "Gradio",
    "FastAPI",
    "FFmpeg",
    "WanGP",
    "Template",
    "GPT4All",
    "KoboldCpp",
]

REQUIRED_ENTRYPOINTS = [
    "run_galFlowAI.py",
    "app/main.py",
    "app/api.py",
]


def test_map_file_exists():
    assert MAP_FILE.exists(), f"02_MAPA_ATUAL_DO_PROJETO.md ausente em {MAP_FILE}"
    logger.info("02_MAPA_ATUAL_DO_PROJETO.md: OK")
    return True


def test_map_has_required_sections():
    content = MAP_FILE.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        assert section in content, f"Seção obrigatória ausente: '{section}'"
        logger.info(f"SEÇÃO {section}: OK")
    return True


def test_map_lists_technologies():
    content = MAP_FILE.read_text(encoding="utf-8")
    for tech in REQUIRED_TECHS:
        assert tech in content, f"Tecnologia obrigatória ausente: '{tech}'"
        logger.info(f"TECH {tech}: OK")
    return True


def test_map_lists_entrypoints():
    content = MAP_FILE.read_text(encoding="utf-8")
    for ep in REQUIRED_ENTRYPOINTS:
        assert ep in content, f"Entrypoint obrigatório ausente: '{ep}'"
        logger.info(f"ENTRYPOINT {ep}: OK")
    return True


def test_map_references_feature_matrix():
    content = MAP_FILE.read_text(encoding="utf-8")
    assert "FEATURE_PRESERVATION_MATRIX" in content, (
        "Referência à Feature Preservation Matrix ausente"
    )
    logger.info("REFERÊNCIA FEATURE MATRIX: OK")
    return True


if __name__ == "__main__":
    results = []
    for name, fn in [
        ("Arquivo existe", test_map_file_exists),
        ("Seções obrigatórias", test_map_has_required_sections),
        ("Tecnologias listadas", test_map_lists_technologies),
        ("Entrypoints listados", test_map_lists_entrypoints),
        ("Referência à Feature Matrix", test_map_references_feature_matrix),
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
