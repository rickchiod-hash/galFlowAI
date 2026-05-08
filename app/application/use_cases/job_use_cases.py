"""Use cases for job queue management (H11)."""
from typing import Dict, Any
from app.application.use_cases.base import UseCase, UseCaseError
from app.jobs.queue import JobQueue, JobStatus, queue


class AddJobUseCase(UseCase):
    """Add job to queue.
    
    3-point standard:
    1. Validate project_id and job_type
    2. Add job to queue
    3. Return job_id
    """
    
    def __init__(self):
        super().__init__()
        self.queue = queue
    
    def execute(self, project_id: str, job_type: str = "video_render") -> Dict[str, Any]:
        """Execute add job use case."""
        try:
            # 1. Validate input
            if not self._validate(project_id=project_id, job_type=job_type):
                return self._build_error("Invalid project_id or job_type")
            
            # 2. Execute business logic
            job_id = self.queue.add_job(job_type, project_id)
            
            # 3. Return result with status
            return self._build_success(
                data={"job_id": job_id, "status": JobStatus.QUEUED},
                project_id=project_id
            )
        except Exception as e:
            return self._build_error(str(e), project_id=project_id)
    
    def _validate(self, **kwargs) -> bool:
        """Validate project_id and job_type."""
        project_id = kwargs.get("project_id", "")
        job_type = kwargs.get("job_type", "")
        return bool(project_id and job_type)


class RemoveJobUseCase(UseCase):
    """Remove job from queue.
    
    3-point standard:
    1. Validate job_id
    2. Remove job from queue
    3. Return success status
    """
    
    def __init__(self):
        super().__init__()
        self.queue = queue
    
    def execute(self, job_id: str) -> Dict[str, Any]:
        """Execute remove job use case."""
        try:
            # 1. Validate input
            if not self._validate(job_id=job_id):
                return self._build_error("Invalid job_id")
            
            # 2. Execute business logic
            success = self.queue.remove_job(job_id)
            
            # 3. Return result with status
            if success:
                return self._build_success(
                    data={"job_id": job_id, "removed": True}
                )
            else:
                return self._build_error("Job not found", job_id=job_id)
        except Exception as e:
            return self._build_error(str(e), job_id=job_id)
    
    def _validate(self, **kwargs) -> bool:
        """Validate job_id."""
        job_id = kwargs.get("job_id", "")
        return bool(job_id)


class ListJobsUseCase(UseCase):
    """List all jobs in queue.
    
    3-point standard:
    1. No validation needed
    2. List jobs from queue
    3. Return jobs list
    """
    
    def __init__(self):
        super().__init__()
        self.queue = queue
    
    def execute(self) -> Dict[str, Any]:
        """Execute list jobs use case."""
        try:
            # 1. Validate input (none needed)
            # 2. Execute business logic
            jobs = self.queue.list_jobs()
            
            # 3. Return result with status
            return self._build_success(
                data={"jobs": jobs, "count": len(jobs)}
            )
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        """No validation needed."""
        return True


class GetQueueStatusUseCase(UseCase):
    """Get queue status.
    
    3-point standard:
    1. No validation needed
    2. Get queue status
    3. Return status dict
    """
    
    def __init__(self):
        super().__init__()
        self.queue = queue
    
    def execute(self) -> Dict[str, Any]:
        """Execute get queue status use case."""
        try:
            # 1. Validate input (none needed)
            # 2. Execute business logic
            status = self.queue.get_status()
            
            # 3. Return result with status
            return self._build_success(data=status)
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        """No validation needed."""
        return True
