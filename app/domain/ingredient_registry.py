"""Ingredient Registry schema (VIS-500).

Define o catálogo de ingredientes (produtos, personagens, cenários, objetos)
para manter consistência entre cenas e sessões.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from app.exceptions import NotFoundError, ValidationError


class IngredientType(str, Enum):
    """Tipos de ingredientes."""
    PRODUCT = "product"
    CHARACTER = "character"
    SCENARIO = "scenario"
    OBJECT = "object"


class VisualReference(BaseModel):
    """Referência visual associada a um ingrediente."""
    file_path: str
    description: str
    is_canonical: bool = False


class Ingredient(BaseModel):
    """Schema de um ingrediente no registry.

    Produtos, personagens, cenários e objetos de cena que precisam
    de consistência visual entre gerações.
    """
    id: str = Field(default_factory=lambda: f"ing_{uuid4().hex[:12]}")
    name: str
    type: IngredientType
    description: str
    visual_references: List[VisualReference] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    version: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class IngredientRegistry:
    """Catálogo versionado de ingredientes.

    Mantém consistência entre cenas e sessões. Todo ingrediente
    possui versão incremental para rastreabilidade.
    """

    def __init__(self):
        self._ingredients: Dict[str, Ingredient] = {}

    def register(self, ingredient: Ingredient) -> str:
        """Registra um novo ingrediente."""
        if not ingredient.name.strip():
            raise ValidationError("Ingredient name cannot be empty", field="name")
        now = datetime.now(timezone.utc)
        ingredient.version = 1
        ingredient.created_at = now
        ingredient.updated_at = now
        self._ingredients[ingredient.id] = ingredient
        return ingredient.id

    def get(self, ingredient_id: str) -> Optional[Ingredient]:
        """Busca ingrediente por ID."""
        return self._ingredients.get(ingredient_id)

    def update(self, ingredient_id: str, **updates: Any) -> Ingredient:
        """Atualiza campos de um ingrediente.

        Incrementa a versão automaticamente.
        """
        ingredient = self._ingredients.get(ingredient_id)
        if not ingredient:
            raise NotFoundError(f"Ingredient not found: {ingredient_id}", entity_type="Ingredient")

        for key, value in updates.items():
            if hasattr(ingredient, key) and key not in ("id", "created_at", "version"):
                setattr(ingredient, key, value)

        ingredient.version += 1
        ingredient.updated_at = datetime.now(timezone.utc)
        return ingredient

    def delete(self, ingredient_id: str) -> bool:
        """Remove um ingrediente do registry."""
        if ingredient_id not in self._ingredients:
            return False
        del self._ingredients[ingredient_id]
        return True

    def list(self, ingredient_type: Optional[IngredientType] = None) -> List[Ingredient]:
        """Lista ingredientes, opcionalmente filtrados por tipo."""
        if ingredient_type is None:
            return list(self._ingredients.values())
        return [
            ing for ing in self._ingredients.values()
            if ing.type == ingredient_type
        ]

    def search(self, query: str) -> List[Ingredient]:
        """Busca ingredientes por nome ou descrição (case-insensitive)."""
        q = query.lower()
        return [
            ing for ing in self._ingredients.values()
            if q in ing.name.lower() or q in ing.description.lower()
        ]

    def count(self) -> int:
        """Número total de ingredientes registrados."""
        return len(self._ingredients)

    def clear(self) -> None:
        """Limpa todos os ingredientes (útil para testes)."""
        self._ingredients.clear()