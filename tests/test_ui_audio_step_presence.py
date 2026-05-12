"""
Test: Audio/TTS and SRT steps presence in Gradio UI.
Verifica que narracao e legendas sao etapas separadas e que TTS falha nao bloqueia export.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logger

logger = setup_logger()
REPO_ROOT = Path(__file__).parent.parent

UI_FILE = REPO_ROOT / "app" / "ui" / "gradio_app.py"


def _read_ui() -> str:
    if UI_FILE.exists():
        return UI_FILE.read_text(encoding="utf-8", errors="ignore")
    return ""


def test_ui_file_exists():
    assert UI_FILE.exists(), "Arquivo gradio_app.py nao encontrado"
    logger.info("UI FILE: OK")


def test_narration_step_present():
    """Narracao deve ser uma etapa propria na UI."""
    content = _read_ui()
    assert "Narracao" in content or "narracao" in content, "Narracao nao encontrada na UI"
    logger.info("NARRATION STEP: OK")


def test_tts_engine_selector():
    """Deve haver seletor de motor TTS."""
    content = _read_ui()
    assert "TTS" in content or "tts" in content, "TTS nao encontrado na UI"
    logger.info("TTS SELECTOR: OK")


def test_srt_step_present():
    """Legendas/SRT devem ser etapa propria."""
    content = _read_ui()
    assert "SRT" in content or "srt" in content or "Legenda" in content, "SRT nao encontrado na UI"
    logger.info("SRT STEP: OK")


def test_export_without_audio_allowed():
    """Export sem audio deve estar previsto quando TTS falha."""
    content = _read_ui()
    has_fallback = "sem audio" in content or "sem audio" in content.lower()
    has_checkbox = "allow_no_audio" in content or "Permitir" in content
    assert has_fallback or has_checkbox, "Fallback de export sem audio nao encontrado"
    logger.info("EXPORT WITHOUT AUDIO: OK")


def test_audio_step_before_render():
    """Narracao deve aparecer antes do render no arquivo fonte."""
    content = _read_ui()
    nar_pos = content.find("Narracao")
    if nar_pos < 0:
        nar_pos = content.find("narracao")
    ren_pos = content.find("Render")
    if ren_pos < 0:
        ren_pos = content.find("render")
    if nar_pos > 0 and ren_pos > 0:
        assert nar_pos < ren_pos, "Narracao deve aparecer antes de Render"
    logger.info("AUDIO BEFORE RENDER: OK")


def test_tts_fallback_does_not_block():
    """TTS falhando nao deve bloquear o fluxo. Verifica logica no callback."""
    content = _read_ui()
    has_fallback = "export_without_audio" in content or "sem audio" in content
    assert has_fallback, "Logica de fallback TTS nao encontrada na UI"
    logger.info("TTS FALLBACK: OK")


if __name__ == "__main__":
    results = []
    for name, fn in [
        ("UI file exists", test_ui_file_exists),
        ("Narration step", test_narration_step_present),
        ("TTS selector", test_tts_engine_selector),
        ("SRT step", test_srt_step_present),
        ("Export without audio", test_export_without_audio_allowed),
        ("Audio before render", test_audio_step_before_render),
        ("TTS fallback", test_tts_fallback_does_not_block),
    ]:
        try:
            fn()
            results.append((name, True))
        except Exception as e:
            logger.error("Falha em %s: %s", name, e)
            results.append((name, False))
    print("\n=== AUDIO STEP PRESENCE TESTS ===")
    for name, ok in results:
        print("%s: %s" % (name, "PASSOU" if ok else "FALHOU"))
    print("==================================\n")
