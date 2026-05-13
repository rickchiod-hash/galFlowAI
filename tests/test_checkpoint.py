import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logger

logger = setup_logger()

DOCS_DIR = Path(__file__).parent.parent / "docs" / "project-control"

REQUIRED_SECTIONS = [
    "Progresso geral",
    "Estado atual",
    "Resumo tipo Daily",
    "Bloqueios",
    "Riscos",
    "Gaps encontrados",
    "TODOs rastreáveis",
    "Arquivos alterados nesta sessão",
    "Comandos executados",
    "Evidências usadas",
]

CHECKPOINT_FILES = [
    "00_STATUS_EXECUTIVO.md",
    "10_DAILY_LOG.md",
    "13_CHECKPOINTS_DE_SESSAO.md",
    "20_DEFINITION_OF_READY_DONE.md",
]


def test_checkpoint_files_exist():
    for fname in CHECKPOINT_FILES:
        path = DOCS_DIR / fname
        assert path.exists(), f"Arquivo obrigatório ausente: {fname}"
        logger.info(f"CHECKPOINT {fname}: OK")




def test_status_file_has_required_sections():
    path = DOCS_DIR / "00_STATUS_EXECUTIVO.md"
    content = path.read_text(encoding="utf-8")

    for section in REQUIRED_SECTIONS:
        assert section in content, f"Seção ausente no status: '{section}'"
        logger.info(f"SEÇÃO {section}: OK")




def test_daily_log_has_entry_format():
    path = DOCS_DIR / "10_DAILY_LOG.md"
    content = path.read_text(encoding="utf-8")

    assert content.startswith("# 10_DAILY_LOG")
    assert "## 2026" in content or "## 2025" in content
    assert "O que fiz" in content
    assert "Bloqueios" in content
    assert "Próximo passo" in content
    logger.info("DAILY_LOG: Formato OK")




if __name__ == "__main__":
    results = []
    try:
        results.append(("Arquivos checkpoint existem", test_checkpoint_files_exist()))
    except Exception as e:
        logger.error("Falha em test_checkpoint_files_exist: %s", e)
        results.append(("Arquivos checkpoint existem", False))

    try:
        results.append(("Seções obrigatórias no status", test_status_file_has_required_sections()))
    except Exception as e:
        logger.error("Falha em test_status_file_has_required_sections: %s", e)
        results.append(("Seções obrigatórias no status", False))

    try:
        results.append(("Formato do daily log", test_daily_log_has_entry_format()))
    except Exception as e:
        logger.error("Falha em test_daily_log_has_entry_format: %s", e)
        results.append(("Formato do daily log", False))

    print("\n=== RESULTADOS DOS TESTES ===")
    for name, result in results:
        status = "PASSOU" if result else "FALHOU"
        print(f"{name}: {status}")
    print("==========================\n")
