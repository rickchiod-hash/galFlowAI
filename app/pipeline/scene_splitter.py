import json
import re
from pathlib import Path
from app.logging_config import setup_logger

logger = setup_logger()

def split_script_into_scenes(script_text: str, project_id: str) -> list:
    """Divide o roteiro em cenas baseado em marcadores [Cena X] ou linhas em branco."""
    msg = "Dividindo roteiro em cenas para %s" % project_id
    logger.info(msg)

    pattern = r'\[Cena\s*(\d+):\s*([^]-]+)\s*-\s*(\d+)s\]'
    matches = re.findall(pattern, script_text, re.IGNORECASE)
    
    if matches:
        scenes = []
        for i, (num, desc, duration) in enumerate(matches):
            scene_id = "scene_%s" % num.zfill(3)
            scenes.append({
                "id": scene_id,
                "scene_number": int(num),
                "description": desc.strip() or "Cena %s" % num,
                "duration_estimate": int(duration),
                "status": "pending",
                "prompt_positive": "",
                "prompt_negative": "blurry, low quality, distorted, bad anatomy",
                "output_path": ""
            })
        msg = "Encontradas %d cenas via marcadores" % len(scenes)
        logger.info(msg)
        return scenes

    blocks = [b.strip() for b in script_text.split("\n\n") if b.strip()]
    scenes = []
    for i, block in enumerate(blocks):
        if block.startswith("[") or block.startswith("#"):
            continue
        scene_id = "scene_%s" % str(i+1).zfill(3)
        desc = block[:200] if len(block) > 200 else block
        scenes.append({
            "id": scene_id,
            "scene_number": i + 1,
            "description": desc,
            "duration_estimate": 5,
            "status": "pending",
            "prompt_positive": "",
            "prompt_negative": "blurry, low quality, distorted, bad anatomy",
            "output_path": ""
        })

    msg = "Dividido em %d cenas via fallback" % len(scenes)
    logger.info(msg)
    return scenes

def save_scenes(project_id: str, scenes: list) -> Path:
    from app.config import PROJECTS_DIR
    proj_dir = PROJECTS_DIR / project_id
    scenes_path = proj_dir / "storyboard" / "scenes.json"
    text = json.dumps(scenes, indent=2, ensure_ascii=False)
    scenes_path.write_text(text, encoding="utf-8")
    
    proj_file = proj_dir / "project.json"
    content = proj_file.read_text(encoding="utf-8")
    proj = json.loads(content)
    proj["scenes"] = scenes
    proj["status"] = "scenes_created"
    proj_file.write_text(json.dumps(proj, indent=2, ensure_ascii=False), encoding="utf-8")
    
    msg = "Cenas salvas para %s: %d cenas" % (project_id, len(scenes))
    logger.info(msg)
    return scenes_path
