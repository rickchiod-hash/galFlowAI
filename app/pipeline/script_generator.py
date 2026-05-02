import json
from app.logging_config import setup_logger

logger = setup_logger()

def generate_script(briefing, project_id=None):
    """Gera roteiro a partir do briefing."""
    msg = "Gerando roteiro para: %s" % str(briefing)[:50]
    logger.info(msg)
    template = (
        "[Cena 1: Introducao]\n"
        "Um ambiente moderno. O produto aparece.\n"
        "Texto: %s\n\n"
        "[Cena 2: Demonstrcao]\n"
        "Demonstracao das funcionalidades.\n\n"
        "[Cena 3: Chamada]\n"
        "Adquira ja o seu!"
    ) % str(briefing)[:100]
    logger.info("Roteiro gerado")
    return template

def save_script(project_id, script_text):
    """Salva roteiro no projeto."""
    from app.config import PROJECTS_DIR
    proj_dir = PROJECTS_DIR / project_id
    script_path = proj_dir / "script" / "script.txt"
    script_path.write_text(script_text, encoding="utf-8")
    proj_file = proj_dir / "project.json"
    content = proj_file.read_text(encoding="utf-8")
    proj = json.loads(content)
    proj["script"] = script_text
    proj["status"] = "script_generated"
    proj_file.write_text(json.dumps(proj, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Roteiro salvo: %s", script_path.name)
    return str(script_path)
