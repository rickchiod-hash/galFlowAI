import json
import time
from pathlib import Path
from app.logging_config import setup_logger
from app.config import PROJECTS_DIR
from app.project_manager import create_project
from app.services.script_service import generate_script_with_details
from app.repositories.script_repository import ScriptRepository

logger = setup_logger()

def run_auto_pipeline(project_name, briefing, commercial_type="produto", duration=30, fmt="9:16", style="comercial moderno", uploaded_images=None, mode="auto"):
    result = {
        "status": "started",
        "project_id": "",
        "script": "",
        "video_preview": None,
        "project_path": "",
        "logs": []
    }
    
    try:
        # 1. Validar briefing
        if not briefing or len(briefing.strip()) < 10:
            briefing = "Comercial de 30 segundos para produto generico, estilo moderno."
            result["logs"].append("Briefing curto; usando fallback.")
            logger.warning("Briefing curto; usando fallback.")
        
        # 2. Gerar nome se vazio
        if not project_name:
            words = briefing.split()[:3]
            slug = "_".join([w.lower() for w in words if w.isalnum()])[:30]
            project_name = slug or "comercial_auto"
            result["logs"].append("Nome gerado: {}".format(project_name))
        
        # 3. Criar projeto
        proj = create_project(project_name)
        project_id = proj["id"]
        result["project_id"] = project_id
        proj_dir = PROJECTS_DIR / project_id
        result["project_path"] = str(proj_dir)
        result["logs"].append("Projeto criado: {}".format(project_id))
        
        # 4. Salvar briefing
        brief_file = proj_dir / "brief" / "brief.txt"
        brief_file.write_text(briefing, encoding="utf-8")
        result["logs"].append("Briefing salvo.")
        
        # 5. Gerar roteiro usando LLM providers (com timeout 120s)
        gen_result = generate_script_with_details(briefing, project_id, mode=mode)
        script = gen_result["script"]
        ScriptRepository(project_id).save_script(script)
        result["script"] = script
        result["logs"].append("Roteiro gerado.")
        
        # Provider info a partir do resultado real
        result["provider_info"] = {
            "provider": gen_result.get("provider", "TemplateProvider"),
            "time": gen_result.get("time", 0),
            "quality": gen_result.get("quality", "fallback")
        }
        
        result["status"] = "completed"
        result["logs"].append("Roteiro gerado com sucesso. Use 'Aprovar Roteiro' para liberar cenas e vídeo.")
        
    except Exception as e:
        result["status"] = "error"
        result["logs"].append("Erro: {}".format(str(e)))
        logger.error("Auto pipeline falhou: %s", e)
    
    return result
