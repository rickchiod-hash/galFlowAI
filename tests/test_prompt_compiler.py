"""Tests for PromptCompiler domain schema (VIS-503).

Cobre compilação de SceneContract para engines WanGP, FFmpeg, VACE,
parâmetros específicos, registry de prompts compilados.
"""

import pytest
from app.domain.scene_contract import (
    CameraDirective,
    CameraMovement,
    IngredientAssignment,
    SceneContract,
    SceneContractStatus,
    ShotSize,
    TransitionType,
)
from app.domain.prompt_compiler import (
    CompiledPrompt,
    EngineParameter,
    EngineType,
    PromptCompilerService,
    PromptFormat,
)


def make_contract(
    scene_number: int = 1,
    description: str = "Cena de teste",
    **kwargs,
) -> SceneContract:
    """Helper para criar SceneContract de teste."""
    return SceneContract(scene_number=scene_number, description=description, **kwargs)


class TestEngineTypes:
    def test_all_engines_defined(self):
        assert EngineType.WAN_GP.value == "wangp"
        assert EngineType.FFMPEG.value == "ffmpeg"
        assert EngineType.VACE.value == "vace"

    def test_engine_count(self):
        assert len(EngineType) == 3


class TestPromptFormat:
    def test_all_formats_defined(self):
        assert PromptFormat.PLAIN_TEXT.value == "plain_text"
        assert PromptFormat.STRUCTURED.value == "structured"
        assert PromptFormat.JSON.value == "json"

    def test_format_count(self):
        assert len(PromptFormat) == 3


class TestCompiledPromptSchema:
    def test_minimal_prompt(self):
        p = CompiledPrompt(
            scene_contract_id="sc_abc",
            engine=EngineType.WAN_GP,
            prompt_text="Cena de ação",
        )
        assert p.id.startswith("cp_")
        assert p.scene_contract_id == "sc_abc"
        assert p.engine == EngineType.WAN_GP
        assert p.prompt_text == "Cena de ação"
        assert p.negative_prompt == ""
        assert p.parameters == []
        assert p.format == PromptFormat.PLAIN_TEXT
        assert p.version == 1

    def test_full_prompt(self):
        p = CompiledPrompt(
            scene_contract_id="sc_xyz",
            engine=EngineType.FFMPEG,
            prompt_text="Cena estática",
            negative_prompt="borrão",
            parameters=[
                EngineParameter(key="duration", value=5, description="Duração"),
            ],
            format=PromptFormat.STRUCTURED,
        )
        assert p.engine == EngineType.FFMPEG
        assert p.negative_prompt == "borrão"
        assert len(p.parameters) == 1
        assert p.parameters[0].key == "duration"
        assert p.format == PromptFormat.STRUCTURED

    def test_unique_ids(self):
        p1 = CompiledPrompt(scene_contract_id="sc_1", engine=EngineType.WAN_GP, prompt_text="A")
        p2 = CompiledPrompt(scene_contract_id="sc_2", engine=EngineType.WAN_GP, prompt_text="B")
        assert p1.id != p2.id

    def test_all_engines_in_prompt(self):
        for engine in EngineType:
            p = CompiledPrompt(scene_contract_id="sc_1", engine=engine, prompt_text="teste")
            assert p.engine == engine


