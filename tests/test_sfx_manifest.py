# -*- coding: utf-8 -*-
"""Tests for SFX Manifest schema (AUD-703)."""

import pytest
from datetime import datetime, timezone

from app.domain.sfx_manifest import SFXAsset, SFXLicenseType, SFXManifest


class TestSFXLicenseType:
    def test_all_types_defined(self):
        assert SFXLicenseType.FREE.value == "free"
        assert SFXLicenseType.ROYALTY_FREE.value == "royalty_free"
        assert SFXLicenseType.LICENSED.value == "licensed"
        assert SFXLicenseType.CC0.value == "cc0"
        assert SFXLicenseType.CC_BY.value == "cc_by"
        assert SFXLicenseType.CUSTOM.value == "custom"
        assert SFXLicenseType.UNKNOWN.value == "unknown"

    def test_default_is_unknown(self):
        asset = SFXAsset(name="boom", file_path="boom.wav")
        assert asset.license_type == SFXLicenseType.UNKNOWN


class TestSFXAssetSchema:
    def test_create_minimal(self):
        asset = SFXAsset(name="explosion", file_path="sfx/explosion.wav")
        assert asset.id.startswith("sfx_")
        assert asset.name == "explosion"
        assert asset.file_path == "sfx/explosion.wav"
        assert isinstance(asset.created_at, datetime)
        assert isinstance(asset.updated_at, datetime)
        assert asset.version == 1
        assert asset.license_url == ""
        assert asset.origin == ""
        assert asset.description == ""
        assert asset.duration_seconds == 0.0
        assert asset.metadata == {}

    def test_create_full(self):
        asset = SFXAsset(
            name="thunder",
            file_path="sfx/thunder.wav",
            license_type=SFXLicenseType.CC0,
            license_url="https://example.com/cc0",
            origin="freesound.org",
            description="Thunder sound effect",
            duration_seconds=3.5,
            metadata={"key": "value"},
        )
        assert asset.license_type == SFXLicenseType.CC0
        assert asset.license_url == "https://example.com/cc0"
        assert asset.origin == "freesound.org"
        assert asset.description == "Thunder sound effect"
        assert asset.duration_seconds == 3.5
        assert asset.metadata == {"key": "value"}

    def test_unique_ids(self):
        a1 = SFXAsset(name="a", file_path="a.wav")
        a2 = SFXAsset(name="b", file_path="b.wav")
        assert a1.id != a2.id

    def test_default_version(self):
        asset = SFXAsset(name="test", file_path="test.wav")
        assert asset.version == 1


