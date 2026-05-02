import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.test_project import test_create_project, test_load_project
from tests.test_hardware import test_gpu_detection, test_disk_info, test_recommended_preset
from tests.test_pipeline import test_script_generator, test_scene_splitter, test_prompt_builder
from app.logging_config import setup_logger

logger = setup_logger()

def run_all():
    results = []
    print("\n=== INICIANDO TESTES GALFLOWAI ===")
    
    # Project tests
    try:
        results.append(("Criacao de projeto", test_create_project()))
    except Exception as e:
        logger.error("Falha: %s", e)
        results.append(("Criacao de projeto", False))
    
    try:
        results.append(("Carregamento de projeto", test_load_project()))
    except Exception as e:
        logger.error("Falha: %s", e)
        results.append(("Carregamento de projeto", False))
    
    # Hardware tests
    try:
        results.append(("GPU deteccao", test_gpu_detection()))
    except Exception as e:
        logger.error("Falha: %s", e)
        results.append(("GPU deteccao", False))
    
    try:
        results.append(("Disco info", test_disk_info()))
    except Exception as e:
        logger.error("Falha: %s", e)
        results.append(("Disco info", False))
    
    try:
        results.append(("Preset recomendado", test_recommended_preset()))
    except Exception as e:
        logger.error("Falha: %s", e)
        results.append(("Preset recomendado", False))
    
    # Pipeline tests
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
    
    # Summary
    print("\n=== RESULTADOS FINAIS GALFLOWAI ===")
    passed = 0
    failed = 0
    for name, result in results:
        status = "PASSOU" if result else "FALHOU"
        print("%s: %s" % (name, status))
        if result:
            passed += 1
        else:
            failed += 1
    print("\nResumo: %d passou, %d falhou" % (passed, failed))
    print("==========================\n")
    return failed == 0

if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
