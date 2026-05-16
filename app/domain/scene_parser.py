"""Domain logic for splitting script text into scene dictionaries."""

import re
from app.logging_config import setup_logger

logger = setup_logger()


def split_script_into_scenes(script_text: str, project_id: str) -> list:
    """Divide o roteiro em cenas baseado em marcadores [Cena X] ou linhas em branco."""
    msg = "Dividindo roteiro em cenas para %s" % project_id
    logger.info(msg)

    pattern = r'(?:Cena|Scene)\s*(\d+)[:\s-]*(.*)'
    matches = re.findall(pattern, script_text, re.IGNORECASE)

    if matches:
        scenes = []
        for i, (num, desc) in enumerate(matches):
            scene_id = "scene_%s" % num.zfill(3)
            scenes.append({
                "id": scene_id,
                "scene_number": int(num),
                "description": desc.strip() or "Cena %s" % num,
                "duration_estimate": 5,
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
