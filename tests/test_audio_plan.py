# -*- coding: utf-8 -*-
"""Tests for AudioPlan domain schema (AUD-700)."""

import pytest
from datetime import datetime, timezone

from app.domain.audio_plan import (
    AudioPlan,
    AudioPlanService,
    AudioPlanStatus,
    NarrationEntry,
)


class TestNarrationEntry:
    def test_create_minimal(self):
        entry = NarrationEntry(
            scene_number=1,
            narration_text="Texto da narracao para cena 1",
        )
        assert entry.scene_number == 1
        assert entry.narration_text == "Texto da narracao para cena 1"
        assert entry.scene_contract_id == ""
        assert entry.style_notes == ""
        assert entry.duration_seconds == 0.0
        assert entry.tts_voice == "default"
        assert entry.language == "pt-BR"

    def test_create_full(self):
        entry = NarrationEntry(
            scene_number=2,
            scene_contract_id="sc_abc123",
            narration_text="Narracao dramatica",
            style_notes="voz grave, ritmo lento",
            duration_seconds=15.5,
            tts_voice="brazil-pt-medium",
            language="pt-BR",
        )
        assert entry.scene_contract_id == "sc_abc123"
        assert entry.style_notes == "voz grave, ritmo lento"
        assert entry.duration_seconds == 15.5
        assert entry.tts_voice == "brazil-pt-medium"


class TestAudioPlanSchema:
    def test_create_minimal(self):
        plan = AudioPlan(project_id="proj_001")
        assert plan.id.startswith("ap_")
        assert plan.project_id == "proj_001"
        assert plan.narrations == []
        assert plan.status == AudioPlanStatus.DRAFT
        assert plan.version == 1
        assert plan.notes == ""
        assert plan.metadata == {}
        assert isinstance(plan.created_at, datetime)
        assert isinstance(plan.updated_at, datetime)

    def test_create_with_narrations(self):
        n1 = NarrationEntry(scene_number=1, narration_text="Cena 1")
        n2 = NarrationEntry(scene_number=2, narration_text="Cena 2")
        plan = AudioPlan(
            project_id="proj_002",
            narrations=[n1, n2],
            status=AudioPlanStatus.FINALIZED,
            notes="Revisado pelo cliente",
        )
        assert len(plan.narrations) == 2
        assert plan.status == AudioPlanStatus.FINALIZED
        assert plan.notes == "Revisado pelo cliente"

    def test_unique_ids(self):
        p1 = AudioPlan(project_id="proj_a")
        p2 = AudioPlan(project_id="proj_b")
        assert p1.id != p2.id
        assert p1.id.startswith("ap_")
        assert p2.id.startswith("ap_")

    def test_all_status_values(self):
        assert AudioPlanStatus.DRAFT.value == "draft"
        assert AudioPlanStatus.FINALIZED.value == "finalized"


