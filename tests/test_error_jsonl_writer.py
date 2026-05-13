import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.error_codes import ErrorCode
from app.core.app_error import AppError, Severity
from app.services.error_jsonl_writer import ErrorJsonlWriter


def test_write_creates_file():
    with tempfile.TemporaryDirectory() as tmp:
        writer = ErrorJsonlWriter(errors_dir=Path(tmp))
        error = AppError(
            code=ErrorCode.FFMPEG_NOT_FOUND,
            severity=Severity.ERROR,
            message="FFmpeg não encontrado.",
            suggestion="Instale o FFmpeg.",
            stage="render",
            retryable=False,
        )
        result = writer.write(error)
        assert result is True
        files = list(Path(tmp).iterdir())
        assert len(files) == 1
        assert files[0].suffix == ".jsonl"


def test_write_appends():
    with tempfile.TemporaryDirectory() as tmp:
        writer = ErrorJsonlWriter(errors_dir=Path(tmp))
        e1 = AppError(ErrorCode.FFMPEG_NOT_FOUND, Severity.ERROR, "msg1", "sug1", "stage", False)
        e2 = AppError(ErrorCode.WANGP_UNAVAILABLE, Severity.WARN, "msg2", "sug2", "stage", True)
        writer.write(e1)
        writer.write(e2)
        lines = writer.read_recent(limit=10)
        assert len(lines) == 2
        assert lines[0]["code"] == "FFMPEG_NOT_FOUND"
        assert lines[1]["code"] == "WANGP_UNAVAILABLE"


def test_write_failure_does_not_crash():
    writer = ErrorJsonlWriter(errors_dir=Path("Z:/nonexistent_path_that_does_not_exist_xyz"))
    error = AppError(ErrorCode.UNKNOWN_ERROR, Severity.ERROR, "msg", "sug", "stage", False)
    result = writer.write(error)
    assert result is False


def test_read_recent_empty():
    with tempfile.TemporaryDirectory() as tmp:
        writer = ErrorJsonlWriter(errors_dir=Path(tmp))
        lines = writer.read_recent(limit=10)
        assert lines == []


def test_read_recent_limit():
    with tempfile.TemporaryDirectory() as tmp:
        writer = ErrorJsonlWriter(errors_dir=Path(tmp))
        for i in range(10):
            err = AppError(f"ERR_{i}", Severity.ERROR, f"msg{i}", "sug", "stage", False)
            writer.write(err)
        lines = writer.read_recent(limit=3)
        assert len(lines) == 3
        assert lines[0]["code"] == "ERR_7"
        assert lines[2]["code"] == "ERR_9"


def test_read_recent_corrupted_line_skipped():
    with tempfile.TemporaryDirectory() as tmp:
        writer = ErrorJsonlWriter(errors_dir=Path(tmp))
        error = AppError(ErrorCode.FFMPEG_NOT_FOUND, Severity.ERROR, "msg", "sug", "stage", False)
        writer.write(error)
        path = writer._file_path()
        with open(path, "a", encoding="utf-8") as f:
            f.write("not valid json\n")
        error2 = AppError(ErrorCode.WANGP_UNAVAILABLE, Severity.WARN, "msg2", "sug2", "stage", True)
        writer.write(error2)
        lines = writer.read_recent(limit=10)
        assert len(lines) == 2
