"""Tests for SceneContract domain schema (VIS-502).

Cobre schemas, CRUD, busca, filtro, versionamento e reordenação.
"""

import pytest
from datetime import datetime, timezone
from app.exceptions import NotFoundError, ValidationError
from app.domain.scene_contract import (
    CameraDirective,
    CameraMovement,
    IngredientAssignment,
    SceneContract,
    SceneContractService,
    SceneContractStatus,
    ShotSize,
    TransitionType,
)


class TestCameraDirective:
    def test_default_camera(self):
        cam = CameraDirective()
        assert cam.angle == "frontal"
        assert cam.movement == CameraMovement.STATIC
        assert cam.shot_size == ShotSize.MEDIUM
        assert cam.notes == ""

    def test_custom_camera(self):
        cam = CameraDirective(
            angle="low",
            movement=CameraMovement.DOLLY,
            shot_size=ShotSize.CLOSE_UP,
            notes="zoom lento",
        )
        assert cam.angle == "low"
        assert cam.movement == CameraMovement.DOLLY
        assert cam.shot_size == ShotSize.CLOSE_UP
        assert cam.notes == "zoom lento"


class TestIngredientAssignment:
    def test_minimal_assignment(self):
        a = IngredientAssignment(ingredient_id="ing_abc", ingredient_name="Produto X")
        assert a.ingredient_id == "ing_abc"
        assert a.ingredient_name == "Produto X"
        assert a.placement == ""
        assert a.visual_bible_ref is None

    def test_full_assignment(self):
        a = IngredientAssignment(
            ingredient_id="ing_def",
            ingredient_name="Personagem Y",
            placement="centro, plano médio",
            visual_bible_ref="bbl_123",
        )
        assert a.visual_bible_ref == "bbl_123"
        assert a.placement == "centro, plano médio"


class TestSceneContractSchema:
    def test_minimal_contract(self):
        c = SceneContract(scene_number=1, description="Cena de abertura")
        assert c.id.startswith("sc_")
        assert c.scene_number == 1
        assert c.description == "Cena de abertura"
        assert c.duration == 5
        assert c.transition_in == TransitionType.CUT
        assert c.transition_out == TransitionType.CUT
        assert isinstance(c.camera, CameraDirective)
        assert c.ingredients == []
        assert c.style == ""
        assert c.status == SceneContractStatus.DRAFT
        assert c.version == 1
        assert c.metadata == {}
        assert isinstance(c.created_at, datetime)
        assert isinstance(c.updated_at, datetime)

    def test_contract_with_all_fields(self):
        c = SceneContract(
            scene_number=2,
            description="Cena de ação",
            prompt_positive="ação, explosão, câmera lenta",
            prompt_negative="borrão, baixa qualidade",
            duration=10,
            transition_in=TransitionType.FADE,
            transition_out=TransitionType.DISSOLVE,
            camera=CameraDirective(
                angle="high",
                movement=CameraMovement.TRACK,
                shot_size=ShotSize.WIDE,
                notes="track lateral",
            ),
            ingredients=[
                IngredientAssignment(
                    ingredient_id="ing_001",
                    ingredient_name="Carro",
                    placement="entrando pela esquerda",
                ),
                IngredientAssignment(
                    ingredient_id="ing_002",
                    ingredient_name="Motorista",
                    visual_bible_ref="bbl_001",
                ),
            ],
            style="cinematic action",
            status=SceneContractStatus.FINALIZED,
            notes="Aprovado pelo diretor",
            metadata={"budget": "high", "render_engine": "wangp"},
        )
        assert c.scene_number == 2
        assert c.prompt_positive == "ação, explosão, câmera lenta"
        assert c.duration == 10
        assert c.transition_in == TransitionType.FADE
        assert c.transition_out == TransitionType.DISSOLVE
        assert c.camera.angle == "high"
        assert len(c.ingredients) == 2
        assert c.ingredients[0].ingredient_id == "ing_001"
        assert c.ingredients[1].visual_bible_ref == "bbl_001"
        assert c.status == SceneContractStatus.FINALIZED
        assert c.metadata["render_engine"] == "wangp"

    def test_unique_ids(self):
        c1 = SceneContract(scene_number=1, description="Cena 1")
        c2 = SceneContract(scene_number=2, description="Cena 2")
        assert c1.id != c2.id

    def test_all_status_values(self):
        for status in SceneContractStatus:
            c = SceneContract(scene_number=1, description="teste", status=status)
            assert c.status == status

    def test_all_transition_types(self):
        for ttype in TransitionType:
            c = SceneContract(scene_number=1, description="teste", transition_in=ttype, transition_out=ttype)
            assert c.transition_in == ttype
            assert c.transition_out == ttype

    def test_all_shot_sizes(self):
        for size in ShotSize:
            cam = CameraDirective(shot_size=size)
            assert cam.shot_size == size

    def test_all_camera_movements(self):
        for mov in CameraMovement:
            cam = CameraDirective(movement=mov)
            assert cam.movement == mov


