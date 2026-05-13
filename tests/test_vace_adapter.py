"""RND-612: VACE adapter tests."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.adapters.vace_adapter import VAceAdapter
from app.core.app_error import AppError
from app.core.error_codes import ErrorCode


def test_disponivel_returns_false_by_default():
    assert VAceAdapter.disponivel() is False


def test_disponivel_false_when_path_missing():
    with patch("os.path.exists", return_value=False):
        assert VAceAdapter.disponivel() is False


def test_disponivel_true_when_main_found():
    with patch("os.path.exists", return_value=True):
        with patch("os.path.join", return_value="/fake/main.py"):
            assert VAceAdapter.disponivel() is True


def test_init_not_available():
    adapter = VAceAdapter(vace_path="/fake")
    assert not adapter.is_available()


def test_metrics_initial_state():
    adapter = VAceAdapter(vace_path="/fake", project_id="proj_test")
    metrics = adapter.get_metrics()
    assert metrics["render_count"] == 0
    assert metrics["render_success_count"] == 0
    assert metrics["render_fail_count"] == 0


def test_generate_video_unavailable_records_error():
    adapter = VAceAdapter(vace_path="/fake", project_id="proj_test")
    with patch.object(adapter, "_get_error_writer") as mock_writer:
        mock_instance = MagicMock()
        mock_writer.return_value = mock_instance
        result = adapter.generate_video(prompt="test", output_path="/tmp/test.mp4")
    assert not result["success"]
    assert result["fallback_suggested"]
    mock_instance.write.assert_called_once()
    call_arg = mock_instance.write.call_args[0][0]
    assert isinstance(call_arg, AppError)
    assert call_arg.code == ErrorCode.WANGP_UNAVAILABLE


def test_generate_video_success():
    adapter = VAceAdapter(vace_path="/fake", project_id="proj_test")
    adapter.available = True
    adapter.main_file = "main.py"
    with patch.object(adapter, "_build_command", return_value=["echo", "ok"]):
        with patch.object(adapter, "_get_python_executable", return_value="python"):
            with patch("subprocess.Popen") as mock_popen:
                proc = MagicMock()
                proc.returncode = 0
                proc.communicate.return_value = ("output", "")
                mock_popen.return_value = proc
                result = adapter.generate_video(
                    prompt="test", output_path="/tmp/test.mp4"
                )
    assert result["success"]
    assert result["provider"] == "VACE"
    assert result["duration_ms"] >= 0


def test_generate_video_failure():
    adapter = VAceAdapter(vace_path="/fake", project_id="proj_test")
    adapter.available = True
    adapter.main_file = "main.py"
    with patch.object(adapter, "_get_error_writer") as mock_writer:
        mock_instance = MagicMock()
        mock_writer.return_value = mock_instance
        with patch.object(adapter, "_build_command", return_value=["echo", "fail"]):
            with patch.object(adapter, "_get_python_executable", return_value="python"):
                with patch("subprocess.Popen") as mock_popen:
                    proc = MagicMock()
                    proc.returncode = 1
                    proc.communicate.return_value = ("", "vace error")
                    mock_popen.return_value = proc
                    adapter.generate_video(
                        prompt="test", output_path="/tmp/test.mp4"
                    )
    mock_instance.write.assert_called_once()
    call_arg = mock_instance.write.call_args[0][0]
    assert isinstance(call_arg, AppError)


def test_render_scene_maps_fields():
    adapter = VAceAdapter(vace_path="/fake", project_id="proj_test")
    adapter.available = True
    adapter.main_file = "main.py"
    with patch.object(adapter, "_build_command", return_value=["echo", "ok"]):
        with patch.object(adapter, "_get_python_executable", return_value="python"):
            with patch("subprocess.Popen") as mock_popen:
                proc = MagicMock()
                proc.returncode = 0
                proc.communicate.return_value = ("output", "")
                mock_popen.return_value = proc
                result = adapter.render_scene(
                    project_id="proj_test",
                    scene={"id": "001", "prompt": "test scene", "duration": 5},
                )
    assert result["success"]
    assert result["provider"] == "VACE"


def test_metrics_accumulate():
    adapter = VAceAdapter(vace_path="/fake", project_id="proj_test")
    adapter.available = True
    adapter.main_file = "main.py"
    for i in range(3):
        with patch.object(adapter, "_build_command", return_value=["echo", "ok"]):
            with patch.object(adapter, "_get_python_executable", return_value="python"):
                with patch("subprocess.Popen") as mock_popen:
                    proc = MagicMock()
                    proc.returncode = 0
                    proc.communicate.return_value = ("output", "")
                    mock_popen.return_value = proc
                    adapter.generate_video(
                        prompt=f"test{i}", output_path=f"/tmp/test{i}.mp4"
                    )
    metrics = adapter.get_metrics()
    assert metrics["render_count"] == 3
    assert metrics["render_success_count"] == 3
    assert metrics["render_fail_count"] == 0


def test_stage_logger_events():
    adapter = VAceAdapter(vace_path="/fake", project_id="proj_test")
    adapter.generate_video(prompt="test", output_path="/tmp/test.mp4")
    events = adapter.get_stage_events()
    assert len(events) >= 1
    assert all(e["stage"] == "VAceAdapter" for e in events)


def test_get_status_keys():
    adapter = VAceAdapter(vace_path="/fake", project_id="proj_test")
    status = adapter.get_status()
    assert "available" in status
    assert "path" in status
    assert "model_preset" in status
    assert "resolution" in status
