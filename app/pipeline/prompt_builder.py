import json
from pathlib import Path
from app.logging_config import setup_logger

logger = setup_logger()


def build_prompts_for_scenes(scenes: list, style: str = "cinematic") -> list:
    """Gera prompts positivos e negativos para cada cena."""
    msg = "Construindo prompts para {} cenas".format(len(scenes))
    logger.info(msg)

    for scene in scenes:
        desc = scene.get("description", "")
        positive = "{} style, {}, high quality, detailed, professional commercial".format(style, desc)
        scene["prompt_positive"] = positive
        
        if not scene.get("prompt_negative"):
            scene["prompt_negative"] = "blurry, low quality, distorted, bad anatomy, watermark, text overlay"
        scene["status"] = "prompt_ready"

    return scenes


def save_prompts(project_id: str, scenes: list) -> Path:
    from app.config import PROJECTS_DIR
    proj_dir = PROJECTS_DIR / project_id
    prompts_path = proj_dir / "prompts" / "prompts.json"
    text = json.dumps(scenes, indent=2, ensure_ascii=False)
    prompts_path.write_text(text, encoding="utf-8")
    
    # Also save individual prompt files
    prompts_dir = proj_dir / "prompts"
    for scene in scenes:
        safe_id = scene["id"].replace("/", "_")
        pos_path = prompts_dir / "{}_positive.txt".format(safe_id)
        neg_path = prompts_dir / "{}_negative.txt".format(safe_id)
        pos_path.write_text(scene["prompt_positive"], encoding="utf-8")
        neg_path.write_text(scene["prompt_negative"], encoding="utf-8")
    
    # Update project.json
    proj_file = proj_dir / "project.json"
    content = proj_file.read_text(encoding="utf-8")
    proj = json.loads(content)
    proj["scenes"] = scenes
    proj["status"] = "prompts_ready"
    proj_file.write_text(json.dumps(proj, indent=2, ensure_ascii=False), encoding="utf-8")
    
    logger.info("Prompts salvos para {}".format(project_id))
    return prompts_path
