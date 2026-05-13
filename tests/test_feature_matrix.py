import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logger

logger = setup_logger()

REPO_ROOT = Path(__file__).parent.parent
MATRIX_FILE = REPO_ROOT / "docs" / "reference" / "FEATURE_PRESERVATION_MATRIX.md"

REQUIRED_COLUMNS = [
    "Feature",
    "Tipo",
    "Obrigatória",
    "História vinculada",
    "Arquivo de contexto",
    "Como validar",
    "Teste esperado",
    "Pode remover?",
]

MANDATORY_FEATURES = [
    "Nome GalFlowAI",
    "Roteiro editável",
    "Aprovação de roteiro",
    "TemplateProvider",
    "FFmpeg fallback",
    "Providers locais",
    "Logs",
    "Métricas",
    "Status diário",
    "TODO rastreável",
]

LIBERATION_FEATURES = [
    "SceneContracts",
    "Visual Bible",
    "Ingredient Registry",
    "RenderPlan",
    "AudioPlan",
    "VectorMemory disabled",
]


def test_matrix_file_exists():
    assert MATRIX_FILE.exists(), f"FEATURE_PRESERVATION_MATRIX.md ausente em {MATRIX_FILE}"
    logger.info("FEATURE_PRESERVATION_MATRIX.md: OK")



def test_matrix_has_required_columns():
    content = MATRIX_FILE.read_text(encoding="utf-8")
    for col in REQUIRED_COLUMNS:
        assert col in content, f"Coluna obrigatória ausente: '{col}'"
        logger.info(f"COLUNA {col}: OK")



def test_mandatory_features_listed():
    content = MATRIX_FILE.read_text(encoding="utf-8")
    for feat in MANDATORY_FEATURES:
        assert feat in content, f"Feature obrigatória ausente na matriz: '{feat}'"
        logger.info(f"FEATURE {feat}: OK")



def test_lib_p1_features_listed():
    content = MATRIX_FILE.read_text(encoding="utf-8")
    for feat in LIBERATION_FEATURES:
        assert feat in content, f"Feature P1 ausente na matriz: '{feat}'"
        logger.info(f"FEATURE {feat}: OK")



def test_mandatory_marked_not_removable():
    content = MATRIX_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    for feat in MANDATORY_FEATURES:
        found = False
        for line in lines:
            if f"| {feat} " in line and "| Não |" in line:
                found = True
                break
        assert found, f"Feature '{feat}' nao marcada como 'Nao' removivel"
        logger.info(f"REMOVIBILIDADE {feat}: OK (Nao)")



if __name__ == "__main__":
    results = []
    for name, fn in [
        ("Arquivo existe", test_matrix_file_exists),
        ("Colunas obrigatórias", test_matrix_has_required_columns),
        ("Features obrigatórias", test_mandatory_features_listed),
        ("Features P1", test_lib_p1_features_listed),
        ("Removibilidade", test_mandatory_marked_not_removable),
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
