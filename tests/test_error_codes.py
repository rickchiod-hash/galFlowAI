import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.error_codes import ErrorCode


def test_error_code_is_str_enum():
    assert issubclass(ErrorCode, str)
    assert hasattr(ErrorCode, "UNKNOWN_ERROR")


def test_error_code_values_are_stable():
    assert ErrorCode.UNKNOWN_ERROR == "UNKNOWN_ERROR"
    assert ErrorCode.GRADIO_START_FAILED == "GRADIO_START_FAILED"
    assert ErrorCode.FASTAPI_UNAVAILABLE == "FASTAPI_UNAVAILABLE"
    assert ErrorCode.LLM_PROVIDER_UNAVAILABLE == "LLM_PROVIDER_UNAVAILABLE"
    assert ErrorCode.SCRIPT_VALIDATION_FAILED == "SCRIPT_VALIDATION_FAILED"
    assert ErrorCode.FFMPEG_NOT_FOUND == "FFMPEG_NOT_FOUND"
    assert ErrorCode.FFMPEG_CONCAT_FAILED == "FFMPEG_CONCAT_FAILED"
    assert ErrorCode.WANGP_UNAVAILABLE == "WANGP_UNAVAILABLE"
    assert ErrorCode.TTS_UNAVAILABLE == "TTS_UNAVAILABLE"
    assert ErrorCode.PROJECT_NOT_FOUND == "PROJECT_NOT_FOUND"
    assert ErrorCode.INVALID_PROJECT_STATE == "INVALID_PROJECT_STATE"
    assert ErrorCode.TEMPLATE_PROVIDER_FAILED == "TEMPLATE_PROVIDER_FAILED"
    assert ErrorCode.FILE_SYSTEM_ERROR == "FILE_SYSTEM_ERROR"
    assert ErrorCode.CONFIG_INVALID == "CONFIG_INVALID"
    assert ErrorCode.BOOT_FAILED == "BOOT_FAILED"


def test_error_code_has_at_least_10_codes():
    assert len(ErrorCode) >= 10


def test_error_code_is_serializable():
    assert ErrorCode.FFMPEG_NOT_FOUND.value == "FFMPEG_NOT_FOUND"
    assert str(ErrorCode.FFMPEG_NOT_FOUND) == "FFMPEG_NOT_FOUND"


def test_error_code_from_string():
    code = ErrorCode("FFMPEG_NOT_FOUND")
    assert code == ErrorCode.FFMPEG_NOT_FOUND


def test_error_code_invalid_value_raises():
    import builtins
    try:
        ErrorCode("INVALID_CODE_THAT_DOES_NOT_EXIST")
        assert False, "Deveria ter levantado ValueError"
    except ValueError:
        pass