class TestAudioPlanService:
    def test_create_plan(self):
        service = AudioPlanService()
        plan = AudioPlan(project_id="proj_001")
        pid = service.create(plan)
        assert pid == plan.id
        assert service.get(pid) is not None

    def test_create_requires_project_id(self):
        service = AudioPlanService()
        plan = AudioPlan(project_id="")
        with pytest.raises(ValueError, match="project_id cannot be empty"):
            service.create(plan)

    def test_create_sets_version_and_timestamps(self):
        service = AudioPlanService()
        plan = AudioPlan(project_id="proj_002")
        service.create(plan)
        assert plan.version == 1
        assert isinstance(plan.created_at, datetime)
        assert isinstance(plan.updated_at, datetime)

    def test_get_existing(self):
        service = AudioPlanService()
        plan = AudioPlan(project_id="proj_003")
        pid = service.create(plan)
        retrieved = service.get(pid)
        assert retrieved is not None
        assert retrieved.id == pid
        assert retrieved.project_id == "proj_003"

    def test_get_nonexistent(self):
        service = AudioPlanService()
        assert service.get("nonexistent") is None

    def test_get_by_project(self):
        service = AudioPlanService()
        plan = AudioPlan(project_id="proj_busca")
        pid = service.create(plan)
        found = service.get_by_project("proj_busca")
        assert found is not None
        assert found.id == pid

    def test_get_by_project_not_found(self):
        service = AudioPlanService()
        assert service.get_by_project("inexistente") is None

    def test_update_status(self):
        service = AudioPlanService()
        plan = AudioPlan(project_id="proj_004")
        pid = service.create(plan)
        updated = service.update(pid, status=AudioPlanStatus.FINALIZED)
        assert updated.status == AudioPlanStatus.FINALIZED
        assert updated.version == 2

    def test_update_notes(self):
        service = AudioPlanService()
        plan = AudioPlan(project_id="proj_005")
        pid = service.create(plan)
        updated = service.update(pid, notes="Aprovado")
        assert updated.notes == "Aprovado"
        assert updated.version == 2

    def test_update_protects_id(self):
        service = AudioPlanService()
        plan = AudioPlan(project_id="proj_006")
        pid = service.create(plan)
        updated = service.update(pid, id="novo_id")
        assert updated.id == pid

    def test_update_protects_created_at(self):
        service = AudioPlanService()
        plan = AudioPlan(project_id="proj_007")
        pid = service.create(plan)
        original = plan.created_at
        updated = service.update(pid, notes="teste")
        assert updated.created_at == original

    def test_update_protects_version(self):
        service = AudioPlanService()
        plan = AudioPlan(project_id="proj_008")
        pid = service.create(plan)
        updated = service.update(pid, version=99)
        assert updated.version != 99
        assert updated.version == 2

    def test_update_nonexistent(self):
        service = AudioPlanService()
        with pytest.raises(KeyError, match="AudioPlan not found"):
            service.update("nonexistent", notes="x")

    def test_delete_existing(self):
        service = AudioPlanService()
        plan = AudioPlan(project_id="proj_009")
        pid = service.create(plan)
        assert service.delete(pid) is True
        assert service.get(pid) is None

    def test_delete_nonexistent(self):
        service = AudioPlanService()
        assert service.delete("nonexistent") is False

    def test_list_all(self):
        service = AudioPlanService()
        service.create(AudioPlan(project_id="proj_a"))
        service.create(AudioPlan(project_id="proj_b"))
        assert len(service.list()) == 2

    def test_list_filter_by_status(self):
        service = AudioPlanService()
        p1 = AudioPlan(project_id="proj_a")
        p2 = AudioPlan(project_id="proj_b", status=AudioPlanStatus.FINALIZED)
        service.create(p1)
        service.create(p2)
        drafts = service.list(status=AudioPlanStatus.DRAFT)
        finalizeds = service.list(status=AudioPlanStatus.FINALIZED)
        assert len(drafts) == 1
        assert len(finalizeds) == 1

    def test_list_empty_by_status(self):
        service = AudioPlanService()
        service.create(AudioPlan(project_id="proj_a"))
        finalizeds = service.list(status=AudioPlanStatus.FINALIZED)
        assert len(finalizeds) == 0

    def test_count(self):
        service = AudioPlanService()
        assert service.count() == 0
        service.create(AudioPlan(project_id="proj_a"))
        assert service.count() == 1
        service.create(AudioPlan(project_id="proj_b"))
        assert service.count() == 2

    def test_clear(self):
        service = AudioPlanService()
        service.create(AudioPlan(project_id="proj_a"))
        service.create(AudioPlan(project_id="proj_b"))
        service.clear()
        assert service.count() == 0


class TestAudioPlanNarrations:
    def test_add_narration(self):
        service = AudioPlanService()
        plan = AudioPlan(project_id="proj_nar")
        pid = service.create(plan)
        entry = NarrationEntry(
            scene_number=1, narration_text="Abertura"
        )
        updated = service.add_narration(pid, entry)
        assert len(updated.narrations) == 1
        assert updated.narrations[0].narration_text == "Abertura"
        assert updated.version == 2

    def test_add_narration_to_nonexistent_plan(self):
        service = AudioPlanService()
        entry = NarrationEntry(scene_number=1, narration_text="x")
        with pytest.raises(KeyError, match="AudioPlan not found"):
            service.add_narration("nonexistent", entry)

    def test_remove_narration(self):
        service = AudioPlanService()
        plan = AudioPlan(
            project_id="proj_rem",
            narrations=[
                NarrationEntry(scene_number=1, narration_text="Cena 1"),
                NarrationEntry(scene_number=2, narration_text="Cena 2"),
            ],
        )
        pid = service.create(plan)
        updated = service.remove_narration(pid, 1)
        assert len(updated.narrations) == 1
        assert updated.narrations[0].scene_number == 2
        assert updated.version == 2

    def test_remove_narration_from_nonexistent_plan(self):
        service = AudioPlanService()
        with pytest.raises(KeyError, match="AudioPlan not found"):
            service.remove_narration("nonexistent", 1)

    def test_update_narration_text(self):
        service = AudioPlanService()
        plan = AudioPlan(
            project_id="proj_upd",
            narrations=[
                NarrationEntry(scene_number=1, narration_text="Original"),
            ],
        )
        pid = service.create(plan)
        updated = service.update_narration_text(
            pid, 1, "Texto revisado"
        )
        assert updated.narrations[0].narration_text == "Texto revisado"
        assert updated.version == 2

    def test_update_narration_text_scene_not_found(self):
        service = AudioPlanService()
        plan = AudioPlan(project_id="proj_err")
        pid = service.create(plan)
        with pytest.raises(ValueError, match="Narration not found"):
            service.update_narration_text(pid, 99, "novo texto")

    def test_update_narration_text_nonexistent_plan(self):
        service = AudioPlanService()
        with pytest.raises(KeyError, match="AudioPlan not found"):
            service.update_narration_text("nonexistent", 1, "x")


