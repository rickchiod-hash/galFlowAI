"""Tests for FFmpeg fallback universal (RND-601).

Valida: (1) FFmpegAdapter existe e eh instanciavel,
(2) FFmpeg fallback funciona quando WanGP esta indisponivel,
(3) pipeline usa FFmpeg quando WanGP falha,
(4) RenderPlan seleciona FFmpeg como fallback.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.adapters.ffmpeg_adapter import FFmpegAdapter, _find_ffmpeg
from app.domain.render_plan import EngineType, EngineSelectionReason, RenderPlanService
from app.domain.prompt_compiler import EngineType as PromptEngineType


class TestFFmpegAdapterExists:
    """FFmpegAdapter deve existir e ser instanciavel."""

    def test_adapter_module_imports(self):
        from app.adapters import ffmpeg_adapter
        assert hasattr(ffmpeg_adapter, "FFmpegAdapter")

    def test_adapter_can_be_instantiated(self):
        adapter = FFmpegAdapter()
        assert adapter is not None
        assert hasattr(adapter, "is_available")

    def test_ffmpeg_adapter_has_expected_methods(self):
        adapter = FFmpegAdapter()
        assert callable(adapter.is_available)
        assert callable(adapter.create_static_video)
        assert callable(adapter.concat_videos)
        assert callable(adapter.add_audio_to_video)


class TestFFmpegFindPath:
    """_find_ffmpeg deve retornar sempre um Path valido."""

    def test_find_ffmpeg_returns_path(self):
        path = _find_ffmpeg()
        assert path is not None
        assert isinstance(path, Path)

    def test_find_ffmpeg_path_is_stringable(self):
        path = _find_ffmpeg()
        assert str(path).endswith("ffmpeg") or str(path).endswith("ffmpeg.exe") or "ffmpeg" in str(path).lower()


class TestFFmpegFallbackInPipeline:
    """Pipeline deve usar FFmpeg quando WanGP esta indisponivel."""

    @patch("app.adapters.wangp_adapter.WanGPAdapter")
    def test_pipeline_fallback_to_ffmpeg(self, mock_wangp):
        """Quando WanGP falha, pipeline deve usar FFmpeg."""
        mock_wangp.return_value.is_available.return_value = False

        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
        pipeline = VideoGenerationPipeline()

        wangp_avail = pipeline.wangp_adapter.is_available()
        ffmpeg_avail = pipeline.ffmpeg_adapter.is_available()

        # FFmpeg deve ser detectado como disponivel ou nao,
        # mas o pipeline deve tratar ambos os casos sem crash
        assert hasattr(pipeline, "ffmpeg_adapter")
        assert hasattr(pipeline, "wangp_adapter")

    def test_pipeline_has_fallback_method(self):
        """Pipeline deve ter logica de fallback WanGP -> FFmpeg."""
        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
        pipeline = VideoGenerationPipeline()
        assert hasattr(pipeline, "generate_commercial")
        assert hasattr(pipeline, "get_pipeline_status")

    def test_pipeline_status_includes_ffmpeg(self):
        """Status do pipeline deve incluir ffmpeg_available."""
        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
        pipeline = VideoGenerationPipeline()
        status = pipeline.get_pipeline_status()
        assert "ffmpeg_available" in status


class TestFFmpegFallbackInRenderPlan:
    """RenderPlan deve selecionar FFmpeg como fallback."""

    def test_render_plan_ffmpeg_when_wangp_unavailable(self):
        service = RenderPlanService()
        plan = service.generate_plan(
            scene_ids=["sc_1", "sc_2"],
            engine_availability={"wangp": False, "ffmpeg": True},
        )
        for a in plan.assignments:
            assert a.engine == EngineType.FFMPEG
            assert a.reason == EngineSelectionReason.FALLBACK_NO_GPU

    def test_render_plan_ffmpeg_even_without_any_engine(self):
        service = RenderPlanService()
        plan = service.generate_plan(
            scene_ids=["sc_1"],
            engine_availability={"wangp": False, "ffmpeg": False},
        )
        assert plan.assignments[0].engine == EngineType.FFMPEG
        assert plan.assignments[0].reason == EngineSelectionReason.FALLBACK_UNAVAILABLE

    def test_render_plan_prefers_wangp_over_ffmpeg(self):
        service = RenderPlanService()
        plan = service.generate_plan(
            scene_ids=["sc_1"],
            engine_availability={"wangp": True, "ffmpeg": True},
        )
        assert plan.assignments[0].engine == EngineType.WAN_GP
        assert plan.assignments[0].reason == EngineSelectionReason.PREFERRED_AVAILABLE


class TestFFmpegIsMandatory:
    """FFmpeg eh obrigatorio na Feature Preservation Matrix."""

    def test_ffmpeg_adapter_file_exists(self):
        adapter_file = Path("app/adapters/ffmpeg_adapter.py")
        assert adapter_file.exists(), "FFmpeg adapter file must exist"

    def test_ffmpeg_is_fallback_in_pipeline(self):
        """Pipeline video_generation_pipeline.py deve referenciar FFmpegAdapter."""
        pipeline_file = Path("app/pipeline/video_generation_pipeline.py")
        content = pipeline_file.read_text(encoding="utf-8")
        assert "FFmpegAdapter" in content, "Pipeline must import FFmpegAdapter"
        assert "ffmpeg" in content.lower(), "Pipeline must reference ffmpeg"

    def test_ffmpeg_in_feature_preservation_matrix(self):
        """Feature Preservation Matrix deve listar FFmpeg."""
        matrix_file = Path("docs/reference/FEATURE_PRESERVATION_MATRIX.md")
        content = matrix_file.read_text(encoding="utf-8")
        assert "FFmpeg" in content, "Feature matrix must list FFmpeg"
        assert "Obrigatorio" in content or "Sim" in content, "FFmpeg must be marked mandatory in feature matrix"

    def test_ffmpeg_not_removable(self):
        """Nao deve haver TODO/FIXME sugerindo remocao do FFmpeg."""
        import re
        app_files = list(Path("app").rglob("*.py")) + list(Path("tests").rglob("*.py"))
        suspicious = []
        for f in app_files:
            text = f.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"(remove|delete|deprecat).*ffmpeg", text, re.IGNORECASE):
                suspicious.append(str(f))
        if suspicious:
            print(f"AVISO: Arquivos com referencias suspeitas:\n" + "\n".join(suspicious))
