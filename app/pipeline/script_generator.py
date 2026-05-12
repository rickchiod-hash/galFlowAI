import json
from app.logging_config import setup_logger
from app.services.script_service import generate_script_with_llm, generate_script_with_provider

logger = setup_logger()

_PROVIDER_MODES = {"lmstudio", "koboldcpp", "llamacpp", "gpt4all", "template"}


def _run_generation(briefing, mode="auto"):
    """Internal: returns dict with script, provider, time, quality."""
    if mode in _PROVIDER_MODES:
        return generate_script_with_provider(briefing, mode)
    else:
        return generate_script_with_llm(briefing, mode)


def generate_script(briefing, project_id=None, mode="auto"):
    """
    Gera roteiro a partir do briefing usando LLMs locais ou templates.
    mode: 'auto', 'fast', 'quality', 'safe', 'template', 'lmstudio', 'koboldcpp', 'llamacpp', 'gpt4all'
    Returns: str (the generated script)
    """
    logger.info("Gerando roteiro para: %s [modo: %s]", str(briefing)[:50], mode)
    try:
        result = _run_generation(briefing, mode)
        logger.info("Roteiro gerado via %s", result.get("provider", "unknown"))
        if not result.get("ok") or "script" not in result:
            raise KeyError("Resultado sem script: %s" % result.get("error", "erro desconhecido"))
        return result["script"]
    except Exception as e:
        logger.error("CAUSA: Falha no servico de roteiro: %s | CORREÇÃO: Verifique LLM provider disponível", e)
        from app.adapters.llm.template_provider import TemplateProvider
        return TemplateProvider().generate(briefing)


def generate_script_with_details(briefing, project_id=None, mode="auto"):
    """
    Gera roteiro e retorna dict com script + metadados do provider.
    Returns: dict with keys: ok, script, provider, time, quality
    """
    logger.info("Gerando roteiro para: %s [modo: %s]", str(briefing)[:50], mode)
    try:
        result = _run_generation(briefing, mode)
        logger.info("Roteiro gerado via %s", result.get("provider", "unknown"))
        if not result.get("ok") or "script" not in result:
            raise KeyError("Resultado sem script: %s" % result.get("error", "erro desconhecido"))
        return result
    except Exception as e:
        logger.error("CAUSA: Falha no servico de roteiro: %s | CORREÇÃO: Verifique LLM provider disponível", e)
        from app.adapters.llm.template_provider import TemplateProvider
        from app.services.script_service import generate_script_with_provider
        tp = TemplateProvider()
        fallback_result = {"ok": True, "script": tp.generate(briefing), "provider": "TemplateProvider", "time": 0, "quality": "fallback"}
        logger.info("Fallback: Script generated via TemplateProvider (time: 0.00s)")
        return fallback_result

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
