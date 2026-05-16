"""GAL-934: Mock E2E tests for WanGP -> FFmpeg fallback with error logging."""
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

from app.config import PROJECTS_DIR
from app.core.error_codes import ErrorCode

REPO_ROOT = Path(__file__).parent.parent


def _ensure_approved_script(project_id: str, script_text: str) -> None:
    approved_dir = PROJECTS_DIR / project_id / "script"
    approved_dir.mkdir(parents=True, exist_ok=True)
    (approved_dir / "script_approved.md").write_text(script_text, encoding="utf-8")


def test_wangp_fail_ffmpeg_fallback_logs_error():
    with (
        patch("app.services.error_jsonl_writer.ErrorJsonlWriter") as mock_writer_cls,
        patch("app.application.use_cases.render_all_scenes_use_case.RenderVideoUseCase") as mock_render_cls,
        patch("app.application.use_cases.render_all_scenes_use_case.CreateStaticVideoUseCase") as mock_static_cls,
        patch("app.pipeline.video_generation_pipeline.GenerateScriptUseCase") as mock_script_uc_cls,
        patch("app.pipeline.video_generation_pipeline.SplitScenesUseCase") as mock_split_uc_cls,
        patch("app.pipeline.video_generation_pipeline.BuildPromptsUseCase") as mock_build_uc_cls,
        patch("app.pipeline.video_generation_pipeline.GenerateAudioUseCase") as mock_audio_uc_cls,
        patch("app.pipeline.video_generation_pipeline.ConcatVideosUseCase") as mock_concat_uc_cls,
        patch("app.pipeline.video_generation_pipeline.WanGPAdapter") as mock_wangp_cls,
        patch("app.pipeline.video_generation_pipeline.TTSAdapter") as mock_tts_cls,
        patch("app.pipeline.video_generation_pipeline.FFmpegAdapter") as mock_ffmpeg_cls):
        mock_writer = MagicMock()
        mock_writer_cls.return_value = mock_writer

        mock_script_uc = MagicMock()
        mock_script_uc.execute.return_value = {"ok": True, "data": {"script": "Cena 1: Teste"}}
        mock_script_uc_cls.return_value = mock_script_uc

        mock_split_uc = MagicMock()
        mock_split_uc.execute.return_value = {
            "ok": True,
            "data": {"scenes": [{"id": 1, "prompt": "Prompt 1", "scene_text": "Scene 1", "duration": 5}]},
        }
        mock_split_uc_cls.return_value = mock_split_uc

        mock_build_uc = MagicMock()
        mock_build_uc.execute.return_value = {
            "ok": True,
            "data": {"scenes": [{"id": 1, "prompt": "Prompt 1", "scene_text": "Scene 1", "duration": 5}]},
        }
        mock_build_uc_cls.return_value = mock_build_uc

        mock_audio_uc = MagicMock()
        mock_audio_uc.execute.return_value = {"ok": True, "data": {"audio_path": "narration.wav"}}
        mock_audio_uc_cls.return_value = mock_audio_uc

        mock_render = MagicMock()
        mock_render.execute.return_value = {"ok": False, "error": "WanGP not available"}
        mock_render_cls.return_value = mock_render

        mock_static = MagicMock()
        mock_static.execute.return_value = {"ok": True, "data": {"video_path": "/tmp/scene_000.mp4"}}
        mock_static_cls.return_value = mock_static

        mock_concat_uc = MagicMock()
        mock_concat_uc.execute.return_value = {"ok": True, "data": {}}
        mock_concat_uc_cls.return_value = mock_concat_uc

        mock_wangp_cls.return_value = MagicMock()
        mock_tts_cls.return_value = MagicMock()
        mock_ffmpeg_cls.return_value = MagicMock()


        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline

        pipeline = VideoGenerationPipeline()
        _ensure_approved_script("test_gal934_wangp_fail", "Cena 1: Teste")

        result = pipeline.generate_commercial(
            project_id="test_gal934_wangp_fail",
            product="Teste",
            target_audience="Teste",
        )

        shutil.rmtree(PROJECTS_DIR / "test_gal934_wangp_fail", ignore_errors=True)

        assert result.get("success") is True, f"Pipeline failed: {result.get('error')}"
        assert mock_writer.write.called, "Error writer should have been called on fallback"

        calls = mock_writer.write.call_args_list
        codes = [c[0][0].code for c in calls]
        assert ErrorCode.WANGP_UNAVAILABLE in codes, (
            "WANGP_UNAVAILABLE should be recorded"
        )

        events = pipeline.render_all_scenes_uc._stage_logger.events
        assert any(
            e.event_type in ("warning", "failure") and "WanGP" in e.message
            for e in events
        ), "StageLogger should have WanGP fallback event"


