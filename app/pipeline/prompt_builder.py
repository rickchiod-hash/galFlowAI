import json
from pathlib import Path
from app.logging_config import setup_logger

logger = setup_logger()

def build_prompts_for_scenes(scenes, project_id=None):
    """
    Build prompts for each scene.
    Returns list of dicts with: scene_id, prompt_pos, prompt_neg, duration
    """
    prompts = []
    for i, scene in enumerate(scenes, 1):
        prompt_pos = scene.get("text", "")
        prompt_neg = "blurry, low quality, static, bad anatomy"
        duration = scene.get("duration", 5)
        
        prompts.append({
            "scene_id": i,
            "prompt_pos": prompt_pos,
            "prompt_neg": prompt_neg,
            "duration": duration,
            "status": "pending",
            "output_path": ""
        })
    
    logger.info("Prompts gerados para %d cenas", len(prompts))
    return prompts

def save_prompts(project_id, prompts):
    """Save prompts to project directory."""
    from app.config import PROJECTS_DIR
    from datetime import datetime
    
    proj_dir = Path(PROJECTS_DIR) / project_id
    prompts_dir = proj_dir / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    
    # Save as JSON
    prompts_file = prompts_dir / "prompts.json"
    prompts_file.write_text(
        json.dumps(prompts, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    
    # Save human-readable version
    readable_file = prompts_dir / "prompts.txt"
    with open(readable_file, "w", encoding="utf-8") as f:
        for p in prompts:
            f.write(f"[Cena {p['scene_id']}]\n")
            f.write(f"Prompt: {p['prompt_pos']}\n")
            f.write(f"Negativo: {p['prompt_neg']}\n")
            f.write(f"Duração: {p['duration']}s\n\n")
    
    logger.info("Prompts salvos em: %s", prompts_file)
    return str(prompts_file)
