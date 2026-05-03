import json
import subprocess
from pathlib import Path
from app.logging_config import setup_logger
from app.config import PROJECTS_DIR
from app.hardware import get_gpu_info, get_recommended_preset

logger = setup_logger()

WANGP_DIR = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/engines/Wan2GP")
WANGP_EXE = WANGP_DIR / "wen2gp_gui.py"  # ou .exe se houver um Windows build

def check_wangp() -> bool:
    """Verifica se Wan2GP existe e está acessível."""
    if not WANGP_DIR.exists():
        logger.warning("Wan2GP não encontrado em %s", WANGP_DIR)
        return False
    logger.info("Wan2GP encontrado em %s", WANGP_DIR)
    return True

def generate_scene_video_wangp(project_id: str, scene: dict, preset: dict = None) -> Path or None:
    """
    Gera vídeo para uma cena usando WanGP 1.3B (modo seguro).
    Retorna caminho do vídeo ou None se falhar.
    """
    if not check_wangp():
        logger.error("WanGP não disponível. Usando fallback FFmpeg.")
        return None

    gpu = get_gpu_info()
    if preset is None:
        preset = get_recommended_preset(gpu["vram_gb"], gpu["name"])

    # Validação de segurança
    if "14B" in preset.get("model", "") and preset.get("model") != "1.3B":
        logger.warning("Modelo 14B bloqueado no modo seguro. Use 1.3B para sua GPU.")
        preset["model"] = "1.3B"
        preset["resolution"] = "480p/512p"

    proj_dir = PROJECTS_DIR / project_id
    scene_id = scene.get("id", "scene_001")
    output_dir = proj_dir / "renders"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "{}_wangp.mp4".format(scene_id)

    # Monta comando básico (ajustar conforme interface real do Wan2GP)
    cmd = [
        "K:/AI_VIDEO_COMERCIAL_STUDIO/envs/studio/python.exe",
        str(WANGP_EXE),
        "--prompt", scene.get("prompt_positive", ""),
        "--negative_prompt", scene.get("prompt_negative", ""),
        "--model", preset.get("model", "1.3B"),
        "--resolution", preset.get("resolution", "480p"),
        "--duration", str(scene.get("duration_estimate", 5)),
        "--output", str(output_path)
    ]

    try:
        logger.info("Gerando cena %s com WanGP 1.3B (seguro)", scene_id)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0 and output_path.exists():
            scene["output_path"] = str(output_path)
            scene["status"] = "rendered"
            # Atualiza project.json
            proj_file = proj_dir / "project.json"
            proj = json.loads(proj_file.read_text(encoding="utf-8"))
            proj["scenes"] = [s if s["id"] != scene_id else scene for s in proj.get("scenes", [])]
            proj_file.write_text(json.dumps(proj, indent=2, ensure_ascii=False), encoding="utf-8")
            logger.info("Cena %s renderizada com sucesso: %s", scene_id, output_path.name)
            return output_path
        else:
            logger.error("Falha no WanGP: %s", result.stderr or "Erro desconhecido")
    except Exception as e:
        logger.error("Erro ao executar WanGP: %s", str(e))

    return None

def batch_render_wangp(project_id: str, scenes: list, max_concurrent: int = 1) -> list:
    """
    Renderiza cenas com WanGP, uma por vez (seguro para 6GB VRAM).
    """
    results = []
    preset = get_recommended_preset(get_gpu_info()["vram_gb"], get_gpu_info()["name"])
    if "14B" in preset.get("model", ""):
        preset["model"] = "1.3B"
        preset["resolution"] = "480p/512p"

    for scene in scenes:
        if scene.get("status") in ("rendered", "approved"):
            results.append(scene.get("output_path"))
            continue
        video = generate_scene_video_wangp(project_id, scene, preset)
        results.append(str(video) if video else None)
    return results
