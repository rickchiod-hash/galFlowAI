import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import patch, MagicMock


class TestVideoService:
    def make_video_service(self, wangp_available=True, ffmpeg_available=True):
        """Helper to create VideoService with mocked adapters."""
        with (
            patch("app.services.video_service.WanGPAdapter") as mock_wangp_cls,
            patch("app.services.video_service.FFmpegAdapter") as mock_ffmpeg_cls,
        ):
            mock_wangp = MagicMock()
            mock_wangp.is_available.return_value = wangp_available
            mock_wangp_cls.return_value = mock_wangp

            mock_ffmpeg = MagicMock()
            mock_ffmpeg.is_available.return_value = ffmpeg_available
            mock_ffmpeg_cls.return_value = mock_ffmpeg

            vs = __import__("app.services.video_service", fromlist=["VideoService"]).VideoService()
            vs.wangp_adapter = mock_wangp
            vs.ffmpeg_adapter = mock_ffmpeg
            return vs

    def test_init_both_available(self):
        with (
            patch("app.services.video_service.WanGPAdapter") as mock_wangp_cls,
            patch("app.services.video_service.FFmpegAdapter") as mock_ffmpeg_cls,
        ):
            mock_wangp_cls.return_value.is_available.return_value = True
            mock_ffmpeg_cls.return_value.is_available.return_value = True
            from app.services.video_service import VideoService
            vs = VideoService()
        assert vs.is_available() is True
        assert vs.wangp_available is True
        assert vs.ffmpeg_available is True

    def test_init_only_wangp(self):
        with (
            patch("app.services.video_service.WanGPAdapter") as mock_wangp_cls,
            patch("app.services.video_service.FFmpegAdapter") as mock_ffmpeg_cls,
        ):
            mock_wangp_cls.return_value.is_available.return_value = True
            mock_ffmpeg_cls.return_value.is_available.return_value = False
            from app.services.video_service import VideoService
            vs = VideoService()
        assert vs.is_available() is True
        assert vs.wangp_available is True
        assert vs.ffmpeg_available is False

    def test_init_only_ffmpeg(self):
        with (
            patch("app.services.video_service.WanGPAdapter") as mock_wangp_cls,
            patch("app.services.video_service.FFmpegAdapter") as mock_ffmpeg_cls,
        ):
            mock_wangp_cls.return_value.is_available.return_value = False
            mock_ffmpeg_cls.return_value.is_available.return_value = True
            from app.services.video_service import VideoService
            vs = VideoService()
        assert vs.is_available() is True
        assert vs.wangp_available is False
        assert vs.ffmpeg_available is True

    def test_init_none_available(self):
        with (
            patch("app.services.video_service.WanGPAdapter") as mock_wangp_cls,
            patch("app.services.video_service.FFmpegAdapter") as mock_ffmpeg_cls,
        ):
            mock_wangp_cls.return_value.is_available.return_value = False
            mock_ffmpeg_cls.return_value.is_available.return_value = False
            from app.services.video_service import VideoService
            vs = VideoService()
        assert vs.is_available() is False

    def test_get_status(self):
        vs = self.make_video_service(wangp_available=True, ffmpeg_available=True)
        status = vs.get_status()
        assert status["available"] is True
        assert status["preferred_provider"] == "WanGP"

    def test_generate_scene_video_not_available(self):
        vs = self.make_video_service(wangp_available=False, ffmpeg_available=False)
        result = vs.generate_scene_video("scene_1", "prompt", "/tmp/out.mp4")
        assert result["success"] is False
        assert "Nenhum motor" in result["error"]

    def test_generate_scene_video_wangp_success(self):
        vs = self.make_video_service(wangp_available=True, ffmpeg_available=True)
        vs.wangp_adapter.generate_video.return_value = {"success": True}
        result = vs.generate_scene_video("scene_1", "prompt", "/tmp/out.mp4", duration_seconds=5)
        assert result["success"] is True
        assert result["provider"] == "WanGP"

    def test_generate_scene_video_wangp_failure_ffmpeg_success(self):
        vs = self.make_video_service(wangp_available=True, ffmpeg_available=True)
        vs.wangp_adapter.generate_video.return_value = {"success": False, "error": "OOM"}
        vs.ffmpeg_adapter.create_static_video.return_value = {"success": True}
        result = vs.generate_scene_video("scene_1", "prompt", "/tmp/out.mp4")
        assert result["success"] is True
        assert result["provider"] == "FFmpeg"

    def test_generate_scene_video_both_fail(self):
        vs = self.make_video_service(wangp_available=True, ffmpeg_available=True)
        vs.wangp_adapter.generate_video.return_value = {"success": False, "error": "OOM"}
        vs.ffmpeg_adapter.create_static_video.return_value = {"success": False, "error": "FFmpeg fail"}
        result = vs.generate_scene_video("scene_1", "prompt", "/tmp/out.mp4")
        assert result["success"] is False
        assert result["error"] == "FFmpeg fail"

    def test_generate_scene_video_with_callback(self):
        cb = MagicMock()
        vs = self.make_video_service(wangp_available=True, ffmpeg_available=True)
        vs.wangp_adapter.generate_video.return_value = {"success": True}
        result = vs.generate_scene_video("scene_1", "prompt", "/tmp/out.mp4", progress_callback=cb)
        assert result["success"] is True
        assert cb.call_count >= 2

    def test_generate_commercial_success(self):
        vs = self.make_video_service(wangp_available=True, ffmpeg_available=True)
        with (
            patch("app.services.script_service.generate_script") as mock_gs,
            patch("app.domain.scene_parser.split_script_into_scenes") as mock_split,
            patch("app.domain.prompt_builder_service.build_prompts_for_scenes") as mock_build,
        ):
            mock_gs.return_value = {"script": "Test script content"}
            mock_split.return_value = [{"id": "s1"}, {"id": "s2"}]
            mock_build.return_value = [
                {"prompt": "p1", "duration": 5},
                {"prompt": "p2", "duration": 5},
            ]
            vs.generate_scene_video = MagicMock(return_value={"success": True})
            vs.ffmpeg_adapter.concat_videos = MagicMock(return_value={"success": True})
            result = vs.generate_commercial("proj_1", "Produto X", "jovens")
        assert result["success"] is True
        assert result["project_id"] == "proj_1"

    def test_generate_commercial_script_fail(self):
        vs = self.make_video_service(wangp_available=True, ffmpeg_available=True)
        with patch("app.services.script_service.generate_script", return_value={"error": "fail"}):
            result = vs.generate_commercial("proj_1", "Produto X", "jovens")
        assert result["success"] is False

    def test_generate_commercial_exception(self):
        vs = self.make_video_service(wangp_available=True, ffmpeg_available=True)
        with patch("app.services.script_service.generate_script", side_effect=RuntimeError("unexpected")):
            result = vs.generate_commercial("proj_1", "Produto X", "jovens")
        assert result["success"] is False
        assert "unexpected" in result["error"]

    def test_export_final_video_video_not_found(self):
        vs = self.make_video_service()
        with patch.object(Path, "exists", return_value=False):
            result = vs.export_final_video("/fake/video.mp4")
        assert result["success"] is False
        assert "nao encontrado" in result["error"]

    def test_export_final_video_success(self):
        vs = self.make_video_service()
        with (
            patch.object(Path, "exists", return_value=True),
            patch.object(Path, "parent"),
            patch.object(Path, "write_text"),
        ):
            vs.ffmpeg_adapter.concat_videos.return_value = {"success": True}
            result = vs.export_final_video("/fake/video.mp4")
        assert result["success"] is True
        assert result["manifest"]["audio"] is False

    def test_export_final_video_with_audio(self):
        vs = self.make_video_service()
        with (
            patch.object(Path, "exists", return_value=True),
            patch.object(Path, "parent"),
            patch.object(Path, "write_text"),
        ):
            vs.ffmpeg_adapter.add_audio_to_video.return_value = {"success": True}
            result = vs.export_final_video("/fake/video.mp4", audio_path="/fake/audio.wav")
        assert result["success"] is True
        assert result["manifest"]["audio"] is True
