"""
Provider Router - manages LLM providers with fallback.
"""
import asyncio
import time
from typing import List, Optional, Dict
from app.adapters.llm.base_provider import BaseLLMProvider, TemplateProvider

# TODO_TECNICO(PROVIDER_ROUTER):
# 1) Aplicar Strategy + Factory para inicialização/configuração de providers.
# 2) Unificar timeout/retry/fallback em funções auxiliares reutilizáveis.
# 3) Criar testes de fallback para indisponibilidade total de providers locais.
# 4) Preservar TemplateProvider como fallback obrigatório.


class ProviderRouter:
    """Routes requests through available LLM providers with fallback."""
    
    def __init__(self, mode: str = "safe"):
        self.mode = mode
        self.providers: List[BaseLLMProvider] = []
        self.template_provider = TemplateProvider()
        self._init_providers()
    
    def _init_providers(self):
        """Initialize all providers."""
        # Always add template as fallback
        self.providers = [self.template_provider]
        
        # Try to add optional providers
        try:
            from app.adapters.llm.lmstudio_provider import LMStudioProvider
            self.providers.insert(0, LMStudioProvider())
        except ImportError:
            pass
        
        try:
            from app.adapters.llm.koboldcpp_provider import KoboldCppProvider
            self.providers.insert(1, KoboldCppProvider())
        except ImportError:
            pass
        
        try:
            from app.adapters.llm.llamacpp_provider import LlamaCppProvider
            self.providers.insert(2, LlamaCppProvider())
        except ImportError:
            pass
        
        try:
            from app.adapters.llm.gpt4all_provider import GPT4AllProvider
            self.providers.insert(3, GPT4AllProvider())
        except ImportError:
            pass
    
    def detect_available(self) -> Dict[str, bool]:
        """Detect which providers are available."""
        result = {"template": True}
        
        for provider in self.providers:
            if provider.name != "TemplateProvider":
                result[provider.name] = provider.is_available()
        
        return result
    
    async def generate_script_fast(self, briefing: str, timeout: int = 5) -> dict:
        """Fast mode: first valid response wins."""
        start = time.time()
        
        # Always have template ready as ultimate fallback
        template_result = None
        
        for provider in self.providers:
            if not provider.available and provider.name != "TemplateProvider":
                continue
            
            try:
                result = provider.generate(briefing, timeout=timeout)
                if result and provider.validate_response(result):
                    return {
                        "script": result,
                        "provider": provider.name,
                        "time": time.time() - start,
                        "quality": "fast"
                    }
            except Exception as e:
                provider.last_error = str(e)
                continue
        
        # Ultimate fallback
        if not template_result:
            template_result = self.template_provider.generate(briefing, timeout=2)
        
        return {
            "script": template_result,
            "provider": "TemplateProvider",
            "time": time.time() - start,
            "quality": "fallback"
        }
    
    async def generate_script_quality(self, briefing: str, timeout: int = 15) -> dict:
        """Quality mode: wait for best response."""
        start = time.time()
        
        results = []
        for provider in self.providers:
            if not provider.available and provider.name != "TemplateProvider":
                continue
            
            try:
                result = provider.generate(briefing, timeout=timeout)
                if result:
                    results.append({
                        "script": result,
                        "provider": provider.name,
                        "time": provider.last_response_time,
                        "valid": provider.validate_response(result)
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
        return {
            "script": self.template_provider.generate(briefing, timeout=2),
            "provider": "TemplateProvider",
            "time": time.time() - start,
            "quality": "fallback"
        }
    
    def generate_script_safe(self, briefing: str) -> dict:
        """Safe mode: try providers sequentially."""
        start = time.time()
        
        for provider in self.providers:
            if not provider.available and provider.name != "TemplateProvider":
                continue
            
            try:
                result = provider.generate(briefing, timeout=10)
                if result and provider.validate_response(result):
                    return {
                        "script": result,
                        "provider": provider.name,
                        "time": provider.last_response_time,
                        "quality": "safe"
                    }
            except Exception as e:
                provider.last_error = str(e)
                continue
        
        return {
            "script": self.template_provider.generate(briefing, timeout=2),
            "provider": "TemplateProvider",
            "time": time.time() - start,
            "quality": "fallback"
        }
