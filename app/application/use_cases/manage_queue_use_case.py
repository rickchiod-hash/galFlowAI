"""Use case for managing job queue (PIPE-400)."""
from typing import Dict, Any, Optional
from app.application.use_cases.base_use_case import BaseUseCase
from app.jobs.queue import JobQueue, queue as default_queue


class ManageQueueUseCase(BaseUseCase):
    """Manage video rendering job queue.

    3-point standard:
    1. Validate queue operation and parameters
    2. Execute queue operation (add, remove, cancel, list, status)
    3. Return operation result
    """

    def __init__(self, queue: Optional[JobQueue] = None):
        super().__init__()
        self.queue = queue or default_queue

    def execute(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Execute queue management use case."""
        try:
            if not self._validate(operation=operation, **kwargs):
                return self._build_error("Invalid operation or parameters")

            result = None
            if operation == "add":
                result = self._add_job(kwargs)
            elif operation == "cancel":
                result = self._cancel_job(kwargs)
            elif operation == "remove":
                result = self._remove_job(kwargs)
            elif operation == "list":
                result = self._list_jobs()
            elif operation == "status":
                result = self._get_status()
            else:
                return self._build_error(f"Unknown operation: {operation}")

            return self._build_success(data=result)
        except Exception as e:
            return self._build_error(str(e))

    def _add_job(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Add job to queue."""
        project_id = kwargs.get("project_id", "")
        job_type = kwargs.get("job_type", "video_render")
        params = kwargs.get("params", {})
        job_id = self.queue.add_job(job_type, project_id, params=params)
        return {"job_id": job_id, "operation": "add"}

    def _cancel_job(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Cancel a job."""
        job_id = kwargs.get("job_id", "")
        success = self.queue.cancel_job(job_id)
        return {"success": success, "operation": "cancel"}

    def _remove_job(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Remove job from queue."""
        job_id = kwargs.get("job_id", "")
        success = self.queue.remove_job(job_id)
        return {"success": success, "operation": "remove"}

    def _list_jobs(self) -> Dict[str, Any]:
        """List all jobs in queue."""
        jobs = self.queue.list_jobs()
        return {"jobs": jobs, "count": len(jobs), "operation": "list"}

    def _get_status(self) -> Dict[str, Any]:
        """Get queue status."""
        status = self.queue.get_status()
        return {"status": status, "operation": "status"}

    def _validate(self, **kwargs) -> bool:
        """Validate operation and parameters."""
        operation = kwargs.get("operation", "")
        valid_ops = ["add", "cancel", "remove", "list", "status"]
        if operation not in valid_ops:
            return False
        if operation == "add":
            return bool(kwargs.get("project_id"))
        elif operation in ("cancel", "remove"):
            return bool(kwargs.get("job_id"))
        return True
