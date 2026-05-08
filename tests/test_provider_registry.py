"""Tests for preserving LLM provider registry."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config_models import LLM_PROVIDERS


def test_required_providers_present():
    """Test that required providers are in the registry."""
    required = ["template", "lm_studio", "koboldcpp", "llamacpp", "gpt4all"]
    for provider in required:
        assert provider in LLM_PROVIDERS, f"Provider {provider} missing from registry"
        # Check that each provider has required fields
        p = LLM_PROVIDERS[provider]
        assert "name" in p, f"Provider {provider} missing 'name'"
        assert "priority" in p, f"Provider {provider} missing 'priority'"
        assert "type" in p, f"Provider {provider} missing 'type'"
    print("PASS: test_required_providers_present")
    return True


def test_template_is_fallback():
    """Test that TemplateProvider is the fallback (lowest priority)."""
    template = LLM_PROVIDERS.get("template")
    assert template is not None, "Template provider missing"
    # Fallback should have highest priority number (lowest priority)
    assert template["priority"] == 999, f"Template priority should be 999, got {template['priority']}"
    # Check that no other provider has priority >= 999
    for name, config in LLM_PROVIDERS.items():
        if name != "template":
            assert config["priority"] < 999, f"Provider {name} has priority >= 999, should be higher than template"
    print("PASS: test_template_is_fallback")
    return True


def test_registry_not_empty():
    """Test that registry is not empty."""
    assert len(LLM_PROVIDERS) > 0, "LLM_PROVIDERS is empty"
    print("PASS: test_registry_not_empty")
    return True


def test_provider_types():
    """Test that provider types are valid."""
    valid_types = ["template", "local_llm"]
    for name, config in LLM_PROVIDERS.items():
        assert config.get("type") in valid_types, f"Provider {name} has invalid type: {config.get('type')}"
    print("PASS: test_provider_types")
    return True


if __name__ == "__main__":
    results = []
    for name, fn in [
        ("Required providers present", test_required_providers_present),
        ("Template is fallback", test_template_is_fallback),
        ("Registry not empty", test_registry_not_empty),
        ("Provider types", test_provider_types),
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
    print("RESULTS: Provider Registry Tests")
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
