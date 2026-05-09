from typing import Any, Optional


class Result(dict):
    def __init__(self, ok: bool, data: Any = None, error: str = None, **extras):
        d = {"ok": ok}
        if ok:
            d["data"] = data
        else:
            d["error"] = error
        d.update(extras)
        super().__init__(d)
        for key, value in extras.items():
            setattr(self, key, value)

    @property
    def ok(self) -> bool:
        return self.get("ok", False)

    @property
    def data(self):
        return self.get("data")

    @property
    def error(self) -> Optional[str]:
        return self.get("error")

    @classmethod
    def success(cls, data: Any = None, **extras) -> "Result":
        return cls(ok=True, data=data, **extras)

    @classmethod
    def failure(cls, error: str, **extras) -> "Result":
        return cls(ok=False, error=error, **extras)

    def is_success(self) -> bool:
        return bool(self.get("ok", False))

    def is_failure(self) -> bool:
        return not self.is_success()

    def __bool__(self):
        return bool(self.get("ok", False))

    def __repr__(self):
        if self.ok:
            return f"Result(ok=True, data={self.data})"
        else:
            return f"Result(ok=False, error='{self.error}')"
