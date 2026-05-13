"""Contract tests for H10 - FastAPI critical endpoints."""
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.api import app


_PROVIDER_PATCHES = [
    patch('app.adapters.llm.lmstudio_provider.LMStudioProvider.is_available', return_value=False),
    patch('app.adapters.llm.koboldcpp_provider.KoboldCppProvider.is_available', return_value=False),
    patch('app.adapters.llm.llamacpp_provider.LlamaCppProvider.is_available', return_value=False),
    patch('app.adapters.llm.gpt4all_provider.GPT4AllProvider.is_available', return_value=False),
]

for _p in _PROVIDER_PATCHES:
    _p.start()

client = TestClient(app)


class TestHealthContract:
    def test_health_returns_200(self):
        r = client.get("/api/v1/health")
        assert r.status_code == 200
    
    def test_health_returns_ok(self):
        r = client.get("/api/v1/health")
        assert r.json()["ok"] is True
    
    def test_health_returns_details(self):
        r = client.get("/api/v1/health")
        assert "details" in r.json()

class TestLLMContract:
    def test_providers_returns_200(self):
        r = client.get("/api/v1/llm/providers")
        assert r.status_code == 200
    
    def test_script_generate_returns_200(self):
        r = client.post("/api/v1/llm/script", json={"briefing": "Test commercial"})
        assert r.status_code == 200
    
    def test_script_generate_returns_ok(self):
        r = client.post("/api/v1/llm/script", json={
            "briefing": "Comercial de teste para produto generico com duração de 30 segundos"
        })
        assert r.status_code == 200
        json_data = r.json()
        # success_response envelop: {ok, code, message, details}
        assert "ok" in json_data
        assert json_data["ok"] is True

class TestHardwareContract:
    def test_hardware_returns_200(self):
        r = client.get("/api/v1/hardware")
        assert r.status_code == 200
    
    def test_hardware_returns_vram(self):
        r = client.get("/api/v1/hardware")
        details = r.json()["details"]
        assert "vram_gb" in details or "gpu" in str(details)
