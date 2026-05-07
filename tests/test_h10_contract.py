"""Contract tests for H10 - FastAPI critical endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

class TestHealthContract:
    def test_health_returns_200(self):
        r = client.get("/api/health")
        assert r.status_code == 200
    
    def test_health_returns_ok(self):
        r = client.get("/api/health")
        assert r.json()["ok"] is True
    
    def test_health_returns_details(self):
        r = client.get("/api/health")
        assert "details" in r.json()

class TestLLMContract:
    def test_providers_returns_200(self):
        r = client.get("/api/llm/providers")
        assert r.status_code == 200
    
    def test_script_generate_returns_200(self):
        r = client.post("/api/llm/script", json={"briefing": "Test commercial"})
        assert r.status_code == 200
    
    def test_script_generate_returns_ok(self):
        r = client.post("/api/llm/script", json={
            "briefing": "Comercial de teste para produto generico com duração de 30 segundos"
        })
        assert r.status_code == 200
        json_data = r.json()
        # success_response envelop: {ok, code, message, details}
        assert "ok" in json_data
        assert json_data["ok"] is True

class TestHardwareContract:
    def test_hardware_returns_200(self):
        r = client.get("/api/hardware")
        assert r.status_code == 200
    
    def test_hardware_returns_vram(self):
        r = client.get("/api/hardware")
        details = r.json()["details"]
        assert "vram_gb" in details or "gpu" in str(details)
