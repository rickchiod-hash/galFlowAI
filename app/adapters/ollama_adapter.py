"""
Integrao com Ollama para geracão de roteiros realistas.
"""
import subprocess
import json
from pathlib import Path
from app.logging_config import setup_logger
from app.config import ENGINES_DIR

logger = setup_logger()

try:
    _OLLAMA_PATH = str(ENGINES_DIR.parent / "envs" / "studio" / "Library" / "bin" / "ollama.exe")
except Exception:
    _OLLAMA_PATH = "ollama.exe"

def check_ollama_available() -> bool:
    """Verifica se Ollama esta instalado."""
    try:
        result = subprocess.run(
            [_OLLAMA_PATH, "list"],
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except Exception as e:
        logger.warning("Ollama not available: %s", e)
        return False

def generate_with_ollama(briefing: str, model: str = "llama3") -> str:
    """Gera roteiro usando Ollama."""
    prompt = """Crie um roteiro para comercial de 30 segundos baseado neste briefing: %s

Divida em 5 cenas com tempos exatos:
[Cena 1: Nome - Xs]
[Duração exata em segundos]
Descrição da cena

Seja criativo e profissional.""" % briefing
    
    try:
        result = subprocess.run(
            [_OLLAMA_PATH,
             "run", model, prompt],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            logger.error("Ollama error: %s", result.stderr)
            return ""
    except Exception as e:
        logger.error("Ollama falhou: %s", e)
        return ""

def get_available_models() -> list:
    """Lista modelos disponíveis no Ollama."""
    try:
        result = subprocess.run(
            [_OLLAMA_PATH, "list"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")[1:]  # Skip header
            return [line.split()[0] for line in lines if line.strip()]
    except Exception:
        pass
    return []