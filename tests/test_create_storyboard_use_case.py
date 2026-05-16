import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import patch, MagicMock
from app.application.use_cases.create_storyboard_use_case import CreateStoryboardUseCase


class TestCreateStoryboardUseCase:
    def test_execute_success(self):
        uc = CreateStoryboardUseCase()
        scenes = [{"id": "s1"}, {"id": "s2"}]
        with (
            patch("app.application.use_cases.create_storyboard_use_case.get_gpu_info") as mock_gpu,
            patch("app.application.use_cases.create_storyboard_use_case.get_recommended_preset") as mock_preset,
            patch("app.application.use_cases.create_storyboard_use_case.create_storyboard_video") as mock_video,
        ):
            mock_gpu.return_value = {"vram_gb": 6, "name": "GTX 1660"}
            mock_preset.return_value = {"model": "wan2gp_1.3b", "resolution": "512x512"}
            mock_video.return_value = Path("/tmp/out.mp4")
            result = uc.execute(project_id="proj_1", scenes=scenes)
        assert result.ok is True
        assert result.data["video_path"] == "\\tmp\\out.mp4"

    def test_execute_no_scenes(self):
        uc = CreateStoryboardUseCase()
        result = uc.execute(project_id="proj_1", scenes=[])
        assert result.ok is False
        assert "Invalid" in result.error

    def test_execute_no_project_id(self):
        uc = CreateStoryboardUseCase()
        result = uc.execute(project_id="", scenes=[{"id": "s1"}])
        assert result.ok is False
        assert "Invalid" in result.error

    def test_execute_video_failure(self):
        uc = CreateStoryboardUseCase()
        with (
            patch("app.application.use_cases.create_storyboard_use_case.get_gpu_info") as mock_gpu,
            patch("app.application.use_cases.create_storyboard_use_case.get_recommended_preset") as mock_preset,
            patch("app.application.use_cases.create_storyboard_use_case.create_storyboard_video") as mock_video,
        ):
            mock_gpu.return_value = {"vram_gb": 6, "name": "GTX 1660"}
            mock_preset.return_value = {"model": "wan2gp_1.3b"}
            mock_video.return_value = None
            result = uc.execute(project_id="proj_1", scenes=[{"id": "s1"}])
        assert result.ok is True
        assert result.data["video_path"] is None

    def test_execute_exception(self):
        uc = CreateStoryboardUseCase()
        with patch("app.application.use_cases.create_storyboard_use_case.get_gpu_info") as mock_gpu:
            mock_gpu.side_effect = ValueError("no gpu")
            result = uc.execute(project_id="proj_1", scenes=[{"id": "s1"}])
        assert result.ok is False
        assert "no gpu" in result.error
