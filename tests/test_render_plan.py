"""Tests for RenderPlan (RND-600) and GpuProfile (RND-602)."""

from app.domain.render_plan import (
    EngineSelectionReason,
    EngineType,
    GpuProfile,
    GpuProfileCatalog,
    RenderPlan,
    RenderPlanService,
    RenderQuality,
    SceneRenderAssignment,
)


class TestSceneRenderAssignment:
    """SceneRenderAssignment schema tests."""

    def test_create_with_minimal_fields(self):
        sra = SceneRenderAssignment(
            scene_number=1,
            scene_contract_id="sc_abc123",
            engine=EngineType.FFMPEG,
            reason=EngineSelectionReason.FALLBACK_NO_GPU,
        )
        assert sra.scene_number == 1
        assert sra.scene_contract_id == "sc_abc123"
        assert sra.engine == EngineType.FFMPEG
        assert sra.reason == EngineSelectionReason.FALLBACK_NO_GPU
        assert sra.id.startswith("sra_")

    def test_create_with_all_fields(self):
        sra = SceneRenderAssignment(
            scene_number=2,
            scene_contract_id="sc_def456",
            engine=EngineType.WAN_GP,
            reason=EngineSelectionReason.PREFERRED_AVAILABLE,
            reason_detail="WanGP disponivel e VRAM suficiente",
            estimated_vram_mb=3072,
            quality=RenderQuality.HIGH,
        )
        assert sra.reason_detail == "WanGP disponivel e VRAM suficiente"
        assert sra.estimated_vram_mb == 3072
        assert sra.quality == RenderQuality.HIGH


class TestRenderPlan:
    """RenderPlan schema tests."""

    def test_create_empty_plan(self):
        plan = RenderPlan()
        assert plan.id.startswith("rp_")
        assert plan.assignments == []
        assert plan.vram_total_mb == 6144
        assert plan.gpu_profile == "GTX 1660 Super (6GB)"

    def test_create_with_assignments(self):
        sra = SceneRenderAssignment(
            scene_number=1,
            scene_contract_id="sc_abc",
            engine=EngineType.FFMPEG,
            reason=EngineSelectionReason.FALLBACK_NO_GPU,
        )
        plan = RenderPlan(
            project_id="proj_001",
            assignments=[sra],
            quality=RenderQuality.DRAFT,
        )
        assert len(plan.assignments) == 1
        assert plan.project_id == "proj_001"
        assert plan.quality == RenderQuality.DRAFT

    def test_plan_has_version_and_timestamp(self):
        plan = RenderPlan()
        assert plan.version == 1
        assert plan.created_at is not None


