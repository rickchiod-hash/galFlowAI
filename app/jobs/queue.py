"""Job queue with formal JobState (PIPE-400)."""
import json
import time
import uuid
from pathlib import Path
from typing import Optional, Dict, Any, List
from app.logging_config import setup_logger
from app.pipeline.job_state import JobState, JobStatus as _JobStatus

# Re-export JobStatus for backward compatibility with existing imports
JobStatus = _JobStatus

logger = setup_logger()

STATE_DIR = Path(__file__).parent.parent.parent / "state"
DEFAULT_QUEUE_FILE = STATE_DIR / "job_queue.json"


def retry_with_backoff(func, max_retries=3, base_delay=0.5, max_delay=5.0, *args, **kwargs):
    """Retry com exponential backoff."""
    last_exception = None
    for attempt in range(max_retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt < max_retries:
                delay = min(base_delay * (2 ** attempt), max_delay)
                logger.warning(f"Tentativa {attempt + 1} falhou: {str(e)}. Retry em {delay}s...")
                time.sleep(delay)
            else:
                logger.error(f"Todas as {max_retries + 1} tentativas falharam.")
                raise last_exception
    raise last_exception


def validate_job_files(script_path: Optional[str] = None,
                       audio_path: Optional[str] = None,
                       video_path: Optional[str] = None) -> bool:
    """Validate that job artifact files exist."""
    for path in [script_path, audio_path, video_path]:
        if path is not None and not Path(path).exists():
            return False
    return True


class JobQueue:
    """Persistent job queue with formal JobState.

    - Uses JobState with guarded transitions
    - Mutex: single running job enforced
    - Persistence to JSON file
    """

    def __init__(self, queue_file: Optional[Path] = None):
        self.queue_file = queue_file or DEFAULT_QUEUE_FILE
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)
        self.jobs: Dict[str, JobState] = {}
        self.running_job_id: Optional[str] = None
        self._load()

    def _load(self):
        """Load jobs from persistent JSON file."""
        if not self.queue_file.exists():
            return
        def do_load():
            data = json.loads(self.queue_file.read_text(encoding="utf-8"))
            for job_data in data.get("jobs", []):
                job = JobState.from_dict(job_data)
                self.jobs[job.job_id] = job
            self.running_job_id = data.get("running_job_id")
            logger.info("Fila carregada: %d jobs", len(self.jobs))
        try:
            retry_with_backoff(do_load, max_retries=3, base_delay=0.2)
        except Exception as e:
            logger.error("CAUSA: Erro ao carregar fila: %s | CORREÇÃO: Verifique se queue.json não está corrompido", e)

    def _save(self):
        """Persist jobs to JSON file."""
        data = {
            "jobs": [job.to_dict() for job in self.jobs.values()],
            "running_job_id": self.running_job_id,
            "updated_at": time.time()
        }
        def do_save():
            self.queue_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        try:
            retry_with_backoff(do_save, max_retries=3, base_delay=0.2)
        except Exception as e:
            logger.error("CAUSA: Erro ao salvar fila após retries: %s | CORREÇÃO: Verifique permissões de escrita", e)

    @staticmethod
    def clear_all():
        """Clear all jobs (for tests)."""
        import gc
        for obj in gc.get_objects():
            if isinstance(obj, JobQueue):
                obj.jobs.clear()
                obj.running_job_id = None

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
        return self.jobs.get(job_id)

    def get_next_job(self) -> Optional[JobState]:
        """Claim next queued job (mutex: only 1 running)."""
        if self.running_job_id is not None:
            logger.warning(
                "CAUSA: Job %s ainda em execução | CORREÇÃO: Aguarde conclusão ou cancele job",
                self.running_job_id
            )
            return None
        for job in self.jobs.values():
            if job.status == JobStatus.QUEUED:
                job.start()
                self.running_job_id = job.job_id
                self._save()
                return job
        return None

    def complete_job(self, job_id: str, output_path: Optional[str] = None):
        """Mark job as completed."""
        job = self.jobs.get(job_id)
        if job:
            try:
                job.complete(output_path=output_path)
            except ValueError:
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
        if job:
            try:
                job.fail(error_msg)
            except ValueError:
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
            return False
        try:
            job.cancel()
        except ValueError:
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
            return False
        del self.jobs[job_id]
        if self.running_job_id == job_id:
            self.running_job_id = None
        self._save()
        logger.info("Job %s removido", job_id)
        return True

    def list_jobs(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List jobs, optionally filtered by status value."""
        jobs = list(self.jobs.values())
        if status:
            jobs = [j for j in jobs if j.status.value == status]
        return [j.to_dict() for j in jobs]

    def get_status(self) -> Dict[str, Any]:
        """Get queue status summary."""
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


queue = JobQueue()
