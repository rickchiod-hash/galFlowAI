"""Tests for provider fallback chain (PROV-302).

Valida: (1) falha de LLM -> template funciona,
(2) fallback chain esta correta,
(3) TemplateProvider gera roteiro valido,
(4) config de providers esta correta.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.adapters.llm.base_provider import TemplateProvider
from app.config_models import LLM_PROVIDERS


class TestTemplateProviderAvailability:
    """TemplateProvider deve estar sempre disponivel."""

    def test_is_available_always_true(self):
        provider = TemplateProvider()
        assert provider.is_available() is True

    def test_name_is_template(self):
        provider = TemplateProvider()
        assert provider.name == "TemplateProvider"


class TestTemplateProviderGenerate:
    """TemplateProvider deve gerar roteiro valido."""

    def test_generates_script_for_basic_briefing(self):
        provider = TemplateProvider()
        result = provider.generate("Produto X. Publico jovem.")
        assert result is not None
        assert "[Cena 1" in result
        assert len(result) > 50

    def test_detects_viral_style_by_default(self):
        provider = TemplateProvider()
        result = provider.generate("Produto comum")
        assert "[Cena 1: Hook" in result

    def test_detects_fantasy_style(self):
        provider = TemplateProvider()
        result = provider.generate("Fantasia medieval personagem")
        assert "[Cena 1: Introducao" in result

    def test_detects_futurist_style(self):
        provider = TemplateProvider()
        result = provider.generate("Tecnologia futurista cyberpunk")
        assert "[Cena 1: Hook" in result

    def test_detects_geek_style(self):
        provider = TemplateProvider()
        result = provider.generate("Colecionavel action figure geek")
        assert "[Cena 1: Hook" in result

    def test_detects_premium_style(self):
        provider = TemplateProvider()
        result = provider.generate("Produto premium luxo elegante")
        assert "[Cena 1: Hook" in result

    def test_detects_3d_print_style(self):
        provider = TemplateProvider()
        result = provider.generate("Impressao 3d customizada")
        assert "[Cena 1: Hook" in result

    def test_detects_local_service_style(self):
        provider = TemplateProvider()
        result = provider.generate("Servico loja local")
        assert "[Cena 1: Hook" in result

    def test_returns_string(self):
        provider = TemplateProvider()
        result = provider.generate("Briefing teste")
        assert isinstance(result, str)

    def test_script_contains_multiple_scenes(self):
        provider = TemplateProvider()
        result = provider.generate("Teste briefing")
        scene_count = result.count("[Cena ")
        assert scene_count >= 3


class TestConfigProviderFallback:
    """Config de providers deve ter fallback corretamente configurado."""

    def test_template_provider_exists_in_config(self):
        assert "template" in LLM_PROVIDERS
        assert LLM_PROVIDERS["template"] is not None

    def test_template_has_highest_priority(self):
        template = LLM_PROVIDERS.get("template", {})
        assert template.get("priority") == 999
        for name, config in LLM_PROVIDERS.items():
            if name != "template":
                p = config.get("priority", 0)
                assert p < 999, f"Provider {name} has priority {p} >= 999"

    def test_all_five_providers_in_config(self):
        expected = {"template", "lm_studio", "koboldcpp", "llamacpp", "gpt4all"}
        actual = set(LLM_PROVIDERS.keys())
        missing = expected - actual
        assert not missing, f"Providers missing from config: {missing}"


class TestProviderFallbackMocked:
    """Provedor de fallback funciona quando providers falham (mocado)."""

    def _make_router(self, strategies):
        from app.adapters.llm.provider_router import ProviderRouter
        router = ProviderRouter.__new__(ProviderRouter)
        router.mode = "safe"
        router.strategies = strategies
        return router

    def _make_fallback_strategy(self, script="[Cena 1: Hook]\nFallback.\n[Cena 2: Solucao]\nDescricao."):
        s = MagicMock()
        p = MagicMock()
        p.name = "TemplateProvider"
        p.generate.return_value = script
        s.provider = p
        s.is_available.return_value = True
        s.generate.return_value = script
        s.validate_response.return_value = True
        return s

    def _make_failing_strategy(self, name="FailingProvider"):
        s = MagicMock()
        p = MagicMock()
        p.name = name
        p.generate.side_effect = Exception("fail")
        s.provider = p
        s.is_available.return_value = True
        s.generate.side_effect = Exception("fail")
        s.validate_response.return_value = False
        return s

    def test_template_provider_mocked_chain(self):
        fallback = self._make_fallback_strategy()
        router = self._make_router([fallback])
        result = router.generate_script_safe("Briefing")
        assert result["provider"] == "TemplateProvider"
        assert "script" in result
        assert "[Cena 1" in result["script"]

    def test_fallback_when_first_strategy_fails_mocked(self):
        first = self._make_failing_strategy("FailingProvider")
        fallback = self._make_fallback_strategy("[Cena 1: Fallback]\nScript.")
        router = self._make_router([first, fallback])
        result = router.generate_script_safe("Briefing")
        assert result["provider"] == "TemplateProvider"
        assert "[Cena 1" in result["script"]

    def test_fallback_when_first_unavailable_mocked(self):
        first = MagicMock()
        first.provider = MagicMock()
        first.provider.name = "UnavailableProvider"
        first.is_available.return_value = False
        fallback = self._make_fallback_strategy("Script disponivel.")
        router = self._make_router([first, fallback])
        result = router.generate_script_safe("Briefing")
        assert result["provider"] == "TemplateProvider"

    def test_fallback_when_strategy_returns_none_mocked(self):
        first = MagicMock()
        first.provider = MagicMock()
        first.provider.name = "NoneProvider"
        first.provider.generate.return_value = None
        first.is_available.return_value = True
        first.generate.return_value = None
        first.validate_response.return_value = False
        fallback = self._make_fallback_strategy("[Cena 1: Fallback]\nScript.")
        router = self._make_router([first, fallback])
        result = router.generate_script_safe("Briefing")
        assert result["provider"] == "TemplateProvider"

    def test_detect_available_includes_template_mocked(self):
        router = self._make_router([])
        available = router.detect_available()
        assert available.get("template") is True

    def test_strategy_without_provider_attribute_mocked(self):
        no_provider = MagicMock()
        no_provider.is_available.return_value = True
        no_provider.generate.return_value = "Direct generate."
        no_provider.validate_response.return_value = True
        router = self._make_router([no_provider])
        result = router.generate_script_safe("Briefing")
        assert "script" in result
