from app.core.result import Result


class TestResult:
    def test_success_creates_ok_result(self):
        r = Result.success(data={"script": "hello"})
        assert r.ok is True
        assert r.data == {"script": "hello"}
        assert r.error is None
        assert r.code == "SUCCESS"

    def test_failure_creates_error_result(self):
        r = Result.failure(error="something went wrong")
        assert r.ok is False
        assert r.error == "something went wrong"
        assert r.data is None

    def test_success_default_data_is_none(self):
        r = Result.success()
        assert r.ok is True
        assert r.data is None

    def test_failure_custom_code(self):
        r = Result.failure(error="not found", code="NOT_FOUND")
        assert r.ok is False
        assert r.code == "NOT_FOUND"

    def test_bool_magic(self):
        assert bool(Result.success()) is True
        assert bool(Result.failure("err")) is False

    def test_to_dict_success(self):
        d = Result.success(data="val").to_dict()
        assert d == {"ok": True, "code": "SUCCESS", "data": "val"}

    def test_to_dict_failure(self):
        d = Result.failure(error="fail", code="ERR").to_dict()
        assert d == {"ok": False, "code": "ERR", "error": "fail"}

    def test_repr_success(self):
        assert repr(Result.success(data=42)) == "Result.ok(data=42)"

    def test_repr_failure(self):
        assert repr(Result.failure(error="bad")) == "Result.fail(error='bad')"
