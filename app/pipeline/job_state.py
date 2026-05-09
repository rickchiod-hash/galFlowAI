"""Job state management for pipeline (PIPE-400 formal JobState)."""

from enum import Enum
from typing import Optional, Dict, Any
import time
import logging

logger = logging.getLogger(__name__)


class JobStatus(Enum):
    """Possible job states (PIPE-400 formal)."""
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobState:
    """Manages job state and metadata (PIPE-400 formal).

    Includes guarded state transitions, progress tracking, and serialization.
    """

    VALID_TRANSITIONS = {
        JobStatus.QUEUED: [JobStatus.RUNNING, JobStatus.CANCELLED],
        JobStatus.RUNNING: [JobStatus.COMPLETED, JobStatus.SUCCEEDED, JobStatus.FAILED, JobStatus.CANCELLED],
        JobStatus.COMPLETED: [],
        JobStatus.SUCCEEDED: [],
        JobStatus.FAILED: [],
        JobStatus.CANCELLED: [],
    }

    def __init__(self, job_id: str, project_id: str, job_type: str = "video_render", params: Optional[Dict[str, Any]] = None):
        self.job_id = job_id
        self.project_id = project_id
        self.job_type = job_type
        self.params = params or {}
        self.status = JobStatus.QUEUED
        self.created_at = time.time()
        self.started_at: Optional[float] = None
        self.completed_at: Optional[float] = None
        self.current_stage: Optional[str] = None
        self.progress: int = 0
        self.message: str = "Job queued"
        self.error: Optional[str] = None
        self.metadata: Dict[str, Any] = {}
        self.output_path: Optional[str] = None

    def _transition(self, new_status: JobStatus):
        """Guard: only allow valid status transitions."""
        allowed = self.VALID_TRANSITIONS.get(self.status, [])
        if new_status not in allowed:
            raise ValueError(
                f"Invalid transition: {self.status.value} -> {new_status.value}. "
                f"Allowed: {[s.value for s in allowed]}"
            )
        self.status = new_status

    def start(self):
        """Mark job as started (QUEUED -> RUNNING)."""
        self._transition(JobStatus.RUNNING)
        self.started_at = time.time()
        self.progress = 0
        self.message = "Job started"
        logger.info(f"Job {self.job_id} started")

    def update_progress(self, progress: int, message: str, stage: Optional[str] = None):
        """Update job progress without changing status."""
        self.progress = max(0, min(100, progress))
        self.message = message
        if stage:
            self.current_stage = stage
        logger.info(f"Job {self.job_id} progress: {progress}% - {message}")

    def succeed(self, metadata: Optional[Dict[str, Any]] = None):
        """Mark job as succeeded (RUNNING -> SUCCEEDED)."""
        self._transition(JobStatus.SUCCEEDED)
        self.completed_at = time.time()
        self.progress = 100
        self.message = "Job completed successfully"
        if metadata:
            self.metadata.update(metadata)
        logger.info(f"Job {self.job_id} succeeded")

    def complete(self, output_path: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        """Mark job as completed (RUNNING -> COMPLETED)."""
        self._transition(JobStatus.COMPLETED)
        self.completed_at = time.time()
        self.progress = 100
        self.message = "Job completed"
        self.output_path = output_path
        if metadata:
            self.metadata.update(metadata)
        logger.info(f"Job {self.job_id} completed")

    def fail(self, error: str, metadata: Optional[Dict[str, Any]] = None):
        """Mark job as failed (RUNNING -> FAILED)."""
        self._transition(JobStatus.FAILED)
        self.completed_at = time.time()
        self.error = error
        self.message = f"Job failed: {error}"
        if metadata:
            self.metadata.update(metadata)
        logger.error(f"Job {self.job_id} failed: {error}")

    def cancel(self):
        """Mark job as cancelled (QUEUED or RUNNING -> CANCELLED)."""
        self._transition(JobStatus.CANCELLED)
        self.completed_at = time.time()
        self.message = "Job cancelled"
        logger.info(f"Job {self.job_id} cancelled")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (ISO strings for dates)."""
        return {
            "job_id": self.job_id,
            "project_id": self.project_id,
            "job_type": self.job_type,
            "status": self.status.value,
            "progress": self.progress,
            "message": self.message,
            "current_stage": self.current_stage,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "error": self.error,
            "output_path": self.output_path,
            "params": self.params,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JobState':
        """Create from dictionary."""
        job = cls(
            data["job_id"],
            data["project_id"],
            job_type=data.get("job_type", "video_render"),
            params=data.get("params", {})
        )
        job.status = JobStatus(data["status"])
        job.progress = data.get("progress", 0)
        job.message = data.get("message", "")
        job.current_stage = data.get("current_stage")
        job.created_at = data.get("created_at", time.time())
        job.started_at = data.get("started_at")
        job.completed_at = data.get("completed_at")
        job.error = data.get("error")
        job.output_path = data.get("output_path")
        job.metadata = data.get("metadata", {})
        return job
