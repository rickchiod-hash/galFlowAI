from pathlib import Path

BASE_DIR = Path("K:/AI_VIDEO_COMERCIAL_STUDIO")
WORKSPACE_DIR = BASE_DIR / "opencodegalpasta"
PROJECTS_DIR = WORKSPACE_DIR / "projects"
LOGS_DIR = WORKSPACE_DIR / "logs"
CACHE_DIR = BASE_DIR / "cache"
MODELS_DIR = BASE_DIR / "models"
TEMP_DIR = BASE_DIR / "temp"

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
