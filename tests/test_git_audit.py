import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logger

logger = setup_logger()

REPO_ROOT = Path(__file__).parent.parent
AUDIT_FILE = REPO_ROOT / "docs" / "project-control" / "01_AUDITORIA_HISTORICO_GIT.md"

REQUIRED_SECTIONS = [
    "Objetivo",
    "Comandos executados",
    "Resultados",
    "Tabelas",
    "Arquivos deletados",
    "Perguntas obrigatórias",
]

REQUIRED_QUESTIONS = [
    "Quais telas existiam e sumiram?",
    "Quais providers foram removidos",
    "Quais fallbacks foram alterados?",
    "Quais docs dizem que algo existe",
    "Quais TODOs foram resolvidos",
    "Quais arquivos mais mudaram",
    "O último commit aproxima ou afasta",
]


def test_audit_file_exists():
    assert AUDIT_FILE.exists(), f"01_AUDITORIA_HISTORICO_GIT.md ausente em {AUDIT_FILE}"
    logger.info("01_AUDITORIA_HISTORICO_GIT.md: OK")
    return True


def test_audit_has_required_sections():
    content = AUDIT_FILE.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        assert section in content, f"Seção obrigatória ausente: '{section}'"
        logger.info(f"SEÇÃO {section}: OK")
    return True


def test_audit_has_git_evidence():
    content = AUDIT_FILE.read_text(encoding="utf-8")
    assert "132" in content or "Commits" in content, "Contagem de commits ausente"
    assert "63839e7" in content or "HEAD" in content, "HEAD commit ausente"
    assert "master" in content, "Branch ausente"
    logger.info("EVIDÊNCIA GIT: OK")
    return True


def test_audit_has_required_questions():
    content = AUDIT_FILE.read_text(encoding="utf-8")
    for question in REQUIRED_QUESTIONS:
        assert question in content, f"Pergunta obrigatória ausente: '{question}'"
        logger.info(f"PERGUNTA: OK")
    return True


def test_audit_commit_count_within_range():
    import subprocess
    result = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        capture_output=True, text=True, cwd=REPO_ROOT
    )
    actual_count = int(result.stdout.strip())
    content = AUDIT_FILE.read_text(encoding="utf-8")
    assert str(actual_count) in content, (
        f"Contagem de commits no audit ({actual_count}) "
        f"diferente do git atual. Audit desatualizado."
    )
    logger.info(f"COMMIT COUNT {actual_count}: OK")
    return True


if __name__ == "__main__":
    results = []
    for name, fn in [
        ("Arquivo existe", test_audit_file_exists),
        ("Seções obrigatórias", test_audit_has_required_sections),
        ("Evidência Git", test_audit_has_git_evidence),
        ("Perguntas obrigatórias", test_audit_has_required_questions),
        ("Contagem de commits", test_audit_commit_count_within_range),
    ]:
        try:
            results.append((name, fn()))
        except Exception as e:
            logger.error(f"Falha em {name}: {e}")
            results.append((name, False))

    print("\n=== RESULTADOS DOS TESTES ===")
    for name, result in results:
        print(f"{name}: {'PASSOU' if result else 'FALHOU'}")
    print("==========================\n")
