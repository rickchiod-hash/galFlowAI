"""
Unit tests for WanGPAdapter.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.adapters.wangp_adapter import WanGPAdapter
from app.logging_config import setup_logger

logger = setup_logger()


def test_wangp_adapter_init():
    """Testa inicializacao do adaptador."""
    adapter = WanGPAdapter()
    assert isinstance(adapter, WanGPAdapter)
    logger.info("test_wangp_adapter_init: PASSOU")


def test_wangp_adapter_get_status():
    """Testa obtenção de status."""
    adapter = WanGPAdapter()
    status = adapter.get_status()
    assert isinstance(status, dict)
    assert "available" in status
    logger.info("test_wangp_adapter_get_status: PASSOU")


def test_wangp_adapter_is_available():
    """is_available should return boolean."""
    adapter = WanGPAdapter()
    result = adapter.is_available()
    assert isinstance(result, bool)
    logger.info("test_wangp_adapter_is_available: PASSED")


def test_wangp_adapter_generate_video_not_available():
    """generate_video should return error if not available."""
    adapter = WanGPAdapter()
    if not adapter.is_available():
        result = adapter.generate_video(
            prompt="test prompt",
            output_path="test.mp4"
        )
        assert result["success"] == False
        assert "error" in result
    logger.info("test_wangp_adapter_generate_video_not_available: PASSED")


if __name__ == "__main__":
    results = []
    try:
        results.append(("WanGPAdapter init", test_wangp_adapter_init()))
    except Exception as e:
        logger.error("Falha: %s", e)
        results.append(("WanGPAdapter init", False))
    
    try:
        results.append(("WanGPAdapter get_status", test_wangp_adapter_get_status()))
    except Exception as e:
        logger.error("Falha: %s", e)
        results.append(("WanGPAdapter get_status", False))
    
    try:
        results.append(("WanGPAdapter is_available", test_wangp_adapter_is_available()))
    except Exception as e:
        logger.error("Falha: %s", e)
        results.append(("WanGPAdapter is_available", False))
    
    try:
        results.append(("WanGPAdapter generate_video not available", test_wangp_adapter_generate_video_not_available()))
    except Exception as e:
        logger.error("Falha: %s", e)
        results.append(("WanGPAdapter generate_video not available", False))
    
    print("\n=== TESTES UNITARIOS WANGP ADAPTER ===")
    for name, result in results:
        status = "PASSOU" if result else "FALHOU"
        print("%s: %s" % (name, status))
    print("=======================\n")
