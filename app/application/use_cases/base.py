"""
Base class for use cases (Clean Architecture).
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class UseCase(ABC):
    """Base class for all use cases."""
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """Execute the use case."""
        pass


class UseCaseError(Exception):
    """Base exception for use case errors."""
    def __init__(self, code: str, message: str, details: Optional[Any] = None):
        self.code = code
        self.message = message
        self.details = details
        super().__init__(f"{code}: {message}")
