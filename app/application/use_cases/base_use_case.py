"""Base use case class following 3-point standard."""
from abc import ABC, abstractmethod
from typing import Dict, Any
from app.logging_config import setup_logger

logger = setup_logger()

class BaseUseCase(ABC):
    """Base class for all use cases.
    
    3-point standard:
    1. Validate input
    2. Execute business logic
    3. Return result with status
    """
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the use case."""
        pass
    
    def _validate(self, **kwargs) -> bool:
        """Validate input parameters."""
        return True
    
    def _build_success(self, data: Any = None, **extra) -> Dict[str, Any]:
        """Build success response."""
        return {"ok": True, "data": data, **extra}
    
    def _build_error(self, error: str, **extra) -> Dict[str, Any]:
        """Build error response."""
        logger.error(error)
        return {"ok": False, "error": error, **extra}
