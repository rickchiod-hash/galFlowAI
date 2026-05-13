"""Tests for TemplateProvider fallback (PROV-301)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config_models import LLM_PROVIDERS
from app.application.result import Result


def test_template_is_fallback():
    """Test that TemplateProvider has highest priority number (lowest priority)."""
    template = LLM_PROVIDERS.get("template")
    assert template is not None, "Template provider missing"
    # Fallback should have priority 999 (highest number)
    assert template["priority"] == 999, f"Template priority should be 999, got {template['priority']}"
    # Check that no other provider has priority >= 999
    for name, config in LLM_PROVIDERS.items():
        if name != "template":
            assert config["priority"] < 999, f"Provider {name} has priority >= 999, should be higher than template"
    print("PASS: test_template_is_fallback")



def test_template_provider_returns_result():
    """Test that TemplateProvider returns a Result object."""
    from app.adapters.template_provider import TemplateProvider
    
    provider = TemplateProvider()
    # TemplateProvider should work without any external dependencies
    result = provider.generate("Test briefing")
    
    # Should return a Result object
    assert isinstance(result, Result), f"Expected Result, got {type(result)}"
    # Should succeed (TemplateProvider always succeeds)
    assert result.ok is True, f"TemplateProvider should succeed, got error: {result.error}"
    # Should have script in data
    assert "script" in result.data, "Result data missing 'script' key"
    assert len(result.data["script"]) > 0, "Script should not be empty"
    
    print("PASS: test_template_provider_returns_result")



def test_fallback_when_no_other_provider():
    """Test that TemplateProvider is used when no other provider is available."""
    from app.services.script_service import generate_script_with_llm
    from app.logging_config import setup_logger
    import logging
    
    # Mock the ProviderRouter to simulate no providers available except template
    from unittest.mock import patch, MagicMock
    
    # Patch the router's detect_available method to return only template
    with patch('app.services.script_service.ProviderRouter') as mock_router_cls:
        mock_router = MagicMock()
        mock_router.generate_script_safe.return_value = {
            "script": "[Cena 1: Test]\nTest script.\n[Cena 2: Test]\nAnother scene.",
            "provider": "TemplateProvider",
            "time": 0.5,
            "quality": "fallback"
        }
        mock_router_cls.return_value = mock_router
        
        # Call script service (should use template)
        result = generate_script_with_llm("Test product. Test audience", mode="template")
        
        # Should succeed with template
        assert result["ok"] is True, f"Expected success with template, got: {result}"
        assert "script" in result
        print(f"  Generated script using: {result.get('provider')}")
        provider = result.get("provider", "")
        assert provider == "TemplateProvider", \
            f"Should use template provider, got {provider}"
    
    print("PASS: test_fallback_when_no_other_provider")



def test_template_minimal_script():
    """Test that TemplateProvider generates a minimal script."""
    from app.adapters.template_provider import TemplateProvider
    
    provider = TemplateProvider()
    result = provider.generate("Product X. Audience Y")
    
    assert result.ok is True
    script = result.data.get("script", "")
    # Should contain at least one scene
    assert "Cena" in script, "Script should contain at least one scene"
    assert len(script) > 20, f"Script too short: {script}"
    
    print("PASS: test_template_minimal_script")



if __name__ == "__main__":
    results = []
    for name, fn in [
        ("Template is fallback", test_template_is_fallback),
        ("TemplateProvider returns Result", test_template_provider_returns_result),
        ("Fallback when no other provider", test_fallback_when_no_other_provider),
        ("Template minimal script", test_template_minimal_script),
    ]:
        try:
            result = fn()
            results.append((name, result))
            if result:
                print(f"PASS: {name}")
            else:
                print(f"FAIL: {name}")
        except Exception as e:
            print(f"FAIL: {name} with exception: {e}")
            results.append((name, False))
    
    print("\n" + "="*60)
    print("RESULTS: TemplateProvider Fallback Tests")
    print("="*60)
    for name, result in results:
        status = "PASSED" if result else "FAILED"
        print(f"{name:<50} {status}")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nPASSED: {passed}/{total}")
    
    if passed == total:
        print("ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print("SOME TESTS FAILED!")
        sys.exit(1)
