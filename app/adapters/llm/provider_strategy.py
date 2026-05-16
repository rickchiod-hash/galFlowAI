"""
Strategy pattern for LLM providers.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List

from app.exceptions import ConfigError


class LLMStrategy(ABC):
    """Base strategy for LLM generation."""
    
    @abstractmethod
    def generate(self, briefing: str, timeout: int = 10) -> str:
        """Generate content from briefing."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if strategy is available."""
        pass
    
    @abstractmethod
    def validate_response(self, response: str) -> bool:
        """Validate generated response."""
        pass


class TemplateStrategy(LLMStrategy):
    """Template fallback strategy."""
    
    def __init__(self):
        from app.adapters.llm.base_provider import TemplateProvider
        self.provider = TemplateProvider()
    
    def generate(self, briefing: str, timeout: int = 10) -> str:
        return self.provider.generate(briefing, timeout)
    
    def is_available(self) -> bool:
        return True
    
    def validate_response(self, response: str) -> bool:
        return bool(response and len(response.strip()) > 10)


class ProviderStrategyFactory:
    """Factory for creating LLM strategies."""
    
    _strategies = {}
    
    @classmethod
    def register(cls, name: str, strategy_class):
        """Register a strategy class."""
        cls._strategies[name] = strategy_class
    
    @classmethod
    def create(cls, name: str, **kwargs) -> LLMStrategy:
        """Create strategy instance."""
        if name not in cls._strategies:
            raise ConfigError(f"Unknown strategy: {name}", param="strategy_name")
        return cls._strategies[name](**kwargs)
    
    @classmethod
    def get_available_strategies(cls) -> List[str]:
        """Get list of available strategy names."""
        return list(cls._strategies.keys())


# Register default strategies
ProviderStrategyFactory.register("template", TemplateStrategy)
