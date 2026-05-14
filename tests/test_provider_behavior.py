"""
Tests for provider behavior observed in S29:
- GPT4AllProvider: success
- LMStudioProvider: failure -> fallback to TemplateProvider
- KoboldCppProvider: failure -> fallback to TemplateProvider
"""
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, "K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta")

from app.services.script_service import generate_script_with_provider
from app.adapters.llm.template_provider import TemplateProvider


def test_gpt4all_provider_success():
    """GPT4AllProvider generates script successfully (as seen in logs: 15.56s)."""
    with patch('app.adapters.llm.gpt4all_provider.GPT4AllProvider.generate', return_value="[Cena 1 - 5s]\nTexto: Produto GPT4All.\nNarracao: Teste.\n\n[Cena 2 - 3s]\nTexto: Compre agora!\nNarracao: CTA final."):
        result = generate_script_with_provider("Teste briefing", "gpt4all")
    assert result.get("ok") is True
    assert "GPT4All" in result.get("provider", "")
    assert result.get("quality") != "fallback"
    assert len(result.get("script", "")) > 50
    print("test_gpt4all_provider_success: PASSED (provider=%s, time=%.2fs)" % (result["provider"], result["time"]))


def test_lmstudio_provider_fallback():
    """LM Studio fails -> falls back to TemplateProvider (as seen in logs: 4.1s timeout)."""
    with patch('app.adapters.llm.lmstudio_provider.LMStudioProvider.generate', side_effect=Exception("LM Studio connection refused")):
        with patch('app.adapters.llm.base_provider.TemplateProvider.generate', return_value="[Cena 1 - 5s]\nTexto: Fallback LM.\nNarracao: Teste.\n\n[Cena 2 - 3s]\nTexto: Compre agora!\nNarracao: CTA final."):
            result = generate_script_with_provider("Teste briefing", "lmstudio")
    assert result.get("ok") is True
    assert "TemplateProvider" in result.get("provider", "")
    assert result.get("quality") == "fallback"
    assert len(result.get("script", "")) > 50
    print("test_lmstudio_provider_fallback: PASSED (provider=%s, quality=%s)" % (result["provider"], result["quality"]))


def test_koboldcpp_provider_fallback():
    """KoboldCpp fails -> falls back to TemplateProvider (as seen in logs: 4.1s timeout)."""
    with patch('app.adapters.llm.koboldcpp_provider.KoboldCppProvider.generate', side_effect=Exception("KoboldCpp not running")):
        with patch('app.adapters.llm.base_provider.TemplateProvider.generate', return_value="[Cena 1 - 5s]\nTexto: Fallback Kobold.\nNarracao: Teste.\n\n[Cena 2 - 3s]\nTexto: Compre agora!\nNarracao: CTA final."):
            result = generate_script_with_provider("Teste briefing", "koboldcpp")
    assert result.get("ok") is True
    assert "TemplateProvider" in result.get("provider", "")
    assert result.get("quality") == "fallback"
    assert len(result.get("script", "")) > 50
    print("test_koboldcpp_provider_fallback: PASSED (provider=%s, quality=%s)" % (result["provider"], result["quality"]))


def test_all_providers_fallback_quality():
    """All providers that fail return quality='fallback' for observability."""
    providers = ["lmstudio", "koboldcpp", "llamacpp", "gpt4all"]
    for p in providers:
        with patch('app.adapters.llm.%s_provider.%s.generate' % (
            p.replace("4all", "4all"),  # lmstudio_provider.LMStudioProvider
            {   "lmstudio": "LMStudioProvider",
                "koboldcpp": "KoboldCppProvider",
                "llamacpp": "LlamaCppProvider",
                "gpt4all": "GPT4AllProvider",
            }[p]
        ), side_effect=Exception("Provider unavailable")):
            with patch('app.adapters.llm.base_provider.TemplateProvider.generate', return_value="[Cena 1 - 5s]\nTexto: Fallback.\nNarracao: Teste.\n\n[Cena 2 - 3s]\nTexto: Compre!\nNarracao: CTA."):
                result = generate_script_with_provider("Teste", p)
        assert result.get("ok") is True
        assert result.get("quality") == "fallback", "%s should report fallback quality" % p
        print("test_all_providers_fallback_quality(%s): PASSED" % p)


def test_fallback_includes_actual_provider_name():
    """Fallback result includes 'TemplateProvider' as provider name for visibility."""
    with patch('app.adapters.llm.lmstudio_provider.LMStudioProvider.generate', side_effect=Exception("Timeout")):
        with patch('app.adapters.llm.base_provider.TemplateProvider.generate', return_value="[Cena 1 - 5s]\nTexto: Teste.\nNarracao: Teste.\n\n[Cena 2 - 3s]\nTexto: CTA.\nNarracao: Final."):
            result = generate_script_with_provider("Teste", "lmstudio")
    assert result.get("provider") == "TemplateProvider"
    assert result.get("quality") == "fallback"
    print("test_fallback_includes_actual_provider_name: PASSED")


if __name__ == "__main__":
    test_gpt4all_provider_success()
    test_lmstudio_provider_fallback()
    test_koboldcpp_provider_fallback()
    test_all_providers_fallback_quality()
    test_fallback_includes_actual_provider_name()
    print("\nAll provider behavior tests PASSED!")
