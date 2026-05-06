"""Tests for H11 - Job Queue Use Cases."""
import pytest
from unittest.mock import patch, MagicMock
from app.application.use_cases.job_use_cases import (
    AddJobUseCase, RemoveJobUseCase, 
    ListJobsUseCase, GetQueueStatusUseCase
)


class TestAddJobUseCase:
    """Test AddJob use case."""
    
    def test_execute_success(self):
        """Test successful job addition."""
        with patch('app.application.use_cases.job_use_cases.queue') as mock_queue:
            mock_queue.add_job.return_value = "job_001"
            
            uc = AddJobUseCase()
            result = uc.execute(project_id="proj_001", job_type="video_render")
            
            assert result["ok"] is True
            assert result["data"]["job_id"] == "job_001"
            assert result["data"]["status"] == "queued"
    
    def test_validate_invalid_project_id(self):
        """Test validation with invalid project_id."""
        uc = AddJobUseCase()
        result = uc.execute(project_id="", job_type="video_render")
        assert result["ok"] is False
        assert "Invalid" in result["error"]


class TestRemoveJobUseCase:
    """Test RemoveJob use case."""
    
    def test_execute_success(self):
        """Test successful job removal."""
        with patch('app.application.use_cases.job_use_cases.queue') as mock_queue:
            mock_queue.remove_job.return_value = True
            
            uc = RemoveJobUseCase()
            result = uc.execute(job_id="job_001")
            
            assert result["ok"] is True
            assert result["data"]["removed"] is True
    
    def test_execute_job_not_found(self):
        """Test job not found."""
        with patch('app.application.use_cases.job_use_cases.queue') as mock_queue:
            mock_queue.remove_job.return_value = False
            
            uc = RemoveJobUseCase()
            result = uc.execute(job_id="job_999")
            
            assert result["ok"] is False


class TestListJobsUseCase:
    """Test ListJobs use case."""
    
    def test_execute_success(self):
        """Test successful job listing."""
        with patch('app.application.use_cases.job_use_cases.queue') as mock_queue:
            mock_queue.list_jobs.return_value = [
                {"job_id": "job_001", "status": "queued"}
            ]
            
            uc = ListJobsUseCase()
            result = uc.execute()
            
            assert result["ok"] is True
            assert result["data"]["count"] == 1


class TestGetQueueStatusUseCase:
    """Test GetQueueStatus use case."""
    
    def test_execute_success(self):
        """Test successful status retrieval."""
        with patch('app.application.use_cases.job_use_cases.queue') as mock_queue:
            mock_queue.get_status.return_value = {"total": 0, "running": 0}
            
            uc = GetQueueStatusUseCase()
            result = uc.execute()
            
            assert result["ok"] is True
            assert "total" in result["data"]