class TestSFXManifest:
    def test_register(self):
        m = SFXManifest()
        asset = SFXAsset(name="boom", file_path="boom.wav")
        aid = m.register(asset)
        assert aid == asset.id
        assert m.get(aid) is not None

    def test_register_empty_name_raises(self):
        m = SFXManifest()
        with pytest.raises(ValueError, match="SFX name cannot be empty"):
            m.register(SFXAsset(name="", file_path="x.wav"))

    def test_register_empty_file_path_raises(self):
        m = SFXManifest()
        with pytest.raises(ValueError, match="SFX file_path cannot be empty"):
            m.register(SFXAsset(name="x", file_path=""))

    def test_register_sets_version_and_timestamps(self):
        m = SFXManifest()
        asset = SFXAsset(name="pop", file_path="pop.wav")
        m.register(asset)
        assert asset.version == 1
        assert isinstance(asset.created_at, datetime)
        assert isinstance(asset.updated_at, datetime)

    def test_get_existing(self):
        m = SFXManifest()
        asset = SFXAsset(name="click", file_path="click.wav")
        aid = m.register(asset)
        assert m.get(aid) is not None
        assert m.get(aid).name == "click"

    def test_get_nonexistent(self):
        m = SFXManifest()
        assert m.get("nonexistent") is None

    def test_get_by_name(self):
        m = SFXManifest()
        m.register(SFXAsset(name="swoosh", file_path="swoosh.wav"))
        found = m.get_by_name("swoosh")
        assert found is not None
        assert found.name == "swoosh"

    def test_get_by_name_case_insensitive(self):
        m = SFXManifest()
        m.register(SFXAsset(name="Swoosh", file_path="swoosh.wav"))
        found = m.get_by_name("swoosh")
        assert found is not None

    def test_get_by_name_not_found(self):
        m = SFXManifest()
        assert m.get_by_name("nope") is None

    def test_update_name(self):
        m = SFXManifest()
        asset = SFXAsset(name="old", file_path="old.wav")
        aid = m.register(asset)
        updated = m.update(aid, name="new_name")
        assert updated.name == "new_name"
        assert updated.version == 2

    def test_update_protects_id(self):
        m = SFXManifest()
        asset = SFXAsset(name="x", file_path="x.wav")
        aid = m.register(asset)
        updated = m.update(aid, id="new_id")
        assert updated.id == aid

    def test_update_protects_created_at(self):
        m = SFXManifest()
        asset = SFXAsset(name="x", file_path="x.wav")
        aid = m.register(asset)
        original = asset.created_at
        updated = m.update(aid, name="y")
        assert updated.created_at == original

    def test_update_protects_version(self):
        m = SFXManifest()
        asset = SFXAsset(name="x", file_path="x.wav")
        aid = m.register(asset)
        updated = m.update(aid, version=99)
        assert updated.version != 99
        assert updated.version == 2

    def test_update_nonexistent(self):
        m = SFXManifest()
        with pytest.raises(KeyError, match="SFXAsset not found"):
            m.update("nonexistent", name="x")

    def test_delete_existing(self):
        m = SFXManifest()
        asset = SFXAsset(name="x", file_path="x.wav")
        aid = m.register(asset)
        assert m.delete(aid) is True
        assert m.get(aid) is None

    def test_delete_nonexistent(self):
        m = SFXManifest()
        assert m.delete("nonexistent") is False

    def test_list_all(self):
        m = SFXManifest()
        m.register(SFXAsset(name="a", file_path="a.wav"))
        m.register(SFXAsset(name="b", file_path="b.wav"))
        assert len(m.list()) == 2

    def test_list_filter_by_license(self):
        m = SFXManifest()
        m.register(SFXAsset(
            name="a", file_path="a.wav",
            license_type=SFXLicenseType.CC0,
        ))
        m.register(SFXAsset(
            name="b", file_path="b.wav",
            license_type=SFXLicenseType.LICENSED,
        ))
        cc0 = m.list(license_type=SFXLicenseType.CC0)
        licensed = m.list(license_type=SFXLicenseType.LICENSED)
        assert len(cc0) == 1
        assert len(licensed) == 1

    def test_list_empty_by_license(self):
        m = SFXManifest()
        m.register(SFXAsset(name="a", file_path="a.wav"))
        free = m.list(license_type=SFXLicenseType.FREE)
        assert len(free) == 0

    def test_search_by_name(self):
        m = SFXManifest()
        m.register(SFXAsset(name="explosion", file_path="e.wav"))
        m.register(SFXAsset(name="wind", file_path="w.wav"))
        result = m.search("explosion")
        assert len(result) == 1
        assert result[0].name == "explosion"

    def test_search_by_description(self):
        m = SFXManifest()
        m.register(SFXAsset(
            name="boom", file_path="b.wav",
            description="loud explosion sound",
        ))
        result = m.search("explosion")
        assert len(result) == 1

    def test_search_case_insensitive(self):
        m = SFXManifest()
        m.register(SFXAsset(name="Explosion", file_path="e.wav"))
        result = m.search("explosion")
        assert len(result) == 1

    def test_search_no_results(self):
        m = SFXManifest()
        m.register(SFXAsset(name="a", file_path="a.wav"))
        assert m.search("nonexistent") == []

    def test_count(self):
        m = SFXManifest()
        assert m.count() == 0
        m.register(SFXAsset(name="a", file_path="a.wav"))
        assert m.count() == 1
        m.register(SFXAsset(name="b", file_path="b.wav"))
        assert m.count() == 2

    def test_clear(self):
        m = SFXManifest()
        m.register(SFXAsset(name="a", file_path="a.wav"))
        m.register(SFXAsset(name="b", file_path="b.wav"))
        m.clear()
        assert m.count() == 0
