"""
Tests for TemplateProvider.
"""
import sys
import os
sys.path.insert(0, "K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta")

from app.adapters.llm.base_provider import TemplateProvider

def test_template_always_available():
    """TemplateProvider should always be available."""
    tp = TemplateProvider()
    assert tp.is_available() == True
    print("test_template_always_available: PASSED")

def test_template_generate_viral():
    """Template should generate viral style script."""
    tp = TemplateProvider()
    result = tp.generate("comercial de bonecos")
    assert result is not None
    assert len(result) > 100
    assert "Cena 1" in result
    print("test_template_generate_viral: PASSED")

def test_template_fantasy_medieval():
    """Template should detect fantasy style."""
    tp = TemplateProvider()
    result = tp.generate("vender fantasia medieval artesanal")
    assert "medieval" in result.lower() or "fantasia" in result.lower()
    assert "Cena" in result
    print("test_template_fantasy_medieval: PASSED")

def test_template_3d_print():
    """Template should detect 3D print style."""
    tp = TemplateProvider()
    result = tp.generate("produto impressao 3D personalizado")
    assert "impress" in result.lower()
    assert "Cena" in result
    print("test_template_3d_print: PASSED")

    def test_template_validate_response():
        """Should validate good vs bad responses."""
        tp = TemplateProvider()
        assert tp.validate_response("") == False
        assert tp.validate_response("curto") == False
        assert tp.validate_response("Cena 1: intro\nCena 2: demo") == False  # Too short
        # A valid response must be at least 50 chars and without robotic phrases
        valid_response = """
[Cena 1: Introducao - 5s]
Foco no produto. Luz suave.
Texto: 'Apresentamos'
Narracao: 'Incrivel'
"""
        assert tp.validate_response(valid_response) == True
        print("test_template_validate_response: PASSED")

if __name__ == "__main__":
    test_template_always_available()
    test_template_generate_viral()
    test_template_fantasy_medieval()
    test_template_3d_print()
    test_template_validate_response()
    print("\nAll TemplateProvider tests PASSED!")