class TestSceneContractService:
    def test_create_contract(self):
        svc = SceneContractService()
        c = SceneContract(scene_number=1, description="Primeira cena")
        cid = svc.create(c)
        assert cid == c.id
        assert svc.count() == 1

    def test_create_requires_description(self):
        svc = SceneContractService()
        with pytest.raises(ValidationError, match="description cannot be empty"):
            svc.create(SceneContract(scene_number=1, description="   "))

    def test_create_requires_non_negative_scene_number(self):
        svc = SceneContractService()
        with pytest.raises(ValidationError, match="scene_number must be non-negative"):
            svc.create(SceneContract(scene_number=-1, description="invalida"))

    def test_create_sets_version_and_timestamps(self):
        svc = SceneContractService()
        c = SceneContract(scene_number=1, description="teste")
        svc.create(c)
        assert c.version == 1
        assert isinstance(c.created_at, datetime)
        assert isinstance(c.updated_at, datetime)

    def test_get_existing(self):
        svc = SceneContractService()
        c = SceneContract(scene_number=1, description="Cena")
        cid = svc.create(c)
        fetched = svc.get(cid)
        assert fetched is not None
        assert fetched.id == cid
        assert fetched.description == "Cena"

    def test_get_nonexistent(self):
        svc = SceneContractService()
        assert svc.get("sc_nonexistent") is None

    def test_get_by_scene_number(self):
        svc = SceneContractService()
        c1 = SceneContract(scene_number=1, description="Cena 1")
        c2 = SceneContract(scene_number=5, description="Cena 5")
        svc.create(c1)
        svc.create(c2)
        assert svc.get_by_scene_number(5).id == c2.id
        assert svc.get_by_scene_number(5).description == "Cena 5"
        assert svc.get_by_scene_number(99) is None

    def test_update_description(self):
        svc = SceneContractService()
        c = SceneContract(scene_number=1, description="Original")
        cid = svc.create(c)
        svc.update(cid, description="Atualizada")
        assert svc.get(cid).description == "Atualizada"
        assert svc.get(cid).version == 2

    def test_update_status(self):
        svc = SceneContractService()
        c = SceneContract(scene_number=1, description="Cena")
        cid = svc.create(c)
        svc.update(cid, status=SceneContractStatus.APPROVED)
        assert svc.get(cid).status == SceneContractStatus.APPROVED
        assert svc.get(cid).version == 2

    def test_update_camera(self):
        svc = SceneContractService()
        c = SceneContract(scene_number=1, description="Cena")
        cid = svc.create(c)
        new_cam = CameraDirective(angle="low", movement=CameraMovement.DOLLY)
        svc.update(cid, camera=new_cam)
        assert svc.get(cid).camera.angle == "low"
        assert svc.get(cid).camera.movement == CameraMovement.DOLLY

    def test_update_protects_id(self):
        svc = SceneContractService()
        c = SceneContract(scene_number=1, description="Cena")
        cid = svc.create(c)
        old_id = c.id
        svc.update(cid, id="sc_hacked")
        assert svc.get(cid).id == old_id

    def test_update_protects_scene_number(self):
        svc = SceneContractService()
        c = SceneContract(scene_number=1, description="Cena")
        cid = svc.create(c)
        svc.update(cid, scene_number=99)
        assert svc.get(cid).scene_number == 1

    def test_update_protects_created_at(self):
        svc = SceneContractService()
        c = SceneContract(scene_number=1, description="Cena")
        cid = svc.create(c)
        orig_created = c.created_at
        svc.update(cid, created_at=datetime.now(timezone.utc))
        assert svc.get(cid).created_at == orig_created

    def test_update_nonexistent(self):
        svc = SceneContractService()
        with pytest.raises(NotFoundError, match="SceneContract not found"):
            svc.update("sc_nonexistent", description="x")

    def test_delete_existing(self):
        svc = SceneContractService()
        c = SceneContract(scene_number=1, description="Cena")
        cid = svc.create(c)
        assert svc.delete(cid) is True
        assert svc.count() == 0

    def test_delete_nonexistent(self):
        svc = SceneContractService()
        assert svc.delete("sc_nonexistent") is False

    def test_list_all(self):
        svc = SceneContractService()
        svc.create(SceneContract(scene_number=2, description="Segunda"))
        svc.create(SceneContract(scene_number=1, description="Primeira"))
        svc.create(SceneContract(scene_number=3, description="Terceira"))
        all_contracts = svc.list()
        assert len(all_contracts) == 3
        assert [c.scene_number for c in all_contracts] == [1, 2, 3]

    def test_list_filter_by_status(self):
        svc = SceneContractService()
        c1 = SceneContract(scene_number=1, description="Cena 1", status=SceneContractStatus.DRAFT)
        c2 = SceneContract(scene_number=2, description="Cena 2", status=SceneContractStatus.FINALIZED)
        c3 = SceneContract(scene_number=3, description="Cena 3", status=SceneContractStatus.APPROVED)
        svc.create(c1)
        svc.create(c2)
        svc.create(c3)
        finalized = svc.list(status=SceneContractStatus.FINALIZED)
        assert len(finalized) == 1
        assert finalized[0].scene_number == 2

    def test_list_empty_by_status(self):
        svc = SceneContractService()
        svc.create(SceneContract(scene_number=1, description="Cena", status=SceneContractStatus.DRAFT))
        approved = svc.list(status=SceneContractStatus.APPROVED)
        assert approved == []

    def test_search_by_description(self):
        svc = SceneContractService()
        svc.create(SceneContract(scene_number=1, description="Abertura épica"))
        svc.create(SceneContract(scene_number=2, description="Diálogo interno"))
        svc.create(SceneContract(scene_number=3, description="Clímax final"))
        results = svc.search("abertura")
        assert len(results) == 1
        assert results[0].scene_number == 1

    def test_search_by_notes(self):
        svc = SceneContractService()
        c = SceneContract(scene_number=1, description="Cena", notes="aprovado pelo cliente")
        svc.create(c)
        results = svc.search("cliente")
        assert len(results) == 1

    def test_search_case_insensitive(self):
        svc = SceneContractService()
        svc.create(SceneContract(scene_number=1, description="CENA PRINCIPAL"))
        results = svc.search("principal")
        assert len(results) == 1

    def test_search_no_results(self):
        svc = SceneContractService()
        svc.create(SceneContract(scene_number=1, description="Ação"))
        results = svc.search("inexistente")
        assert results == []

    def test_get_contracts_for_ingredient(self):
        svc = SceneContractService()
        c1 = SceneContract(
            scene_number=1,
            description="Cena 1",
            ingredients=[IngredientAssignment(ingredient_id="ing_001", ingredient_name="Carro")],
        )
        c2 = SceneContract(
            scene_number=2,
            description="Cena 2",
            ingredients=[
                IngredientAssignment(ingredient_id="ing_001", ingredient_name="Carro"),
                IngredientAssignment(ingredient_id="ing_002", ingredient_name="Motorista"),
            ],
        )
        c3 = SceneContract(
            scene_number=3,
            description="Cena 3",
            ingredients=[IngredientAssignment(ingredient_id="ing_003", ingredient_name="Cenário")],
        )
        svc.create(c1)
        svc.create(c2)
        svc.create(c3)

        results = svc.get_contracts_for_ingredient("ing_001")
        assert len(results) == 2
        assert {r.scene_number for r in results} == {1, 2}

        results = svc.get_contracts_for_ingredient("ing_003")
        assert len(results) == 1
        assert results[0].scene_number == 3

        results = svc.get_contracts_for_ingredient("ing_nonexistent")
        assert results == []

    def test_reorder_contracts(self):
        svc = SceneContractService()
        c1 = SceneContract(scene_number=10, description="Antiga 10")
        c2 = SceneContract(scene_number=20, description="Antiga 20")
        c3 = SceneContract(scene_number=30, description="Antiga 30")
        svc.create(c1)
        svc.create(c2)
        svc.create(c3)

        reordered = svc.reorder([c3.id, c1.id, c2.id])
        assert len(reordered) == 3
        assert reordered[0].scene_number == 1
        assert reordered[0].id == c3.id
        assert reordered[1].scene_number == 2
        assert reordered[1].id == c1.id
        assert reordered[2].scene_number == 3
        assert reordered[2].id == c2.id

    def test_reorder_increments_version(self):
        svc = SceneContractService()
        c = SceneContract(scene_number=5, description="Cena")
        cid = svc.create(c)
        old_version = c.version
        svc.reorder([cid])
        assert svc.get(cid).version == old_version + 1

    def test_reorder_skips_invalid_ids(self):
        svc = SceneContractService()
        c = SceneContract(scene_number=1, description="Cena")
        svc.create(c)
        reordered = svc.reorder(["sc_invalid", c.id])
        assert len(reordered) == 1
        assert reordered[0].scene_number == 1

    def test_count(self):
        svc = SceneContractService()
        assert svc.count() == 0
        svc.create(SceneContract(scene_number=1, description="Cena 1"))
        assert svc.count() == 1
        svc.create(SceneContract(scene_number=2, description="Cena 2"))
        assert svc.count() == 2

    def test_clear(self):
        svc = SceneContractService()
        svc.create(SceneContract(scene_number=1, description="Cena 1"))
        svc.create(SceneContract(scene_number=2, description="Cena 2"))
        assert svc.count() == 2
        svc.clear()
        assert svc.count() == 0

    def test_version_increments_on_update(self):
        svc = SceneContractService()
        c = SceneContract(scene_number=1, description="Versão 1")
        cid = svc.create(c)
        assert svc.get(cid).version == 1
        svc.update(cid, description="Versão 2")
        assert svc.get(cid).version == 2
        svc.update(cid, notes="Melhorada")
        assert svc.get(cid).version == 3

    def test_ingredients_list_empty_by_default(self):
        svc = SceneContractService()
        c = SceneContract(scene_number=1, description="Cena sem ingredientes")
        cid = svc.create(c)
        assert svc.get(cid).ingredients == []
        assert svc.get_contracts_for_ingredient("qualquer") == []
