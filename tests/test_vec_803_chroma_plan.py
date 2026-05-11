"""Tests for VEC-803: Chroma integration planned in VECTOR_MEMORY_PLAYBOOK."""
import pytest


class TestChromaPlanPlaybook:
    def test_vec_803_playbook_section_exists(self):
        with open("docs/project-control/VECTOR_MEMORY_PLAYBOOK.md", encoding="utf-8") as f:
            content = f.read()
        assert "VEC-803" in content
        assert "ChromaStore" in content

    def test_chroma_comparison_table_exists(self):
        with open("docs/project-control/VECTOR_MEMORY_PLAYBOOK.md", encoding="utf-8") as f:
            content = f.read()
        assert "Qdrant" in content and "Chroma" in content

    def test_playbook_marks_803_concluida(self):
        with open("docs/project-control/VECTOR_MEMORY_PLAYBOOK.md", encoding="utf-8") as f:
            content = f.read()
        assert "Concluida" in content or "Concluída" in content


class TestVectorStorePersistenceRule:
    def test_inmemory_is_fallback(self):
        """InMemoryVectorStore must remain as fallback per preservation rule #6."""
        from app.adapters.vector_store import InMemoryVectorStore
        store = InMemoryVectorStore()
        assert store.is_available() is True

    def test_adapter_methods_defined(self):
        from app.adapters.vector_store import VectorStoreAdapter
        import inspect
        methods = [m for m in dir(VectorStoreAdapter) if not m.startswith("_")]
        for required in ["upsert", "get", "delete", "search", "count", "clear", "is_available"]:
            assert required in methods, f"Missing method: {required}"