def test_wangp_and_ffmpeg_both_fail_records_both():
    with (
        patch("app.services.error_jsonl_writer.ErrorJsonlWriter") as mock_writer_cls,
        patch("app.application.use_cases.render_all_scenes_use_case.RenderVideoUseCase") as mock_render_cls,
        patch("app.application.use_cases.render_all_scenes_use_case.CreateStaticVideoUseCase") as mock_static_cls,
        patch("app.pipeline.video_generation_pipeline.GenerateScriptUseCase") as mock_script_uc_cls,
        patch("app.pipeline.video_generation_pipeline.SplitScenesUseCase") as mock_split_uc_cls,
        patch("app.pipeline.video_generation_pipeline.BuildPromptsUseCase") as mock_build_uc_cls,
        patch("app.pipeline.video_generation_pipeline.GenerateAudioUseCase") as mock_audio_uc_cls,
        patch("app.pipeline.video_generation_pipeline.ConcatVideosUseCase") as mock_concat_uc_cls,
        patch("app.pipeline.video_generation_pipeline.WanGPAdapter") as mock_wangp_cls,
        patch("app.pipeline.video_generation_pipeline.TTSAdapter") as mock_tts_cls,
        patch("app.pipeline.video_generation_pipeline.FFmpegAdapter") as mock_ffmpeg_cls):
        mock_writer = MagicMock()
        mock_writer_cls.return_value = mock_writer

        mock_script_uc = MagicMock()
        mock_script_uc.execute.return_value = {"ok": True, "data": {"script": "Cena 1: Teste"}}
        mock_script_uc_cls.return_value = mock_script_uc

        mock_split_uc = MagicMock()
        mock_split_uc.execute.return_value = {
            "ok": True,
            "data": {"scenes": [{"id": 1, "prompt": "Prompt 1", "scene_text": "Scene 1", "duration": 5}]},
        }
        mock_split_uc_cls.return_value = mock_split_uc

        mock_build_uc = MagicMock()
        mock_build_uc.execute.return_value = {
            "ok": True,
            "data": {"scenes": [{"id": 1, "prompt": "Prompt 1", "scene_text": "Scene 1", "duration": 5}]},
        }
        mock_build_uc_cls.return_value = mock_build_uc

        mock_audio_uc = MagicMock()
        mock_audio_uc.execute.return_value = {"ok": True, "data": {"audio_path": "narration.wav"}}
        mock_audio_uc_cls.return_value = mock_audio_uc

        mock_render = MagicMock()
        mock_render.execute.return_value = {"ok": False, "error": "WanGP not available"}
        mock_render_cls.return_value = mock_render

        mock_static = MagicMock()
        mock_static.execute.return_value = {"ok": False, "error": "FFmpeg not found"}
        mock_static_cls.return_value = mock_static

        mock_concat_uc = MagicMock()
        mock_concat_uc.execute.return_value = {"ok": True, "data": {}}
        mock_concat_uc_cls.return_value = mock_concat_uc

        mock_wangp_cls.return_value = MagicMock()
        mock_tts_cls.return_value = MagicMock()
        mock_ffmpeg_cls.return_value = MagicMock()

        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline

        pipeline = VideoGenerationPipeline()
        _ensure_approved_script("test_gal934_both_fail", "Cena 1: Teste")

        result = pipeline.generate_commercial(
            project_id="test_gal934_both_fail",
            product="Teste",
            target_audience="Teste",
        )

        shutil.rmtree(PROJECTS_DIR / "test_gal934_both_fail", ignore_errors=True)

        assert result.get("success") is False, "Pipeline fails when no scenes rendered"
        assert "Nenhum vídeo" in result.get("error", "")

        assert mock_writer.write.called
        calls = mock_writer.write.call_args_list
        codes = [c[0][0].code for c in calls]
        assert ErrorCode.WANGP_UNAVAILABLE in codes
        assert ErrorCode.FFMPEG_NOT_FOUND in codes

        events = pipeline.render_all_scenes_uc._stage_logger.events
        failure_events = [e for e in events if e.event_type == "failure" and "FFmpeg" in e.message]
        assert len(failure_events) >= 1


