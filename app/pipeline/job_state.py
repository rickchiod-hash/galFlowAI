"""Job state management for pipeline"""

from enum import Enum
from typing import Optional, Dict, Any
import time
import logging

logger = logging.getLogger(__name__)


class JobStatus(Enum):
    """Possible job states"""
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobState:
    """Manages job state and metadata"""
    
    def __init__(self, job_id: str, project_id: str):
        self.job_id = job_id
        self.project_id = project_id
        self.status = JobStatus.QUEUED
        self.created_at = time.time()
        self.started_at: Optional[float] = None
        self.completed_at: Optional[float] = None
        self.current_stage: Optional[str] = None
        self.progress: int = 0
        self.message: str = "Job queued"
        self.error: Optional[str] = None
        self.metadata: Dict[str, Any] = {}
    
    def start(self):
        """Mark job as started"""
        self.status = JobStatus.RUNNING
        self.started_at = time.time()
        self.progress = 0
        self.message = "Job started"
        logger.info(f"Job {self.job_id} started")
    
    def update_progress(self, progress: int, message: str, stage: Optional[str] = None):
        """Update job progress"""
        self.progress = progress
        self.message = message
        if stage:
            self.current_stage = stage
        logger.info(f"Job {self.job_id} progress: {progress}% - {message}")
    
    def succeed(self, metadata: Optional[Dict[str, Any]] = None):
        """Mark job as succeeded"""
        self.status = JobStatus.SUCCEEDED
        self.completed_at = time.time()
        self.progress = 100
        self.message = "Job completed successfully"
        if metadata:
            self.metadata.update(metadata)
        logger.info(f"Job {self.job_id} succeeded")
    
    def fail(self, error: str, metadata: Optional[Dict[str, Any]] = None):
        """Mark job as failed"""
        self.status = JobStatus.FAILED
        self.completed_at = time.time()
        self.error = error
        self.message = f"Job failed: {error}"
        if metadata:
            self.metadata.update(metadata)
        logger.error(f"Job {self.job_id} failed: {error}")
    
    def cancel(self):
        """Mark job as cancelled"""
        self.status = JobStatus.CANCELLED
        self.completed_at = time.time()
        self.message = "Job cancelled"
        logger.info(f"Job {self.job_id} cancelled")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "job_id": self.job_id,
            "project_id": self.project_id,
            "status": self.status.value,
            "progress": self.progress,
            "message": self.message,
            "current_stage": self.current_stage,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "error": self.error,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JobState':
        """Create from dictionary"""
        job = cls(data["job_id"], data["project_id"])
        job.status = JobStatus(data["status"])
        job.progress = data.get("progress", 0)
        job.message = data.get("message", "")
        job.current_stage = data.get("current_stage")
        job.created_at = data.get("created_at", time.time())
        job.started_at = data.get("started_at")
        job.completed_at = data.get("completed_at")
        job.error = data.get("error")
        job.metadata = data.get("metadata", {})
        return job