"""Tests for H11 - Mutex: Only 1 render at a time."""
import pytest
from unittest.mock import patch, MagicMock
from app.jobs.queue import JobQueue, JobStatus
from app.application.use_cases.job_use_cases import GetQueueStatusUseCase

class TestMutexSingleRender:
    """Test that only 1 job runs at a time."""
    
    def test_get_next_job_returns_none_when_running(self):
        """When a job is running, get_next_job should return None."""
        queue = JobQueue()
        
        # Add a job and start it
        job_id = queue.add_job("proj_001", "video_render")
        job = queue.get_job(job_id)
        job.status = JobStatus.RUNNING
        queue.running_job_id = job_id
        queue._save()
        
        # Try to get next job
        next_job = queue.get_next_job()
        assert next_job is None
        
        # Cleanup
        queue.jobs.clear()
        queue.running_job_id = None
        queue._save()
    
    def test_get_next_job_returns_queued_when_none_running(self):
        """When no job running, should return queued job."""
        queue = JobQueue()
        
        # Add a job
        job_id = queue.add_job("proj_001", "video_render")
        
        # Get next job (should work)
        next_job = queue.get_next_job()
        assert next_job is not None
        assert next_job.job_id == job_id
        
        # Cleanup
        queue.jobs.clear()
        queue._save()
    
    def test_complete_job_frees_mutex(self):
        """When job completes, next job can start."""
        queue = JobQueue()
        
        # Add 2 jobs
        job_id1 = queue.add_job("proj_001", "video_render")
        job_id2 = queue.add_job("proj_002", "video_render")
        
        # Start first job
        job1 = queue.get_job(job_id1)
        job1.status = JobStatus.RUNNING
        queue.running_job_id = job_id1
        queue._save()
        
        # Second job should not start
        assert queue.get_next_job() is None
        
        # Complete first job
        queue.complete_job(job_id1, "/path/to/video.mp4")
        
        # Now second job should be available
        next_job = queue.get_next_job()
        assert next_job is not None
        assert next_job.job_id == job_id2
        
        # Cleanup
        queue.jobs.clear()
        queue.running_job_id = None
        queue._save()
    
    def test_running_job_id_persists_after_restart(self):
        """running_job_id should persist after queue reload."""
        queue1 = JobQueue()
        job_id = queue1.add_job("proj_001", "video_render")
        job = queue1.get_job(job_id)
        job.status = JobStatus.RUNNING
        queue1.running_job_id = job_id
        queue1._save()
        
        # Create new queue instance (simulate restart)
        queue2 = JobQueue()
        assert queue2.running_job_id == job_id
        assert queue2.get_next_job() is None  # Because job is still running
        
        # Cleanup
        queue2.jobs.clear()
        queue2.running_job_id = None
        queue2._save()


class TestGetQueueStatusMutex:
    """Test queue status shows running job info."""
    
    def test_status_shows_running_job(self):
        """Queue status should show running job ID."""
        with patch('app.application.use_cases.job_use_cases.JobQueue') as mock_class:
            mock_queue = MagicMock()
            mock_queue.get_status.return_value = {
                "total": 2,
                "queued": 1,
                "running": 1,
                "completed": 0,
                "failed": 0,
                "running_job_id": "job_001"
            }
            mock_class.return_value = mock_queue
            
            uc = GetQueueStatusUseCase()
            result = uc.execute()
            
            assert result["ok"] is True
            assert result["data"]["running_job_id"] == "job_001"
