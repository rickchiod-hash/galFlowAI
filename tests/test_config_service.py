"""Tests for ConfigService (UI-204)."""
import json
import pytest
from pathlib import Path

from app.services.config_service import ConfigService, DEFAULT_CONFIG


class TestConfigService:
    def test_default_values(self, tmp_path):
        svc = ConfigService()
        svc._config = dict(DEFAULT_CONFIG)
        assert svc.get("default_llm_provider") == "auto"
        assert svc.get("default_quality") == "STANDARD"
        assert svc.get("default_duration_sec") == 30

    def test_set_and_get(self, tmp_path):
        svc = ConfigService()
        svc._config = dict(DEFAULT_CONFIG)
        svc.set("default_llm_provider", "lm_studio")
        assert svc.get("default_llm_provider") == "lm_studio"

    def test_set_multi(self, tmp_path):
        svc = ConfigService()
        svc._config = dict(DEFAULT_CONFIG)
        svc.set_multi({"default_quality": "HIGH", "default_duration_sec": 45})
        assert svc.get("default_quality") == "HIGH"
        assert svc.get("default_duration_sec") == 45

    def test_get_all(self, tmp_path):
        svc = ConfigService()
        svc._config = dict(DEFAULT_CONFIG)
        all_cfg = svc.get_all()
        assert all_cfg["default_llm_provider"] == "auto"
        assert all_cfg["default_quality"] == "STANDARD"

    def test_reset_restores_defaults(self, tmp_path):
        svc = ConfigService()
        svc._config = dict(DEFAULT_CONFIG)
        svc.set("default_llm_provider", "gpt4all")
        svc.reset()
        assert svc.get("default_llm_provider") == "auto"

    def test_get_with_default(self, tmp_path):
        svc = ConfigService()
        svc._config = dict(DEFAULT_CONFIG)
        assert svc.get("nonexistent_key", "fallback") == "fallback"

    def test_get_existing_key_no_default(self, tmp_path):
        svc = ConfigService()
        svc._config = dict(DEFAULT_CONFIG)
        assert svc.get("default_quality") == "STANDARD"
