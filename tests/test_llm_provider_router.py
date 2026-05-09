"""
Tests for ProviderRouter.
"""
import sys
sys.path.insert(0, "K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta")

from app.adapters.llm.provider_router import ProviderRouter

def test_router_init():
    """Router should initialize with template always."""
    router = ProviderRouter()
    # Template provider is always available via detect_available
    available = router.detect_available()
    assert "template" in available
    assert available["template"] == True
    print("test_router_init: PASSED")

def test_router_detect_available():
    """Detect which providers are available."""
    router = ProviderRouter()
    available = router.detect_available()
    assert "template" in available
    assert available["template"] == True
    print("test_router_detect_available: PASSED")

def test_router_safe_mode():
    """Safe mode should always return something."""
    router = ProviderRouter(mode="safe")
    result = router.generate_script_safe("comercial de teste")
    assert result["script"] is not None
    assert result["provider"] is not None
    print("test_router_safe_mode: PASSED")

def test_router_fallback_to_template():
    """Should fallback to template if no LLM available."""
    router = ProviderRouter(mode="safe")
    result = router.generate_script_safe("comercial qualquer")
    assert result["provider"] == "TemplateProvider"
    print("test_router_fallback_to_template: PASSED")

if __name__ == "__main__":
    test_router_init()
    test_router_detect_available()
    test_router_safe_mode()
    test_router_fallback_to_template()
    print("\nAll ProviderRouter tests PASSED!")
