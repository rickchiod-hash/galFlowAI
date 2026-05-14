"""ChromaStore (VEC-811).

Implementacao real do VectorStoreAdapter usando Chroma.
Opcional — pipeline funciona sem ele.
Suporta modo ephemeral (memoria) e persistent (disco).

Uso:
    store = ChromaStore()
    store.is_available()  # True se chromadb instalado
    store.upsert(record)
    results = store.search(query_vector, top_k=5)
"""

import json
import logging
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.adapters.vector_store import VectorStoreAdapter, VectorRecord, SearchResult

logger = logging.getLogger(__name__)


class ChromaStore(VectorStoreAdapter):
    """Implementacao do VectorStoreAdapter usando Chroma embedded.

    Suporta:
    - Modo ephemeral (sem persistencia, ideal para testes)
    - Modo persistent (disco, via path)
    - Multi-tenancy via collection por project_id
    """

    def __init__(
        self,
        path: Optional[str] = None,
        collection_prefix: str = "galflow_",
    ):
        self._path = path
        self._collection_prefix = collection_prefix
        self._client = None
        self._collections: Dict[str, Any] = {}

    def _lazy_init(self) -> bool:
        if self._client is not None:
            return True
        try:
            import chromadb

            if self._path:
                self._client = chromadb.PersistentClient(path=self._path)
            else:
                self._client = chromadb.EphemeralClient()
            return True
        except ImportError:
            logger.warning(
                "chromadb nao instalado. "
                "Instale com: pip install chromadb"
            )
            return False
        except Exception as e:
            logger.error("Falha ao conectar no Chroma: %s", e)
            return False

    def _collection_name(self, project_id: str = "") -> str:
        return "%s%s" % (self._collection_prefix, project_id if project_id else "default")

    def _ensure_collection(self, project_id: str = "") -> Any:
        if not self._lazy_init():
            return None
        name = self._collection_name(project_id)
        if name in self._collections:
            return self._collections[name]
        try:
            collection = self._client.get_collection(name)
        except Exception:
            collection = self._client.create_collection(name)
        self._collections[name] = collection
        return collection

    def is_available(self) -> bool:
        return self._lazy_init()

    def upsert(self, record: VectorRecord, project_id: str = "") -> str:
        collection = self._ensure_collection(project_id)
        if collection is None:
            raise RuntimeError("Chroma nao disponivel")
        point_id = record.id if record.id.strip() else str(uuid4())
        collection.upsert(
            ids=[point_id],
            embeddings=[record.vector],
            metadatas=[{
                "_payload_json": json.dumps(record.payload),
                "_metadata_json": json.dumps(record.metadata),
            }],
        )
        return point_id

    def get(self, record_id: str, project_id: str = "") -> Optional[VectorRecord]:
        collection = self._ensure_collection(project_id)
        if collection is None:
            return None
        try:
            result = collection.get(ids=[record_id])
            if not result["ids"]:
                return None
            meta = result["metadatas"][0] if result.get("metadatas") else {}
            return VectorRecord(
                id=result["ids"][0],
                vector=list(result["embeddings"][0]) if result.get("embeddings") else [],
                payload=json.loads(meta.get("_payload_json", "{}")),
                metadata=json.loads(meta.get("_metadata_json", "{}")),
            )
        except Exception:
            return None

    def delete(self, record_id: str, project_id: str = "") -> bool:
        collection = self._ensure_collection(project_id)
        if collection is None:
            return False
        try:
            collection.delete(ids=[record_id])
            return True
        except Exception:
            return False

    def search(
        self,
        query_vector: List[float],
        top_k: int = 10,
        project_id: str = "",
    ) -> List[SearchResult]:
        collection = self._ensure_collection(project_id)
        if collection is None:
            return []
        try:
            results = collection.query(
                query_embeddings=[query_vector],
                n_results=top_k,
            )
            if not results["ids"] or not results["ids"][0]:
                return []
            output = []
            for i in range(len(results["ids"][0])):
                meta = results["metadatas"][0][i] if results.get("metadatas") else {}
                distance = results["distances"][0][i] if results.get("distances") else 0.0
                score = 1.0 / (1.0 + distance)
                output.append(
                    SearchResult(
                        record=VectorRecord(
                            id=results["ids"][0][i],
                            vector=[],
                            payload=json.loads(meta.get("_payload_json", "{}")),
                            metadata=json.loads(meta.get("_metadata_json", "{}")),
                        ),
                        score=score,
                    )
                )
            return output
        except Exception as e:
            logger.error("Erro ao buscar no Chroma: %s", e)
            return []

    def count(self, project_id: str = "") -> int:
        collection = self._ensure_collection(project_id)
        if collection is None:
            return 0
        try:
            return collection.count()
        except Exception:
            return 0

    def clear(self, project_id: str = "") -> None:
        name = self._collection_name(project_id)
        try:
            self._client.delete_collection(name)
            self._collections.pop(name, None)
        except Exception:
            pass

    def list_collections(self) -> List[str]:
        if not self._lazy_init():
            return []
        try:
            return [c.name for c in self._client.list_collections()]
        except Exception:
            return []
