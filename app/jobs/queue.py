import json
import time
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
from app.logging_config import setup_logger
from app.exceptions import JobError, FallbackWarning

logger = setup_logger()

def retry_with_backoff(func, max_retries=3, base_delay=0.5, max_delay=5.0, *args, **kwargs):
    """Retry com exponential backoff para operações de fila."""
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
        self.status = "queued"
        self.created_at = datetime.now().isoformat()
        self.started_at = None
        self.finished_at = None
        self.result = None
        self.error = None
    
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
            "error": self.error
        }

class JobQueue:
    def __init__(self, queue_file=None):
        self.queue_file = queue_file or Path("K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta/state/job_queue.json")
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)
        self.jobs = {}
        self.running_job_id = None  # Controle de concorrência: apenas 1 job por vez
        self.load()
    
    def load(self):
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
                    self.jobs[job.job_id] = job
                logger.info("Fila carregada: %d jobs", len(self.jobs))
            try:
                retry_with_backoff(do_load, max_retries=3, base_delay=0.2)
            except Exception as e:
                logger.error("Erro ao carregar fila: %s", e)
    
    def save(self):
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
    
    def add_job(self, job_type, project_id, params=None):
        job_id = "job_{}".format(int(time.time()))
        job = Job(job_id, job_type, project_id, params)
        self.jobs[job_id] = job
        self.save()
        logger.info("Job adicionado: %s (%s)", job_id, job_type)
        return job
    
    def get_next_job(self):
        # Controle de concorrência: apenas 1 job por vez (GPU 6GB)
        if self.running_job_id is not None:
            logger.warning("Job %s ainda em execução. Aguardando...", self.running_job_id)
            return None
        
        for job in self.jobs.values():
            if job.status == "queued":
                return job
        return None
    
    def validate_job_files(self, job) -> tuple[bool, str]:
        """
        Valida se os arquivos necessários para o job existem.
        Retorna (válido, mensagem).
        """
        params = job.params or {}
        
        # Verifica arquivos de entrada
        input_files = params.get("input_files", [])
        if input_files:
            for f in input_files:
                if not Path(f).exists():
                    return False, f"Arquivo não encontrado: {f}"
        
        # Verifica se diretórios de saída são válidos
        output_dir = params.get("output_dir")
        if output_dir:
            try:
                Path(output_dir).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                return False, f"Erro ao criar diretório de saída: {e}"
        
        return True, "Arquivos validados"
    
    def get_job(self, job_id):
        return self.jobs.get(job_id)
    
    def update_job_status(self, job_id, status, result=None, error=None):
        job = self.jobs.get(job_id)
        if job:
            job.status = status
            if status == "running" and not job.started_at:
                job.started_at = datetime.now().isoformat()
                self.running_job_id = job_id  # Controle de concorrência
            if status in ("completed", "failed", "cancelled"):
                job.finished_at = datetime.now().isoformat()
                if self.running_job_id == job_id:
                    self.running_job_id = None  # Libera para próximo job
            if result:
                job.result = result
            if error:
                job.error = str(error)
            self.save()
            logger.info("Job %s atualizado: %s", job_id, status)
    
    def get_project_jobs(self, project_id):
        return [job.to_dict() for job in self.jobs.values() if job.project_id == project_id]
    
    def get_queue_status(self):
        status = {"queued": 0, "running": 0, "completed": 0, "failed": 0, "cancelled": 0}
        for job in self.jobs.values():
            if job.status in status:
                status[job.status] += 1
        return status

queue = JobQueue()
