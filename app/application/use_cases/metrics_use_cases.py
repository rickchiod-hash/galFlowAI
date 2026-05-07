"""Use cases for metrics and monitoring (H12)."""
from typing import Dict, Any, List
from app.application.use_cases.base import UseCase
from app.services.metrics_service import get_metrics_service


class GetMetricsSummaryUseCase(UseCase):
    """Get metrics summary.
    
    3-point standard:
    1. Validate input (none needed)
    2. Get summary from metrics service
    3. Return summary dict
    """
    
    def __init__(self):
        super().__init__()
        self.metrics = get_metrics_service()
    
    def execute(self) -> Dict[str, Any]:
        """Execute get metrics summary."""
        try:
            summary = self.metrics.get_summary()
            return self._build_success(data=summary)
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        return True


class GetRecentOperationsUseCase(UseCase):
    """Get recent operations.
    
    3-point standard:
    1. Validate limit parameter
    2. Get recent operations from metrics service
    3. Return operations list
    """
    
    def __init__(self):
        super().__init__()
        self.metrics = get_metrics_service()
    
    def execute(self, limit: int = 10) -> Dict[str, Any]:
        """Execute get recent operations."""
        try:
            if not self._validate(limit=limit):
                return self._build_error("Invalid limit")
            
            operations = self.metrics.get_recent_operations(limit=limit)
            return self._build_success(data={"operations": operations, "count": len(operations)})
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        limit = kwargs.get("limit", 10)
        return isinstance(limit, int) and limit > 0


class RecordScriptMetricUseCase(UseCase):
    """Record script generation metric.
    
    3-point standard:
    1. Validate parameters
    2. Record metric via metrics service
    3. Return success
    """
    
    def __init__(self):
        super().__init__()
        self.metrics = get_metrics_service()
    
    def execute(
        self,
        success: bool,
        duration: float,
        provider: str,
        used_fallback: bool = False,
        project_id: str = ""
    ) -> Dict[str, Any]:
        """Execute record script metric."""
        try:
            if not self._validate(success=success, duration=duration, provider=provider):
                return self._build_error("Invalid parameters")
            
            self.metrics.record_script_generation(
                success=success,
                duration=duration,
                provider=provider,
                used_fallback=used_fallback,
                project_id=project_id
            )
            return self._build_success(data={"recorded": True})
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        success = kwargs.get("success")
        duration = kwargs.get("duration")
        provider = kwargs.get("provider", "")
        return isinstance(success, bool) and isinstance(duration, (int, float)) and bool(provider)


class RecordVideoMetricUseCase(UseCase):
    """Record video generation metric.
    
    3-point standard:
    1. Validate parameters
    2. Record metric via metrics service
    3. Return success
    """
    
    def __init__(self):
        super().__init__()
        self.metrics = get_metrics_service()
    
    def execute(
        self,
        success: bool,
        duration: float,
        engine: str,
        used_fallback: bool = False,
        project_id: str = ""
    ) -> Dict[str, Any]:
        """Execute record video metric."""
        try:
            if not self._validate(success=success, duration=duration, engine=engine):
                return self._build_error("Invalid parameters")
            
            self.metrics.record_video_generation(
                success=success,
                duration=duration,
                engine=engine,
                used_fallback=used_fallback,
                project_id=project_id
            )
            return self._build_success(data={"recorded": True})
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        success = kwargs.get("success")
        duration = kwargs.get("duration")
        engine = kwargs.get("engine", "")
        return isinstance(success, bool) and isinstance(duration, (int, float)) and bool(engine)
