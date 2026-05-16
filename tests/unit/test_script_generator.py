"""
Unit tests for script_generator module.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.services.script_service import generate_script
from app.repositories.script_repository import ScriptRepository
from app.logging_config import setup_logger

logger = setup_logger()


def test_generate_script_returns_string():
    """generate_script should return a string."""
    result = generate_script("Test briefing for commercial", mode="template")
    assert isinstance(result, str)
    assert len(result) > 0
    logger.info("test_generate_script_returns_string: PASSED")


def test_generate_script_contains_scenes():
    """Generated script should contain scene markers."""
    result = generate_script("Comercial de bonecos colecionaveis", mode="template")
    assert "[Cena" in result or "Cena" in result
    logger.info("test_generate_script_contains_scenes: PASSED")


def test_save_script(tmp_path):
    """save_script should save script to project directory."""
    from app.config import PROJECTS_DIR
    import tempfile
    
    # Use a temporary project ID
    project_id = "test_save_script"
    proj_dir = PROJECTS_DIR / project_id
    proj_dir.mkdir(parents=True, exist_ok=True)
    
    # Create project.json
    import json
    proj_file = proj_dir / "project.json"
    proj_file.write_text(json.dumps({"id": project_id, "name": "test"}), encoding="utf-8")
    
    result = ScriptRepository(project_id).save_script("Test script content")
    assert result is not None
    assert result.success
    logger.info("test_save_script: PASSED")


if __name__ == "__main__":
    results = []
    try:
        results.append(("Generate script returns string", test_generate_script_returns_string()))
    except Exception as e:
        logger.error("Falha: %s", e)
        results.append(("Generate script returns string", False))
    
    try:
        results.append(("Generate script contains scenes", test_generate_script_contains_scenes()))
    except Exception as e:
        logger.error("Falha: %s", e)
        results.append(("Generate script contains scenes", False))
    
    print("\n=== TESTES UNITARIOS SCRIPT GENERATOR ===")
    for name, result in results:
        status = "PASSOU" if result else "FALHOU"
        print("%s: %s" % (name, status))
    print("=======================\n")
