import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.hardware import get_gpu_info, get_disk_info, get_ram_info, get_recommended_preset
from app.logging_config import setup_logger

logger = setup_logger()

def test_gpu_detection():
    """Testa deteccao de GPU."""
    gpu = get_gpu_info()
    assert "name" in gpu
    assert "vram_gb" in gpu
    assert "cuda_available" in gpu
    logger.info("test_gpu_detection: PASSOU")

def test_disk_info():
    """Testa info de disco."""
    disk = get_disk_info()
    assert "free_gb" in disk
    assert "total_gb" in disk
    logger.info("test_disk_info: PASSOU")

def test_recommended_preset():
    """Testa preset recomendado."""
    preset = get_recommended_preset(6.44, "NVIDIA GeForce GTX 1660 SUPER")
    assert preset["model"] == "1.3B"
    assert "512p" in preset["resolution"]
    logger.info("test_recommended_preset: PASSOU")

if __name__ == "__main__":
    results = []
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
    
    print("\n=== TESTES DE HARDWARE ===")
    for name, result in results:
        status = "PASSOU" if result else "FALHOU"
        print("%s: %s" % (name, status))
    print("======================\n")
