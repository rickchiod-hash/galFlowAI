import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.project_manager import create_project, load_project
from app.config import PROJECTS_DIR
from app.logging_config import setup_logger

logger = setup_logger()

def test_create_project():
    """Testa criacao de projeto."""
    project_name = "Test Project"
    proj_dir = None
    
    # Create project
    result = create_project(project_name)
    assert result is not None
    project_id = result["id"]
    proj_dir = PROJECTS_DIR / project_id
    assert proj_dir.exists()
    assert (proj_dir / "project.json").exists()
    logger.info("test_create_project: PASSOU")

def test_load_project():
    """Testa carregamento de projeto."""
    project_name = "Test Project"
    
    # Create project first
    result = create_project(project_name)
    assert result is not None
    project_id = result["id"]
    proj_dir = PROJECTS_DIR / project_id
    
    # Load project
    loaded_project = load_project(project_id)
    assert loaded_project is not None
    assert loaded_project["id"] == project_id
    assert loaded_project["name"] == "Test Project"
    logger.info("test_load_project: PASSOU")

if __name__ == "__main__":
    results = []
    try:
        results.append(("Criacao de projeto", test_create_project()))
    except Exception as e:
        logger.error("Falha em test_create_project: %s", e)
        results.append(("Criacao de projeto", False))
    
    try:
        results.append(("Carregamento de projeto", test_load_project()))
    except Exception as e:
        logger.error("Falha em test_load_project: %s", e)
        results.append(("Carregamento de projeto", False))
    
    print("\n=== RESULTADOS DOS TESTES ===")
    for name, result in results:
        status = "PASSOU" if result else "FALHOU"
        print("%s: %s" % (name, status))
    print("==========================\n")
