"""Tests for SQLite WAL job ledger (PIPE-403)."""
import json
import os
import tempfile
from pathlib import Path

import pytest

from app.pipeline.job_ledger import SQLiteJobLedger
from app.pipeline.job_state import JobState, JobStatus
from app.jobs.queue import JobQueue


class TestSQLiteJobLedger:
    """Test SQLite job ledger functionality."""

    def test_ledger_creation(self):
        """Test that ledger creates database file and tables."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test_ledger.db")
            ledger = SQLiteJobLedger(db_path)
            
            # Check that database file was created
            assert Path(db_path).exists()
            
            # Check that we can save and load a job
            job = JobState("test_job_1", "test_project", job_type="test")
            ledger.save_job(job)
            
            loaded_job = ledger.load_job("test_job_1")
            assert loaded_job is not None
            assert loaded_job.job_id == "test_job_1"
            assert loaded_job.project_id == "test_project"
            assert loaded_job.status == JobStatus.QUEUED

    def test_job_save_and_load(self):
        """Test saving and loading jobs with all fields."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test_ledger.db")
            ledger = SQLiteJobLedger(db_path)
            
            # Create a job with various fields
            original_job = JobState("job_123", "proj_456", job_type="video_render", 
                                  params={"resolution": "1080p", "fps": 30})
            original_job.start()
            original_job.update_progress(50, "Processing", stage="encoding")
            original_job.succeed({"quality": 0.95, "frames": 1500})
            
            # Save job
            ledger.save_job(original_job)
            
            # Load job
            loaded_job = ledger.load_job("job_123")
            
            # Verify all fields match
            assert loaded_job is not None
            assert loaded_job.job_id == original_job.job_id
            assert loaded_job.project_id == original_job.project_id
            assert loaded_job.job_type == original_job.job_type
            assert loaded_job.status == original_job.status
            assert loaded_job.params == original_job.params
            assert loaded_job.progress == original_job.progress
            assert loaded_job.message == original_job.message
            assert loaded_job.current_stage == original_job.current_stage
            assert loaded_job.metadata == original_job.metadata
            assert loaded_job.started_at == original_job.started_at
            assert loaded_job.completed_at == original_job.completed_at

    def test_load_nonexistent_job(self):
        """Test loading a job that doesn't exist returns None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test_ledger.db")
            ledger = SQLiteJobLedger(db_path)
            
            job = ledger.load_job("nonexistent_job")
            assert job is None

    def test_load_jobs_with_filters(self):
        """Test loading jobs with project_id and status filters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test_ledger.db")
            ledger = SQLiteJobLedger(db_path)
            
            # Create test jobs
            job1 = JobState("job_1", "proj_alpha", job_type="test")
            job2 = JobState("job_2", "proj_alpha", job_type="test")
            job3 = JobState("job_3", "proj_beta", job_type="test")
            
            job1.start()
            job2.start()  # Must start before failing
            job2.fail("Test failure")
            job3.start()  # Must start before succeeding
            job3.succeed()
            
            ledger.save_job(job1)
            ledger.save_job(job2)
            ledger.save_job(job3)
            
            # Filter by project
            alpha_jobs = ledger.load_jobs(project_id="proj_alpha")
            assert len(alpha_jobs) == 2
            job_ids = {j.job_id for j in alpha_jobs}
            assert job_ids == {"job_1", "job_2"}
            
            # Filter by status
            running_jobs = ledger.load_jobs(status=JobStatus.RUNNING)
            assert len(running_jobs) == 1
            assert running_jobs[0].job_id == "job_1"
            
            failed_jobs = ledger.load_jobs(status=JobStatus.FAILED)
            assert len(failed_jobs) == 1
            assert failed_jobs[0].job_id == "job_2"
            
            succeeded_jobs = ledger.load_jobs(status=JobStatus.SUCCEEDED)
            assert len(succeeded_jobs) == 1
            assert succeeded_jobs[0].job_id == "job_3"

    def test_delete_job(self):
        """Test deleting jobs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test_ledger.db")
            ledger = SQLiteJobLedger(db_path)
            
            job = JobState("job_to_delete", "test_project", job_type="test")
            ledger.save_job(job)
            
            # Verify job exists
            assert ledger.load_job("job_to_delete") is not None
            
            # Delete job
            result = ledger.delete_job("job_to_delete")
            assert result is True
            
            # Verify job is gone
            assert ledger.load_job("job_to_delete") is None
            
            # Try to delete non-existent job
            result = ledger.delete_job("nonexistent")
            assert result is False

    def test_running_job_id_management(self):
        """Test setting and getting running job ID."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test_ledger.db")
            ledger = SQLiteJobLedger(db_path)
            
            # Initially no running job
            assert ledger.get_running_job_id() is None
            
            # Set running job ID
            ledger.set_running_job_id("job_123")
            assert ledger.get_running_job_id() == "job_123"
            
            # Clear running job ID
            ledger.set_running_job_id(None)
            assert ledger.get_running_job_id() is None

    def test_wal_mode_enabled(self):
        """Test that WAL mode is enabled on database connection."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test_ledger.db")
            ledger = SQLiteJobLedger(db_path)
            
            # Check that WAL mode is enabled
            with ledger._transaction() as conn:
                cursor = conn.execute("PRAGMA journal_mode")
                mode = cursor.fetchone()[0].upper()
                assert mode == "WAL"

    def test_concurrent_access_safety(self):
        """Test that the ledger handles concurrent access safely."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test_ledger.db")
            ledger1 = SQLiteJobLedger(db_path)
            ledger2 = SQLiteJobLedger(db_path)  # Second connection to same DB
            
            # Save job from first ledger
            job = JobState("concurrent_test", "test_project", job_type="test")
            ledger1.save_job(job)
            
            # Load from second ledger
            loaded_job = ledger2.load_job("concurrent_test")
            assert loaded_job is not None
            assert loaded_job.job_id == "concurrent_test"


