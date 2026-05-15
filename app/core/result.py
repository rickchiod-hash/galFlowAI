from typing import Generic, TypeVar, Optional, Dict, Any

T = TypeVar('T')


class Result(Generic[T]):
    """Generic Result type for standardized success/failure returns.

    Usage:
        Result.success(data={"script": "..."})
        Result.failure(error="Something went wrong")
    """

    def __init__(self, ok: bool, data: Optional[T] = None, error: Optional[str] = None, code: str = "SUCCESS"):
        self._ok = ok
        self._data = data
        self._error = error
        self._code = code

    @property
    def ok(self) -> bool:
        return self._ok

    @property
    def data(self) -> Optional[T]:
        return self._data

    @property
    def error(self) -> Optional[str]:
        return self._error

    @property
    def code(self) -> str:
        return self._code

    @classmethod
    def success(cls, data: T = None, code: str = "SUCCESS") -> 'Result[T]':
        return cls(ok=True, data=data, code=code)

    @classmethod
    def failure(cls, error: str, code: str = "ERROR") -> 'Result[T]':
        return cls(ok=False, error=error, code=code)

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"ok": self._ok, "code": self._code}
        if self._data is not None:
            d["data"] = self._data
        if self._error is not None:
            d["error"] = self._error
        return d

    def __bool__(self) -> bool:
        return self._ok

    def __repr__(self) -> str:
        if self._ok:
            return f"Result.ok(data={self._data!r})"
        return f"Result.fail(error={self._error!r})"
