from pathlib import Path
import os

# Default: project root (parent of app/ directory)
_DEFAULT_BASE_DIR = Path(__file__).resolve().parent.parent
# Allow override via environment variable
BASE_DIR = Path(os.environ.get("GALFLOWAI_BASE_DIR", _DEFAULT_BASE_DIR))

# Workspace is the project root itself (where app/ is located)
WORKSPACE_DIR = BASE_DIR
PROJECTS_DIR = BASE_DIR / "projects"
LOGS_DIR = BASE_DIR / "logs"
CACHE_DIR = BASE_DIR / "cache"
MODELS_DIR = BASE_DIR / "models"
ENGINES_DIR = BASE_DIR / "engines"
ASSETS_DIR = BASE_DIR / "assets"
TEMP_DIR = BASE_DIR / "temp"

# LLM Settings
LLM_PROVIDER_MODE = "auto"  # auto, fast, quality, safe
LLM_FAST_TIMEOUT_SECONDS = 5
LLM_QUALITY_TIMEOUT_SECONDS = 15

LMSTUDIO_BASE_URL = "http://localhost:1234/v1"
KOBOLDCPP_BASE_URL = "http://localhost:5001"
LLAMACPP_BASE_URL = "http://localhost:8080/v1"
GPT4ALL_MODEL_DIR = str(MODELS_DIR / "gpt4all")
GGUF_MODEL_DIR = str(MODELS_DIR / "gguf")

GRADIO_HOST = "127.0.0.1"
GRADIO_PORT = 7860

def setup_env_vars():
    import os
    os.environ["PIP_CACHE_DIR"] = str(CACHE_DIR / "pip")
    os.environ["HF_HOME"] = str(CACHE_DIR / "huggingface")
    os.environ["TORCH_HOME"] = str(CACHE_DIR / "torch")
    os.environ["XDG_CACHE_HOME"] = str(CACHE_DIR)
    os.environ["TEMP"] = str(TEMP_DIR)
    os.environ["TMP"] = str(TEMP_DIR)
    os.environ["OLLAMA_MODELS"] = str(MODELS_DIR / "ollama")
