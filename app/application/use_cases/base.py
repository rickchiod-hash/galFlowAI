"""
Base class for use cases (Clean Architecture).
3-point standard: Validate -> Execute -> Return result.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from app.logging_config import setup_logger

logger = setup_logger()

class UseCase(ABC):
    """Base class for all use cases.
    
    3-point standard:
    1. Validate input
    2. Execute business logic
    3. Return result with status
    """
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """Execute the use case."""
        pass
    
    def _validate(self, **kwargs) -> bool:
        """Validate input parameters. Override in subclasses."""
        return True
    
    def _build_success(self, data: Any = None, **extra) -> Dict[str, Any]:
        """Build success response."""
        return {"ok": True, "data": data, **extra}
    
    def _build_error(self, error: str, **extra) -> Dict[str, Any]:
        """Build error response."""
        logger.error(error)
        return {"ok": False, "error": error, **extra}


class UseCaseError(Exception):
    """Base exception for use case errors."""
    def __init__(self, code: str, message: str, details: Optional[Any] = None):
        self.code = code
        self.message = message
        self.details = details
        super().__init__(f"{code}: {message}")
