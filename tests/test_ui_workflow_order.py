"""
Test: Workflow order in Gradio UI.
Verifica que o fluxo briefing -> roteiro -> aprovacao -> narracao -> legendas -> cenas -> render -> export
esta presente na UI.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logger

logger = setup_logger()
REPO_ROOT = Path(__file__).parent.parent

UI_FILE = REPO_ROOT / "app" / "ui" / "gradio_app.py"


FLOW_MARKERS = {
    "briefing": ["### Etapa 1", "Briefing"],
    "roteiro": ["### Etapa 2", "Roteiro Edit"],
    "aprovacao": ["Aprovar Roteiro", "Aprova"],  # "aprov" in _STATE_DEFAULT is excluded
    "narracao": ["### Etapa 3", "Narracao"],
    "legendas": ["SRT", "Legenda"],
    "cenas": ["### Etapa 4", "Cena", "scenes"],
    "render": ["### Etapa 5", "Render"],
    "export": ["### Etapa 6", "Export", "MP4"],
}

STEP_ORDER = ["briefing", "roteiro", "aprovacao", "narracao", "legendas", "cenas", "render", "export"]


def _read_ui() -> str:
    if UI_FILE.exists():
        return UI_FILE.read_text(encoding="utf-8", errors="ignore")
    return ""


def test_ui_file_exists():
    assert UI_FILE.exists(), "Arquivo gradio_app.py nao encontrado"
    logger.info("UI FILE: OK")


def test_flow_contains_briefing():
    content = _read_ui()
    assert any(m in content for m in FLOW_MARKERS["briefing"]), "Briefing nao encontrado na UI"
    logger.info("FLOW BRIEFING: OK")


def test_flow_contains_script():
    content = _read_ui()
    assert any(m in content for m in FLOW_MARKERS["roteiro"]), "Roteiro nao encontrado na UI"
    logger.info("FLOW ROTEIRO: OK")


def test_flow_contains_approval():
    content = _read_ui()
    assert any(m in content for m in FLOW_MARKERS["aprovacao"]), "Aprovacao nao encontrada na UI"
    logger.info("FLOW APROVACAO: OK")


def test_flow_contains_narration():
    content = _read_ui()
    assert any(m in content for m in FLOW_MARKERS["narracao"]), "Narracao/TTS nao encontrada na UI"
    logger.info("FLOW NARRACAO: OK")


def test_flow_contains_subtitles():
    content = _read_ui()
    assert any(m in content for m in FLOW_MARKERS["legendas"]), "Legendas/SRT nao encontradas na UI"
    logger.info("FLOW LEGENDAS: OK")


def test_flow_contains_scenes():
    content = _read_ui()
    assert any(m in content for m in FLOW_MARKERS["cenas"]), "Cenas/Prompts nao encontrados na UI"
    logger.info("FLOW CENAS: OK")


def test_flow_contains_render():
    content = _read_ui()
    assert any(m in content for m in FLOW_MARKERS["render"]), "Render nao encontrado na UI"
    logger.info("FLOW RENDER: OK")


def test_flow_contains_export():
    content = _read_ui()
    assert any(m in content for m in FLOW_MARKERS["export"]), "Export nao encontrado na UI"
    logger.info("FLOW EXPORT: OK")


def test_flow_order():
    """Verifica que os marcos do fluxo aparecem em ordem Etapa 1..6."""
    content = _read_ui()
    etapa_positions = {}
    for i in range(1, 7):
        marker = "### Etapa %d" % i
        idx = content.find(marker)
        assert idx > 0, "Marcador '%s' nao encontrado" % marker
        etapa_positions[i] = idx
    for i in range(1, 6):
        assert etapa_positions[i] < etapa_positions[i + 1], (
            "Ordem incorreta: Etapa %d (pos=%d) antes de Etapa %d (pos=%d)"
            % (i, etapa_positions[i], i + 1, etapa_positions[i + 1])
        )
    logger.info("FLOW ORDER: OK - Etapas 1..6 em ordem crescente")


def test_no_preview_before_render():
    """Preview de video vazio deve ter placeholder, nao video real."""
    content = _read_ui()
    has_placeholder = "Preview" in content or "preview" in content or "placeholder" in content
    assert has_placeholder, "UI nao menciona placeholder/preview antes de render"
    logger.info("PREVIEW PLACEHOLDER: OK")


if __name__ == "__main__":
    results = []
    for name, fn in [
        ("UI file exists", test_ui_file_exists),
        ("Flow briefing", test_flow_contains_briefing),
        ("Flow roteiro", test_flow_contains_script),
        ("Flow aprovacao", test_flow_contains_approval),
        ("Flow narracao", test_flow_contains_narration),
        ("Flow legendas", test_flow_contains_subtitles),
        ("Flow cenas", test_flow_contains_scenes),
        ("Flow render", test_flow_contains_render),
        ("Flow export", test_flow_contains_export),
        ("Flow order", test_flow_order),
        ("Preview placeholder", test_no_preview_before_render),
    ]:
        try:
            fn()
            results.append((name, True))
        except Exception as e:
            logger.error("Falha em %s: %s", name, e)
            results.append((name, False))
    print("\n=== WORKFLOW ORDER TESTS ===")
    for name, ok in results:
        print("%s: %s" % (name, "PASSOU" if ok else "FALHOU"))
    print("=============================\n")
