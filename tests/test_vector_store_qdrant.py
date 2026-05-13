"""VEC-810: QdrantStore tests."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, PropertyMock

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.adapters.vector_store_qdrant import QdrantStore
from app.adapters.vector_store import VectorRecord


def _mock_qdrant_client():
    """Patch qdrant-client imports and return mock client."""
    mock_client = MagicMock()
    mock_models = MagicMock()
    mock_models.VectorParams = MagicMock()
    mock_models.Distance = MagicMock()
    mock_models.Distance.COSINE = "Cosine"
    mock_models.PointStruct = MagicMock()
    mock_models.Filter = MagicMock()
    mock_models.FieldCondition = MagicMock()
    mock_models.MatchValue = MagicMock()

    # get_collections default return empty list
    mock_client.get_collections.return_value.collections = []

    return mock_client, mock_models


def test_not_available_without_qdrant_client():
    store = QdrantStore(location=":memory:")
    assert store.is_available() is False


def test_is_available_with_client_set():
    store = QdrantStore(location=":memory:")
    mock_client, mock_models = _mock_qdrant_client()
    store._client = mock_client
    store._qdrant_models = mock_models
    assert store.is_available() is True


def test_upsert_and_search():
    store = QdrantStore(location=":memory:")
    mock_client, mock_models = _mock_qdrant_client()
    store._client = mock_client
    store._qdrant_models = mock_models
    store._collections["galflow_default"] = True

    record = VectorRecord(
        id="test_001",
        vector=[0.1, 0.2, 0.3],
        payload={"type": "product"},
        metadata={"source": "test"},
    )

    store.upsert(record)
    assert mock_client.upsert.called

    mock_client.search.return_value = [
        MagicMock(
            id="test_001",
            vector=[0.1, 0.2, 0.3],
            payload={"payload": {"type": "product"}, "metadata": {"source": "test"}},
            score=0.95,
        )
    ]
    results = store.search(query_vector=[0.1, 0.2, 0.3], top_k=5)
    assert len(results) == 1
    assert results[0].score == 0.95
    assert results[0].record.id == "test_001"
    assert results[0].record.payload["type"] == "product"


def test_search_empty():
    store = QdrantStore(location=":memory:")
    mock_client, mock_models = _mock_qdrant_client()
    store._client = mock_client
    store._qdrant_models = mock_models
    store._collections["galflow_default"] = True
    mock_client.search.return_value = []

    results = store.search(query_vector=[0.1, 0.2, 0.3])
    assert results == []


def test_count():
    store = QdrantStore(location=":memory:")
    mock_client, mock_models = _mock_qdrant_client()
    store._client = mock_client
    store._qdrant_models = mock_models
    store._collections["galflow_default"] = True
    mock_client.count.return_value = MagicMock(count=5)

    assert store.count() == 5


def test_get_existing():
    store = QdrantStore(location=":memory:")
    mock_client, mock_models = _mock_qdrant_client()
    store._client = mock_client
    store._qdrant_models = mock_models
    store._collections["galflow_default"] = True
    mock_client.retrieve.return_value = [
        MagicMock(
            id="test_001",
            vector=[0.1, 0.2, 0.3],
            payload={"payload": {"type": "product"}, "metadata": {"source": "test"}},
        )
    ]

    record = store.get("test_001")
    assert record is not None
    assert record.id == "test_001"
    assert record.payload["type"] == "product"


def test_get_missing():
    store = QdrantStore(location=":memory:")
    mock_client, mock_models = _mock_qdrant_client()
    store._client = mock_client
    store._qdrant_models = mock_models
    store._collections["galflow_default"] = True
    mock_client.retrieve.return_value = []

    assert store.get("nonexistent") is None


def test_delete():
    store = QdrantStore(location=":memory:")
    mock_client, mock_models = _mock_qdrant_client()
    store._client = mock_client
    store._qdrant_models = mock_models
    store._collections["galflow_default"] = True

    result = store.delete("test_001")
    assert result is True
    assert mock_client.delete.called


def test_clear():
    store = QdrantStore(location=":memory:")
    mock_client, mock_models = _mock_qdrant_client()
    store._client = mock_client
    store._qdrant_models = mock_models
    store._collections["galflow_default"] = True

    store.clear()
    assert mock_client.delete_collection.called


def test_list_collections():
    store = QdrantStore(location=":memory:")
    mock_client, mock_models = _mock_qdrant_client()
    store._client = mock_client
    store._qdrant_models = mock_models

    class FakeCollection:
        def __init__(self, name):
            self.name = name

    mock_client.get_collections.return_value = MagicMock(
        collections=[FakeCollection("galflow_proj1"), FakeCollection("galflow_proj2")]
    )

    cols = store.list_collections()
    assert "galflow_proj1" in cols
    assert "galflow_proj2" in cols


def test_multi_tenancy():
    store = QdrantStore(location=":memory:", collection_prefix="proj_")
    mock_client, mock_models = _mock_qdrant_client()
    store._client = mock_client
    store._qdrant_models = mock_models

    col_name = store._collection_name("project_123")
    assert col_name == "proj_project_123"


def test_upsert_generates_id_when_empty():
    store = QdrantStore(location=":memory:")
    mock_client, mock_models = _mock_qdrant_client()
    store._client = mock_client
    store._qdrant_models = mock_models
    store._collections["galflow_default"] = True

    record = VectorRecord(id="", vector=[0.1, 0.2, 0.3])
    point_id = store.upsert(record)
    assert point_id != ""
    assert mock_client.upsert.called


def test_not_available_returns_empty_search():
    store = QdrantStore(location=":memory:")
    results = store.search(query_vector=[0.1, 0.2, 0.3])
    assert results == []


def test_not_available_count_zero():
    store = QdrantStore(location=":memory:")
    assert store.count() == 0
