"""Template Provider - Fallback para geração de roteiros quando LLMs falham"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class TemplateProvider:
    """Provider de templates para geração de roteiros (fallback)"""
    
    def __init__(self):
        self.name = "TemplateProvider"
        self.available = True
    
    def generate(self, briefing: str, **kwargs) -> str:
        """
        Gera roteiro básico baseado em template.
        
        Args:
            briefing: Texto do briefing
            **kwargs: Argumentos adicionais (ignorados)
            
        Returns:
            Roteiro gerado via template
        """
        logger.info("Usando TemplateProvider para gerar roteiro")
        
        # Template básico de comercial
        template = """
# Roteiro de Comercial

## Introdução
Apresentação do produto: {product}

## Desenvolvimento
- Demonstração das principais funcionalidades
- Depoimentos de usuários satisfeitos
- Comparação com concorrentes

## Conclusão
Chamada para ação: Adquira já o seu!

---
Gerado via TemplateProvider (fallback)
Briefing original: {briefing}
"""
        
        # Extrai produto do briefing (primeira linha ou palavras-chave)
        product = briefing.split('\n')[0][:50] if briefing else "Nosso Produto"
        
        return template.format(
            product=product,
            briefing=briefing[:100] + "..." if len(briefing) > 100 else briefing
        )
    
    def is_available(self) -> bool:
        """Sempre disponível"""
        return True
    
    def get_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o provider"""
        return {
            "name": self.name,
            "type": "template",
            "available": self.available,
            "offline": True
        }
