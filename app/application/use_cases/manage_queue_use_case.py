"""Use case for managing job queue."""
from typing import Dict, Any
from app.application.use_cases.base_use_case import BaseUseCase
from app.jobs.queue import JobQueue

class ManageQueueUseCase(BaseUseCase):
    """Manage video rendering job queue.
    
    3-point standard:
    1. Validate queue operation and parameters
    2. Execute queue operation (add, remove, list, status)
    3. Return operation result
    """
    
    def __init__(self):
        super().__init__()
        self.queue = JobQueue()
    
    def execute(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Execute queue management use case."""
        try:
            # 1. Validate input
            if not self._validate(operation=operation, **kwargs):
                return self._build_error("Invalid operation or parameters")
            
            # 2. Execute business logic
            result = None
            if operation == "add":
                result = self._add_job(kwargs)
            elif operation == "remove":
                result = self._remove_job(kwargs)
            elif operation == "list":
                result = self._list_jobs()
            elif operation == "status":
                result = self._get_status(kwargs)
            else:
                return self._build_error(f"Unknown operation: {operation}")
            
            # 3. Return result with status
            return self._build_success(data=result)
        except Exception as e:
            return self._build_error(str(e))
    
    def _add_job(self, kwargs) -> Dict[str, Any]:
        """Add job to queue."""
        project_id = kwargs.get("project_id", "")
        scene_id = kwargs.get("scene_id", "")
        job_id = self.queue.add_job(project_id, scene_id)
        return {"job_id": job_id, "operation": "add"}
    
    def _remove_job(self, kwargs) -> Dict[str, Any]:
        """Remove job from queue."""
        job_id = kwargs.get("job_id", "")
        success = self.queue.remove_job(job_id)
        return {"success": success, "operation": "remove"}
    
    def _list_jobs(self) -> Dict[str, Any]:
        """List all jobs in queue."""
        jobs = self.queue.list_jobs()
        return {"jobs": jobs, "count": len(jobs), "operation": "list"}
    
    def _get_status(self, kwargs) -> Dict[str, Any]:
        """Get queue status."""
        status = self.queue.get_status()
        return {"status": status, "operation": "status"}
    
    def _validate(self, **kwargs) -> bool:
        """Validate operation and parameters."""
        operation = kwargs.get("operation", "")
        valid_ops = ["add", "remove", "list", "status"]
        if operation not in valid_ops:
            return False
        
        if operation == "add":
            return bool(kwargs.get("project_id") and kwargs.get("scene_id"))
        elif operation == "remove":
            return bool(kwargs.get("job_id"))
        
        return True
