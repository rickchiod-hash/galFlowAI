"""Contratos de Erro - Exceções customizadas para o Gal AI Studio."""
from typing import Optional, Dict, Any

class GalAIError(Exception):
    """Base exception para o Gal AI."""
    def __init__(self, message: str, code: int = 500, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(message)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": True,
            "message": self.message,
            "code": self.code,
            "details": self.details
        }

class ScriptGenerationError(GalAIError):
    """Erro na geração de roteiro."""
    def __init__(self, message: str, provider: str = "unknown"):
        super().__init__(
            message=message,
            code=400,
            details={"provider": provider, "stage": "script_generation"}
        )

class VideoGenerationError(GalAIError):
    """Erro na geração de vídeo."""
    def __init__(self, message: str, engine: str = "unknown"):
        super().__init__(
            message=message,
            code=500,
            details={"engine": engine, "stage": "video_generation"}
        )

class AdapterError(GalAIError):
    """Erro em adapters (FFmpeg, WanGP, TTS)."""
    def __init__(self, message: str, adapter: str = "unknown"):
        super().__init__(
            message=message,
            code=500,
            details={"adapter": adapter, "stage": "adapter"}
        )

class ProjectError(GalAIError):
    """Erro na criação/gerenciamento de projetos."""
    def __init__(self, message: str, project_id: str = ""):
        super().__init__(
            message=message,
            code=400,
            details={"project_id": project_id, "stage": "project"}
        )

class ConfigError(GalAIError):
    """Erro de configuração (caminhos, variáveis de ambiente)."""
    def __init__(self, message: str, config_key: str = ""):
        super().__init__(
            message=message,
            code=500,
            details={"config_key": config_key, "stage": "config"}
        )

class HardwareError(GalAIError):
    """Erro relacionado a hardware (GPU, VRAM, disco)."""
    def __init__(self, message: str, hardware_type: str = "unknown"):
        super().__init__(
            message=message,
            code=500,
            details={"hardware": hardware_type, "stage": "hardware"}
        )

class FallbackWarning(Warning):
    """Aviso de fallback controlado (não é erro fatal)."""
    def __init__(self, message: str, fallback_type: str = "unknown"):
        self.message = message
        self.fallback_type = fallback_type
        self.is_fallback = True
        super().__init__(message)
