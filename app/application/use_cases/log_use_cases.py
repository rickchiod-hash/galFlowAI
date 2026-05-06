"""Use cases for logs and diagnostics (V2.1 / H13)."""
from typing import Dict, Any, Optional, List
from app.application.use_cases.base import UseCase
from app.services.log_service import (
    get_recent_logs,
    get_log_summary,
    get_last_error,
    copy_diagnostic_bundle
)


class GetRecentLogsUseCase(UseCase):
    """Get recent logs with filters.
    
    3-point standard:
    1. Validate level, search, limit parameters
    2. Get recent logs from log service
    3. Return logs list with metadata
    """
    
    def __init__(self):
        super().__init__()
    
    def execute(
        self,
        level: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 200
    ) -> Dict[str, Any]:
        """Execute get recent logs."""
        try:
            if not self._validate(level=level, search=search, limit=limit):
                return self._build_error("Invalid parameters")
            
            result = get_recent_logs(level=level, search=search, limit=limit)
            return self._build_success(data=result)
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        level = kwargs.get("level")
        limit = kwargs.get("limit", 200)
        
        valid_levels = [None, "info", "warn", "error"]
        if level not in valid_levels:
            return False
        if not isinstance(limit, int) or limit <= 0:
            return False
        return True


class GetLogSummaryUseCase(UseCase):
    """Get log summary statistics.
    
    3-point standard:
    1. Validate input (none needed)
    2. Get log summary from log service
    3. Return summary dict
    """
    
    def __init__(self):
        super().__init__()
    
    def execute(self) -> Dict[str, Any]:
        """Execute get log summary."""
        try:
            result = get_log_summary()
            return self._build_success(data=result)
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        return True


class GetLastErrorUseCase(UseCase):
    """Get last error from logs.
    
    3-point standard:
    1. Validate input (none needed)
    2. Get last error from log service
    3. Return error dict or None
    """
    
    def __init__(self):
        super().__init__()
    
    def execute(self) -> Dict[str, Any]:
        """Execute get last error."""
        try:
            result = get_last_error()
            return self._build_success(data=result)
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        return True


class GetDiagnosticBundleUseCase(UseCase):
    """Get diagnostic bundle for support.
    
    3-point standard:
    1. Validate input (none needed)
    2. Get diagnostic bundle from log service
    3. Return diagnostic string
    """
    
    def __init__(self):
        super().__init__()
    
    def execute(self) -> Dict[str, Any]:
        """Execute get diagnostic bundle."""
        try:
            result = copy_diagnostic_bundle()
            return self._build_success(data={"diagnostic": result})
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        return True
