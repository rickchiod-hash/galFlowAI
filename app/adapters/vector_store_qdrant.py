"""QdrantStore (VEC-810).

Implementacao real do VectorStoreAdapter usando Qdrant.
Opcional — pipeline funciona sem ele.
Suporta modo embedded (:memory: ou local path) sem Docker.

Uso:
    store = QdrantStore(location=":memory:", embedding_dim=384)
    store.is_available()  # True se qdrant-client instalado
    store.upsert(record)
    results = store.search(query_vector, top_k=5)
"""

import logging
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.adapters.vector_store import VectorStoreAdapter, VectorRecord, SearchResult

logger = logging.getLogger(__name__)


class QdrantStore(VectorStoreAdapter):
    """Implementacao do VectorStoreAdapter usando Qdrant embedded.

    Suporta:
    - Modo :memory: (sem persistencia, ideal para testes)
    - Modo local path (persistencia em disco)
    - Multi-tenancy via collection por project_id
    """

    def __init__(
        self,
        location: str = ":memory:",
        embedding_dim: int = 384,
        collection_prefix: str = "galflow_",
        host: Optional[str] = None,
        port: Optional[int] = None,
        prefer_grpc: bool = False,
    ):
        self._location = location
        self._embedding_dim = embedding_dim
        self._collection_prefix = collection_prefix
        self._host = host
        self._port = port
        self._prefer_grpc = prefer_grpc
        self._client = None
        self._collections: Dict[str, bool] = {}

    def _lazy_init(self) -> bool:
        if self._client is not None:
            return True
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.http import models

            self._qdrant_models = models

            if self._host and self._port:
                self._client = QdrantClient(
                    host=self._host,
                    port=self._port,
                    prefer_grpc=self._prefer_grpc,
                )
            else:
                self._client = QdrantClient(location=self._location)
            return True
        except ImportError:
            logger.warning(
                "qdrant-client nao instalado. "
                "Instale com: pip install qdrant-client"
            )
            return False
        except Exception as e:
            logger.error("Falha ao conectar no Qdrant: %s", e)
            return False

    def _collection_name(self, project_id: str = "") -> str:
        return "%s%s" % (self._collection_prefix, project_id if project_id else "default")

    def _ensure_collection(self, project_id: str = "") -> bool:
        if not self._lazy_init():
            return False
        name = self._collection_name(project_id)
        if self._collections.get(name):
            return True
        try:
            existing = self._client.get_collections()
            existing_names = [c.name for c in existing.collections]
            if name not in existing_names:
                self._client.create_collection(
                    collection_name=name,
                    vectors_config=self._qdrant_models.VectorParams(
                        size=self._embedding_dim,
                        distance=self._qdrant_models.Distance.COSINE,
                    ),
                )
            self._collections[name] = True
            return True
        except Exception as e:
            logger.error("Falha ao criar colecao %s: %s", name, e)
            return False

    def is_available(self) -> bool:
        return self._lazy_init()

    def upsert(self, record: VectorRecord, project_id: str = "") -> str:
        if not self._ensure_collection(project_id):
            raise RuntimeError("Qdrant nao disponivel")
        point_id = record.id if record.id.strip() else str(uuid4())
        payload = {
            "payload": record.payload,
            "metadata": record.metadata,
        }
        self._client.upsert(
            collection_name=self._collection_name(project_id),
            points=[
                self._qdrant_models.PointStruct(
                    id=point_id,
                    vector=record.vector,
                    payload=payload,
                )
            ],
        )
        return point_id

    def get(self, record_id: str, project_id: str = "") -> Optional[VectorRecord]:
        if not self._ensure_collection(project_id):
            return None
        try:
            points = self._client.retrieve(
                collection_name=self._collection_name(project_id),
                ids=[record_id],
            )
            if not points:
                return None
            p = points[0]
            return VectorRecord(
                id=str(p.id),
                vector=list(p.vector) if hasattr(p, "vector") else [],
                payload=p.payload.get("payload", {}),
                metadata=p.payload.get("metadata", {}),
            )
        except Exception:
            return None

    def delete(self, record_id: str, project_id: str = "") -> bool:
        if not self._ensure_collection(project_id):
            return False
        try:
            self._client.delete(
                collection_name=self._collection_name(project_id),
                points_selector=self._qdrant_models.Filter(
                    must=[
                        self._qdrant_models.FieldCondition(
                            key="id",
                            match=self._qdrant_models.MatchValue(value=record_id),
                        )
                    ]
                ),
            )
            return True
        except Exception:
            return False

    def search(
        self,
        query_vector: List[float],
        top_k: int = 10,
        project_id: str = "",
    ) -> List[SearchResult]:
        if not self._ensure_collection(project_id):
            return []
        try:
            results = self._client.search(
                collection_name=self._collection_name(project_id),
                query_vector=query_vector,
                limit=top_k,
            )
            return [
                SearchResult(
                    record=VectorRecord(
                        id=str(r.id),
                        vector=list(r.vector) if hasattr(r, "vector") else [],
                        payload=r.payload.get("payload", {}),
                        metadata=r.payload.get("metadata", {}),
                    ),
                    score=r.score,
                )
                for r in results
            ]
        except Exception as e:
            logger.error("Erro ao buscar no Qdrant: %s", e)
            return []

    def count(self, project_id: str = "") -> int:
        if not self._ensure_collection(project_id):
            return 0
        try:
            result = self._client.count(
                collection_name=self._collection_name(project_id),
            )
            return result.count
        except Exception:
            return 0

    def clear(self, project_id: str = "") -> None:
        if not self._ensure_collection(project_id):
            return
        try:
            self._client.delete_collection(
                collection_name=self._collection_name(project_id)
            )
            self._collections.pop(self._collection_name(project_id), None)
            self._ensure_collection(project_id)
        except Exception as e:
            logger.error("Erro ao limpar colecao: %s", e)

    def list_collections(self) -> List[str]:
        if not self._lazy_init():
            return []
        try:
            result = self._client.get_collections()
            return [c.name for c in result.collections]
        except Exception:
            return []
