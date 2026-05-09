import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.pipeline.script_generator import generate_script, save_script
from app.pipeline.scene_splitter import split_script_into_scenes, save_scenes
from app.pipeline.prompt_builder import build_prompts_for_scenes, save_prompts
from app.logging_config import setup_logger

logger = setup_logger()

def test_script_generator():
    """Testa gerador de roteiro."""
    result = generate_script("Teste de roteiro", mode="template")
    assert isinstance(result, str)
    assert len(result) > 0
    assert "[Cena" in result or "Cena" in result
    logger.info("test_script_generator: PASSOU")

def test_scene_splitter():
    """Testa divisao de cenas."""
    script = """[Cena 1: Introducao]
    Primeira cena de teste.
    [Cena 2: Desenvolvimento]
    Segunda cena com mais detalhes.
    [Cena 3: Conclusao]
    Ultima cena."""
    scenes = split_script_into_scenes(script, "test_project")
    assert len(scenes) == 3
    assert scenes[0]["scene_number"] == 1
    logger.info("test_scene_splitter: PASSOU")

def test_prompt_builder():
    """Testa builder de prompts."""
    scenes = [{"text": "teste", "id": "scene_001"}]
    result = build_prompts_for_scenes(scenes)
    # Function returns prompt key (not prompt_pos)
    assert "prompt" in result[0]
    assert result[0]["prompt"] == "teste"
    logger.info("test_prompt_builder: PASSOU")

if __name__ == "__main__":
    results = []
    try:
        results.append(("Gerador de roteiro", test_script_generator()))
    except Exception as e:
        logger.error("Falha: %s", e)
        results.append(("Gerador de roteiro", False))
    
    try:
        results.append(("Divisao em cenas", test_scene_splitter()))
    except Exception as e:
        logger.error("Falha: %s", e)
        results.append(("Divisao em cenas", False))
    
    try:
        results.append(("Builder de prompts", test_prompt_builder()))
    except Exception as e:
        logger.error("Falha: %s", e)
        results.append(("Builder de prompts", False))
    
    print("\n=== TESTES DE PIPELINE ===")
    for name, result in results:
        status = "PASSOU" if result else "FALHOU"
        print("%s: %s" % (name, status))
    print("======================\n")
