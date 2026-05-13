"""RND-610: WanGP adapter hardening tests (telemetry, structured errors)."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, ANY

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.adapters.wangp_adapter import WanGPAdapter
from app.core.app_error import AppError
from app.core.error_codes import ErrorCode


def test_metrics_initial_state():
    adapter = WanGPAdapter(wangp_path="/fake", project_id="proj_test")
    metrics = adapter.get_metrics()
    assert metrics["render_count"] == 0
    assert metrics["render_success_count"] == 0
    assert metrics["render_fail_count"] == 0
    assert metrics["total_duration_ms"] == 0.0
    assert metrics["avg_duration_ms"] == 0.0


def test_metrics_after_unavailable():
    adapter = WanGPAdapter(wangp_path="/fake", project_id="proj_test")
    with patch.object(adapter, 'available', False):
        result = adapter.generate_video(prompt="test", output_path="/tmp/test.mp4")
    assert not result["success"]
    metrics = adapter.get_metrics()
    assert metrics["render_count"] == 1
    assert metrics["render_fail_count"] == 1
    assert metrics["render_success_count"] == 0


def test_metrics_after_success():
    adapter = WanGPAdapter(wangp_path="/fake", project_id="proj_test")
    adapter.main_file = "main.py"
    with patch.object(adapter, 'available', True):
        with patch.object(adapter, '_build_command', return_value=["echo", "ok"]):
            with patch.object(adapter, '_get_python_executable', return_value="python"):
                with patch("subprocess.Popen") as mock_popen:
                    proc = MagicMock()
                    proc.returncode = 0
                    proc.communicate.return_value = ("output", "")
                    mock_popen.return_value = proc
                    result = adapter.generate_video(
                        prompt="test", output_path="/tmp/test.mp4"
                    )
    assert result["success"]
    assert result["duration_ms"] >= 0
    metrics = adapter.get_metrics()
    assert metrics["render_count"] == 1
    assert metrics["render_success_count"] == 1
    assert metrics["render_fail_count"] == 0
    assert metrics["total_duration_ms"] >= 0
    assert metrics["avg_duration_ms"] >= 0


def test_structured_error_on_unavailable():
    adapter = WanGPAdapter(wangp_path="/fake", project_id="proj_test")
    with patch.object(adapter, '_get_error_writer') as mock_writer:
        mock_writer_instance = MagicMock()
        mock_writer.return_value = mock_writer_instance
        with patch.object(adapter, 'available', False):
            adapter.generate_video(prompt="test", output_path="/tmp/test.mp4")
        mock_writer_instance.write.assert_called_once()
        call_arg = mock_writer_instance.write.call_args[0][0]
        assert isinstance(call_arg, AppError)
        assert call_arg.code == ErrorCode.WANGP_UNAVAILABLE


def test_structured_error_on_failure():
    adapter = WanGPAdapter(wangp_path="/fake", project_id="proj_test")
    adapter.main_file = "main.py"
    with patch.object(adapter, '_get_error_writer') as mock_writer:
        mock_writer_instance = MagicMock()
        mock_writer.return_value = mock_writer_instance
        with patch.object(adapter, 'available', True):
            with patch.object(adapter, '_build_command', return_value=["echo", "fail"]):
                with patch.object(adapter, '_get_python_executable', return_value="python"):
                    with patch("subprocess.Popen") as mock_popen:
                        proc = MagicMock()
                        proc.returncode = 1
                        proc.communicate.return_value = ("", "error msg")
                        mock_popen.return_value = proc
                        adapter.generate_video(
                            prompt="test", output_path="/tmp/test.mp4"
                        )
        mock_writer_instance.write.assert_called_once()
        call_arg = mock_writer_instance.write.call_args[0][0]
        assert isinstance(call_arg, AppError)
        assert call_arg.code == ErrorCode.WANGP_UNAVAILABLE


def test_stage_logger_events():
    adapter = WanGPAdapter(wangp_path="/fake", project_id="proj_test")
    with patch.object(adapter, 'available', False):
        adapter.generate_video(prompt="test", output_path="/tmp/test.mp4")
    events = adapter.get_stage_events()
    assert len(events) >= 1
    assert any(e["event_type"] in ("warning", "failure") for e in events)
    assert all(e["stage"] == "WanGPAdapter" for e in events)


def test_render_scene_logs_start():
    adapter = WanGPAdapter(wangp_path="/fake", project_id="proj_test")
    adapter.main_file = "main.py"
    with patch.object(adapter, 'available', True):
        with patch.object(adapter, '_build_command', return_value=["echo", "ok"]):
            with patch.object(adapter, '_get_python_executable', return_value="python"):
                with patch("subprocess.Popen") as mock_popen:
                    proc = MagicMock()
                    proc.returncode = 0
                    proc.communicate.return_value = ("output", "")
                    mock_popen.return_value = proc
                    adapter.render_scene(
                        project_id="proj_test",
                        scene={"id": "001", "prompt": "test scene"},
                    )
    events = adapter.get_stage_events()
    assert len(events) >= 1
    assert events[0]["event_type"] == "start"


def test_get_stage_events_empty_initially():
    adapter = WanGPAdapter(wangp_path="/fake", project_id="proj_test")
    assert adapter.get_stage_events() == []


def test_project_id_passed_to_app_error():
    adapter = WanGPAdapter(wangp_path="/fake", project_id="proj_rnd610")
    with patch.object(adapter, '_get_error_writer') as mock_writer:
        mock_writer_instance = MagicMock()
        mock_writer.return_value = mock_writer_instance
        with patch.object(adapter, 'available', False):
            adapter.generate_video(prompt="test", output_path="/tmp/test.mp4")
        call_arg = mock_writer_instance.write.call_args[0][0]
        assert call_arg.project_id == "proj_rnd610"


def test_metrics_accumulate_across_calls():
    adapter = WanGPAdapter(wangp_path="/fake", project_id="proj_test")
    adapter.main_file = "main.py"
    for i in range(3):
        with patch.object(adapter, 'available', True):
            with patch.object(adapter, '_build_command', return_value=["echo", "ok"]):
                with patch.object(adapter, '_get_python_executable', return_value="python"):
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
    assert metrics["total_duration_ms"] >= 0
