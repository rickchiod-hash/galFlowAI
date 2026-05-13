import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.app_error import AppError, Severity
from app.core.error_codes import ErrorCode


def test_app_error_creation_minimal():
    err = AppError(
        code=ErrorCode.FFMPEG_NOT_FOUND,
        severity=Severity.ERROR,
        message="FFmpeg não encontrado.",
        suggestion="Instale FFmpeg ou configure o path.",
        stage="render",
        retryable=True,
    )
    assert err.code == ErrorCode.FFMPEG_NOT_FOUND
    assert err.severity == Severity.ERROR
    assert err.retryable is True
    assert err.project_id is None
    assert err.job_id is None
    assert err.provider is None
    assert err.fallback_used is False
    assert err.details is None


def test_app_error_creation_full():
    err = AppError(
        code=ErrorCode.FFMPEG_CONCAT_FAILED,
        severity=Severity.ERROR,
        message="FFmpeg falhou ao concatenar vídeos.",
        suggestion="Verifique inputs.txt, caminhos dos arquivos e -safe 0.",
        stage="concat",
        retryable=True,
        project_id="proj_123",
        job_id="job_456",
        provider="ffmpeg",
        fallback_used=True,
        details={"input_count": 3, "output": "final.mp4"},
    )
    assert err.project_id == "proj_123"
    assert err.job_id == "job_456"
    assert err.provider == "ffmpeg"
    assert err.fallback_used is True
    assert err.details == {"input_count": 3, "output": "final.mp4"}


def test_app_error_to_dict():
    err = AppError(
        code=ErrorCode.WANGP_UNAVAILABLE,
        severity=Severity.WARN,
        message="WanGP indisponível, usando FFmpeg.",
        suggestion="Verifique se o modelo WanGP está baixado.",
        stage="render",
        retryable=False,
        project_id="proj_123",
    )
    d = err.to_dict()
    assert d["code"] == "WANGP_UNAVAILABLE"
    assert d["severity"] == "WARN"
    assert d["project_id"] == "proj_123"
    assert "job_id" not in d
    assert "provider" not in d


def test_app_error_to_json_line():
    err = AppError(
        code=ErrorCode.LLM_PROVIDER_UNAVAILABLE,
        severity=Severity.WARN,
        message="LLM provider indisponível, usando template.",
        suggestion="Verifique se o servidor LLM está rodando.",
        stage="script",
        retryable=True,
        project_id="proj_123",
        provider="lm_studio",
    )
    line = err.to_json_line()
    assert '"code": "LLM_PROVIDER_UNAVAILABLE"' in line
    assert '"severity": "WARN"' in line
    assert '"project_id": "proj_123"' in line
    assert line.endswith("}")


def test_severity_values():
    assert Severity.DEBUG == "DEBUG"
    assert Severity.INFO == "INFO"
    assert Severity.WARN == "WARN"
    assert Severity.ERROR == "ERROR"


def test_app_error_with_string_code():
    err = AppError(
        code="CUSTOM_ERROR",
        severity=Severity.ERROR,
        message="Erro customizado.",
        suggestion="Entre em contato com o suporte.",
        stage="general",
        retryable=False,
    )
    assert err.code == "CUSTOM_ERROR"
    assert err.to_dict()["code"] == "CUSTOM_ERROR"
