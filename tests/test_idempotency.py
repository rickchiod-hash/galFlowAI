"""Tests for Idempotency Service and Use Cases (PIPE-401)."""
import pytest
import json
from app.services.idempotency_service import IdempotencyRegistry, generate_key
from app.application.use_cases.idempotency_use_cases import (
    CheckIdempotencyUseCase,
    RegisterIdempotencyUseCase
)


class TestGenerateKey:
    """Test idempotency key generation."""

    def test_key_is_deterministic(self):
        """Same stage + params produces same key."""
        params = {"briefing": "test", "project_id": "proj_001"}
        key1 = generate_key("script_gen", params)
        key2 = generate_key("script_gen", params)
        assert key1 == key2
        assert len(key1) == 64  # SHA-256 hex

    def test_key_changes_with_params(self):
        """Different params produce different keys."""
        params_a = {"briefing": "A"}
        params_b = {"briefing": "B"}
        assert generate_key("stage", params_a) != generate_key("stage", params_b)

    def test_key_changes_with_stage(self):
        """Different stage names produce different keys."""
        params = {"briefing": "test"}
        assert generate_key("stage_a", params) != generate_key("stage_b", params)

    def test_key_is_sort_independent(self):
        """Key is independent of param dict ordering."""
        params1 = {"a": 1, "b": 2}
        params2 = {"b": 2, "a": 1}
        assert generate_key("stage", params1) == generate_key("stage", params2)

    def test_key_handles_empty_params(self):
        """Empty params dict produces valid key."""
        key = generate_key("stage", {})
        assert len(key) == 64


class TestIdempotencyRegistry:
    """Test IdempotencyRegistry persistence and lookups."""

    @pytest.fixture
    def reg(self, tmp_path):
        """Create a registry with temp file."""
        reg_file = tmp_path / "test_registry.json"
        registry = IdempotencyRegistry(registry_file=reg_file)
        yield registry
        registry.clear()

    def test_check_missing_key(self, reg):
        """Missing key returns None."""
        assert reg.check("nonexistent") is None

    def test_register_and_check(self, reg):
        """Registered key can be checked."""
        key = generate_key("test_stage", {"input": "value"})
        reg.register(key, "test_stage", {"result": "ok"})
        entry = reg.check(key)
        assert entry is not None
        assert entry["stage"] == "test_stage"
        assert entry["output"]["result"] == "ok"

    def test_is_completed(self, reg):
        """is_completed returns True for registered key."""
        key = generate_key("stage", {"x": 1})
        reg.register(key, "stage", {"done": True})
        assert reg.is_completed(key) is True

    def test_is_completed_missing(self, reg):
        """is_completed returns False for missing key."""
        assert reg.is_completed("missing") is False

    def test_register_twice_overwrites(self, reg):
        """Registering same key twice updates the entry."""
        key = generate_key("stage", {"x": 1})
        reg.register(key, "stage", {"result": "first"})
        reg.register(key, "stage", {"result": "second"})
        assert reg.check(key)["output"]["result"] == "second"

    def test_persistence_across_instances(self, tmp_path):
        """Registry persists across instances via JSON file."""
        reg_file = tmp_path / "persist.json"
        reg1 = IdempotencyRegistry(registry_file=reg_file)
        key = generate_key("stage", {"p": 1})
        reg1.register(key, "stage", {"done": True})
        reg1._save()

        reg2 = IdempotencyRegistry(registry_file=reg_file)
        assert reg2.is_completed(key) is True
        reg2.clear()

    def test_get_stats(self, reg):
        """get_stats returns summary with entry count and stages."""
        reg.register(generate_key("s1", {"a": 1}), "s1", {})
        reg.register(generate_key("s2", {"b": 2}), "s2", {})
        stats = reg.get_stats()
        assert stats["total_entries"] == 2
        assert "s1" in stats["stages"]
        assert "s2" in stats["stages"]

    def test_clear_removes_all(self, reg):
        """clear() removes all entries and file."""
        reg.register(generate_key("s", {"a": 1}), "s", {})
        reg.clear()
        assert reg.get_stats()["total_entries"] == 0
        assert not reg.registry_file.exists()

    def test_ttl_expiration(self, reg):
        """Entry with TTL expires after the TTL period."""
        key = generate_key("s", {"x": 1})
        reg.register(key, "s", {"result": "ok"}, ttl_seconds=0)
        assert reg.is_completed(key) is False

    def test_load_corrupted_file(self, tmp_path):
        """Corrupted registry file loads as empty without crashing."""
        reg_file = tmp_path / "corrupt.json"
        reg_file.write_text("not json", encoding="utf-8")
        reg = IdempotencyRegistry(registry_file=reg_file)
        assert reg.get_stats()["total_entries"] == 0
        reg.clear()


class TestCheckIdempotencyUseCase:
    """Test CheckIdempotencyUseCase."""

    def test_not_cached(self):
        """First check with fresh params returns cached=False."""
        uc = CheckIdempotencyUseCase()
        result = uc.execute(stage="script_gen", params={"briefing": "new"})
        assert result["ok"] is True
        assert result["data"]["cached"] is False
        assert "key" in result["data"]

    def test_cached_after_register(self):
        """Second check after register returns cached=True."""
        check_uc = CheckIdempotencyUseCase()
        reg_uc = RegisterIdempotencyUseCase()

        params = {"briefing": "same", "style": "viral"}
        reg_uc.execute(stage="script_gen", params=params, output={"script": "..."})

        result = check_uc.execute(stage="script_gen", params=params)
        assert result["ok"] is True
        assert result["data"]["cached"] is True
        assert result["data"]["output"]["script"] == "..."

    def test_different_params_not_cached(self):
        """Different params after register returns cached=False."""
        reg_uc = RegisterIdempotencyUseCase()
        check_uc = CheckIdempotencyUseCase()

        reg_uc.execute(stage="script_gen", params={"briefing": "A"}, output={"script": "..."})
        result = check_uc.execute(stage="script_gen", params={"briefing": "B"})
        assert result["data"]["cached"] is False

    def test_validate_empty_stage(self):
        """Empty stage returns error."""
        uc = CheckIdempotencyUseCase()
        result = uc.execute(stage="", params={})
        assert result["ok"] is False


class TestRegisterIdempotencyUseCase:
    """Test RegisterIdempotencyUseCase."""

    def test_register_success(self):
        """Register returns success with key."""
        uc = RegisterIdempotencyUseCase()
        result = uc.execute(stage="render", params={"scene": 1}, output={"path": "/out.mp4"})
        assert result["ok"] is True
        assert result["data"]["registered"] is True
        assert len(result["data"]["key"]) == 64

    def test_validate_missing_output(self):
        """Missing output returns error."""
        uc = RegisterIdempotencyUseCase()
        result = uc.execute(stage="render", params={"scene": 1}, output={})
        assert result["ok"] is False