class TestPromptCompilerWanGP:
    def test_basic_description_included(self):
        svc = PromptCompilerService()
        contract = make_contract(description="Close-up dramático do produto")
        result = svc.compile(contract, EngineType.WAN_GP)
        assert "Close-up dramático do produto" in result.prompt_text
        assert result.engine == EngineType.WAN_GP

    def test_camera_directive_included(self):
        svc = PromptCompilerService()
        contract = make_contract(
            camera=CameraDirective(
                angle="low",
                movement=CameraMovement.DOLLY,
                shot_size=ShotSize.CLOSE_UP,
                notes="zoom dramático",
            )
        )
        result = svc.compile(contract, EngineType.WAN_GP)
        assert "ângulo low" in result.prompt_text
        assert "movimento dolly" in result.prompt_text
        assert "plano close up" in result.prompt_text
        assert "zoom dramático" in result.prompt_text

    def test_ingredients_included(self):
        svc = PromptCompilerService()
        contract = make_contract(
            ingredients=[
                IngredientAssignment(
                    ingredient_id="ing_001",
                    ingredient_name="Smartphone X",
                    placement="centro, destaque",
                ),
            ]
        )
        result = svc.compile(contract, EngineType.WAN_GP)
        assert "Smartphone X" in result.prompt_text
        assert "centro, destaque" in result.prompt_text

    def test_style_included(self):
        svc = PromptCompilerService()
        contract = make_contract(style="cinematic, slow motion")
        result = svc.compile(contract, EngineType.WAN_GP)
        assert "cinematic, slow motion" in result.prompt_text

    def test_positive_prompt_appended(self):
        svc = PromptCompilerService()
        contract = make_contract(
            prompt_positive="iluminação dramática, cores vibrantes"
        )
        result = svc.compile(contract, EngineType.WAN_GP)
        assert "iluminação dramática, cores vibrantes" in result.prompt_text

    def test_negative_prompt_uses_contract(self):
        svc = PromptCompilerService()
        contract = make_contract(prompt_negative="borrão, baixa qualidade")
        result = svc.compile(contract, EngineType.WAN_GP)
        assert result.negative_prompt == "borrão, baixa qualidade"

    def test_negative_prompt_default(self):
        svc = PromptCompilerService()
        contract = make_contract()
        result = svc.compile(contract, EngineType.WAN_GP)
        assert "blurry" in result.negative_prompt
        assert "low quality" in result.negative_prompt

    def test_duration_parameter(self):
        svc = PromptCompilerService()
        contract = make_contract()
        contract.duration = 8
        result = svc.compile(contract, EngineType.WAN_GP)
        params = {p.key: p.value for p in result.parameters}
        assert params["duration"] == 8

    def test_transition_parameters(self):
        svc = PromptCompilerService()
        contract = make_contract(
            transition_in=TransitionType.FADE,
            transition_out=TransitionType.DISSOLVE,
        )
        result = svc.compile(contract, EngineType.WAN_GP)
        params = {p.key: p.value for p in result.parameters}
        assert params["transition_in"] == "fade"
        assert params["transition_out"] == "dissolve"

    def test_visual_bible_references_in_parameters(self):
        svc = PromptCompilerService()
        contract = make_contract(
            ingredients=[
                IngredientAssignment(
                    ingredient_id="ing_001",
                    ingredient_name="Produto",
                    visual_bible_ref="bbl_001",
                ),
                IngredientAssignment(
                    ingredient_id="ing_002",
                    ingredient_name="Cenário",
                ),
            ]
        )
        result = svc.compile(contract, EngineType.WAN_GP)
        params = {p.key: p.value for p in result.parameters}
        assert params.get("visual_bible_ref_ing_001") == "bbl_001"
        assert "visual_bible_ref_ing_002" not in params

    def test_format_is_structured(self):
        svc = PromptCompilerService()
        contract = make_contract()
        result = svc.compile(contract, EngineType.WAN_GP)
        assert result.format == PromptFormat.STRUCTURED

    def test_compile_all_wangp(self):
        svc = PromptCompilerService()
        contracts = [
            make_contract(scene_number=1, description="Cena 1"),
            make_contract(scene_number=2, description="Cena 2"),
        ]
        results = svc.compile_all(contracts, EngineType.WAN_GP)
        assert len(results) == 2
        assert all(r.engine == EngineType.WAN_GP for r in results)


class TestPromptCompilerFFmpeg:
    def test_basic_description(self):
        svc = PromptCompilerService()
        contract = make_contract(description="Cena com texto")
        result = svc.compile(contract, EngineType.FFMPEG)
        assert result.prompt_text == "Cena com texto"
        assert result.engine == EngineType.FFMPEG

    def test_text_overlay_parameter(self):
        svc = PromptCompilerService()
        contract = make_contract(description="Cena principal do comercial")
        result = svc.compile(contract, EngineType.FFMPEG)
        params = {p.key: p.value for p in result.parameters}
        assert "Cena principal do comercial" in params["text_overlay"]

    def test_duration_parameter(self):
        svc = PromptCompilerService()
        contract = make_contract()
        contract.duration = 10
        result = svc.compile(contract, EngineType.FFMPEG)
        params = {p.key: p.value for p in result.parameters}
        assert params["duration"] == 10

    def test_transition_parameters(self):
        svc = PromptCompilerService()
        contract = make_contract(
            transition_in=TransitionType.WIPE,
            transition_out=TransitionType.CUT,
        )
        result = svc.compile(contract, EngineType.FFMPEG)
        params = {p.key: p.value for p in result.parameters}
        assert params["transition_in"] == "wipe"
        assert params["transition_out"] == "cut"

    def test_style_parameter(self):
        svc = PromptCompilerService()
        contract = make_contract(style="clean, minimal")
        result = svc.compile(contract, EngineType.FFMPEG)
        params = {p.key: p.value for p in result.parameters}
        assert params["style"] == "clean, minimal"

    def test_no_style_parameter(self):
        svc = PromptCompilerService()
        contract = make_contract()
        result = svc.compile(contract, EngineType.FFMPEG)
        params = {p.key: p.value for p in result.parameters}
        assert "style" not in params

    def test_negative_prompt_empty_for_ffmpeg(self):
        svc = PromptCompilerService()
        contract = make_contract()
        result = svc.compile(contract, EngineType.FFMPEG)
        assert result.negative_prompt == ""

    def test_format_is_structured(self):
        svc = PromptCompilerService()
        contract = make_contract()
        result = svc.compile(contract, EngineType.FFMPEG)
        assert result.format == PromptFormat.STRUCTURED

    def test_text_overlay_truncated(self):
        svc = PromptCompilerService()
        long_desc = "X" * 500
        contract = make_contract(description=long_desc)
        result = svc.compile(contract, EngineType.FFMPEG)
        params = {p.key: p.value for p in result.parameters}
        assert len(params["text_overlay"]) == 200