def test_wangp_available_no_fallback():
    with (
        patch("app.services.error_jsonl_writer.ErrorJsonlWriter") as mock_writer_cls,
        patch("app.application.use_cases.render_all_scenes_use_case.RenderVideoUseCase") as mock_render_cls,
        patch("app.application.use_cases.render_all_scenes_use_case.CreateStaticVideoUseCase") as mock_static_cls,
        patch("app.pipeline.video_generation_pipeline.GenerateScriptUseCase") as mock_script_uc_cls,
        patch("app.pipeline.video_generation_pipeline.SplitScenesUseCase") as mock_split_uc_cls,
        patch("app.pipeline.video_generation_pipeline.BuildPromptsUseCase") as mock_build_uc_cls,
        patch("app.pipeline.video_generation_pipeline.GenerateAudioUseCase") as mock_audio_uc_cls,
        patch("app.pipeline.video_generation_pipeline.ConcatVideosUseCase") as mock_concat_uc_cls,
        patch("app.pipeline.video_generation_pipeline.WanGPAdapter") as mock_wangp_cls,
        patch("app.pipeline.video_generation_pipeline.TTSAdapter") as mock_tts_cls,
        patch("app.pipeline.video_generation_pipeline.FFmpegAdapter") as mock_ffmpeg_cls):
        mock_writer = MagicMock()
        mock_writer_cls.return_value = mock_writer

        mock_script_uc = MagicMock()
        mock_script_uc.execute.return_value = {"ok": True, "data": {"script": "Cena 1: Teste"}}
        mock_script_uc_cls.return_value = mock_script_uc

        mock_split_uc = MagicMock()
        mock_split_uc.execute.return_value = {
            "ok": True,
            "data": {"scenes": [{"id": 1, "prompt": "Prompt 1", "scene_text": "Scene 1", "duration": 5}]},
        }
        mock_split_uc_cls.return_value = mock_split_uc

        mock_build_uc = MagicMock()
        mock_build_uc.execute.return_value = {
            "ok": True,
            "data": {"scenes": [{"id": 1, "prompt": "Prompt 1", "scene_text": "Scene 1", "duration": 5}]},
        }
        mock_build_uc_cls.return_value = mock_build_uc

        mock_audio_uc = MagicMock()
        mock_audio_uc.execute.return_value = {"ok": True, "data": {"audio_path": "narration.wav"}}
        mock_audio_uc_cls.return_value = mock_audio_uc

        mock_render = MagicMock()
        mock_render.execute.return_value = {
            "ok": True, "data": {"video_path": "/tmp/scene_000.mp4"}
        }
        mock_render_cls.return_value = mock_render

        mock_concat_uc = MagicMock()
        mock_concat_uc.execute.return_value = {"ok": True, "data": {}}
        mock_concat_uc_cls.return_value = mock_concat_uc

        mock_wangp_cls.return_value = MagicMock()
        mock_tts_cls.return_value = MagicMock()
        mock_ffmpeg_cls.return_value = MagicMock()


        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline

        pipeline = VideoGenerationPipeline()
        _ensure_approved_script("test_gal934_wangp_ok", "Cena 1: Teste")

        result = pipeline.generate_commercial(
            project_id="test_gal934_wangp_ok",
            product="Teste",
            target_audience="Teste",
        )

        shutil.rmtree(PROJECTS_DIR / "test_gal934_wangp_ok", ignore_errors=True)

        assert result.get("success") is True

        assert not mock_writer.write.called, "No error should be logged on happy path"
        assert mock_static_cls.return_value.execute.called is not True

        events = pipeline.render_all_scenes_uc._stage_logger.events
        assert len(events) == 0, "No events on happy path"