class TestRenderPlanService:
    """RenderPlanService tests."""

    def test_generate_plan_ffmpeg_fallback_when_no_gpu(self):
        service = RenderPlanService()
        plan = service.generate_plan(
            scene_ids=["sc_1", "sc_2"],
            engine_availability={"wangp": False, "ffmpeg": True},
        )
        assert len(plan.assignments) == 2
        for a in plan.assignments:
            assert a.engine == EngineType.FFMPEG
            assert a.reason == EngineSelectionReason.FALLBACK_NO_GPU

    def test_generate_plan_wangp_when_available(self):
        service = RenderPlanService()
        plan = service.generate_plan(
            scene_ids=["sc_1"],
            engine_availability={"wangp": True, "ffmpeg": True},
        )
        assert len(plan.assignments) == 1
        assert plan.assignments[0].engine == EngineType.WAN_GP
        assert plan.assignments[0].reason == EngineSelectionReason.PREFERRED_AVAILABLE

    def test_generate_plan_wangp_high_quality(self):
        service = RenderPlanService()
        plan = service.generate_plan(
            scene_ids=["sc_1"],
            engine_availability={"wangp": True, "ffmpeg": True},
            quality=RenderQuality.HIGH,
        )
        assert plan.assignments[0].engine == EngineType.WAN_GP
        assert plan.assignments[0].reason == EngineSelectionReason.QUALITY_PROFILE

    def test_fallback_when_vram_insufficient(self):
        profile = GpuProfile(
            name="Low VRAM (1GB)",
            vram_total_mb=1024,
            max_resolution=(480, 360),
            recommended_resolution=(480, 360),
            wangp_vram_per_scene_mb=3072,
        )
        service = RenderPlanService(gpu_profile=profile)
        plan = service.generate_plan(
            scene_ids=["sc_1"],
            engine_availability={"wangp": True, "ffmpeg": True},
        )
        assert plan.assignments[0].engine == EngineType.FFMPEG
        assert plan.assignments[0].reason == EngineSelectionReason.FALLBACK_VRAM_LIMIT
        assert "VRAM" in plan.assignments[0].reason_detail

    def test_fallback_when_no_engine_available(self):
        service = RenderPlanService()
        plan = service.generate_plan(
            scene_ids=["sc_1"],
            engine_availability={"wangp": False, "ffmpeg": False},
        )
        assert plan.assignments[0].engine == EngineType.FFMPEG
        assert plan.assignments[0].reason == EngineSelectionReason.FALLBACK_UNAVAILABLE

    def test_generate_plan_with_default_availability(self):
        service = RenderPlanService()
        plan = service.generate_plan(scene_ids=["sc_1", "sc_2", "sc_3"])
        # Default: wangp=False, ffmpeg=True
        assert len(plan.assignments) == 3
        for a in plan.assignments:
            assert a.engine == EngineType.FFMPEG

    def test_scene_numbers_are_sequential(self):
        service = RenderPlanService()
        plan = service.generate_plan(
            scene_ids=["sc_a", "sc_b", "sc_c"],
            engine_availability={"wangp": False, "ffmpeg": True},
        )
        for i, a in enumerate(plan.assignments):
            assert a.scene_number == i + 1

    def test_get_plan_by_id(self):
        service = RenderPlanService()
        plan = service.generate_plan(
            scene_ids=["sc_1"],
            engine_availability={"wangp": False, "ffmpeg": True},
        )
        retrieved = service.get_plan(plan.id)
        assert retrieved is not None
        assert retrieved.id == plan.id

    def test_get_plan_not_found(self):
        service = RenderPlanService()
        assert service.get_plan("nonexistent") is None

    def test_list_plans(self):
        service = RenderPlanService()
        plan1 = service.generate_plan(scene_ids=["sc_1"], engine_availability={"wangp": False, "ffmpeg": True})
        plan2 = service.generate_plan(scene_ids=["sc_2"], engine_availability={"wangp": True, "ffmpeg": True})
        plans = service.list_plans()
        assert len(plans) == 2
        assert plan1.id in [p.id for p in plans]
        assert plan2.id in [p.id for p in plans]

    def test_vram_estimate_per_engine(self):
        service = RenderPlanService()
        assert service._estimate_vram(EngineType.WAN_GP) == 3072
        assert service._estimate_vram(EngineType.FFMPEG) == 128
        assert service._estimate_vram(EngineType.VACE) == 2048

    def test_generate_plan_stores_project_id(self):
        service = RenderPlanService()
        plan = service.generate_plan(
            scene_ids=["sc_1"],
            project_id="proj_rnd_600",
            engine_availability={"wangp": False, "ffmpeg": True},
        )
        assert plan.project_id == "proj_rnd_600"

    def test_generate_plan_draft_quality_still_uses_fallback(self):
        service = RenderPlanService()
        plan = service.generate_plan(
            scene_ids=["sc_1"],
            engine_availability={"wangp": False, "ffmpeg": True},
            quality=RenderQuality.DRAFT,
        )
        assert plan.assignments[0].engine == EngineType.FFMPEG
        assert plan.quality == RenderQuality.DRAFT


