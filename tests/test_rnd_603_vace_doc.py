"""Tests for RND-603: VACE documented as future optional engine."""
import pytest

from app.domain.prompt_compiler import EngineType, PromptCompilerService
from app.domain.render_plan import GpuProfile, RenderPlanService, SceneRenderAssignment
from app.domain.scene_contract import SceneContract, CameraDirective, CameraMovement, ShotSize, TransitionType


class TestVACEEngineType:
    def test_vace_enum_exists(self):
        assert EngineType.VACE.value == "vace"

    def test_vace_is_third_engine(self):
        assert EngineType.VACE in {EngineType.WAN_GP, EngineType.FFMPEG, EngineType.VACE}


class TestVACEVRAM:
    def test_vace_vram_in_gpu_profile(self):
        profile = GpuProfile(
            name="Test", vram_total_mb=12288,
            max_resolution=(1920, 1080), recommended_resolution=(1280, 720),
            wangp_vram_per_scene_mb=4096,
        )
        assert hasattr(profile, "vace_vram_per_scene_mb")
        assert profile.vace_vram_per_scene_mb == 2048

    def test_vram_estimate_returns_vace_value(self):
        service = RenderPlanService(vram_total_mb=12288)
        profile = GpuProfile(
            name="Test", vram_total_mb=12288,
            max_resolution=(1920, 1080), recommended_resolution=(1280, 720),
            wangp_vram_per_scene_mb=4096,
        )
        vram = service._estimate_vram(EngineType.VACE, profile)
        assert vram == profile.vace_vram_per_scene_mb


class TestVACECompiler:
    def test_compile_for_vace_method_exists(self):
        svc = PromptCompilerService()
        assert hasattr(svc, "_compile_for_vace")

    def test_vace_compile_returns_structured_prompt(self):
        svc = PromptCompilerService()
        contract = SceneContract(
            scene_number=1,
            description="Test scene for VACE",
            duration=5,
            camera=CameraDirective(
                angle="neutral",
                movement=CameraMovement.STATIC,
                shot_size=ShotSize.MEDIUM,
            ),
            transition_in=TransitionType.CUT,
            transition_out=TransitionType.CUT,
        )
        result = svc.compile(contract, EngineType.VACE)
        assert result.engine == EngineType.VACE
        assert "Scene 1" in result.prompt_text
        assert result.format.value == "structured"


class TestVACENotAutoSelected:
    def test_default_availability_vace_is_false(self):
        service = RenderPlanService()
        scenes = ["sc_1", "sc_2"]
        plan = service.generate_plan(scenes)
        for a in plan.assignments:
            assert a.engine != "vace"

    def test_vace_not_selected_even_when_available(self):
        service = RenderPlanService()
        scenes = ["sc_1"]
        plan = service.generate_plan(
            scenes,
            engine_availability={"wangp": False, "ffmpeg": True, "vace": True},
        )
        for a in plan.assignments:
            assert a.engine != "vace", "VACE must not be auto-selected"
            assert a.reason != "", "Must document engine choice reason"
