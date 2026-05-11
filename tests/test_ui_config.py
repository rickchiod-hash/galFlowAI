"""Tests for Config tab in UI (UI-204)."""
import pytest


class TestConfigTabStructure:
    def test_config_tab_exists(self):
        with open("app/ui/gradio_app.py", encoding="utf-8") as f:
            content = f.read()
        assert 'gr.Tab("Configuracoes")' in content

    def test_config_has_provider_dropdown(self):
        with open("app/ui/gradio_app.py", encoding="utf-8") as f:
            content = f.read()
        assert "Provedor LLM Padrao" in content

    def test_config_has_quality_dropdown(self):
        with open("app/ui/gradio_app.py", encoding="utf-8") as f:
            content = f.read()
        assert "Qualidade Padrao" in content

    def test_config_has_duration_slider(self):
        with open("app/ui/gradio_app.py", encoding="utf-8") as f:
            content = f.read()
        assert "Duracao Padrao" in content

    def test_config_has_save_button(self):
        with open("app/ui/gradio_app.py", encoding="utf-8") as f:
            content = f.read()
        assert "Salvar Configuracoes" in content

    def test_config_has_reset_button(self):
        with open("app/ui/gradio_app.py", encoding="utf-8") as f:
            content = f.read()
        assert "Restaurar Padroes" in content

    def test_config_service_imported(self):
        with open("app/ui/gradio_app.py", encoding="utf-8") as f:
            content = f.read()
        assert "get_config_service" in content


class TestConfigServiceIntegration:
    def test_config_service_can_save_and_load(self):
        from app.services.config_service import get_config_service
        svc = get_config_service()
        original = svc.get("default_llm_provider")
        svc.set("default_llm_provider", "lm_studio")
        assert svc.get("default_llm_provider") == "lm_studio"
        svc.set("default_llm_provider", original)

    def test_quality_draft_valid(self):
        from app.services.config_service import get_config_service
        svc = get_config_service()
        svc.set("default_quality", "DRAFT")
        assert svc.get("default_quality") == "DRAFT"
