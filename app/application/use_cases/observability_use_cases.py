"""Use cases for Advanced Observability (V3.0 / H18)."""
from typing import Dict, Any, List, Optional
from app.application.use_cases.base import UseCase
from app.config import LOGS_DIR, BASE_DIR
from datetime import datetime
import json
from pathlib import Path


class GetHealthDashboardUseCase(UseCase):
    """Get comprehensive health dashboard data.
    
    3-point standard:
    1. Validate input (none needed)
    2. Collect health metrics from all services
    3. Return dashboard data
    """
    
    def __init__(self):
        super().__init__()
        self.log_dir = LOGS_DIR
    
    def execute(self) -> Dict[str, Any]:
        """Execute health dashboard collection."""
        try:
            dashboard = {
                "timestamp": datetime.now().isoformat(),
                "status": "healthy",
                "services": self._check_services(),
                "system": self._check_system(),
                "metrics": self._get_metrics_summary(),
                "recent_errors": self._get_recent_errors(limit=5)
            }
            
            # Determine overall status
            failed_services = [s for s in dashboard["services"].values() if not s.get("available")]
            if failed_services:
                dashboard["status"] = "degraded" if len(failed_services) < len(dashboard["services"]) else "unhealthy"
            
            return self._build_success(data=dashboard)
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        return True
    
    def _check_services(self) -> Dict[str, Any]:
        """Check availability of all services."""
        services = {}
        
        # Check FFmpeg
        try:
            from app.adapters.ffmpeg_adapter import FFmpegAdapter
            adapter = FFmpegAdapter()
            status = adapter.get_status()
            services["ffmpeg"] = {
                "available": status.get("available", False),
                "path": status.get("path", "N/A")
            }
        except Exception as e:
            services["ffmpeg"] = {"available": False, "error": str(e)}
        
        # Check WanGP
        try:
            from app.adapters.wangp_adapter import WanGPAdapter
            adapter = WanGPAdapter()
            services["wangp"] = {
                "available": adapter.is_available(),
                "path": str(BASE_DIR / "engines" / "Wan2GP")
            }
        except Exception as e:
            services["wangp"] = {"available": False, "error": str(e)}
        
        # Check Ollama
        try:
            import subprocess
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            services["ollama"] = {
                "available": result.returncode == 0,
                "models": result.stdout.count("\n") if result.returncode == 0 else 0
            }
        except Exception as e:
            services["ollama"] = {"available": False, "error": str(e)}
        
        return services
    
    def _check_system(self) -> Dict[str, Any]:
        """Check system resources."""
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage(str(BASE_DIR))
            
            return {
                "cpu_percent": cpu_percent,
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "percent_used": memory.percent
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "percent_used": disk.percent
                }
            }
        except ImportError:
            return {"error": "psutil not installed"}
        except Exception as e:
            return {"error": str(e)}
    
    def _get_metrics_summary(self) -> Dict[str, Any]:
        """Get metrics summary."""
        try:
            from app.services.metrics_service import get_metrics_service
            metrics = get_metrics_service()
            return metrics.get_summary()
        except Exception:
            return {"error": "Metrics service unavailable"}
    
    def _get_recent_errors(self, limit: int = 5) -> List[Dict]:
        """Get recent errors from logs."""
        try:
            from app.services.log_service import get_recent_logs
            result = get_recent_logs(level="error", limit=limit)
            return result.get("logs", [])[:limit]
        except Exception:
            return []


class GetStructuredLogsUseCase(UseCase):
    """Get logs in structured JSON format.
    
    3-point standard:
    1. Validate filters
    2. Parse logs into structured format
    3. Return JSON logs
    """
    
    def __init__(self):
        super().__init__()
        self.log_dir = LOGS_DIR
    
    def execute(
        self,
        level: Optional[str] = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Execute structured logs retrieval."""
        try:
            if not self._validate(level=level, limit=limit):
                return self._build_error("Invalid parameters")
            
            logs = self._parse_logs(level=level, limit=limit)
            
            return self._build_success(data={
                "logs": logs,
                "count": len(logs),
                "format": "json"
            })
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        level = kwargs.get("level")
        limit = kwargs.get("limit", 100)
        
        valid_levels = [None, "INFO", "WARN", "ERROR", "DEBUG"]
        if level not in valid_levels:
            return False
        if not isinstance(limit, int) or limit <= 0:
            return False
        return True
    
    def _parse_logs(self, level: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """Parse log file into structured JSON."""
        log_file = self.log_dir / "galflowai.log"
        if not log_file.exists():
            return []
        
        structured = []
        try:
            lines = log_file.read_text(encoding="utf-8", errors="ignore").splitlines()
            lines = [l for l in lines if l.strip()][-limit:]
            
            for line in lines:
                parsed = self._parse_line(line)
                if parsed and (not level or parsed.get("level") == level):
                    structured.append(parsed)
            
            return structured[-limit:]
        except Exception:
            return []
    
    def _parse_line(self, line: str) -> Optional[Dict]:
        """Parse a single log line into structured format."""
        try:
            # Expected format: timestamp [LEVEL] message
            import re
            match = re.match(r'^(.+?)\s+$$(\w+)$$\s+(.+)$', line)
            if match:
                return {
                    "timestamp": match.group(1).strip(),
                    "level": match.group(2).strip(),
                    "message": match.group(3).strip()
                }
            return None
        except Exception:
            return None
