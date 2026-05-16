"""Job queue with formal JobState using SQLite WAL ledger (PIPE-400 & PIPE-403)."""
import json
import time
import uuid
from pathlib import Path
from typing import Optional, Dict, Any, List
from app.logging_config import setup_logger
from app.pipeline.job_state import JobState, JobStatus as _JobStatus
from app.pipeline.job_ledger import SQLiteJobLedger
from app.exceptions import ValidationError

# Re-export JobStatus for backward compatibility with existing imports
JobStatus = _JobStatus

logger = setup_logger()

# Global SQLite ledger instance
_global_job_ledger = SQLiteJobLedger()


class JobQueue:
    """Persistent job queue with formal JobState using SQLite WAL ledger.

    - Uses JobState with guarded transitions
    - Mutex: single running job enforced
    - Persistence to SQLite WAL database (no JSON file needed)
    """

    def __init__(self, queue_file: Optional[Path] = None, job_ledger: Optional[SQLiteJobLedger] = None):
        # queue_file parameter kept for backward compatibility but ignored
        # as we now use SQLite ledger for persistence
        self._job_ledger = job_ledger or _global_job_ledger
        self.jobs: Dict[str, JobState] = {}  # In-memory cache for active jobs
        self.running_job_id: Optional[str] = None
        self._load()

    def _load(self):
        """Load jobs from persistent SQLite ledger into memory cache."""
        try:
            # Load all jobs from SQLite ledger
            jobs_from_ledger = self._job_ledger.load_jobs(limit=1000)  # Load recent jobs
            self.jobs = {job.job_id: job for job in jobs_from_ledger}
            
            # Get running job ID from ledger metadata
            self.running_job_id = self._job_ledger.get_running_job_id()
            
            logger.info("Fila carregada do SQLite ledger: %d jobs", len(self.jobs))
        except Exception as e:
            logger.error("CAUSA: Erro ao carregar fila do SQLite ledger: %s | CORREÇÃO: Verifique se o banco de dados está acessível", e)
            # Fallback to empty state if ledger fails
            self.jobs = {}
            self.running_job_id = None

    def _save(self):
        """Persist jobs to SQLite ledger."""
        try:
            # Save all cached jobs to SQLite ledger
            for job in self.jobs.values():
                self._job_ledger.save_job(job)
            
            # Update running job ID in ledger metadata
            self._job_ledger.set_running_job_id(self.running_job_id)
            
            logger.debug("Fila persistida no SQLite ledger: %d jobs", len(self.jobs))
        except Exception as e:
            logger.error("CAUSA: Erro ao salvar fila no SQLite ledger: %s | CORREÇÃO: Verifique permissões de banco de dados", e)
            # In a production system, we might want to retry or alert here

    @staticmethod
    def clear_all():
        """Clear all jobs (for tests)."""
        import gc
        for obj in gc.get_objects():
            if isinstance(obj, JobQueue):
                obj.jobs.clear()
                obj.running_job_id = None
        # Also clear the ledger for test isolation
        try:
            # Note: In a real test scenario, we might want to recreate the ledger
            # For now, we'll just clear the in-memory cache
            pass
        except Exception as e:
            logger.debug("Queue cleanup error: %s", e)

    def add_job(self, job_type: str, project_id: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Add a new job to queue."""
        job_id = "job_{}_{}".format(int(time.time() * 1000), uuid.uuid4().hex[:8])
        job = JobState(job_id, project_id, job_type=job_type, params=params)
        self.jobs[job_id] = job
        self._save()
        logger.info("Job adicionado: %s (%s)", job_id, job_type)
        return job_id

    def get_job(self, job_id: str) -> Optional[JobState]:
        """Get job by ID."""
        # Try memory cache first
        if job_id in self.jobs:
            return self.jobs[job_id]
        
        # Fallback to ledger
        job = self._job_ledger.load_job(job_id)
        if job:
            self.jobs[job_id] = job  # Cache for future access
        return job

    def get_next_job(self) -> Optional[JobState]:
        """Claim next queued job (mutex: only 1 running)."""
        if self.running_job_id is not None:
            logger.warning(
                "CAUSA: Job %s ainda em execução | CORREÇÃO: Aguarde conclusão ou cancele job",
                self.running_job_id
            )
            return None
        
        # Find next queued job
        for job in self.jobs.values():
            if job.status == JobStatus.QUEUED:
                job.start()
                self.running_job_id = job.job_id
                self._save()
                return job
        
        # If not found in cache, check ledger directly
        queued_jobs = self._job_ledger.load_jobs(status=JobStatus.QUEUED, limit=1)
        if queued_jobs:
            job = queued_jobs[0]
            job.start()
            self.jobs[job.job_id] = job  # Cache it
            self.running_job_id = job.job_id
            self._save()
            return job
            
        return None

    def complete_job(self, job_id: str, output_path: Optional[str] = None):
        """Mark job as completed."""
        job = self.jobs.get(job_id)
        if not job:
            # Try to load from ledger if not in cache
            job = self._job_ledger.load_job(job_id)
            if job:
                self.jobs[job_id] = job  # Cache it
        
        if job:
            try:
                job.complete(output_path=output_path)
            except (ValueError, ValidationError):
                job.status = JobStatus.COMPLETED
                job.completed_at = time.time()
                job.progress = 100
                job.output_path = output_path
            if self.running_job_id == job_id:
                self.running_job_id = None
            self._save()
            logger.info("Job %s completado", job_id)

    def fail_job(self, job_id: str, error_msg: str = ""):
        """Mark job as failed."""
        job = self.jobs.get(job_id)
        if not job:
            # Try to load from ledger if not in cache
            job = self._job_ledger.load_job(job_id)
            if job:
                self.jobs[job_id] = job  # Cache it
        
        if job:
            try:
                job.fail(error_msg)
            except (ValueError, ValidationError):
                job.status = JobStatus.FAILED
                job.completed_at = time.time()
                job.error = error_msg
            if self.running_job_id == job_id:
                self.running_job_id = None
            self._save()
            logger.info("Job %s falhou: %s", job_id, error_msg)

    def cancel_job(self, job_id: str) -> bool:
        """Cancel a queued or running job. Returns True if cancelled."""
        job = self.jobs.get(job_id)
        if not job:
            # Try to load from ledger if not in cache
            job = self._job_ledger.load_job(job_id)
            if job:
                self.jobs[job_id] = job  # Cache it
        
        if not job:
            return False
            
        try:
            job.cancel()
        except (ValueError, ValidationError):
            logger.warning("Job %s cannot be cancelled (status: %s)", job_id, job.status.value)
            return False
        if self.running_job_id == job_id:
            self.running_job_id = None
        self._save()
        logger.info("Job %s cancelado", job_id)
        return True

    def remove_job(self, job_id: str) -> bool:
        """Remove a job entirely from the queue. Returns True if removed."""
        if job_id not in self.jobs:
            # Check ledger directly
            if not self._job_ledger.load_job(job_id):
                return False
        
        # Remove from cache and ledger
        if job_id in self.jobs:
            del self.jobs[job_id]
        
        deleted = self._job_ledger.delete_job(job_id)
        
        if self.running_job_id == job_id:
            self.running_job_id = None
        self._save()
        logger.info("Job %s removido", job_id)
        return deleted

    def list_jobs(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List jobs, optionally filtered by status value."""
        # Try to get from ledger for consistency
        try:
            if status is not None:
                job_status = JobStatus(status)
                jobs_from_ledger = self._job_ledger.load_jobs(status=job_status)
            else:
                jobs_from_ledger = self._job_ledger.load_jobs()
            
            # Update cache
            for job in jobs_from_ledger:
                self.jobs[job.job_id] = job
                
            return [job.to_dict() for job in jobs_from_ledger]
        except Exception as e:
            logger.error("CAUSA: Erro ao listar jobs do SQLite ledger: %s | CORREÇÃO: Verifique o banco de dados", e)
            # Fallback to cache
            jobs = list(self.jobs.values())
            if status:
                jobs = [j for j in jobs if j.status.value == status]
            return [j.to_dict() for j in jobs]

    def get_status(self) -> Dict[str, Any]:
        """Get queue status summary."""
        try:
            # Get accurate counts from ledger
            total_jobs = self._job_ledger.load_jobs(limit=10000)  # Get all jobs for counting
            status_counts = {
                "queued": 0,
                "running": 0,
                "completed": 0,
                "failed": 0,
                "cancelled": 0
            }
            
            for job in total_jobs:
                status_value = job.status.value
                if status_value in status_counts:
                    status_counts[status_value] += 1
            
            # Get running job ID from ledger
            running_job_id = self._job_ledger.get_running_job_id()
            
            return {
                "total": len(total_jobs),
                "queued": status_counts["queued"],
                "running": status_counts["running"],
                "completed": status_counts["completed"] + status_counts.get("succeeded", 0),
                "failed": status_counts["failed"],
                "cancelled": status_counts["cancelled"],
                "running_job_id": running_job_id
            }
        except Exception as e:
            logger.error("CAUSA: Erro ao obter status do SQLite ledger: %s | CORREÇÃO: Verifique o banco de dados", e)
            # Fallback to cache-based calculation
            values = [j.status.value for j in self.jobs.values()]
            return {
                "total": len(self.jobs),
                "queued": values.count("queued"),
                "running": values.count("running"),
                "completed": values.count("completed") + values.count("succeeded"),
                "failed": values.count("failed"),
                "cancelled": values.count("cancelled"),
                "running_job_id": self.running_job_id
            }


# Global queue instance for backward compatibility
queue = JobQueue()
