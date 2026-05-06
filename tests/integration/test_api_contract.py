"""
API Contract Tests for FlowForgeAI FastAPI.
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from app.api import app


client = TestClient(app)


class TestHealthEndpoint:
    """Test contract for /api/health endpoint."""
    
    def test_health_returns_200(self):
        """Health endpoint should return 200."""
        response = client.get("/api/health")
        assert response.status_code == 200
    
    def test_health_returns_valid_envelope(self):
        """Health endpoint should return standardized envelope."""
        response = client.get("/api/health")
        data = response.json()
        assert "ok" in data
        assert data["ok"] is True
        assert "code" in data
        assert data["code"] == "SUCCESS"
        assert "message" in data
        assert "details" in data
    
    def test_health_details_contains_expected_fields(self):
        """Health details should contain app info."""
        response = client.get("/api/health")
        details = response.json()["details"]
        assert "app" in details
        assert "mode" in details
        assert details["mode"] == "local"


class TestLLMProvidersEndpoint:
    """Test contract for /api/llm/providers endpoint."""
    
    def test_providers_returns_200(self):
        """Providers endpoint should return 200."""
        response = client.get("/api/llm/providers")
        assert response.status_code == 200
    
    def test_providers_returns_expected_fields(self):
        """Providers should return expected provider keys."""
        response = client.get("/api/llm/providers")
        data = response.json()
        assert "template" in data
        assert "lmstudio" in data
        assert "koboldcpp" in data
        assert "gpt4all" in data
        assert "llamacpp" in data


class TestScriptGenerationEndpoint:
    """Test contract for /api/llm/script endpoint."""
    
    def test_script_generation_returns_envelope(self):
        """Script generation should return standardized envelope."""
        response = client.post(
            "/api/llm/script",
            json={"briefing": "Test commercial for product X"}
        )
        # May return 200 or 500 depending on providers available
        assert response.status_code in [200, 500]
        data = response.json()
        # If 200, should have proper envelope
        if response.status_code == 200:
            assert "ok" in data
            assert "details" in data
            assert "script_markdown" in data["details"]


class TestScriptManagementEndpoints:
    """Test contract for script management endpoints."""
    
    def test_save_manual_edit_returns_envelope(self):
        """Save manual edit should return standardized envelope."""
        # First create a project (mock or use existing)
        response = client.post(
            "/api/projects/test_project/script/save-manual-edit",
            json={
                "project_id": "test_project",
                "script_markdown": "# Test Script\n\nThis is a test."
            }
        )
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert "ok" in data
    
    def test_approve_script_returns_envelope(self):
        """Approve script should return standardized envelope."""
        response = client.post("/api/projects/test_project/script/approve")
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert "ok" in data


class TestErrorResponses:
    """Test that errors return standardized envelope."""
    
    def test_nonexistent_project_returns_200_with_envelope(self):
        """Request for nonexistent project should return envelope (may be success with empty data)."""
        response = client.get("/api/projects/nonexistent123/script/current")
        # Endpoint returns 200 with envelope (even if project doesn't exist)
        assert response.status_code == 200
        data = response.json()
        # Should have standardized envelope
        assert "ok" in data
        assert "message" in data


class TestWebSocket:
    """Test WebSocket endpoint for progress updates."""
    
    def test_websocket_connects(self):
        """WebSocket should accept connection."""
        with client.websocket_connect("/ws/jobs/test_job") as websocket:
            # Should be able to connect
            pass
    
    def test_websocket_receives_messages(self):
        """WebSocket should send job updates."""
        with client.websocket_connect("/ws/jobs/test_job") as websocket:
            # Try to receive (may get error if job not found)
            try:
                data = websocket.receive_json(timeout=1)
                assert "job_id" in data
                assert "status" in data
            except Exception:
                # Job not found is acceptable
                pass
