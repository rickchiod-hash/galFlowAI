"""Metrics Service - Métricas do GalFlowAI Studio."""
import logging
import time
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from collections import defaultdict

from app.config import LOGS_DIR

logger = logging.getLogger(__name__)
METRICS_DIR = LOGS_DIR
METRICS_FILE = METRICS_DIR / "metrics.json"


class MetricsService:
    """Serviço para coleta e consulta de métricas."""
    
    def __init__(self):
        self.metrics_file = METRICS_FILE
        METRICS_DIR.mkdir(parents=True, exist_ok=True)
        self._ensure_file()
    
    def _ensure_file(self):
        """Garante que arquivo de métricas existe."""
        if not self.metrics_file.exists():
            initial_data = {
                "generated_scripts": 0,
                "generated_videos": 0,
                "fallback_used": 0,
                "errors": 0,
                "total_generation_time": 0.0,
                "operations": []
            }
            self._save_data(initial_data)
    
    def _load_data(self) -> Dict[str, Any]:
        """Carrega dados do arquivo."""
        try:
            return json.loads(self.metrics_file.read_text(encoding="utf-8"))
        except Exception as e:
            logger.warning("Metrics load failed, resetting: %s", e)
            self.metrics_file.unlink(missing_ok=True)
            self._ensure_file()
            return json.loads(self.metrics_file.read_text(encoding="utf-8"))
    
    def _save_data(self, data: Dict[str, Any]):
        """Salva dados no arquivo."""
        self.metrics_file.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    
    def record_script_generation(
        self,
        success: bool,
        duration: float,
        provider: str,
        used_fallback: bool = False,
        project_id: str = ""
    ):
        """Registra geração de roteiro."""
        data = self._load_data()
        data["generated_scripts"] += 1
        data["total_generation_time"] += duration
        
        if not success:
            data["errors"] += 1
        
        if used_fallback:
            data["fallback_used"] += 1
        
        operation = {
            "type": "script_generation",
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "duration": duration,
            "provider": provider,
            "used_fallback": used_fallback,
            "project_id": project_id
        }
        data["operations"].append(operation)
        self._save_data(data)
    
    def record_video_generation(
        self,
        success: bool,
        duration: float,
        engine: str,
        used_fallback: bool = False,
        project_id: str = ""
    ):
        """Registra geração de vídeo."""
        data = self._load_data()
        data["generated_videos"] += 1
        data["total_generation_time"] += duration
        
        if not success:
            data["errors"] += 1
        
        if used_fallback:
            data["fallback_used"] += 1
        
        operation = {
            "type": "video_generation",
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "duration": duration,
            "engine": engine,
            "used_fallback": used_fallback,
            "project_id": project_id
        }
        data["operations"].append(operation)
        self._save_data(data)
    
    def get_summary(self) -> Dict[str, Any]:
        """Retorna resumo das métricas."""
        data = self._load_data()
        
        total_ops = len(data.get("operations", []))
        recent_ops = data.get("operations", [])[-20:]  # Últimas 20
        
        success_rate = 0.0
        if total_ops > 0:
            success_count = sum(1 for op in data.get("operations", []) if op.get("success"))
            success_rate = (success_count / total_ops) * 100
        
        avg_time = 0.0
        if data["generated_scripts"] + data["generated_videos"] > 0:
            avg_time = data["total_generation_time"] / (data["generated_scripts"] + data["generated_videos"])
        
        return {
            "generated_scripts": data["generated_scripts"],
            "generated_videos": data["generated_videos"],
            "fallback_used": data["fallback_used"],
            "errors": data["errors"],
            "success_rate_percent": round(success_rate, 2),
            "average_generation_time": round(avg_time, 2),
            "total_operations": total_ops,
            "recent_operations": len(recent_ops)
        }
    
    def get_recent_operations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retorna operações recentes."""
        data = self._load_data()
        operations = data.get("operations", [])
        return operations[-limit:] if operations else []
    
    def get_fallback_rate(self) -> float:
        """Retorna taxa de uso de fallback."""
        data = self._load_data()
        total = data["generated_scripts"] + data["generated_videos"]
        if total == 0:
            return 0.0
        return (data["fallback_used"] / total) * 100


# Instância global
_metrics_service = None

def get_metrics_service() -> MetricsService:
    """Retorna instância singleton do MetricsService."""
    global _metrics_service
    if _metrics_service is None:
        _metrics_service = MetricsService()
    return _metrics_service
