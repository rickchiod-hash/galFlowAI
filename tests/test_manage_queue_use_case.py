import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import MagicMock
from app.application.use_cases.manage_queue_use_case import ManageQueueUseCase


class TestManageQueueUseCase:
    def test_add_job(self):
        mock_queue = MagicMock()
        mock_queue.add_job.return_value = "job_abc"
        uc = ManageQueueUseCase(queue=mock_queue)
        result = uc.execute(operation="add", project_id="proj_1", job_type="video_render", params={"scene": "1"})
        assert result.ok is True
        assert result.data["job_id"] == "job_abc"
        mock_queue.add_job.assert_called_once_with("video_render", "proj_1", params={"scene": "1"})

    def test_cancel_job(self):
        mock_queue = MagicMock()
        mock_queue.cancel_job.return_value = True
        uc = ManageQueueUseCase(queue=mock_queue)
        result = uc.execute(operation="cancel", job_id="job_abc")
        assert result.ok is True
        assert result.data["success"] is True
        mock_queue.cancel_job.assert_called_once_with("job_abc")

    def test_remove_job(self):
        mock_queue = MagicMock()
        mock_queue.remove_job.return_value = True
        uc = ManageQueueUseCase(queue=mock_queue)
        result = uc.execute(operation="remove", job_id="job_abc")
        assert result.ok is True
        assert result.data["success"] is True

    def test_list_jobs(self):
        mock_queue = MagicMock()
        mock_queue.list_jobs.return_value = [{"id": "j1"}, {"id": "j2"}]
        uc = ManageQueueUseCase(queue=mock_queue)
        result = uc.execute(operation="list")
        assert result.ok is True
        assert result.data["count"] == 2

    def test_get_status(self):
        mock_queue = MagicMock()
        mock_queue.get_status.return_value = {"pending": 1, "running": 0}
        uc = ManageQueueUseCase(queue=mock_queue)
        result = uc.execute(operation="status")
        assert result.ok is True
        assert result.data["status"]["pending"] == 1

    def test_invalid_operation(self):
        mock_queue = MagicMock()
        uc = ManageQueueUseCase(queue=mock_queue)
        result = uc.execute(operation="fly")
        assert result.ok is False
        assert "Invalid operation" in result.error

    def test_missing_project_id_on_add(self):
        mock_queue = MagicMock()
        uc = ManageQueueUseCase(queue=mock_queue)
        result = uc.execute(operation="add")
        assert result.ok is False
        assert "Invalid" in result.error

    def test_missing_job_id_on_cancel(self):
        mock_queue = MagicMock()
        uc = ManageQueueUseCase(queue=mock_queue)
        result = uc.execute(operation="cancel")
        assert result.ok is False
        assert "Invalid" in result.error

    def test_exception(self):
        mock_queue = MagicMock()
        mock_queue.add_job.side_effect = RuntimeError("queue full")
        uc = ManageQueueUseCase(queue=mock_queue)
        result = uc.execute(operation="add", project_id="proj_1")
        assert result.ok is False
        assert "queue full" in result.error
