import json
import time
from pathlib import Path
from app.logging_config import setup_logger
from app.config import PROJECTS_DIR
from app.project_manager import create_project
from app.pipeline.script_generator import generate_script, save_script
from app.pipeline.scene_splitter import split_script_into_scenes, save_scenes
from app.pipeline.prompt_builder import build_prompts_for_scenes, save_prompts
from app.adapters.ffmpeg_adapter import create_storyboard_video
from app.hardware import get_gpu_info, get_recommended_preset

logger = setup_logger()

def run_auto_pipeline(project_name, briefing, commercial_type="produto", duration=30, fmt="9:16", style="comercial moderno", uploaded_images=None, mode="auto"):
    result = {
        "status": "started",
        "project_id": "",
        "script": "",
        "scenes": [],
        "video_preview": "",
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
<<<<<<< HEAD
        proj_dir = PROJECTS_DIR / project_id
        result["project_path"] = str(proj_dir)
        result["logs"].append("Projeto criado: {}".format(project_id))
        
        # 4. Salvar briefing
        brief_file = proj_dir / "brief" / "brief.txt"
        brief_file.write_text(briefing, encoding="utf-8")
        result["logs"].append("Briefing salvo.")
        
        # 5. Gerar roteiro using LLM providers
        from app.pipeline.script_generator import generate_script
        script = generate_script(briefing, project_id, mode=mode)
        save_script(project_id, script)
        result["script"] = script
        result["logs"].append("Roteiro gerado.")
        
        # Capture provider info
        from app.services.script_service import generate_script_with_llm
        try:
            router_result = generate_script_with_llm(briefing, mode)
            result["provider_info"] = {
                "provider": router_result.get("provider", "TemplateProvider"),
                "time": router_result.get("time", 0),
                "quality": router_result.get("quality", "fallback")
            }
        except:
            result["provider_info"] = {"provider": "TemplateProvider", "time": 0, "quality": "fallback"}
        
        # 6. Dividir em cenas
        scenes = split_script_into_scenes(script, project_id)
        save_scenes(project_id, scenes)
        result["scenes"] = scenes
        result["logs"].append("{} cenas criadas.".format(len(scenes)))
        
        # 7. Gerar prompts
        scenes = build_prompts_for_scenes(scenes, style)
        save_prompts(project_id, scenes)
        result["logs"].append("Prompts gerados.")
        
        # 8. Gerar storyboard via FFmpeg
        gpu = get_gpu_info()
        preset = get_recommended_preset(gpu["vram_gb"], gpu["name"])
        result["logs"].append("Preset: {}".format(preset["model"]))
        
        try:
            video_path = create_storyboard_video(project_id, scenes)
            if video_path:
                result["video_preview"] = str(video_path)
                result["logs"].append("Storyboard criado: {}".format(video_path.name))
        except Exception as e:
            result["logs"].append("Erro no storyboard: {}".format(str(e)))
        
        result["status"] = "completed"
        result["logs"].append("Pipeline concluido.")
        
    except Exception as e:
        result["status"] = "error"
        result["logs"].append("Erro: {}".format(str(e)))
        logger.error("Auto pipeline falhou: %s", e)
    
    return result
