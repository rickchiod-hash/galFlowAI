import subprocess
from pathlib import Path
from app.logging_config import setup_logger

logger = setup_logger()

FFMPEG_PATH = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/envs/studio/Library/bin/ffmpeg.exe")

def check_ffmpeg():
    """Verifica se FFmpeg está disponível."""
    if FFMPEG_PATH.exists():
        logger.info("FFmpeg encontrado: %s", FFMPEG_PATH)
        return True
    logger.warning("FFmpeg não encontrado em %s", FFMPEG_PATH)
    return False

def create_storyboard_video(project_id: str, scenes: list) -> Path or None:
    """
    Cria vídeo de storyboard usando FFmpeg.
    Fallback: imagens estáticas + áudio.
    """
    from app.config import PROJECTS_DIR
    proj_dir = PROJECTS_DIR / project_id
    output_dir = proj_dir / "final"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "comercial_storyboard.mp4"
    
    if not check_ffmpeg():
        logger.error("FFmpeg não disponível. Impossível criar vídeo.")
        return None
    
    storyboard_dir = proj_dir / "storyboard"
    storyboard_dir.mkdir(parents=True, exist_ok=True)
    list_file = storyboard_dir / "inputs.txt"
    
    # Criar imagens placeholder se necessário
    valid_scenes = []
    for scene in scenes:
        scene_id = scene.get("id", "unknown")
        img_path = storyboard_dir / "{}_placeholder.png".format(scene_id)
        if not img_path.exists():
            create_placeholder_image(img_path, scene.get("description", "Cena"))
        if img_path.exists():
            valid_scenes.append((img_path, scene.get("duration_estimate", 5)))
    
    if not valid_scenes:
        logger.error("Nenhuma imagem disponível para criar vídeo.")
        return None
    
    # Escrever lista para FFmpeg
    list_content = ""
    for img_path, duration in valid_scenes:
        list_content += "file '{}'\nduration {}\n".format(img_path.resolve(), duration)
    # Repetir último arquivo (requisito FFmpeg)
    if valid_scenes:
        list_content += "file '{}'\n".format(valid_scenes[-1][0].resolve())
    
    list_file.write_text(list_content, encoding="utf-8")
    logger.info("Arquivo de lista criado: %s", list_file)
    
    # Comando FFmpeg
    cmd = [
        str(FFMPEG_PATH), "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-vf", "fps=24,scale=854:480",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        str(output_path)
    ]
    
    try:
        logger.info("Criando vídeo storyboard com FFmpeg...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0 and output_path.exists():
            logger.info("Vídeo criado: %s", output_path.name)
            return output_path
        else:
            logger.error("Erro FFmpeg (código %d): %s", result.returncode, result.stderr[-500:] if result.stderr else "Sem erro")
    except Exception as e:
        logger.error("Erro ao executar FFmpeg: %s", str(e))
    return None

def create_placeholder_image(output_path: Path, text: str):
    """Cria imagem placeholder com texto (requer PIL/Pillow)."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGB", (854, 480), color=(30, 30, 30))
        draw = ImageDraw.Draw(img)
        # Texto centralizado
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        position = ((854 - w) / 2, (480 - h) / 2)
        draw.text(position, text, fill=(255, 255, 255), font=font)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(output_path))
        logger.info("Placeholder criado: %s", output_path.name)
    except ImportError:
        logger.warning("Pillow não instalado. Imagem placeholder não criada.")
    except Exception as e:
        logger.error("Erro ao criar placeholder: %s", str(e))

def compile_final_video(project_id: str, video_paths: list, audio_path: Path = None) -> Path or None:
    """Compila vídeos renderizados em um único MP4 final."""
    from app.config import PROJECTS_DIR
    proj_dir = PROJECTS_DIR / project_id
    output_path = proj_dir / "final" / "comercial_final.mp4"
    
    if not video_paths:
        logger.error("Nenhum vídeo para compilar.")
        return None
    
    if len(video_paths) == 1:
        import shutil
        shutil.copy2(video_paths[0], output_path)
        logger.info("Vídeo único copiado para final: %s", output_path.name)
        return output_path
    
    # Múltiplos vídeos: concatenar
    final_dir = proj_dir / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    list_file = final_dir / "concat_list.txt"
    
    list_content = ""
    for vp in video_paths:
        vp_path = Path(vp)
        if vp_path.exists():
            list_content += "file '{}'\n".format(vp_path.resolve())
    
    list_file.write_text(list_content, encoding="utf-8")
    
    cmd = [
        str(FFMPEG_PATH), "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c", "copy",
        str(output_path)
    ]
    if audio_path and Path(audio_path).exists():
        cmd = [
            str(FFMPEG_PATH), "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(list_file),
            "-i", str(audio_path),
            "-c:v", "copy", "-c:a", "aac",
            "-shortest",
            str(output_path)
        ]
    
    try:
        logger.info("Compilando vídeo final...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0 and output_path.exists():
            logger.info("Vídeo final criado: %s", output_path.name)
            return output_path
        else:
            logger.error("Erro ao compilar vídeo final: %s", result.stderr[-500:] if result.stderr else "Sem erro")
    except Exception as e:
        logger.error("Erro: %s", str(e))
    return None