class TestGpuProfile:
    """GpuProfile dataclass tests (RND-602)."""

    def test_create_gpu_profile(self):
        profile = GpuProfile(
            name="Test GPU (4GB)",
            vram_total_mb=4096,
            max_resolution=(640, 480),
            recommended_resolution=(480, 360),
            wangp_vram_per_scene_mb=2048,
        )
        assert profile.name == "Test GPU (4GB)"
        assert profile.vram_total_mb == 4096
        assert profile.max_resolution == (640, 480)
        assert profile.recommended_resolution == (480, 360)
        assert profile.wangp_vram_per_scene_mb == 2048
        assert profile.ffmpeg_vram_per_scene_mb == 128
        assert profile.vace_vram_per_scene_mb == 2048

    def test_gpu_profile_default_constants(self):
        profile = GpuProfile(
            name="Minimal",
            vram_total_mb=512,
            max_resolution=(320, 240),
            recommended_resolution=(320, 240),
            wangp_vram_per_scene_mb=0,
        )
        assert profile.ffmpeg_vram_per_scene_mb == 128
        assert profile.vace_vram_per_scene_mb == 2048


class TestGpuProfileCatalog:
    """GpuProfileCatalog tests (RND-602)."""

    def test_get_default_profile(self):
        profile = GpuProfileCatalog.get_default()
        assert profile is not None
        assert profile.name == "GTX 1660 Super (6GB)"
        assert profile.vram_total_mb == 6144

    def test_get_profile_by_name(self):
        profile = GpuProfileCatalog.get("RTX 3060 (12GB)")
        assert profile is not None
        assert profile.vram_total_mb == 12288
        assert profile.max_resolution == (1024, 576)
        assert profile.recommended_resolution == (832, 512)
        assert profile.wangp_vram_per_scene_mb == 4096

    def test_get_profile_not_found(self):
        profile = GpuProfileCatalog.get("NonExistent GPU")
        assert profile is None

    def test_list_profiles(self):
        profiles = GpuProfileCatalog.list_profiles()
        assert len(profiles) == 3
        names = [p.name for p in profiles]
        assert "GTX 1660 Super (6GB)" in names
        assert "RTX 3060 (12GB)" in names
        assert "Fallback (CPU/FFmpeg)" in names

    def test_get_profile_for_vram_exact_match(self):
        profile = GpuProfileCatalog.get_profile_for_vram(6144)
        assert profile.name == "GTX 1660 Super (6GB)"

    def test_get_profile_for_vram_above_all(self):
        profile = GpuProfileCatalog.get_profile_for_vram(24000)
        assert profile.name == "RTX 3060 (12GB)"

    def test_get_profile_for_vram_below_minimum(self):
        profile = GpuProfileCatalog.get_profile_for_vram(256)
        assert profile.name == "Fallback (CPU/FFmpeg)"


class TestRenderPlanResolution:
    """Resolution selection tests (RND-602)."""

    def test_standard_resolution_uses_recommended(self):
        profile = GpuProfileCatalog.get("GTX 1660 Super (6GB)")
        service = RenderPlanService(gpu_profile=profile)
        plan = service.generate_plan(
            scene_ids=["sc_1"],
            engine_availability={"wangp": False, "ffmpeg": True},
            quality=RenderQuality.STANDARD,
        )
        assert plan.assignments[0].resolution == (640, 480)
        assert plan.max_resolution == (832, 512)

    def test_high_resolution_uses_max(self):
        profile = GpuProfileCatalog.get("GTX 1660 Super (6GB)")
        service = RenderPlanService(gpu_profile=profile)
        plan = service.generate_plan(
            scene_ids=["sc_1"],
            engine_availability={"wangp": True, "ffmpeg": True},
            quality=RenderQuality.HIGH,
        )
        assert plan.assignments[0].resolution == (832, 512)

    def test_draft_resolution_is_low(self):
        profile = GpuProfileCatalog.get("GTX 1660 Super (6GB)")
        service = RenderPlanService(gpu_profile=profile)
        plan = service.generate_plan(
            scene_ids=["sc_1"],
            engine_availability={"wangp": False, "ffmpeg": True},
            quality=RenderQuality.DRAFT,
        )
        assert plan.assignments[0].resolution == (480, 360)

    def test_rtx_3060_high_resolution(self):
        profile = GpuProfileCatalog.get("RTX 3060 (12GB)")
        service = RenderPlanService(gpu_profile=profile)
        plan = service.generate_plan(
            scene_ids=["sc_1"],
            engine_availability={"wangp": True, "ffmpeg": True},
            quality=RenderQuality.HIGH,
        )
        assert plan.assignments[0].resolution == (1024, 576)

    def test_rtx_3060_standard_resolution(self):
        profile = GpuProfileCatalog.get("RTX 3060 (12GB)")
        service = RenderPlanService(gpu_profile=profile)
        plan = service.generate_plan(
            scene_ids=["sc_1"],
            engine_availability={"wangp": True, "ffmpeg": True},
            quality=RenderQuality.STANDARD,
        )
        assert plan.assignments[0].resolution == (832, 512)