def test_concat_failure_logs_ffmpeg_concat_failed():
    with (
        patch("app.services.error_jsonl_writer.ErrorJsonlWriter") as mock_writer_cls,
        patch("app.application.use_cases.render_all_scenes_use_case.RenderVideoUseCase") as mock_render_cls,
        patch("app.application.use_cases.render_all_scenes_use_case.CreateStaticVideoUseCase") as mock_static_cls,
        patch("app.pipeline.video_generation_pipeline.GenerateScriptUseCase") as mock_script_uc_cls,
        patch("app.pipeline.video_generation_pipeline.SplitScenesUseCase") as mock_split_uc_cls,
        patch("app.pipeline.video_generation_pipeline.BuildPromptsUseCase") as mock_build_uc_cls,
        patch("app.pipeline.video_generation_pipeline.GenerateAudioUseCase") as mock_audio_uc_cls,
        patch("app.pipeline.video_generation_pipeline.ConcatVideosUseCase") as mock_concat_uc_cls,
        patch("app.pipeline.video_generation_pipeline.WanGPAdapter") as mock_wangp_cls,
        patch("app.pipeline.video_generation_pipeline.TTSAdapter") as mock_tts_cls,
        patch("app.pipeline.video_generation_pipeline.FFmpegAdapter") as mock_ffmpeg_cls):
        mock_writer = MagicMock()
        mock_writer_cls.return_value = mock_writer

        mock_script_uc = MagicMock()
        mock_script_uc.execute.return_value = {"ok": True, "data": {"script": "Cena 1: Teste"}}
        mock_script_uc_cls.return_value = mock_script_uc

        mock_split_uc = MagicMock()
        mock_split_uc.execute.return_value = {
            "ok": True,
            "data": {"scenes": [{"id": 1, "prompt": "Prompt 1", "scene_text": "Scene 1", "duration": 5}]},
        }
        mock_split_uc_cls.return_value = mock_split_uc

        mock_build_uc = MagicMock()
        mock_build_uc.execute.return_value = {
            "ok": True,
            "data": {"scenes": [{"id": 1, "prompt": "Prompt 1", "scene_text": "Scene 1", "duration": 5}]},
        }
        mock_build_uc_cls.return_value = mock_build_uc

        mock_audio_uc = MagicMock()
        mock_audio_uc.execute.return_value = {"ok": True, "data": {"audio_path": "narration.wav"}}
        mock_audio_uc_cls.return_value = mock_audio_uc

        mock_render = MagicMock()
        mock_render.execute.return_value = {
            "ok": True, "data": {"video_path": "/tmp/scene_000.mp4"}
        }
        mock_render_cls.return_value = mock_render

        mock_concat_uc = MagicMock()
        mock_concat_uc.execute.return_value = {"ok": False, "error": "Input/output error"}
        mock_concat_uc_cls.return_value = mock_concat_uc

        mock_wangp_cls.return_value = MagicMock()
        mock_tts_cls.return_value = MagicMock()
        mock_ffmpeg_cls.return_value = MagicMock()


        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline

        pipeline = VideoGenerationPipeline()
        _ensure_approved_script("test_gal934_concat_fail", "Cena 1: Teste")

        result = pipeline.generate_commercial(
            project_id="test_gal934_concat_fail",
            product="Teste",
            target_audience="Teste",
        )

        shutil.rmtree(PROJECTS_DIR / "test_gal934_concat_fail", ignore_errors=True)

        assert result.get("success") is False, "Pipeline should fail on concat error"

        assert mock_writer.write.called
        calls = mock_writer.write.call_args_list
        codes = [c[0][0].code for c in calls]
        assert ErrorCode.FFMPEG_CONCAT_FAILED in codes

        events = pipeline._stage_logger.events
        assert any(
            e.event_type == "failure" and "FFmpeg concat" in e.message
            for e in events
        )
