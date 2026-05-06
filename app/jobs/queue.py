import json
import time
import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, Tuple
from app.logging_config import setup_logger
from app.exceptions import FallbackWarning

logger = setup_logger()

class JobStatus:
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

def validate_job_files(script_path: Optional[str] = None, 
                       audio_path: Optional[str] = None, 
                       video_path: Optional[str] = None) -> bool:
    """Valida se arquivos de job existam."""
    for path in [script_path, audio_path, video_path]:
        if path is not None:
            if not Path(path).exists():
                return False
    return True

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

class Job:
    def __init__(self, job_id, job_type, project_id, params=None):
        self.job_id = job_id
        self.job_type = job_type
        self.project_id = project_id
        self.params = params or {}
        self.status = JobStatus.QUEUED
        self.created_at = datetime.now().isoformat()
        self.started_at = None
        self.finished_at = None
        self.result = None
        self.error = None
        self.output_path = None
    
    def to_dict(self):
        return {
            "job_id": self.job_id,
            "job_type": self.job_type,
            "project_id": self.project_id,
            "status": self.status,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "result": self.result,
            "error": self.error,
            "output_path": self.output_path
        }

class JobQueue:
    def __init__(self, queue_file=None):
        self.queue_file = queue_file or Path("K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta/state/job_queue.json")
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)
        self.jobs = {}
        self.running_job_id = None
        self._load()
    
    def _load(self):
        if self.queue_file.exists():
            def do_load():
                data = json.loads(self.queue_file.read_text(encoding="utf-8"))
                for job_data in data.get("jobs", []):
                    job = Job(job_data["job_id"], job_data["job_type"], job_data["project_id"])
                    job.status = job_data["status"]
                    job.created_at = job_data["created_at"]
                    job.started_at = job_data.get("started_at")
                    job.finished_at = job_data.get("finished_at")
                    job.result = job_data.get("result")
                    job.error = job_data.get("error")
                    job.params = job_data.get("params", {})
                    job.output_path = job_data.get("output_path")
                    self.jobs[job.job_id] = job
                logger.info("Fila carregada: %d jobs", len(self.jobs))
            try:
                retry_with_backoff(do_load, max_retries=3, base_delay=0.2)
            except Exception as e:
                logger.error("Erro ao carregar fila: %s", e)
    
    def _save(self):
        data = {
            "jobs": [job.to_dict() for job in self.jobs.values()],
            "updated_at": datetime.now().isoformat()
        }
        
        def do_save():
            self.queue_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        
        try:
            retry_with_backoff(do_save, max_retries=3, base_delay=0.2)
            logger.info("Fila salva com sucesso")
        except Exception as e:
            logger.error("Erro ao salvar fila após retries: %s", e)
    
    @staticmethod
    def clear_all():
        """Limpa todos os jobs (para testes)."""
        import gc
        for obj in gc.get_objects():
            if isinstance(obj, JobQueue):
                obj.jobs.clear()
                obj.running_job_id = None
    
    def add_job(self, job_type, project_id, params=None):
        job_id = "job_{}_{}".format(int(time.time() * 1000), uuid.uuid4().hex[:8])
        job = Job(job_id, job_type, project_id, params)
        self.jobs[job_id] = job
        self._save()
        logger.info("Job adicionado: %s (%s)", job_id, job_type)
        return job_id
    
    def get_next_job(self):
        if self.running_job_id is not None:
            logger.warning("Job %s ainda em execução.", self.running_job_id)
            return None
        
        for job in self.jobs.values():
            if job.status == JobStatus.QUEUED:
                job.status = JobStatus.RUNNING
                job.started_at = datetime.now().isoformat()
                self.running_job_id = job.job_id
                self._save()
                return job
        return None
    
    def get_job(self, job_id):
        return self.jobs.get(job_id)
    
    def complete_job(self, job_id, output_path=None):
        job = self.jobs.get(job_id)
        if job:
            job.status = JobStatus.COMPLETED
            job.finished_at = datetime.now().isoformat()
            job.output_path = output_path
            if self.running_job_id == job_id:
                self.running_job_id = None
            self._save()
            logger.info("Job %s completado", job_id)
    
    def fail_job(self, job_id, error_msg=""):
        job = self.jobs.get(job_id)
        if job:
            job.status = JobStatus.FAILED
            job.finished_at = datetime.now().isoformat()
            job.error = error_msg
            if self.running_job_id == job_id:
                self.running_job_id = None
            self._save()
            logger.info("Job %s falhou: %s", job_id, error_msg)
    
    def list_jobs(self, status=None):
        jobs = list(self.jobs.values())
        if status:
            jobs = [j for j in jobs if j.status == status]
        return [j.to_dict() for j in jobs]

queue = JobQueue()
