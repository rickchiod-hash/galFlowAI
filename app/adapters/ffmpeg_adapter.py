import subprocess
from pathlib import Path
from app.logging_config import setup_logger
from app.config import PROJECTS_DIR

logger = setup_logger()

def check_ffmpeg() -> bool:
    try:
        result = subprocess.run(
            ["K:/AI_VIDEO_COMMERCIAL_STUDIO/envs/studio/Library/bin/ffmpeg.exe", "-version"],
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except Exception as e:
        logger.error(f"FFmpeg check failed: {e}")
        return False

def create_storyboard_video(project_id: str, scenes: list) -> Path:
    """
    Cria um vídeo de storyboard estático usando FFmpeg.
    Gera clipes coloridos com texto para cada cena e monta em um MP4 final.
    """
    proj_dir = PROJECTS_DIR / project_id
    storyboard_dir = proj_dir / "storyboard"
    storyboard_dir.mkdir(parents=True, exist_ok=True)
    renders_dir = proj_dir / "renders"
    renders_dir.mkdir(parents=True, exist_ok=True)

    ffmpeg_exe = "K:/AI_VIDEO_COMMERCIAL_STUDIO/envs/studio/Library/bin/ffmpeg.exe"
    scene_clips = []

    for scene in scenes:
        scene_id = scene["id"]
        duration = scene.get("duration_estimate", 5)
        desc_clean = scene.get("description", "Cena")[:30].encode("latin-1", "replace").decode("latin-1")
        clip_path = renders_dir / (scene_id + "_storyboard.mp4")
        filter_complex = (
            "color=c=navy:s=480x512:d=%d,"
            "drawtext=text='%s':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=(h-text_h)/2"
            % (duration, desc_clean)
        )
        cmd = [
            ffmpeg_exe, "-f", "lavfi", "-i", filter_complex,
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-y", str(clip_path)
        ]
        try:
            logger.info("Creating storyboard clip for %s", scene_id)
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode != 0:
                logger.error("FFmpeg error for %s: %s", scene_id, result.stderr)
            elif clip_path.exists():
                scene_clips.append(clip_path)
                scene["output_path"] = str(clip_path)
                scene["status"] = "storyboard_rendered"
                logger.info("Clip created: %s", clip_path)
            else:
                logger.error("Clip file not created for %s", scene_id)
        except Exception as e:
            logger.error("Failed to create clip for %s: %s", scene_id, e)

    if not scene_clips:
        logger.error("No storyboard clips created")
        return None

    # Concatenate clips
    concat_file = storyboard_dir / "concat_list.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for clip in scene_clips:
            f.write(f"file '{clip.as_posix()}'\n")

    output_path = proj_dir / "final" / "preview_storyboard.mp4"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd_concat = [
        ffmpeg_exe, "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-c", "copy", "-y", str(output_path)
    ]
    try:
        logger.info(f"Assembling storyboard video: {output_path}")
        subprocess.run(cmd_concat, capture_output=True, text=True, timeout=120)
        if output_path.exists():
            logger.info(f"Storyboard video created: {output_path}")
            return output_path
    except Exception as e:
        logger.error(f"Failed to assemble storyboard: {e}")
    return None

def assemble_final_video(project_id: str, scenes: list, audio_path: str = None) -> Path:
    """
    Montagem final usando FFmpeg com cenas reais ou storyboard.
    """
    proj_dir = PROJECTS_DIR / project_id
    final_dir = proj_dir / "final"
    final_dir.mkdir(parents=True, exist_ok=True)

    ffmpeg_exe = "K:/AI_VIDEO_COMMERCIAL_STUDIO/envs/studio/Library/bin/ffmpeg.exe"
    # Filter valid rendered clips
    valid_clips = [s for s in scenes if s.get("output_path") and Path(s["output_path"]).exists()]
    if not valid_clips:
        logger.warning("No valid clips found, falling back to storyboard")
        return create_storyboard_video(project_id, scenes)

    concat_file = final_dir / "final_concat.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for scene in valid_clips:
            f.write(f"file '{Path(scene['output_path']).as_posix()}'\n")

    output_path = final_dir / "final_30fps_preview.mp4"
    cmd = [
        ffmpeg_exe, "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-c:v", "libx264", "-preset", "fast", "-r", "30", "-pix_fmt", "yuv420p"
    ]
    if audio_path and Path(audio_path).exists():
        cmd.extend(["-i", audio_path, "-c:a", "aac", "-map", "0:v", "-map", "1:a"])
    else:
        cmd.extend(["-an"])
    cmd.extend(["-y", str(output_path)])

    try:
        logger.info(f"Assembling final video: {output_path}")
        subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if output_path.exists():
            logger.info(f"Final video created: {output_path}")
            return output_path
    except Exception as e:
        logger.error(f"Failed to assemble final video: {e}")
    return None
