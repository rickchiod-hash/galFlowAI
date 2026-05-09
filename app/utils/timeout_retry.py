import time
import logging
from typing import Callable, Any, Optional

logger = logging.getLogger(__name__)

class TimeoutRetry:
    def __init__(self, max_retries=3, base_delay=1.0, max_delay=10.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
    
    def execute(self, func, *args, **kwargs):
        last_exception = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    delay = min(self.base_delay * (2 ** (attempt - 1)), self.max_delay)
                    time.sleep(delay)
        raise last_exception