class TestNarrationScriptGeneration:
    def test_generates_markdown_with_header(self):
        service = AudioPlanService()
        plan = AudioPlan(project_id="proj_script")
        pid = service.create(plan)
        md = service.generate_narration_script(pid)
        assert md.startswith("# Narration Script")
        assert "proj_script" in md

    def test_generates_markdown_with_narrations(self):
        service = AudioPlanService()
        plan = AudioPlan(
            project_id="proj_nar",
            narrations=[
                NarrationEntry(
                    scene_number=1,
                    narration_text="Abertura impactante",
                    style_notes="energico",
                    duration_seconds=10.0,
                ),
                NarrationEntry(
                    scene_number=2,
                    narration_text="Desenvolvimento do produto",
                    duration_seconds=15.5,
                ),
            ],
        )
        pid = service.create(plan)
        md = service.generate_narration_script(pid)
        assert "## Cena 1" in md
        assert "## Cena 2" in md
        assert "Abertura impactante" in md
        assert "Desenvolvimento do produto" in md
        assert "energico" in md
        assert "10.0s" in md
        assert "15.5s" in md
        assert "**Total" in md
        assert "25.5s" in md
        assert md.count("## Cena") == 2

    def test_generates_markdown_with_status_and_version(self):
        service = AudioPlanService()
        plan = AudioPlan(
            project_id="proj_status",
            status=AudioPlanStatus.FINALIZED,
        )
        pid = service.create(plan)
        md = service.generate_narration_script(pid)
        assert "finalized" in md
        assert "Versao:" in md or "Vers" in md

    def test_generates_markdown_with_scenes_sorted(self):
        service = AudioPlanService()
        plan = AudioPlan(
            project_id="proj_sort",
            narrations=[
                NarrationEntry(scene_number=3, narration_text="Cena 3"),
                NarrationEntry(scene_number=1, narration_text="Cena 1"),
                NarrationEntry(scene_number=2, narration_text="Cena 2"),
            ],
        )
        pid = service.create(plan)
        md = service.generate_narration_script(pid)
        c1 = md.index("## Cena 1")
        c2 = md.index("## Cena 2")
        c3 = md.index("## Cena 3")
        assert c1 < c2 < c3

    def test_generates_markdown_empty_plan(self):
        service = AudioPlanService()
        plan = AudioPlan(project_id="proj_empty")
        pid = service.create(plan)
        md = service.generate_narration_script(pid)
        assert "**Total" in md
        assert "0.0s" in md

    def test_generates_markdown_nonexistent_plan(self):
        service = AudioPlanService()
        with pytest.raises(KeyError, match="AudioPlan not found"):
            service.generate_narration_script("nonexistent")

    def test_narration_script_includes_tts_voice(self):
        service = AudioPlanService()
        plan = AudioPlan(
            project_id="proj_voice",
            narrations=[
                NarrationEntry(
                    scene_number=1,
                    narration_text="Teste",
                    tts_voice="brazil-pt-medium",
                ),
            ],
        )
        pid = service.create(plan)
        md = service.generate_narration_script(pid)
        assert "brazil-pt-medium" in md

    def test_narration_script_includes_language(self):
        service = AudioPlanService()
        plan = AudioPlan(project_id="proj_lang")
        pid = service.create(plan)
        md = service.generate_narration_script(pid)
        assert "pt-BR" in md
