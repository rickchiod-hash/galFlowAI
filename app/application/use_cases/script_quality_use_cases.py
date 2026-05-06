"""Use cases for Script Quality (V2.4 / H15)."""
from typing import Dict, Any, List, Optional
from app.application.use_cases.base import UseCase
from pathlib import Path
import json


# Templates por tipo de comercial
SCRIPT_TEMPLATES = {
    "produto": {
        "name": "Comercial de Produto",
        "structure": ["hook", "apresentacao", "beneficios", "chamada"],
        "hooks": ["Você sabia?", "Imagine ter...", "O que se fosse possível..."],
        "min_words": 50,
        "max_words": 200
    },
    "servico": {
        "name": "Comercial de Serviço",
        "structure": ["problema", "solucao", "beneficios", "prova_social", "chamada"],
        "hooks": ["Cansado de...?", "E se você pudesse...", "A solução chegou..."],
        "min_words": 80,
        "max_words": 300
    },
    "marca": {
        "name": "Comercial de Marca",
        "structure": ["contexto", "valores", "diferencial", "emocao", "chamada"],
        "hooks": ["Mais que uma marca...", "Conheça a história...", "Nossa missão é..."],
        "min_words": 100,
        "max_words": 400
    }
}


class ScoreScriptUseCase(UseCase):
    """Score a script based on quality criteria.
    
    3-point standard:
    1. Validate script text and project_id
    2. Calculate quality score
    3. Return score dict
    """
    
    def __init__(self):
        super().__init__()
    
    def execute(self, script: str, project_id: str = "") -> Dict[str, Any]:
        """Execute script scoring."""
        try:
            if not self._validate(script=script, project_id=project_id):
                return self._build_error("Invalid script or project_id")
            
            # Calculate score
            score_data = self._calculate_score(script)
            
            return self._build_success(data=score_data)
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        script = kwargs.get("script", "")
        project_id = kwargs.get("project_id", "")
        return bool(script) and isinstance(script, str)
    
    def _calculate_score(self, script: str) -> Dict[str, Any]:
        """Calculate script quality score."""
        words = script.split()
        word_count = len(words)
        
        # Base score
        score = 50  # Base score
        
        # Word count score (0-30 points)
        if 50 <= word_count <= 200:
            score += 30
        elif word_count > 200:
            score += 20
        elif word_count < 20:
            score += 5
        
        # Structure score (0-20 points)
        has_hook = any(word in script.lower() for word in ["você", "imagine", "se", "já"])
        has_call_to_action = any(word in script.lower() for word in ["clique", "acesse", "compre", "ligue"])
        
        if has_hook:
            score += 10
        if has_call_to_action:
            score += 10
        
        # Language score (0-10 points)
        if "?" in script or "!" in script:
            score += 5
        
        # Cap at 100
        score = min(score, 100)
        
        return {
            "score": score,
            "word_count": word_count,
            "has_hook": has_hook,
            "has_call_to_action": has_call_to_action,
            "quality": "Excelente" if score >= 80 else "Bom" if score >= 60 else "Regular" if score >= 40 else "Fraco",
            "suggestions": self._get_suggestions(score, word_count, has_hook, has_call_to_action)
        }
    
    def _get_suggestions(self, score: int, word_count: int, has_hook: bool, has_cta: bool) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []
        
        if word_count < 50:
            suggestions.append("Aumente o texto para pelo menos 50 palavras")
        if not has_hook:
            suggestions.append("Adicione um gancho inicial (hook)")
        if not has_cta:
            suggestions.append("Inclua uma chamada para ação")
        if score < 60:
            suggestions.append("Revise a estrutura: hook + benefícios + chamada")
        
        return suggestions if suggestions else ["Roteiro de boa qualidade!"]


class GetScriptTemplateUseCase(UseCase):
    """Get script template by commercial type.
    
    3-point standard:
    1. Validate commercial type
    2. Get template from registry
    3. Return template dict
    """
    
    def __init__(self):
        super().__init__()
    
    def execute(self, commercial_type: str = "produto") -> Dict[str, Any]:
        """Execute get template."""
        try:
            if not self._validate(commercial_type=commercial_type):
                return self._build_error("Invalid commercial type")
            
            template = SCRIPT_TEMPLATES.get(commercial_type)
            if not template:
                return self._build_error(f"Template not found for type: {commercial_type}")
            
            return self._build_success(data=template)
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        commercial_type = kwargs.get("commercial_type", "")
        return commercial_type in SCRIPT_TEMPLATES


class EnrichBriefingUseCase(UseCase):
    """Enrich briefing with suggestions.
    
    3-point standard:
    1. Validate briefing text
    2. Analyze and suggest improvements
    3. Return enriched briefing
    """
    
    def __init__(self):
        super().__init__()
    
    def execute(self, briefing: str, project_id: str = "") -> Dict[str, Any]:
        """Execute enrich briefing."""
        try:
            if not self._validate(briefing=briefing):
                return self._build_error("Invalid briefing")
            
            suggestions = self._analyze_briefing(briefing)
            
            return self._build_success(data={
                "original": briefing,
                "suggestions": suggestions,
                "enriched": self._apply_suggestions(briefing, suggestions)
            })
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        briefing = kwargs.get("briefing", "")
        return bool(briefing) and isinstance(briefing, str)
    
    def _analyze_briefing(self, briefing: str) -> List[str]:
        """Analyze briefing and return suggestions."""
        suggestions = []
        
        if len(briefing.split()) < 10:
            suggestions.append("Briefing muito curto. Adicione mais detalhes sobre o público-alvo.")
        
        if "produto" not in briefing.lower() and "serviço" not in briefing.lower():
            suggestions.append("Especifique se é produto ou serviço.")
        
        if "público" not in briefing.lower() and "target" not in briefing.lower():
            suggestions.append("Defina o público-alvo claramente.")
        
        return suggestions if suggestions else ["Briefing adequado."]
    
    def _apply_suggestions(self, briefing: str, suggestions: List[str]) -> str:
        """Apply suggestions to briefing (simple concat)."""
        return briefing + "\n\nSugestões de melhoria:\n- " + "\n- ".join(suggestions)
