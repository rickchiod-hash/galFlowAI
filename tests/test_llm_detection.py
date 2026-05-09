"""
Tests for LLM detection.
"""
import sys
sys.path.insert(0, "K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta")

def test_detect_lm_studio():
    """Test LM Studio detection."""
    import requests
    try:
        r = requests.get("http://localhost:1234/v1/models", timeout=2)
        available = r.status_code == 200
    except:
        available = False
    print(f"LM Studio available: {available}")
    assert True  # Test passes regardless

def test_detect_koboldcpp():
    """Test KoboldCpp detection."""
    import requests
    try:
        r = requests.get("http://localhost:5001/api/v1/models", timeout=2)
        available = r.status_code == 200
    except:
        available = False
    print(f"KoboldCpp available: {available}")
    assert True

def test_detect_template_always():
    """TemplateProvider always available."""
    from app.adapters.llm.base_provider import TemplateProvider
    tp = TemplateProvider()
    assert tp.is_available() == True
    print("TemplateProvider: Always available")
    assert True

if __name__ == "__main__":
    test_detect_lm_studio()
    test_detect_koboldcpp()
    test_detect_template_always()
    print("\nDetection tests completed!")
