import json
from pathlib import Path
from app.logging_config import setup_logger
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
        proj_dir = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta/projects") / project_id
        result["project_path"] = str(proj_dir)
        result["logs"].append("Projeto criado: {}".format(project_id))
        
        # 4. Salvar briefing
        brief_file = proj_dir / "brief" / "brief.txt"
        brief_file.write_text(briefing, encoding="utf-8")
        result["logs"].append("Briefing salvo.")
        
        # 5. Gerar roteiro
        script = generate_script(briefing, project_id, mode)
        save_script(project_id, script)
        result["script"] = script
        result["logs"].append("Roteiro gerado.")
        
        # 6. Dividir em cenas
        scenes = split_script_into_scenes(script, project_id)
        save_scenes(project_id, scenes)
        result["scenes"] = scenes
        result["logs"].append("{} cenas criadas.".format(len(scenes)))
        
        # 7. Gerar prompts
        scenes = build_prompts_for_scenes(scenes, style)
        save_prompts(project_id, scenes)
        result["logs"].append("Prompts gerados.")
        
        # 8. Renderizar cenas (WanGP 1.3B primeiro, FFmpeg fallback)
        gpu = get_gpu_info()
        preset = get_recommended_preset(gpu["vram_gb"], gpu["name"])
        result["logs"].append("Preset: {}".format(preset["model"]))
        
        # Tradutor para prompts PT-BR → EN
        from app.adapters.translator_adapter import TranslatorAdapter
        translator = TranslatorAdapter()
        result["logs"].append("Tradutor inicializado.")
        
        # WanGP adapter
        from app.adapters.wangp_adapter import WanGPAdapter
        wangp = WanGPAdapter()
        
        rendered_videos = []
        for scene in scenes:
            # Traduzir prompt para EN (WanGP espera EN)
            prompt_en = translator.traduzir(scene.get("prompt_positive", ""))
            scene["prompt_positive_en"] = prompt_en
            
            # Tentar WanGP 1.3B primeiro
            if wangp.available:
                result["logs"].append("Renderizando {} via WanGP 1.3B...".format(scene.get("id")))
                video = wangp.gerar_cena(
                    prompt=prompt_en,
                    duracao_seg=scene.get("duration_estimate", 5),
                    output_path=Path(proj_dir / "renders" / "{}_wgp.mp4".format(scene.get("id"))),
                    progress_callback=None
                )
                if video:
                    rendered_videos.append(str(video))
                    scene["output_path"] = str(video)
                    scene["status"] = "rendered"
                    result["logs"].append("Cena {} renderizada via WanGP.".format(scene.get("id")))
                    continue
            
            # Fallback: FFmpeg storyboard
            result["logs"].append("WanGP indisponível/falhou. Usando FFmpeg...")
            break
        
        # Se WanGP não renderizou tudo, usar FFmpeg para o resto
        if len(rendered_videos) < len(scenes):
            result["logs"].append("Renderizando storyboard FFmpeg para cenas restantes...")
            video_path = create_storyboard_video(project_id, scenes)
            if video_path:
                rendered_videos.append(str(video_path))
                result["video_preview"] = str(video_path)
                result["logs"].append("Storyboard FFmpeg criado: {}".format(video_path.name))
        else:
            # Se WanGP renderizou tudo, compilar vídeo final
            from app.adapters.ffmpeg_adapter import compile_final_video
            final_video = compile_final_video(project_id, rendered_videos)
            if final_video:
                result["video_preview"] = str(final_video)
                result["logs"].append("Vídeo final compilado: {}".format(final_video.name))
        
        result["status"] = "completed"
        result["logs"].append("Pipeline concluido.")
        
    except Exception as e:
        result["status"] = "error"
        result["logs"].append("Erro: {}".format(str(e)))
        logger.error("Auto pipeline falhou: %s", e)
    
    return result
