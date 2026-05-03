import json
from pathlib import Path
from app.logging_config import setup_logger

logger = setup_logger()

def check_tts_engine():
    """Verifica se há engine TTS disponível (pyttsx3, Kokoro, Coqui)."""
    engines = []
    
    # 1. pyttsx3 (built-in Windows)
    try:
        import pyttsx3
        engines.append("pyttsx3")
        logger.info("pyttsx3 disponível")
    except ImportError:
        logger.warning("pyttsx3 não encontrado")
    
    # 2. Kokoro (recomendado após MVP)
    try:
        import kokoro
        engines.append("kokoro")
        logger.info("Kokoro disponível")
    except ImportError:
        logger.info("Kokoro não encontrado (futuro)")
    
    # 3. Coqui TTS
    try:
        import TTS
        engines.append("coqui")
        logger.info("Coqui TTS disponível")
    except ImportError:
        logger.info("Coqui TTS não encontrado (futuro)")
    
    return engines

def generate_speech_pyttsx3(text: str, output_path: Path) -> Path or None:
    """Gera áudio usando pyttsx3 (offline, Windows)."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.save_to_file(text, str(output_path))
        engine.runAndWait()
        if output_path.exists():
            logger.info("Áudio gerado (pyttsx3): %s", output_path.name)
            return output_path
    except Exception as e:
        logger.error("Erro pyttsx3: %s", str(e))
    return None

def generate_speech(text: str, project_id: str, scene_id: str = "narration") -> Path or None:
    """
    Gera narração para o comercial.
    Fallback: pyttsx3 -> texto salvo (sem áudio).
    """
    proj_dir = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta/projects") / project_id
    audio_dir = proj_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    output_path = audio_dir / "{}_narration.wav".format(scene_id)
    
    # Tenta pyttsx3 primeiro
    if "pyttsx3" in check_tts_engine():
        result = generate_speech_pyttsx3(text, output_path)
        if result:
            return result
    
    # Fallback: salva texto para referência
    text_path = audio_dir / "{}_narration.txt".format(scene_id)
    text_path.write_text(text, encoding="utf-8")
    logger.warning("Narração: áudio não gerado. Texto salvo em %s", text_path.name)
    return text_path

def generate_project_narration(project_id: str, script_text: str = None) -> list:
    """Gera narração para todo o roteiro ou cenas."""
    proj_dir = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta/projects") / project_id
    proj_file = proj_dir / "project.json"
    
    if not proj_file.exists():
        logger.error("Projeto %s não encontrado", project_id)
        return []
    
    proj = json.loads(proj_file.read_text(encoding="utf-8"))
    results = []
    
    # Se tem cenas, gera por cena
    if proj.get("scenes"):
        for scene in proj["scenes"]:
            scene_id = scene.get("id", "scene_001")
            narration_text = scene.get("narration", scene.get("description", ""))
            audio = generate_speech(narration_text, project_id, scene_id)
            if audio:
                scene["audio_path"] = str(audio)
                results.append(str(audio))
    # Caso contrário, gera para roteiro inteiro
    elif script_text or proj.get("script"):
        text = script_text or proj.get("script", "")
        audio = generate_speech(text, project_id, "full")
        if audio:
            results.append(str(audio))
    
    # Atualiza project.json
    proj_file.write_text(json.dumps(proj, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Narração concluída: %d arquivos", len(results))
    return results
