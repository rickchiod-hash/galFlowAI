"""VectorStoreAdapter (VEC-800).

Adapter pattern para storage vetorial opcional.
Interface abstrata + implementacao in-memory sem runtime externo.

O pipeline funciona sem vector store — a ativacao e via configuracao.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from uuid import uuid4

logger = logging.getLogger(__name__)


@dataclass
class VectorRecord:
    """Registro unico no vector store."""
    id: str
    vector: List[float]
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchResult:
    """Resultado de busca com score de similaridade."""
    record: VectorRecord
    score: float


class VectorStoreAdapter(ABC):
    """Interface abstrata para vector store.

    Implementacoes concretas (Chroma, Qdrant, InMemory)
    devem herdar desta classe.
    """

    @abstractmethod
    def is_available(self) -> bool:
        """Retorna se o backend esta disponivel."""
        ...

    @abstractmethod
    def upsert(self, record: VectorRecord) -> str:
        """Insere ou atualiza um registro."""
        ...

    @abstractmethod
    def get(self, record_id: str) -> Optional[VectorRecord]:
        """Busca registro por ID."""
        ...

    @abstractmethod
    def delete(self, record_id: str) -> bool:
        """Remove um registro."""
        ...

    @abstractmethod
    def search(
        self,
        query_vector: List[float],
        top_k: int = 10,
    ) -> List[SearchResult]:
        """Busca por similaridade vetorial."""
        ...

    @abstractmethod
    def count(self) -> int:
        """Numero total de registros."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Remove todos os registros."""
        ...


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calcula similaridade cosseno entre dois vetores."""
    if len(a) != len(b):
        raise ValueError("Vetores devem ter mesma dimensao")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class InMemoryVectorStore(VectorStoreAdapter):
    """Implementacao in-memory sem runtime externo.

    Util para testes e desenvolvimento local.
    Nao persiste dados entre sessoes.
    """

    def __init__(self):
        self._records: Dict[str, VectorRecord] = {}

    def is_available(self) -> bool:
        return True

    def upsert(self, record: VectorRecord) -> str:
        if not record.id.strip():
            record.id = f"vec_{uuid4().hex[:12]}"
        self._records[record.id] = record
        return record.id

    def get(self, record_id: str) -> Optional[VectorRecord]:
        return self._records.get(record_id)

    def delete(self, record_id: str) -> bool:
        if record_id not in self._records:
            return False
        del self._records[record_id]
        return True

    def search(
        self,
        query_vector: List[float],
        top_k: int = 10,
    ) -> List[SearchResult]:
        results = []
        for rec in self._records.values():
            if len(rec.vector) != len(query_vector):
                continue
            score = cosine_similarity(query_vector, rec.vector)
            results.append(SearchResult(record=rec, score=score))
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]

    def count(self) -> int:
        return len(self._records)

    def clear(self) -> None:
        self._records.clear()
