"""Use cases for idempotency (PIPE-401)."""
from typing import Dict, Any, Optional
from app.application.use_cases.base_use_case import BaseUseCase
from app.services.idempotency_service import registry, generate_key


class CheckIdempotencyUseCase(BaseUseCase):
    """Check if a pipeline stage has already been completed with identical inputs.

    3-point standard:
    1. Validate stage name and params
    2. Generate hash key and check registry
    3. Return cached output if found, or indicate not cached
    """

    def execute(self, stage: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute idempotency check use case."""
        try:
            if not self._validate(stage=stage, params=params):
                return self._build_error("Invalid stage name or params")

            key = generate_key(stage, params)
            entry = registry.check(key)
            if entry and registry.is_completed(key):
                return self._build_success(data={
                    "cached": True,
                    "key": key,
                    "output": entry["output"],
                    "stage": stage
                })
            return self._build_success(data={
                "cached": False,
                "key": key,
                "stage": stage
            })
        except Exception as e:
            return self._build_error(str(e))

    def _validate(self, **kwargs) -> bool:
        stage = kwargs.get("stage", "")
        params = kwargs.get("params", {})
        return bool(stage and isinstance(params, dict))


class RegisterIdempotencyUseCase(BaseUseCase):
    """Register a completed pipeline stage output for future idempotency checks.

    3-point standard:
    1. Validate stage, params and output
    2. Generate hash key and register in registry
    3. Return registration status
    """

    def execute(self, stage: str, params: Dict[str, Any],
                output: Dict[str, Any],
                ttl_seconds: Optional[int] = None) -> Dict[str, Any]:
        """Execute idempotency registration use case."""
        try:
            if not self._validate(stage=stage, params=params, output=output):
                return self._build_error("Invalid stage, params or output")

            key = generate_key(stage, params)
            registry.register(key, stage, output, ttl_seconds=ttl_seconds)

            return self._build_success(data={
                "registered": True,
                "key": key,
                "stage": stage
            })
        except Exception as e:
            return self._build_error(str(e))

    def _validate(self, **kwargs) -> bool:
        stage = kwargs.get("stage", "")
        params = kwargs.get("params", {})
        output = kwargs.get("output", {})
        return bool(stage and isinstance(params, dict) and isinstance(output, dict) and output)
