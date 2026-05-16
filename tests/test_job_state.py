"""Tests for JobState formal state machine (PIPE-400)."""
import pytest
from app.exceptions import ValidationError
from app.pipeline.job_state import JobState, JobStatus


class TestJobStateCreation:
    """Test JobState creation."""

    def test_create_queued(self):
        """Job is created in QUEUED state."""
        job = JobState("job_001", "proj_001", job_type="video_render")
        assert job.job_id == "job_001"
        assert job.project_id == "proj_001"
        assert job.job_type == "video_render"
        assert job.status == JobStatus.QUEUED
        assert job.progress == 0
        assert job.message == "Job queued"

    def test_create_with_params(self):
        """Job creation accepts optional params."""
        job = JobState("job_002", "proj_002", job_type="audio_gen", params={"voice": "pt-BR"})
        assert job.job_type == "audio_gen"
        assert job.params == {"voice": "pt-BR"}


class TestJobStateTransitions:
    """Test guarded state transitions."""

    def test_start_transition(self):
        """QUEUED -> RUNNING is valid."""
        job = JobState("job_001", "proj_001")
        job.start()
        assert job.status == JobStatus.RUNNING
        assert job.started_at is not None
        assert job.progress == 0
        assert job.message == "Job started"

    def test_complete_transition(self):
        """RUNNING -> COMPLETED is valid."""
        job = JobState("job_001", "proj_001")
        job.start()
        job.complete(output_path="/tmp/video.mp4")
        assert job.status == JobStatus.COMPLETED
        assert job.completed_at is not None
        assert job.progress == 100
        assert job.output_path == "/tmp/video.mp4"

    def test_succeed_transition(self):
        """RUNNING -> SUCCEEDED is valid."""
        job = JobState("job_001", "proj_001")
        job.start()
        job.succeed(metadata={"quality": 0.95})
        assert job.status == JobStatus.SUCCEEDED
        assert job.completed_at is not None
        assert job.progress == 100
        assert job.metadata.get("quality") == 0.95

    def test_fail_transition(self):
        """RUNNING -> FAILED is valid."""
        job = JobState("job_001", "proj_001")
        job.start()
        job.fail("GPU out of memory")
        assert job.status == JobStatus.FAILED
        assert job.error == "GPU out of memory"
        assert "failed" in job.message

    def test_cancel_queued(self):
        """QUEUED -> CANCELLED is valid."""
        job = JobState("job_001", "proj_001")
        job.cancel()
        assert job.status == JobStatus.CANCELLED
        assert job.completed_at is not None

    def test_cancel_running(self):
        """RUNNING -> CANCELLED is valid."""
        job = JobState("job_001", "proj_001")
        job.start()
        job.cancel()
        assert job.status == JobStatus.CANCELLED

    def test_cannot_start_twice(self):
        """RUNNING -> RUNNING is invalid."""
        job = JobState("job_001", "proj_001")
        job.start()
        with pytest.raises(ValidationError, match="Invalid transition"):
            job.start()

    def test_cannot_complete_queued(self):
        """QUEUED -> COMPLETED is invalid."""
        job = JobState("job_001", "proj_001")
        with pytest.raises(ValidationError, match="Invalid transition"):
            job.complete()

    def test_cannot_cancel_completed(self):
        """COMPLETED -> CANCELLED is invalid."""
        job = JobState("job_001", "proj_001")
        job.start()
        job.complete()
        with pytest.raises(ValidationError, match="Invalid transition"):
            job.cancel()

    def test_cannot_fail_completed(self):
        """COMPLETED -> FAILED is invalid."""
        job = JobState("job_001", "proj_001")
        job.start()
        job.complete()
        with pytest.raises(ValidationError, match="Invalid transition"):
            job.fail("too late")

    def test_cannot_succeed_failed(self):
        """FAILED -> SUCCEEDED is invalid."""
        job = JobState("job_001", "proj_001")
        job.start()
        job.fail("error")
        with pytest.raises(ValidationError, match="Invalid transition"):
            job.succeed()


class TestJobStateProgress:
    """Test progress tracking."""

    def test_update_progress(self):
        """Progress can be updated without changing status."""
        job = JobState("job_001", "proj_001")
        job.update_progress(50, "Rendering scene 2", stage="rendering")
        assert job.progress == 50
        assert job.message == "Rendering scene 2"
        assert job.current_stage == "rendering"
        assert job.status == JobStatus.QUEUED  # Status unchanged

    def test_progress_clamped(self):
        """Progress is clamped 0-100."""
        job = JobState("job_001", "proj_001")
        job.update_progress(150, "Over 100")
        assert job.progress == 100
        job.update_progress(-10, "Under 0")
        assert job.progress == 0


class TestJobStateSerialization:
    """Test to_dict / from_dict."""

    def test_to_dict(self):
        """to_dict returns all fields."""
        job = JobState("job_001", "proj_001", job_type="test", params={"key": "val"})
        d = job.to_dict()
        assert d["job_id"] == "job_001"
        assert d["project_id"] == "proj_001"
        assert d["job_type"] == "test"
        assert d["status"] == "queued"
        assert d["params"] == {"key": "val"}
        assert d["progress"] == 0

    def test_roundtrip(self):
        """from_dict(to_dict()) restores identical state."""
        job = JobState("job_001", "proj_001", job_type="video", params={"dur": 30})
        job.start()
        job.update_progress(75, "Almost done", stage="final")
        d = job.to_dict()

        restored = JobState.from_dict(d)
        assert restored.job_id == job.job_id
        assert restored.project_id == job.project_id
        assert restored.job_type == job.job_type
        assert restored.status == job.status
        assert restored.params == job.params
        assert restored.progress == job.progress
        assert restored.message == job.message
        assert restored.current_stage == job.current_stage

    def test_roundtrip_completed(self):
        """from_dict roundtrips completed job with output_path."""
        job = JobState("job_001", "proj_001")
        job.start()
        job.complete(output_path="/out/video.mp4")
        d = job.to_dict()
        restored = JobState.from_dict(d)
        assert restored.status == JobStatus.COMPLETED
        assert restored.output_path == "/out/video.mp4"
        assert restored.progress == 100


class TestJobStateEdgeCases:
    """Test edge cases."""

    def test_metadata_accumulates(self):
        """Multiple metadata updates accumulate."""
        job = JobState("job_001", "proj_001")
        job.start()
        job.succeed(metadata={"first": 1})
        assert job.metadata["first"] == 1

    def test_metadata_with_complete(self):
        """Metadata can be passed to complete()."""
        job = JobState("job_001", "proj_001")
        job.start()
        job.complete(metadata={"render_time": 42.5})
        assert job.metadata["render_time"] == 42.5
