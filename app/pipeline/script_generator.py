import json
from app.logging_config import setup_logger
from app.services.script_service import generate_script_with_llm

logger = setup_logger()

def generate_script(briefing, project_id=None, mode="auto"):
    """
    Gera roteiro a partir do briefing usando LLMs locais ou templates.
    mode: 'auto', 'fast', 'quality', 'safe', 'template'
    """
    msg = "Gerando roteiro para: %s [modo: %s]" % (str(briefing)[:50], mode)
    logger.info(msg)
    
    try:
        result = generate_script_with_llm(briefing, mode)
        logger.info(
            "Roteiro gerado via %s",
            result.get("provider", "unknown")
        )
        return result["script"]
    except Exception as e:
        logger.error("CAUSA: Falha no servico de roteiro: %s | CORREÇÃO: Verifique LLM provider disponível", e)
        # Fallback final
        from app.adapters.llm.template_provider import TemplateProvider
        tp = TemplateProvider()
        return tp.generate(briefing)

def save_script(project_id, script_text):
    """Salva roteiro no projeto."""
    from app.config import PROJECTS_DIR
    from pathlib import Path
    
    proj_dir = Path(PROJECTS_DIR) / project_id
    script_path = proj_dir / "script" / "script.txt"
    
    # Cria diretórios se não existirem
    script_path.parent.mkdir(parents=True, exist_ok=True)
    
    script_path.write_text(script_text, encoding="utf-8")
    
    # Atualiza project.json se existir
    proj_file = proj_dir / "project.json"
    if proj_file.exists():
        content = proj_file.read_text(encoding="utf-8")
        proj = json.loads(content)
        proj["script"] = script_text
        proj["status"] = "script_generated"
        proj_file.write_text(json.dumps(proj, indent=2, ensure_ascii=False), encoding="utf-8")
    
    logger.info("Roteiro salvo: %s", script_path.name)
    return str(script_path)
