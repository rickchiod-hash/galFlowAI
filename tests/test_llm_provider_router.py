"""
Tests for ProviderRouter.
"""
import sys
from unittest.mock import patch

sys.path.insert(0, "K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta")

from app.adapters.llm.provider_router import ProviderRouter


_PROVIDER_PATCHES = [
    patch('app.adapters.llm.lmstudio_provider.LMStudioProvider.is_available', return_value=False),
    patch('app.adapters.llm.koboldcpp_provider.KoboldCppProvider.is_available', return_value=False),
    patch('app.adapters.llm.llamacpp_provider.LlamaCppProvider.is_available', return_value=False),
    patch('app.adapters.llm.gpt4all_provider.GPT4AllProvider.is_available', return_value=False),
]


def _with_mocked_providers():
    """Context manager that mocks is_available on all non-template providers."""
    from contextlib import contextmanager
    from unittest.mock import patch

    @contextmanager
    def _cm():
        patches = [
            patch('app.adapters.llm.lmstudio_provider.LMStudioProvider.is_available', return_value=False),
            patch('app.adapters.llm.koboldcpp_provider.KoboldCppProvider.is_available', return_value=False),
            patch('app.adapters.llm.llamacpp_provider.LlamaCppProvider.is_available', return_value=False),
            patch('app.adapters.llm.gpt4all_provider.GPT4AllProvider.is_available', return_value=False),
        ]
        for p in patches:
            p.start()
        try:
            yield
        finally:
            for p in patches:
                p.stop()
    return _cm()


def test_router_init():
    """Router should initialize with template always."""
    with _with_mocked_providers():
        router = ProviderRouter()
        available = router.detect_available()
        assert "template" in available
        assert available["template"] == True
    print("test_router_init: PASSED")

def test_router_detect_available():
    """Detect which providers are available."""
    with _with_mocked_providers():
        router = ProviderRouter()
        available = router.detect_available()
        assert "template" in available
        assert available["template"] == True
    print("test_router_detect_available: PASSED")

def test_router_safe_mode():
    """Safe mode should always return something."""
    with _with_mocked_providers():
        router = ProviderRouter(mode="safe")
        result = router.generate_script_safe("comercial de teste")
        assert result["script"] is not None
        assert result["provider"] is not None
    print("test_router_safe_mode: PASSED")

def test_router_fallback_to_template():
    """Should fallback to template if no LLM available."""
    with _with_mocked_providers():
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
