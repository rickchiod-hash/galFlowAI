"""Tests for the standardized Result class."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.application.result import Result


def test_result_success():
    """Test creating a success result."""
    r = Result.success(data={"script": "test"}, provider="test_provider")
    assert r.ok is True
    assert r["ok"] is True  # dict access works
    assert r.data == {"script": "test"}
    assert r["data"] == {"script": "test"}
    assert r.provider == "test_provider"
    assert r["provider"] == "test_provider"
    assert bool(r) is True
    assert r.is_success() is True
    assert r.is_failure() is False
    print("PASS: test_result_success passed")
    return True


def test_result_failure():
    """Test creating a failure result."""
    r = Result.failure(error="something went wrong", project_id="123")
    assert r.ok is False
    assert r["ok"] is False
    assert r.error == "something went wrong"
    assert r["error"] == "something went wrong"
    assert r.project_id == "123"
    assert bool(r) is False
    assert r.is_success() is False
    assert r.is_failure() is True
    print("PASS: test_result_failure passed")
    return True


def test_result_dict_compatibility():
    """Test that Result behaves like a dict for backward compatibility."""
    r = Result.success(data={"key": "value"}, extra="extra")
    # Should be able to use .get()
    assert r.get("ok") is True
    assert r.get("data") == {"key": "value"}
    assert r.get("extra") == "extra"
    assert r.get("nonexistent") is None
    assert r.get("nonexistent", "default") == "default"
    # Should be iterable as dict
    assert "ok" in r
    assert "data" in r
    assert "extra" in r
    print("PASS: test_result_dict_compatibility passed")
    return True


def test_result_boolean_context():
    """Test using Result in boolean context."""
    success = Result.success(data="test")
    failure = Result.failure(error="fail")
    
    if success:
        pass  # Should enter
    else:
        assert False, "Success result should be truthy"
    
    if failure:
        assert False, "Failure result should be falsy"
    else:
        pass  # Should enter
    
    print("PASS: test_result_boolean_context passed")
    return True


def test_result_repr():
    """Test Result representation."""
    success = Result.success(data="test")
    failure = Result.failure(error="oops")
    
    repr_success = repr(success)
    repr_failure = repr(failure)
    
    assert "ok=True" in repr_success
    assert "ok=False" in repr_failure
    print("PASS: test_result_repr passed")
    return True


if __name__ == "__main__":
    results = []
    for name, fn in [
        ("Result success", test_result_success),
        ("Result failure", test_result_failure),
        ("Result dict compatibility", test_result_dict_compatibility),
        ("Result boolean context", test_result_boolean_context),
        ("Result repr", test_result_repr),
    ]:
        try:
            result = fn()
            results.append((name, result))
            if result:
                print(f"PASS: {name}")
            else:
                print(f"FAIL: {name}")
        except Exception as e:
            print(f"FAIL: {name} with exception: {e}")
            results.append((name, False))
    
    print("\n" + "="*60)
    print("RESULTS: Result class tests")
    print("="*60)
    for name, result in results:
        status = "PASSED" if result else "FAILED"
        print(f"{name:<50} {status}")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nPASSED: {passed}/{total}")
    
    if passed == total:
        print("ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print("SOME TESTS FAILED!")
        sys.exit(1)
