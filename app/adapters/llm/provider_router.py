"""
Provider Router - manages LLM providers with fallback.
Uses Strategy + Factory pattern for provider management.
"""
import time
from typing import List, Optional, Dict
from app.adapters.llm.base_provider import BaseLLMProvider, TemplateProvider
from app.adapters.llm.provider_strategy import ProviderStrategyFactory, LLMStrategy


class ProviderRouter:
    """Routes requests through available LLM providers with fallback.
    
    Uses Strategy pattern for generation and Factory pattern for creation.
    """
    
    def __init__(self, mode: str = "safe"):
        self.mode = mode
        self.strategies: List[LLMStrategy] = []
        self._init_strategies()
    
    def _init_strategies(self):
        """Initialize all strategies using Factory pattern."""
        # Always add template as fallback
        self.strategies = [ProviderStrategyFactory.create("template")]
        
        # Try to add optional providers using Factory
        provider_configs = [
            ("lmstudio", "LMStudioProvider", "app.adapters.llm.lmstudio_provider"),
            ("koboldcpp", "KoboldCppProvider", "app.adapters.llm.koboldcpp_provider"),
            ("llamacpp", "LlamaCppProvider", "app.adapters.llm.llamacpp_provider"),
            ("gpt4all", "GPT4AllProvider", "app.adapters.llm.gpt4all_provider"),
        ]
        
        for name, class_name, module in provider_configs:
            try:
                # Dynamically import and register strategy
                exec(f"from {module} import {class_name}")
                # For now, use base provider directly; strategy wraps it
                strategy_class = type(f"{name}Strategy", (LLMStrategy,), {
                    'provider': locals().get(class_name)(),
                    'generate': lambda self, briefing, timeout: self.provider.generate(briefing, timeout),
                    'is_available': lambda self: self.provider.is_available(),
                    'validate_response': lambda self, response: self.provider.validate_response(response)
                })
                ProviderStrategyFactory.register(name, strategy_class)
                self.strategies.insert(0, ProviderStrategyFactory.create(name))
            except (ImportError, Exception):
                pass
    
    def detect_available(self) -> Dict[str, bool]:
        """Detect which providers are available."""
        result = {"template": True}
        
        for strategy in self.strategies:
            if hasattr(strategy, 'provider') and strategy.provider.name != "TemplateProvider":
                result[strategy.provider.name] = strategy.is_available()
        
        return result
    
    def generate_script_fast(self, briefing: str, timeout: int = 5) -> dict:
        """Fast mode: first valid response wins."""
        start = time.time()
        
        for strategy in self.strategies:
            if not strategy.is_available() and not isinstance(strategy, type(ProviderStrategyFactory.create("template"))):
                continue
            
            try:
                result = strategy.generate(briefing, timeout)
                if result and strategy.validate_response(result):
                    return {
                        "script": result,
                        "provider": strategy.provider.name if hasattr(strategy, 'provider') else "Template",
                        "time": time.time() - start,
                        "quality": "fast"
                    }
            except Exception as e:
                if hasattr(strategy, 'provider'):
                    strategy.provider.last_error = str(e)
                continue
        
        # Ultimate fallback
        template_strategy = self.strategies[-1]  # Template is always last
        template_result = template_strategy.generate(briefing, timeout=2)
        
        return {
            "script": template_result,
            "provider": "TemplateProvider",
            "time": time.time() - start,
            "quality": "fallback"
        }
    
    def generate_script_quality(self, briefing: str, timeout: int = 15) -> dict:
        """Quality mode: wait for best response."""
        start = time.time()
        
        results = []
        for strategy in self.strategies:
            if not strategy.is_available() and not isinstance(strategy, type(ProviderStrategyFactory.create("template"))):
                continue
            
            try:
                result = strategy.generate(briefing, timeout)
                if result:
                    provider_name = strategy.provider.name if hasattr(strategy, 'provider') else "Template"
                    results.append({
                        "script": result,
                        "provider": provider_name,
                        "time": timeout,  # Approximate
                        "valid": strategy.validate_response(result)
                    })
            except Exception:
                continue
        
        if results:
            # Return first valid result, or best available
            for r in results:
                if r["valid"]:
                    return {
                        "script": r["script"],
                        "provider": r["provider"],
                        "time": time.time() - start,
                        "quality": "quality"
                    }
            # If none valid, return first
            return {
                "script": results[0]["script"],
                "provider": results[0]["provider"],
                "time": time.time() - start,
                "quality": "low"
            }
        
        # Fallback
        template_strategy = self.strategies[-1]
        return {
            "script": template_strategy.generate(briefing, timeout=2),
            "provider": "TemplateProvider",
            "time": time.time() - start,
            "quality": "fallback"
        }
    
    def generate_script_safe(self, briefing: str) -> dict:
        """Safe mode: try providers sequentially."""
        start = time.time()
        
        for strategy in self.strategies:
            if not strategy.is_available() and not isinstance(strategy, type(ProviderStrategyFactory.create("template"))):
                continue
            
            try:
                # Use sync version for safe mode
                if hasattr(strategy, 'provider'):
                    result = strategy.provider.generate(briefing, timeout=10)
                else:
                    result = strategy.generate(briefing, timeout=10)
                
                if result and strategy.validate_response(result):
                    provider_name = strategy.provider.name if hasattr(strategy, 'provider') else "Template"
                    return {
                        "script": result,
                        "provider": provider_name,
                        "time": time.time() - start,
                        "quality": "safe"
                    }
            except Exception as e:
                if hasattr(strategy, 'provider'):
                    strategy.provider.last_error = str(e)
                continue
        
        # Fallback
        template_strategy = self.strategies[-1]
        return {
            "script": template_strategy.generate(briefing, timeout=2),
            "provider": "TemplateProvider",
            "time": time.time() - start,
            "quality": "fallback"
        }
