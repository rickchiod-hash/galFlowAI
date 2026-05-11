"""Tests for VEC-802: Qdrant integration planned in VECTOR_MEMORY_PLAYBOOK."""
import pytest

from app.adapters.vector_store import VectorStoreAdapter, InMemoryVectorStore


class TestQdrantPlanPlaybook:
    def test_vec_802_playbook_section_exists(self):
        """Verify VEC-802 section exists and is marked Concluida in playbook."""
        with open("docs/project-control/VECTOR_MEMORY_PLAYBOOK.md", encoding="utf-8") as f:
            content = f.read()
        assert "VEC-802" in content
        assert "Concluida" in content or "Concluída" in content


class TestVectorStoreAdapterInterface:
    def test_adapter_has_search_method(self):
        assert hasattr(VectorStoreAdapter, "search")

    def test_adapter_has_upsert_method(self):
        assert hasattr(VectorStoreAdapter, "upsert")

    def test_adapter_has_delete_method(self):
        assert hasattr(VectorStoreAdapter, "delete")

    def test_adapter_is_abc(self):
        import abc
        assert issubclass(VectorStoreAdapter, abc.ABC)


class TestInMemoryStoreFallback:
    def test_inmemory_implements_adapter(self):
        store = InMemoryVectorStore()
        assert isinstance(store, VectorStoreAdapter)

    def test_inmemory_search_returns_results(self):
        from app.adapters.vector_store import VectorRecord
        store = InMemoryVectorStore()
        store.upsert(VectorRecord(id="vec_1", vector=[0.1, 0.2, 0.3], payload={"name": "test"}))
        results = store.search([0.1, 0.2, 0.3], top_k=5)
        assert len(results) >= 1

    def test_inmemory_upsert_then_delete(self):
        from app.adapters.vector_store import VectorRecord
        store = InMemoryVectorStore()
        store.upsert(VectorRecord(id="vec_1", vector=[0.1, 0.2, 0.3], payload={"name": "test"}))
        store.delete("vec_1")
        results = store.search([0.1, 0.2, 0.3], top_k=5)
        assert len(results) == 0
