"""Domain logic for building scene prompts."""

from app.logging_config import setup_logger

logger = setup_logger()


def build_prompts_for_scenes(scenes, project_id=None):
    """
    Build prompts for each scene.
    Returns list of dicts with: scene_id, prompt, negative_prompt, duration
    """
    prompts = []
    for scene in scenes:
        prompt_text = scene.get("text", "")
        negative_prompt = "blurry, low quality, static, bad anatomy"
        duration = scene.get("duration", 5)

        scene_id = scene.get("id", "unknown")
        prompts.append({
            "id": scene_id,
            "scene_id": scene_id,
            "prompt": prompt_text,
            "negative_prompt": negative_prompt,
            "duration": duration,
            "status": "pending",
            "output_path": ""
        })

    logger.info("Prompts gerados para %d cenas", len(prompts))
    return prompts
