"""Base use case class following 3-point standard."""
from abc import ABC, abstractmethod
from typing import Dict, Any
from app.logging_config import setup_logger
from app.application.result import Result

logger = setup_logger()

class BaseUseCase(ABC):
    """Base class for all use cases.
    
    3-point standard:
    1. Validate input
    2. Execute business logic
    3. Return result with status
    """
    
    @abstractmethod
    def execute(self, **kwargs) -> Result:
        """Execute the use case."""
        pass
    
    def _validate(self, **kwargs) -> bool:
        """Validate input parameters."""
        return True
    
    def _build_success(self, data: Any = None, **extra) -> Result:
        """Build success response."""
        return Result.success(data=data, **extra)
    
    def _build_error(self, error: str, **extra) -> Result:
        """Build error response."""
        logger.error(error)
        return Result.failure(error=error, **extra)
