"""MemoryQualityGate (VEC-801).

Barreira de qualidade que impede indexacao de
dados de baixa qualidade no vector store.

Deve ser executado antes de qualquer upsert
no VectorStoreAdapter quando a memoria esta ativa.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.domain.ingredient_registry import Ingredient
from app.domain.visual_bible import BibleEntry


@dataclass
class QualityGateResult:
    """Resultado da validacao do quality gate."""
    approved: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class MemoryQualityGate:
    """Valida dados antes de indexacao no vector store.

    Criterios:
    - Completude minima: name, description obrigatorios
    - Presenca de referencia visual (ao menos uma)
    - Schema valido (tipos corretos)
    """

    def validate_ingredient(self, ingredient: Ingredient) -> QualityGateResult:
        """Valida um Ingredient para indexacao."""
        errors: List[str] = []
        warnings: List[str] = []

        if not ingredient.name.strip():
            errors.append("Ingredient name cannot be empty")
        elif len(ingredient.name.strip()) < 2:
            errors.append("Ingredient name too short (min 2 chars)")

        if not ingredient.description.strip():
            errors.append("Ingredient description cannot be empty")
        elif len(ingredient.description.strip()) < 10:
            warnings.append("Ingredient description is short (under 10 chars)")

        if not ingredient.visual_references:
            warnings.append("No visual references — ingredient may be abstract")

        if ingredient.type is None:
            errors.append("Ingredient type is required")

        return QualityGateResult(
            approved=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )

    def validate_bible_entry(self, entry: BibleEntry) -> QualityGateResult:
        """Valida um BibleEntry para indexacao."""
        errors: List[str] = []
        warnings: List[str] = []

        if not entry.ingredient_id.strip():
            errors.append("Bible entry must reference an ingredient_id")
        if not entry.ingredient_name.strip():
            errors.append("Bible entry ingredient name cannot be empty")
        if not entry.references:
            warnings.append("No approved references — entry may lack visual grounding")

        return QualityGateResult(
            approved=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )
