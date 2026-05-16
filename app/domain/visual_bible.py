"""Visual Bible schema (VIS-501).

Fixa referências visuais aprovadas por ingrediente para reduzir
drift visual entre gerações. Consultada pelo Prompt Compiler
para incluir referências canônicas nos prompts de vídeo.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from app.exceptions import NotFoundError, ValidationError


class BibleEntryStatus(str, Enum):
    """Status de uma entrada na Visual Bible."""
    APPROVED = "approved"
    DRAFT = "draft"
    ARCHIVED = "archived"


class ApprovedReference(BaseModel):
    """Referência visual aprovada na bíblia."""
    file_path: str
    description: str
    angle: Optional[str] = None
    lighting_notes: Optional[str] = None
    is_primary: bool = False


class BibleEntry(BaseModel):
    """Entrada aprovada na Visual Bible para um ingrediente.

    Cada entrada vincula um ingrediente do Registry a referências
    visuais canônicas, aprovadas para uso em geração de vídeo.
    """
    id: str = Field(default_factory=lambda: f"bbl_{uuid4().hex[:12]}")
    ingredient_id: str
    ingredient_name: str
    references: List[ApprovedReference] = Field(default_factory=list)
    status: BibleEntryStatus = BibleEntryStatus.DRAFT
    notes: str = ""
    version: int = 1
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class VisualBible:
    """Catálogo de referências visuais aprovadas.

    Mantém o conjunto canônico de imagens de referência por
    ingrediente. Serve como fonte de verdade visual para o
    Prompt Compiler e motores de renderização.
    """

    def __init__(self):
        self._entries: Dict[str, BibleEntry] = {}

    def add(self, entry: BibleEntry) -> str:
        """Adiciona uma nova entrada à bíblia."""
        if not entry.ingredient_id.strip():
            raise ValidationError("ingredient_id cannot be empty", field="ingredient_id")
        if not entry.ingredient_name.strip():
            raise ValidationError("ingredient_name cannot be empty", field="ingredient_name")
        now = datetime.now(timezone.utc)
        entry.version = 1
        entry.created_at = now
        entry.updated_at = now
        self._entries[entry.id] = entry
        return entry.id

    def get(self, entry_id: str) -> Optional[BibleEntry]:
        """Busca entrada por ID."""
        return self._entries.get(entry_id)

    def get_by_ingredient(self, ingredient_id: str) -> List[BibleEntry]:
        """Busca todas as entradas para um ingrediente."""
        return [
            e for e in self._entries.values()
            if e.ingredient_id == ingredient_id
        ]

    def update(self, entry_id: str, **updates: Any) -> BibleEntry:
        """Atualiza campos de uma entrada.

        Incrementa a versão automaticamente.
        """
        entry = self._entries.get(entry_id)
        if not entry:
            raise NotFoundError(f"Bible entry not found: {entry_id}", entity_type="BibleEntry")

        for key, value in updates.items():
            if hasattr(entry, key) and key not in ("id", "ingredient_id", "created_at", "version"):
                setattr(entry, key, value)

        entry.version += 1
        entry.updated_at = datetime.now(timezone.utc)
        return entry

    def delete(self, entry_id: str) -> bool:
        """Remove uma entrada da bíblia."""
        if entry_id not in self._entries:
            return False
        del self._entries[entry_id]
        return True

    def list(self, status: Optional[BibleEntryStatus] = None) -> List[BibleEntry]:
        """Lista entradas, opcionalmente filtradas por status."""
        if status is None:
            return list(self._entries.values())
        return [e for e in self._entries.values() if e.status == status]

    def search(self, query: str) -> List[BibleEntry]:
        """Busca entradas por nome do ingrediente (case-insensitive)."""
        q = query.lower()
        return [
            e for e in self._entries.values()
            if q in e.ingredient_name.lower() or q in e.notes.lower()
        ]

    def count(self) -> int:
        """Número total de entradas na bíblia."""
        return len(self._entries)

    def count_by_ingredient(self, ingredient_id: str) -> int:
        """Número de entradas para um ingrediente específico."""
        return len(self.get_by_ingredient(ingredient_id))

    def clear(self) -> None:
        """Limpa todas as entradas (útil para testes)."""
        self._entries.clear()
