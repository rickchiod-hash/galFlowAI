"""
Tests for script quality validation.
"""
import sys
sys.path.insert(0, "K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta")

from app.adapters.llm.base_provider import BaseLLMProvider, TemplateProvider

def test_validate_good_script():
    """Good script should pass validation."""
    tp = TemplateProvider()
    good_script = """
[Cena 1: Introducao - 5s]
Foco no produto. Luz suave e convidativa, destacando os detalhes.
Texto: 'Produto incrível'
Narracao: 'Conheça nosso produto incrível e surpreenda-se'
"""
    assert tp.validate_response(good_script) == True
    print("test_validate_good_script: PASSED")

def test_validate_bad_script_robotic():
    """Robotic phrases should fail."""
    tp = TemplateProvider()
    bad_script = "Apresentamos o novo produto. Solucao completa para suas necessidades."
    assert tp.validate_response(bad_script) == False
    print("test_validate_bad_script_robotic: PASSED")

def test_validate_empty():
    """Empty script should fail."""
    tp = TemplateProvider()
    assert tp.validate_response("") == False
    assert tp.validate_response(None) == False
    print("test_validate_empty: PASSED")

def test_validate_no_scenes():
    """Script without scenes should fail."""
    tp = TemplateProvider()
    no_scenes = "Um texto qualquer sem marcadores de cena."
    assert tp.validate_response(no_scenes) == False
    print("test_validate_no_scenes: PASSED")

if __name__ == "__main__":
    test_validate_good_script()
    test_validate_bad_script_robotic()
    test_validate_empty()
    test_validate_no_scenes()
    print("\nAll script quality tests PASSED!")
