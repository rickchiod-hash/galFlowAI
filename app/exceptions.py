"""Contratos de Erro - Exceções customizadas para o GalFlowAI."""
from typing import Optional, Dict, Any

class FlowForgeException(Exception):
    """Base exception para o GalFlowAI."""
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

class ScriptError(FlowForgeException):
    """Erro na geração de roteiro."""
    def __init__(self, message: str, project_id: str = ""):
        super().__init__(
            message=message,
            code=400,
            details={"project_id": project_id, "stage": "script"}
        )

class VideoError(FlowForgeException):
    """Erro na geração de vídeo."""
    def __init__(self, message: str, scene_id: str = ""):
        super().__init__(
            message=message,
            code=500,
            details={"scene_id": scene_id, "stage": "video"}
        )

class ConfigError(FlowForgeException):
    """Erro de configuração."""
    def __init__(self, message: str, param: str = ""):
        super().__init__(
            message=message,
            code=500,
            details={"param": param, "stage": "config"}
        )

class ProviderError(FlowForgeException):
    """Erro em providers LLM."""
    def __init__(self, message: str, provider: str = ""):
        super().__init__(
            message=message,
            code=500,
            details={"provider": provider, "stage": "provider"}
        )

class LLMError(ProviderError):
    """Erro específico de LLM."""
    def __init__(self, message: str, model: str = ""):
        super().__init__(message, provider="llm")
        self.details["model"] = model

class FFmpegError(FlowForgeException):
    """Erro no FFmpeg."""
    def __init__(self, message: str, command: str = ""):
        super().__init__(
            message=message,
            code=500,
            details={"command": command, "stage": "ffmpeg"}
        )

class WanGPError(FlowForgeException):
    """Erro no WanGP."""
    def __init__(self, message: str, model: str = ""):
        super().__init__(
            message=message,
            code=500,
            details={"model": model, "stage": "wangp"}
        )

class ValidationError(FlowForgeException):
    """Erro de validação de domínio (campos obrigatórios, formato inválido)."""
    def __init__(self, message: str, field: str = ""):
        super().__init__(
            message=message,
            code=422,
            details={"field": field, "stage": "validation"}
        )

class NotFoundError(FlowForgeException):
    """Entidade não encontrada (repositório/domínio)."""
    def __init__(self, message: str, entity_type: str = ""):
        super().__init__(
            message=message,
            code=404,
            details={"entity_type": entity_type, "stage": "domain"}
        )

class CacheError(FlowForgeException):
    """Erro no serviço de cache."""
    def __init__(self, message: str, cache_key: str = ""):
        super().__init__(
            message=message,
            code=500,
            details={"cache_key": cache_key, "stage": "cache"}
        )

class VectorStoreError(FlowForgeException):
    """Erro no vector store."""
    def __init__(self, message: str, store_type: str = ""):
        super().__init__(
            message=message,
            code=500,
            details={"store_type": store_type, "stage": "vector_store"}
        )

class FallbackWarning(Warning):
    """Aviso de fallback controlado."""
    def __init__(self, message: str, fallback_type: str = "unknown"):
        self.message = message
        self.fallback_type = fallback_type
        self.is_fallback = True
        super().__init__(message)