class TestJobQueueWithSQLiteLedger:
    """Test JobQueue using SQLite ledger as backend."""

    def test_job_queue_add_and_get(self):
        """Test adding and retrieving jobs through JobQueue."""
        # Use temporary directory for SQLite database
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = str(Path(tmpdir) / "test_ledger.db")
            job_ledger = SQLiteJobLedger(db_path)
            
            # Create queue with the temporary ledger
            queue = JobQueue(job_ledger=job_ledger)
            
            # Add a job
            job_id = queue.add_job("video_render", "test_project", {"quality": "high"})
            
            # Get the job
            job = queue.get_job(job_id)
            assert job is not None
            assert job.job_id == job_id
            assert job.project_id == "test_project"
            assert job.job_type == "video_render"
            assert job.params == {"quality": "high"}
            assert job.status == JobStatus.QUEUED

    def test_job_queue_persistence(self):
        """Test that jobs persist across queue instances."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = str(Path(tmpdir) / "test_ledger.db")
            job_ledger = SQLiteJobLedger(db_path)
            
            # Create first queue and add job
            queue1 = JobQueue(job_ledger=job_ledger)
            job_id = queue1.add_job("test_job", "test_project", {})
            job1 = queue1.get_job(job_id)
            assert job1 is not None
            
            # Create second queue with same ledger (should load same job)
            queue2 = JobQueue(job_ledger=job_ledger)
            job2 = queue2.get_job(job_id)
            
            # Verify job persisted
            assert job2 is not None
            assert job2.job_id == job_id
            assert job2.project_id == "test_project"
            assert job2.job_type == job1.job_type
            assert job2.params == job1.params

    def test_job_queue_running_job_mutex(self):
        """Test that only one job can be running at a time."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = str(Path(tmpdir) / "test_ledger.db")
            job_ledger = SQLiteJobLedger(db_path)
            
            # Create queue with the temporary ledger
            queue = JobQueue(job_ledger=job_ledger)
            
            # Add two jobs
            job_id_1 = queue.add_job("test", "test_project")
            job_id_2 = queue.add_job("test", "test_project")
            
            # Get first job - should succeed
            job1 = queue.get_next_job()
            assert job1 is not None
            assert job1.job_id == job_id_1
            assert job1.status == JobStatus.RUNNING
            
            # Try to get second job - should return None (mutex)
            job2 = queue.get_next_job()
            assert job2 is None
            
            # Complete first job
            queue.complete_job(job_id_1)
            
            # Now second job should be available
            job2 = queue.get_next_job()
            assert job2 is not None
            assert job2.job_id == job_id_2
            assert job2.status == JobStatus.RUNNING

    def test_job_queue_status_reporting(self):
        """Test that queue status reporting works correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = str(Path(tmpdir) / "test_ledger.db")
            job_ledger = SQLiteJobLedger(db_path)
            
            # Create queue with the temporary ledger
            queue = JobQueue(job_ledger=job_ledger)
            
            # Add jobs in different states
            job_id_1 = queue.add_job("test", "test_project", {})
            job_id_2 = queue.add_job("test", "test_project", {})
            
            # Check initial status
            status = queue.get_status()
            assert status["total"] == 2
            assert status["queued"] == 2
            assert status["running"] == 0
            
            # Start one job
            job1 = queue.get_next_job()
            assert job1 is not None
            
            status = queue.get_status()
            assert status["total"] == 2
            assert status["queued"] == 1
            assert status["running"] == 1
            
            # Complete the job
            queue.complete_job(job_id_1)
            
            status = queue.get_status()
            assert status["total"] == 2
            assert status["queued"] == 1
            assert status["completed"] == 1
            assert status["running"] == 0