class TestPromptCompilerVACE:
    def test_basic_structure(self):
        svc = PromptCompilerService()
        contract = make_contract(scene_number=3, description="Cena VACE")
        result = svc.compile(contract, EngineType.VACE)
        assert "Scene 3" in result.prompt_text
        assert "Cena VACE" in result.prompt_text
        assert result.engine == EngineType.VACE

    def test_camera_parameters(self):
        svc = PromptCompilerService()
        contract = make_contract(
            camera=CameraDirective(
                angle="high",
                movement=CameraMovement.PAN,
                shot_size=ShotSize.WIDE,
            )
        )
        result = svc.compile(contract, EngineType.VACE)
        params = {p.key: p.value for p in result.parameters}
        assert params["camera_angle"] == "high"
        assert params["camera_movement"] == "pan"
        assert params["shot_size"] == "wide"

    def test_ingredients_included(self):
        svc = PromptCompilerService()
        contract = make_contract(
            ingredients=[
                IngredientAssignment(ingredient_id="ing_001", ingredient_name="Carro"),
            ]
        )
        result = svc.compile(contract, EngineType.VACE)
        assert "Carro" in result.prompt_text

    def test_duration_parameter(self):
        svc = PromptCompilerService()
        contract = make_contract()
        contract.duration = 15
        result = svc.compile(contract, EngineType.VACE)
        params = {p.key: p.value for p in result.parameters}
        assert params["duration"] == 15

    def test_format_is_structured(self):
        svc = PromptCompilerService()
        contract = make_contract()
        result = svc.compile(contract, EngineType.VACE)
        assert result.format == PromptFormat.STRUCTURED


class TestMultiEngineCompilation:
    def test_compile_multi_engine(self):
        svc = PromptCompilerService()
        contract = make_contract()
        results = svc.compile_multi_engine(
            contract,
            [EngineType.WAN_GP, EngineType.FFMPEG, EngineType.VACE],
        )
        assert len(results) == 3
        engines = {r.engine for r in results}
        assert engines == {EngineType.WAN_GP, EngineType.FFMPEG, EngineType.VACE}

    def test_compile_multi_engine_all_have_same_contract_id(self):
        svc = PromptCompilerService()
        contract = make_contract()
        results = svc.compile_multi_engine(contract, list(EngineType))
        assert all(r.scene_contract_id == contract.id for r in results)


class TestPromptCompilerRegistry:
    def test_save_and_get(self):
        svc = PromptCompilerService()
        contract = make_contract()
        result = svc.compile(contract, EngineType.WAN_GP)
        cid = svc.save(result)
        assert svc.get(cid).id == result.id

    def test_get_nonexistent(self):
        svc = PromptCompilerService()
        assert svc.get("cp_nonexistent") is None

    def test_list_by_engine(self):
        svc = PromptCompilerService()
        c1 = make_contract(scene_number=1, description="Cena 1")
        c2 = make_contract(scene_number=2, description="Cena 2")
        svc.save(svc.compile(c1, EngineType.WAN_GP))
        svc.save(svc.compile(c2, EngineType.WAN_GP))
        svc.save(svc.compile(c1, EngineType.FFMPEG))
        assert len(svc.list_by_engine(EngineType.WAN_GP)) == 2
        assert len(svc.list_by_engine(EngineType.FFMPEG)) == 1
        assert len(svc.list_by_engine(EngineType.VACE)) == 0

    def test_list_by_contract(self):
        svc = PromptCompilerService()
        c1 = make_contract(scene_number=1, description="Cena 1")
        c2 = make_contract(scene_number=2, description="Cena 2")
        svc.save(svc.compile(c1, EngineType.WAN_GP))
        svc.save(svc.compile(c1, EngineType.FFMPEG))
        svc.save(svc.compile(c2, EngineType.WAN_GP))
        c1_prompts = svc.list_by_contract(c1.id)
        assert len(c1_prompts) == 2
        c2_prompts = svc.list_by_contract(c2.id)
        assert len(c2_prompts) == 1

    def test_clear(self):
        svc = PromptCompilerService()
        contract = make_contract()
        svc.save(svc.compile(contract, EngineType.WAN_GP))
        assert len(svc.list_by_engine(EngineType.WAN_GP)) == 1
        svc.clear()
        assert len(svc.list_by_engine(EngineType.WAN_GP)) == 0


class TestEngineParameter:
    def test_minimal(self):
        p = EngineParameter(key="duration", value=5)
        assert p.key == "duration"
        assert p.value == 5
        assert p.description == ""

    def test_full(self):
        p = EngineParameter(
            key="resolution",
            value="1920x1080",
            description="Resolução do vídeo",
        )
        assert p.description == "Resolução do vídeo"


class TestCompilationError:
    def test_unsupported_engine(self):
        svc = PromptCompilerService()
        contract = make_contract()
        with pytest.raises(ValueError, match="Unsupported engine"):
            svc.compile(contract, "invalid_engine")  # type: ignore
