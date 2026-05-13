import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.error_codes import ErrorCode
from app.core.app_error import AppError, Severity
from app.services.error_catalog_service import ErrorCatalogService


def test_get_error_definition_exists():
    svc = ErrorCatalogService()
    definition = svc.get_error_definition(ErrorCode.FFMPEG_NOT_FOUND)
    assert definition is not None
    assert "message" in definition
    assert "suggestion" in definition
    assert "severity" in definition


def test_get_error_definition_unknown():
    svc = ErrorCatalogService()
    definition = svc.get_error_definition("NONEXISTENT_CODE")
    assert definition is None


def test_build_user_message():
    svc = ErrorCatalogService()
    error = AppError(
        code=ErrorCode.FFMPEG_NOT_FOUND,
        severity=Severity.ERROR,
        message="FFmpeg não encontrado.",
        suggestion="Instale o FFmpeg.",
        stage="render",
        retryable=False,
    )
    msg = svc.build_user_message(error)
    assert "FFmpeg não encontrado" in msg
    assert "Instale o FFmpeg" in msg


def test_build_diagnostic_message():
    svc = ErrorCatalogService()
    error = AppError(
        code=ErrorCode.FFMPEG_CONCAT_FAILED,
        severity=Severity.ERROR,
        message="Falha na concatenação.",
        suggestion="Verifique inputs.txt.",
        stage="render",
        retryable=True,
        project_id="proj_123",
        job_id="job_456",
        provider="ffmpeg",
        fallback_used=True,
    )
    diag = svc.build_diagnostic_message(error)
    assert "[ERROR]" in diag
    assert "FFMPEG_CONCAT_FAILED" in diag
    assert "proj_123" in diag
    assert "job_456" in diag
    assert "ffmpeg" in diag
    assert "Fallback usado: sim" in diag


def test_is_retryable_true():
    svc = ErrorCatalogService()
    assert svc.is_retryable(ErrorCode.FFMPEG_CONCAT_FAILED) is True


def test_is_retryable_false():
    svc = ErrorCatalogService()
    assert svc.is_retryable(ErrorCode.PROJECT_NOT_FOUND) is False


def test_is_retryable_unknown():
    svc = ErrorCatalogService()
    assert svc.is_retryable("NONEXISTENT") is False


def test_get_suggestion():
    svc = ErrorCatalogService()
    suggestion = svc.get_suggestion(ErrorCode.WANGP_UNAVAILABLE)
    assert "FFmpeg será usado como fallback" in suggestion or "FFmpeg" in suggestion


def test_get_suggestion_unknown():
    svc = ErrorCatalogService()
    suggestion = svc.get_suggestion("NONEXISTENT")
    assert suggestion == "Consulte os logs para mais detalhes."


def test_all_error_codes_have_definitions():
    svc = ErrorCatalogService()
    for code in ErrorCode:
        definition = svc.get_error_definition(code)
        assert definition is not None, f"ErrorCode {code} missing definition"
        assert "message" in definition
        assert "suggestion" in definition
        assert "severity" in definition
        assert "retryable" in definition
        assert "stage" in definition


def test_llm_provider_unavailable_suggests_template():
    svc = ErrorCatalogService()
    suggestion = svc.get_suggestion(ErrorCode.LLM_PROVIDER_UNAVAILABLE)
    assert "TemplateProvider" in suggestion


def test_wangp_unavailable_suggests_ffmpeg():
    svc = ErrorCatalogService()
    suggestion = svc.get_suggestion(ErrorCode.WANGP_UNAVAILABLE)
    assert "FFmpeg" in suggestion


def test_fastapi_unavailable_suggests_health():
    svc = ErrorCatalogService()
    suggestion = svc.get_suggestion(ErrorCode.FASTAPI_UNAVAILABLE)
    assert "health" in suggestion.lower()
