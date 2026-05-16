"""VEC-811: ChromaStore tests."""

import sys
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.adapters.vector_store_chroma import ChromaStore
from app.adapters.vector_store import VectorRecord
from app.exceptions import ProviderError


def _mock_chroma_client():
    """Patch chromadb imports and return mock client."""
    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_collection.name = "galflow_default"
    mock_client.get_or_create_collection.return_value = mock_collection
    mock_client.get_collection.side_effect = Exception("not found")
    mock_client.create_collection.return_value = mock_collection
    # list_collections returns list of mock collection objects
    mock_client.list_collections.return_value = [mock_collection]
    return mock_client, mock_collection


def test_not_available_without_chromadb():
    store = ChromaStore()
    assert store.is_available() is False


def test_is_available_with_client_set():
    store = ChromaStore()
    mock_client, _ = _mock_chroma_client()
    store._client = mock_client
    assert store.is_available() is True


def test_upsert_and_search():
    store = ChromaStore()
    mock_client, mock_collection = _mock_chroma_client()
    store._client = mock_client
    store._collections["galflow_default"] = mock_collection

    record = VectorRecord(
        id="test_001",
        vector=[0.1, 0.2, 0.3],
        payload={"type": "product"},
        metadata={"source": "test"},
    )

    store.upsert(record)
    assert mock_collection.upsert.called

    mock_collection.query.return_value = {
        "ids": [["test_001"]],
        "distances": [[0.05]],
        "metadatas": [[{
            "_payload_json": json.dumps({"type": "product"}),
            "_metadata_json": json.dumps({"source": "test"}),
        }]],
        "embeddings": [[[0.1, 0.2, 0.3]]],
    }
    results = store.search(query_vector=[0.1, 0.2, 0.3], top_k=5)
    assert len(results) == 1
    assert results[0].score > 0.9
    assert results[0].record.id == "test_001"
    assert results[0].record.payload["type"] == "product"
    assert results[0].record.metadata["source"] == "test"


def test_search_empty():
    store = ChromaStore()
    mock_client, mock_collection = _mock_chroma_client()
    store._client = mock_client
    store._collections["galflow_default"] = mock_collection
    mock_collection.query.return_value = {"ids": [[]], "distances": [[]], "metadatas": [[]]}

    results = store.search(query_vector=[0.1, 0.2, 0.3])
    assert results == []


def test_count():
    store = ChromaStore()
    mock_client, mock_collection = _mock_chroma_client()
    store._client = mock_client
    store._collections["galflow_default"] = mock_collection
    mock_collection.count.return_value = 5

    assert store.count() == 5


def test_get_existing():
    store = ChromaStore()
    mock_client, mock_collection = _mock_chroma_client()
    store._client = mock_client
    store._collections["galflow_default"] = mock_collection
    mock_collection.get.return_value = {
        "ids": ["test_001"],
        "embeddings": [[0.1, 0.2, 0.3]],
        "metadatas": [{
            "_payload_json": json.dumps({"type": "product"}),
            "_metadata_json": json.dumps({"source": "test"}),
        }],
    }

    record = store.get("test_001")
    assert record is not None
    assert record.id == "test_001"
    assert record.payload["type"] == "product"


def test_get_missing():
    store = ChromaStore()
    mock_client, mock_collection = _mock_chroma_client()
    store._client = mock_client
    store._collections["galflow_default"] = mock_collection
    mock_collection.get.return_value = {"ids": [], "embeddings": [], "metadatas": []}

    assert store.get("nonexistent") is None


def test_delete():
    store = ChromaStore()
    mock_client, mock_collection = _mock_chroma_client()
    store._client = mock_client
    store._collections["galflow_default"] = mock_collection

    result = store.delete("test_001")
    assert result is True
    assert mock_collection.delete.called


def test_clear():
    store = ChromaStore()
    mock_client, _ = _mock_chroma_client()
    store._client = mock_client
    store._collections["galflow_default"] = True

    store.clear()
    assert mock_client.delete_collection.called


def test_list_collections():
    store = ChromaStore()
    mock_client, mock_collection = _mock_chroma_client()
    store._client = mock_client

    class FakeCollection:
        def __init__(self, name):
            self.name = name

    mock_client.list_collections.return_value = [
        FakeCollection("galflow_proj1"),
        FakeCollection("galflow_proj2"),
    ]

    cols = store.list_collections()
    assert "galflow_proj1" in cols
    assert "galflow_proj2" in cols


def test_multi_tenancy():
    store = ChromaStore(collection_prefix="proj_")
    name = store._collection_name("project_123")
    assert name == "proj_project_123"


def test_upsert_generates_id_when_empty():
    store = ChromaStore()
    mock_client, mock_collection = _mock_chroma_client()
    store._client = mock_client
    store._collections["galflow_default"] = mock_collection

    record = VectorRecord(id="", vector=[0.1, 0.2, 0.3])
    point_id = store.upsert(record)
    assert point_id != ""
    assert mock_collection.upsert.called


def test_not_available_returns_empty_search():
    store = ChromaStore()
    results = store.search(query_vector=[0.1, 0.2, 0.3])
    assert results == []


def test_not_available_count_zero():
    store = ChromaStore()
    assert store.count() == 0


def test_persistent_path():
    store = ChromaStore(path="/tmp/chroma_test")
    assert store._path == "/tmp/chroma_test"

    mock_client, mock_collection = _mock_chroma_client()
    store._client = mock_client
    assert store.is_available() is True


def test_not_available_upsert_raises():
    store = ChromaStore()
    record = VectorRecord(id="x", vector=[0.1])
    try:
        store.upsert(record)
        assert False, "Deveria levantar ProviderError"
    except ProviderError as e:
        assert "Chroma nao disponivel" in str(e)
