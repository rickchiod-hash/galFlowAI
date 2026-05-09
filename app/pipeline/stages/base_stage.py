"""Base class for pipeline stages"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class BaseStage(ABC):
    """Base class for all pipeline stages"""
    
    def __init__(self):
        self.name = self.__class__.__name__
    
    @abstractmethod
    def execute(self, input_data: Any, **kwargs) -> Dict[str, Any]:
        """
        Execute the stage
        
        Args:
            input_data: Input data for the stage
            **kwargs: Additional parameters
            
        Returns:
            Dict with execution results
        """
        pass
    
    def _create_result(self, success: bool, data: Any = None, error: str = None) -> Dict[str, Any]:
        """Create standardized result dict"""
        result = {"success": success}
        if data is not None:
            result["data"] = data
        if error is not None:
            result["error"] = error
        return result