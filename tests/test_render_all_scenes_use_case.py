"""Tests for RenderAllScenesUseCase — WanGP -> FFmpeg fallback chain."""
from unittest.mock import MagicMock, patch
from app.application.use_cases.render_all_scenes_use_case import RenderAllScenesUseCase


def _make_scene_prompts(count=3):
    return [
        {"id": f"scene_{i}", "prompt": f"Prompt for scene {i}", "duration": 5}
        for i in range(count)
    ]


class TestRenderAllScenesSuccess:
    def test_all_scenes_render_with_wangp(self):
        mock_render = MagicMock()
        mock_render.execute.return_value = {"ok": True, "data": {"video_path": "/tmp/scene_000.mp4"}}
        mock_static = MagicMock()
        uc = RenderAllScenesUseCase(render_video_uc=mock_render, create_static_video_uc=mock_static)

        result = uc.execute(project_id="p1", scene_prompts=_make_scene_prompts(2))

        assert result.get("ok") is True
        data = result.get("data", {})
        assert data["count"] == 2
        assert len(data["rendered_scenes"]) == 2
        assert data["rendered_scenes"][0]["status"] == "completed"
        assert data["rendered_scenes"][0]["video_path"] == "/tmp/scene_000.mp4"
        mock_render.execute.assert_called()
        mock_static.execute.assert_not_called()

    def test_fallback_to_ffmpeg_when_wangp_fails(self):
        mock_render = MagicMock()
        mock_render.execute.return_value = {"ok": False, "error": "WanGP not available"}
        mock_static = MagicMock()
        mock_static.execute.return_value = {"ok": True, "data": {"video_path": "/tmp/scene_000.mp4"}}
        uc = RenderAllScenesUseCase(render_video_uc=mock_render, create_static_video_uc=mock_static)

        result = uc.execute(project_id="p1", scene_prompts=_make_scene_prompts(1))

        assert result.get("ok") is True
        data = result.get("data", {})
        assert data["count"] == 1
        assert data["rendered_scenes"][0]["status"] == "completed"
        assert data["rendered_scenes"][0]["video_path"] == "/tmp/scene_000.mp4"
        mock_render.execute.assert_called_once()
        mock_static.execute.assert_called_once()

    def test_both_fail_marks_scene_as_failed(self):
        mock_render = MagicMock()
        mock_render.execute.return_value = {"ok": False, "error": "WanGP not available"}
        mock_static = MagicMock()
        mock_static.execute.return_value = {"ok": False, "error": "FFmpeg not found"}
        uc = RenderAllScenesUseCase(render_video_uc=mock_render, create_static_video_uc=mock_static)

        result = uc.execute(project_id="p1", scene_prompts=_make_scene_prompts(1))

        assert result.get("ok") is True
        data = result.get("data", {})
        assert data["count"] == 0
        assert len(data["rendered_scenes"]) == 0


class TestRenderAllScenesPartialFailure:
    def test_mixed_success_and_fallback(self):
        mock_render = MagicMock()
        mock_render.execute.side_effect = [
            {"ok": True, "data": {"video_path": "/tmp/scene_000.mp4"}},
            {"ok": False, "error": "WanGP not available"},
        ]
        mock_static = MagicMock()
        mock_static.execute.return_value = {"ok": True, "data": {"video_path": "/tmp/scene_001.mp4"}}
        uc = RenderAllScenesUseCase(render_video_uc=mock_render, create_static_video_uc=mock_static)

        result = uc.execute(project_id="p1", scene_prompts=_make_scene_prompts(2))

        assert result.get("ok") is True
        data = result.get("data", {})
        assert data["count"] == 2
        assert data["rendered_scenes"][0]["status"] == "completed"
        assert data["rendered_scenes"][1]["status"] == "completed"
        assert data["rendered_scenes"][1]["video_path"] == "/tmp/scene_001.mp4"
        assert mock_render.execute.call_count == 2
        assert mock_static.execute.call_count == 1


class TestRenderAllScenesValidation:
    def test_empty_scene_prompts_returns_error(self):
        uc = RenderAllScenesUseCase()
        result = uc.execute(project_id="p1", scene_prompts=[])
        assert result.get("ok") is False

    def test_empty_project_id_returns_error(self):
        uc = RenderAllScenesUseCase()
        result = uc.execute(project_id="", scene_prompts=_make_scene_prompts(1))
        assert result.get("ok") is False

    def test_exception_in_execute_returns_error(self):
        mock_render = MagicMock()
        mock_render.execute.side_effect = RuntimeError("Unexpected error")
        uc = RenderAllScenesUseCase(render_video_uc=mock_render)
        result = uc.execute(project_id="p1", scene_prompts=_make_scene_prompts(1))
        assert result.get("ok") is False


class TestRenderAllScenesDefaultFallback:
    @patch("app.application.use_cases.render_all_scenes_use_case.RenderVideoUseCase")
    @patch("app.application.use_cases.render_all_scenes_use_case.CreateStaticVideoUseCase")
    def test_default_instantiation(self, mock_static_cls, mock_render_cls):
        mock_render_cls.return_value = MagicMock()
        mock_static_cls.return_value = MagicMock()
        uc = RenderAllScenesUseCase()
        assert uc._render_video_uc is not None
        assert uc._create_static_video_uc is not None
        mock_render_cls.assert_called_once()
        mock_static_cls.assert_called_once()

    def test_scene_text_fallback_when_no_prompt(self):
        mock_render = MagicMock()
        mock_render.execute.return_value = {"ok": False, "error": "WanGP not available"}
        mock_static = MagicMock()
        mock_static.execute.return_value = {"ok": True, "data": {"video_path": "/tmp/scene_000.mp4"}}
        uc = RenderAllScenesUseCase(render_video_uc=mock_render, create_static_video_uc=mock_static)

        prompts = [{"id": "s1", "scene_text": "Direct scene text", "duration": 5}]
        result = uc.execute(project_id="p1", scene_prompts=prompts)

        assert result.get("ok") is True
        _, kwargs = mock_static.execute.call_args
        assert kwargs["text"] == "Direct scene text"
