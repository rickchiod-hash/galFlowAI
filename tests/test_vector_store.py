# -*- coding: utf-8 -*-
"""Tests for VectorStoreAdapter (VEC-800)."""

import pytest
from typing import List

from app.adapters.vector_store import (
    VectorRecord,
    SearchResult,
    VectorStoreAdapter,
    InMemoryVectorStore,
    cosine_similarity,
)


class TestCosineSimilarity:
    def test_identical_vectors(self):
        assert cosine_similarity([1, 0, 0], [1, 0, 0]) == pytest.approx(1.0)

    def test_opposite_vectors(self):
        assert cosine_similarity([1, 0], [-1, 0]) == pytest.approx(-1.0)

    def test_orthogonal_vectors(self):
        assert cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0)

    def test_partial_similarity(self):
        sim = cosine_similarity([1, 0, 0], [0.5, 0.5, 0])
        assert 0.5 < sim < 1.0

    def test_zero_vector(self):
        assert cosine_similarity([0, 0], [1, 0]) == pytest.approx(0.0)

    def test_different_dimensions_raises(self):
        with pytest.raises(ValueError, match="mesma dimensao"):
            cosine_similarity([1, 0], [1, 0, 0])


class TestVectorRecord:
    def test_create_minimal(self):
        rec = VectorRecord(id="v1", vector=[1.0, 2.0])
        assert rec.id == "v1"
        assert rec.vector == [1.0, 2.0]
        assert rec.payload == {}
        assert rec.metadata == {}

    def test_create_with_payload(self):
        rec = VectorRecord(
            id="v2", vector=[0.5], payload={"key": "val"},
            metadata={"source": "test"},
        )
        assert rec.payload == {"key": "val"}
        assert rec.metadata == {"source": "test"}


class TestSearchResult:
    def test_create(self):
        rec = VectorRecord(id="v1", vector=[1.0])
        sr = SearchResult(record=rec, score=0.95)
        assert sr.record.id == "v1"
        assert sr.score == 0.95


class TestInMemoryVectorStore:
    def test_is_available(self):
        store = InMemoryVectorStore()
        assert store.is_available() is True

    def test_upsert(self):
        store = InMemoryVectorStore()
        rec = VectorRecord(id="v1", vector=[1.0, 0.0])
        rid = store.upsert(rec)
        assert rid == "v1"
        assert store.count() == 1

    def test_upsert_empty_id_generates_uuid(self):
        store = InMemoryVectorStore()
        rec = VectorRecord(id="", vector=[1.0])
        rid = store.upsert(rec)
        assert rid.startswith("vec_")
        assert store.count() == 1

    def test_get_existing(self):
        store = InMemoryVectorStore()
        rec = VectorRecord(id="v1", vector=[1.0])
        store.upsert(rec)
        assert store.get("v1") is not None
        assert store.get("v1").id == "v1"

    def test_get_nonexistent(self):
        store = InMemoryVectorStore()
        assert store.get("nope") is None

    def test_delete_existing(self):
        store = InMemoryVectorStore()
        store.upsert(VectorRecord(id="v1", vector=[1.0]))
        assert store.delete("v1") is True
        assert store.get("v1") is None

    def test_delete_nonexistent(self):
        store = InMemoryVectorStore()
        assert store.delete("nope") is False

    def test_search_returns_sorted_by_score(self):
        store = InMemoryVectorStore()
        store.upsert(VectorRecord(id="v1", vector=[1.0, 0.0, 0.0]))
        store.upsert(VectorRecord(id="v2", vector=[0.9, 0.1, 0.0]))
        store.upsert(VectorRecord(id="v3", vector=[0.0, 1.0, 0.0]))
        results = store.search(query_vector=[1.0, 0.0, 0.0], top_k=3)
        assert len(results) == 3
        assert results[0].record.id == "v1"
        assert results[0].score == pytest.approx(1.0)
        assert results[2].record.id == "v3"

    def test_search_respects_top_k(self):
        store = InMemoryVectorStore()
        for i in range(10):
            store.upsert(VectorRecord(id=f"v{i}", vector=[float(i) / 10, 0.0]))
        results = store.search(query_vector=[1.0, 0.0], top_k=3)
        assert len(results) == 3

    def test_search_skips_different_dimensions(self):
        store = InMemoryVectorStore()
        store.upsert(VectorRecord(id="v1", vector=[1.0, 0.0]))
        store.upsert(VectorRecord(id="v2", vector=[1.0]))
        results = store.search(query_vector=[1.0, 0.0], top_k=5)
        assert len(results) == 1
        assert results[0].record.id == "v1"

    def test_search_empty_store(self):
        store = InMemoryVectorStore()
        results = store.search(query_vector=[1.0], top_k=5)
        assert results == []

    def test_count(self):
        store = InMemoryVectorStore()
        assert store.count() == 0
        store.upsert(VectorRecord(id="v1", vector=[1.0]))
        assert store.count() == 1
        store.upsert(VectorRecord(id="v2", vector=[2.0]))
        assert store.count() == 2

    def test_clear(self):
        store = InMemoryVectorStore()
        store.upsert(VectorRecord(id="v1", vector=[1.0]))
        store.upsert(VectorRecord(id="v2", vector=[2.0]))
        store.clear()
        assert store.count() == 0

    def test_upsert_replaces_existing(self):
        store = InMemoryVectorStore()
        store.upsert(VectorRecord(id="v1", vector=[1.0], payload={"val": 1}))
        store.upsert(VectorRecord(id="v1", vector=[2.0], payload={"val": 2}))
        rec = store.get("v1")
        assert rec.vector == [2.0]
        assert rec.payload == {"val": 2}

    def test_search_includes_payload(self):
        store = InMemoryVectorStore()
        store.upsert(VectorRecord(
            id="v1", vector=[1.0, 0.0],
            payload={"name": "test", "value": 42},
        ))
        results = store.search(query_vector=[1.0, 0.0], top_k=1)
        assert results[0].record.payload["name"] == "test"
        assert results[0].record.payload["value"] == 42


class TestVectorStoreAdapterABC:
    def test_cannot_instantiate_abstract(self):
        with pytest.raises(TypeError):
            VectorStoreAdapter()
