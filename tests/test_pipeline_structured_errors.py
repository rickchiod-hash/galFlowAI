"""RND-611: Pipeline fallback chama log_structured_error tests."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, PropertyMock

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
from app.core.app_error import AppError
from app.core.error_codes import ErrorCode


def _make_pipeline():
    """Helper to create a pipeline with mocks for all adapters."""
    pipeline = VideoGenerationPipeline()
    pipeline.wangp_adapter = MagicMock()
    pipeline.wangp_adapter.is_available.return_value = False
    pipeline.tts_adapter = MagicMock()
    pipeline.ffmpeg_adapter = MagicMock()
    pipeline.generate_script_use_case = MagicMock()
    pipeline.split_scenes_use_case = MagicMock()
    pipeline.build_prompts_use_case = MagicMock()
    pipeline.generate_audio_use_case = MagicMock()
    pipeline.render_all_scenes_uc._render_video_uc = MagicMock()
    pipeline.render_all_scenes_uc._create_static_video_uc = MagicMock()
    pipeline.concat_videos_use_case = MagicMock()
    return pipeline


def test_fallback_records_wangp_unavailable():
    pipeline = _make_pipeline()
    writer_mock = MagicMock()
    pipeline.render_all_scenes_uc._get_error_writer = MagicMock(return_value=writer_mock)

    pipeline.generate_script_use_case.execute.return_value = {
        "ok": True,
        "data": {"script": "test script"},
    }
    pipeline.split_scenes_use_case.execute.return_value = {
        "ok": True,
        "data": {"scenes": [{"scene": 1, "text": "cena 1"}]},
    }

    with patch("pathlib.Path.exists", return_value=True):
        with patch("pathlib.Path.read_text", return_value="test script approved"):
            pipeline.render_all_scenes_uc._render_video_uc.execute.return_value = {
                "ok": False,
                "error": "WanGP not available",
            }
            pipeline.render_all_scenes_uc._create_static_video_uc.execute.return_value = {
                "ok": True,
                "data": {"video_path": "/tmp/scene_000.mp4"},
            }
            pipeline.concat_videos_use_case.execute.return_value = {
                "ok": True,
                "data": {},
            }

            result = pipeline.generate_commercial(
                project_id="test_rnd611",
                product="Teste",
                target_audience="Teste",
            )

    assert result.get("success"), "Pipeline should succeed with FFmpeg fallback"
    assert writer_mock.write.called, "Error writer should have been called"
    calls = writer_mock.write.call_args_list
    codes = [c[0][0].code for c in calls]
    assert ErrorCode.WANGP_UNAVAILABLE in codes, (
        "WANGP_UNAVAILABLE should be recorded on fallback"
    )


def test_ffmpeg_concat_failure_records_error():
    pipeline = _make_pipeline()
    writer_mock = MagicMock()
    pipeline._get_error_writer = MagicMock(return_value=writer_mock)

    pipeline.generate_script_use_case.execute.return_value = {
        "ok": True,
        "data": {"script": "test script"},
    }
    pipeline.split_scenes_use_case.execute.return_value = {
        "ok": True,
        "data": {"scenes": [{"scene": 1, "text": "cena 1"}]},
    }

    with patch("pathlib.Path.exists", return_value=True):
        with patch("pathlib.Path.read_text", return_value="test script approved"):
            pipeline.render_all_scenes_uc._render_video_uc.execute.return_value = {
                "ok": True,
                "data": {"video_path": "/tmp/scene_000.mp4"},
            }
            pipeline.concat_videos_use_case.execute.return_value = {
                "ok": False,
                "error": "Input/output error",
            }

            result = pipeline.generate_commercial(
                project_id="test_rnd611_concat",
                product="Teste",
                target_audience="Teste",
            )

    assert not result.get("success"), "Pipeline should fail on concat error"
    calls = writer_mock.write.call_args_list
    codes = [c[0][0].code for c in calls]
    assert ErrorCode.FFMPEG_CONCAT_FAILED in codes, (
        "FFMPEG_CONCAT_FAILED should be recorded on concat failure"
    )


def test_ffmpeg_fallback_also_fails_records_both():
    pipeline = _make_pipeline()
    writer_mock = MagicMock()
    pipeline.render_all_scenes_uc._get_error_writer = MagicMock(return_value=writer_mock)

    pipeline.generate_script_use_case.execute.return_value = {
        "ok": True,
        "data": {"script": "test script"},
    }
    pipeline.split_scenes_use_case.execute.return_value = {
        "ok": True,
        "data": {"scenes": [{"scene": 1, "text": "cena 1"}]},
    }

    with patch("pathlib.Path.exists", return_value=True):
        with patch("pathlib.Path.read_text", return_value="test script approved"):
            pipeline.render_all_scenes_uc._render_video_uc.execute.return_value = {
                "ok": False,
                "error": "WanGP not available",
            }
            pipeline.render_all_scenes_uc._create_static_video_uc.execute.return_value = {
                "ok": False,
                "error": "FFmpeg not found",
            }

            result = pipeline.generate_commercial(
                project_id="test_rnd611_double_fail",
                product="Teste",
                target_audience="Teste",
            )

    assert not result.get("success"), "Pipeline should fail when both fail"
    calls = writer_mock.write.call_args_list
    codes = [c[0][0].code for c in calls]
    assert ErrorCode.WANGP_UNAVAILABLE in codes
    assert ErrorCode.FFMPEG_NOT_FOUND in codes


def test_stage_logger_has_events_on_fallback():
    pipeline = _make_pipeline()
    pipeline.render_all_scenes_uc._get_error_writer = MagicMock(return_value=MagicMock())

    pipeline.generate_script_use_case.execute.return_value = {
        "ok": True,
        "data": {"script": "test script"},
    }
    pipeline.split_scenes_use_case.execute.return_value = {
        "ok": True,
        "data": {"scenes": [{"scene": 1, "text": "cena 1"}]},
    }

    with patch("pathlib.Path.exists", return_value=True):
        with patch("pathlib.Path.read_text", return_value="test script approved"):
            pipeline.render_all_scenes_uc._render_video_uc.execute.return_value = {
                "ok": False,
                "error": "WanGP not available",
            }
            pipeline.render_all_scenes_uc._create_static_video_uc.execute.return_value = {
                "ok": True,
                "data": {"video_path": "/tmp/scene_000.mp4"},
            }
            pipeline.concat_videos_use_case.execute.return_value = {
                "ok": True,
                "data": {},
            }

            pipeline.generate_commercial(
                project_id="test_rnd611_events",
                product="Teste",
                target_audience="Teste",
            )

    events = pipeline.render_all_scenes_uc._stage_logger.events
    assert len(events) >= 1
    assert any(
        e.event_type in ("warning", "failure") and "WanGP" in e.message
        for e in events
    )
