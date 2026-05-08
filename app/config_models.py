"""Configuração centralizada de modelos para GalFlowAI"""

from pathlib import Path
from typing import Dict, Any, Optional
import os

# Use BASE_DIR from config for consistency
from app.config import BASE_DIR
MODELS_DIR = BASE_DIR / "models"
ENGINES_DIR = BASE_DIR / "engines"

# ========== LLM Providers ==========
# TemplateProvider é sempre o fallback obrigatório
# Ollama removido da prioridade (conforme solicitado)

LLM_PROVIDERS = {
    "template": {
        "name": "TemplateProvider",
        "available": True,  # Sempre disponível
        "priority": 999,  # Último (fallback)
        "type": "template"
    },
    "lm_studio": {
        "name": "LMStudioProvider",
        "module": "app.adapters.llm.lmstudio_provider",
        "class": "LMStudioProvider",
        "priority": 1,
        "type": "local_llm"
    },
    "koboldcpp": {
        "name": "KoboldCppProvider", 
        "module": "app.adapters.llm.koboldcpp_provider",
        "class": "KoboldCppProvider",
        "priority": 2,
        "type": "local_llm"
    },
    "llamacpp": {
        "name": "LlamaCppProvider",
        "module": "app.adapters.llm.llamacpp_provider", 
        "class": "LlamaCppProvider",
        "priority": 3,
        "type": "local_llm"
    },
    "gpt4all": {
        "name": "GPT4AllProvider",
        "module": "app.adapters.llm.gpt4all_provider",
        "class": "GPT4AllProvider", 
        "priority": 4,
        "type": "local_llm"
    }
}

# ========== Video Models ==========

VIDEO_MODELS = {
    "wangp_1.3B": {
        "name": "WanGP 1.3B",
        "path": str(ENGINES_DIR / "Wan2GP"),
        "model_preset": "1.3B",
        "resolution": "480p",
        "vram_gb": 6,  # Mínimo para GTX 1660 Super
        "priority": 1,
        "type": "wgp",
        "experimental": False
    },
    "wangp_14B": {
        "name": "WanGP 14B",
        "path": str(ENGINES_DIR / "Wan2GP"),
        "model_preset": "14B",
        "resolution": "720p",
        "vram_gb": 12,  # NÃO usar em 6GB VRAM
        "priority": 2,
        "type": "wgp",
        "experimental": False,
        "disabled": True  # Desabilitado para 6GB VRAM
    },
    "framepack_1.3B": {
        "name": "FramePack 1.3B",
        "path": str(ENGINES_DIR / "FramePack"),
        "model_preset": "1.3B",
        "resolution": "480p",
        "vram_gb": 6,
        "priority": 3,
        "type": "framepack",
        "experimental": True
    }
}

# ========== TTS Models ==========

TTS_MODELS = {
    "pyttsx3": {
        "name": "pyttsx3 (Offline)",
        "module": "app.services.tts_service",
        "class": "TTSService",
        "available": False,  # Será verificado em runtime
        "priority": 1,
        "type": "offline_tts",
        "offline": True
    },
    "kokoro": {
        "name": "Kokoro TTS",
        "module": "kokoro",  # Placeholder
        "priority": 2,
        "type": "tts",
        "offline": True
    }
}

# ========== Hardware Constraints ==========

HARDWARE = {
    "gpu": "NVIDIA GTX 1660 Super",
    "vram_gb": 6,
    "ram_gb": 16,
    "cpu": "AMD Ryzen 5 5600"
}

# ========== Safe Defaults ==========

DEFAULTS = {
    "video_model": "wangp_1.3B",  # Seguro para 6GB VRAM
    "video_resolution": "480p",
    "video_duration_max": 60,  # segundos
    "video_scene_duration": 5,  # segundos por cena
    "tts_engine": "pyttsx3",
    "llm_mode": "safe",  # safe, fast, quality
    "fallback_provider": "template"
}

# ========== Functions ==========

def get_available_video_models() -> Dict[str, Any]:
    """Retorna modelos de vídeo disponíveis considerando VRAM"""
    available = {}
    max_vram = HARDWARE["vram_gb"]
    
    for key, config in VIDEO_MODELS.items():
        if config.get("disabled"):
            continue
        if config["vram_gb"] <= max_vram:
            available[key] = config
    
    return available

def get_default_video_model() -> Optional[str]:
    """Retorna model de vídeo padrão para hardware atual"""
    available = get_available_video_models()
    if not available:
        return None
    
    # Retorna o de maior prioridade (menor número)
    return min(available.items(), key=lambda x: x[1]["priority"])[0]

def validate_model_config() -> Dict[str, Any]:
    """Valida configurações de modelos"""
    results = {
        "valid": True,
        "warnings": [],
        "errors": []
    }
    
    # Verifica WanGP
    wangp_path = Path(ENGINES_DIR / "Wan2GP")
    if not wangp_path.exists():
        results["warnings"].append(f"WanGP não encontrado em {wangp_path}")
    
    # Verifica FramePack
    framepack_path = Path(ENGINES_DIR / "FramePack")
    if not framepack_path.exists():
        results["warnings"].append(f"FramePack não encontrado em {framepack_path}")
    
    return results