class TestRenderPlanGpuProfile:
    """GPU profile integration tests (RND-602)."""

    def test_service_uses_default_profile(self):
        service = RenderPlanService()
        assert service.gpu_profile.name == "GTX 1660 Super (6GB)"
        assert service.gpu_profile.vram_total_mb == 6144

    def test_service_with_custom_vram_uses_gtx_1660_super_default(self):
        service = RenderPlanService(vram_total_mb=4096)
        assert service.gpu_profile.name == "GTX 1660 Super (6GB)"

    def test_generate_plan_with_rtx_3060_profile(self):
        profile = GpuProfileCatalog.get("RTX 3060 (12GB)")
        service = RenderPlanService(gpu_profile=profile)
        plan = service.generate_plan(
            scene_ids=["sc_1", "sc_2"],
            project_id="proj_rnd_602",
            engine_availability={"wangp": True, "ffmpeg": True},
        )
        assert plan.gpu_profile == "RTX 3060 (12GB)"
        assert plan.vram_total_mb == 12288
        assert plan.assignments[0].engine == EngineType.WAN_GP
        assert plan.assignments[0].estimated_vram_mb == 4096

    def test_profile_estimates_vram_per_engine(self):
        profile = GpuProfileCatalog.get("GTX 1660 Super (6GB)")
        service = RenderPlanService(gpu_profile=profile)
        assert service._estimate_vram(EngineType.WAN_GP, profile) == 3072
        assert service._estimate_vram(EngineType.FFMPEG, profile) == 128
        assert service._estimate_vram(EngineType.VACE, profile) == 2048

    def test_rtx_3060_estimates_vram_per_engine(self):
        profile = GpuProfileCatalog.get("RTX 3060 (12GB)")
        service = RenderPlanService(gpu_profile=profile)
        assert service._estimate_vram(EngineType.WAN_GP, profile) == 4096
        assert service._estimate_vram(EngineType.FFMPEG, profile) == 128
        assert service._estimate_vram(EngineType.VACE, profile) == 2048

    def test_fallback_profile_vram(self):
        profile = GpuProfileCatalog.get("Fallback (CPU/FFmpeg)")
        service = RenderPlanService(gpu_profile=profile)
        plan = service.generate_plan(
            scene_ids=["sc_1"],
            engine_availability={"wangp": True, "ffmpeg": True},
        )
        assert plan.assignments[0].engine == EngineType.FFMPEG
        assert plan.assignments[0].reason == EngineSelectionReason.FALLBACK_VRAM_LIMIT

    def test_generate_plan_overrides_profile(self):
        service = RenderPlanService()
        rtx_profile = GpuProfileCatalog.get("RTX 3060 (12GB)")
        plan = service.generate_plan(
            scene_ids=["sc_1"],
            engine_availability={"wangp": True, "ffmpeg": True},
            gpu_profile=rtx_profile,
        )
        assert plan.assignments[0].estimated_vram_mb == 4096
        assert plan.gpu_profile == "RTX 3060 (12GB)"

    def test_plan_stores_max_resolution_from_profile(self):
        profile = GpuProfileCatalog.get("RTX 3060 (12GB)")
        service = RenderPlanService(gpu_profile=profile)
        plan = service.generate_plan(
            scene_ids=["sc_1"],
            engine_availability={"wangp": False, "ffmpeg": True},
        )
        assert plan.max_resolution == (1024, 576)
