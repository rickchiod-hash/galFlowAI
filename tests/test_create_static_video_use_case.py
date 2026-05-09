"""Tests for CreateStaticVideoUseCase."""
import pytest
from unittest.mock import patch, MagicMock
from app.application.use_cases.create_static_video_use_case import CreateStaticVideoUseCase


class TestCreateStaticVideoUseCase:
    """Test CreateStaticVideoUseCase."""
    
    def test_create_static_video_use_case_exists(self):
        """Test that the use case can be instantiated."""
        use_case = CreateStaticVideoUseCase()
        assert use_case is not None
    
    @patch('app.application.use_cases.create_static_video_use_case.FFmpegAdapter')
    def test_execute_success(self, mock_ffmpeg_adapter):
        """Test successful execution of the use case."""
        # Setup mock
        mock_adapter_instance = MagicMock()
        mock_adapter_instance.is_available.return_value = True
        mock_adapter_instance.create_static_video.return_value = {
            'success': True,
            'video_path': 'K:\\AI_VIDEO_COMMERCIAL_STUDIO\\opencodegalpasta\\projects\\test_project\\renders\\scene_test.mp4'
        }
        mock_ffmpeg_adapter.return_value = mock_adapter_instance
        
        # Execute use case
        use_case = CreateStaticVideoUseCase()
        result = use_case.execute(
            project_id='test_project',
            text='Test text for video',
            output_name='scene_test.mp4'
        )
        
        # Assertions
        assert result['ok'] is True
        assert result['data']['video_path'] == 'K:\\AI_VIDEO_COMMERCIAL_STUDIO\\opencodegalpasta\\projects\\test_project\\renders\\scene_test.mp4'
        assert result['data']['text'] == 'Test text for video'
        mock_adapter_instance.is_available.assert_called_once()
        mock_adapter_instance.create_static_video.assert_called_once()
    
    @patch('app.application.use_cases.create_static_video_use_case.FFmpegAdapter')
    def test_execute_ffmpeg_not_available(self, mock_ffmpeg_adapter):
        """Test execution when FFmpeg is not available."""
        # Setup mock
        mock_adapter_instance = MagicMock()
        mock_adapter_instance.is_available.return_value = False
        mock_ffmpeg_adapter.return_value = mock_adapter_instance
        
        # Execute use case
        use_case = CreateStaticVideoUseCase()
        result = use_case.execute(
            project_id='test_project',
            text='Test text for video'
        )
        
        # Assertions
        assert result['ok'] is False
        assert 'FFmpeg not available' in result['error']
        mock_adapter_instance.is_available.assert_called_once()
        mock_adapter_instance.create_static_video.assert_not_called()
    
    @patch('app.application.use_cases.create_static_video_use_case.FFmpegAdapter')
    def test_execute_ffmpeg_failure(self, mock_ffmpeg_adapter):
        """Test execution when FFmpeg fails to create video."""
        # Setup mock
        mock_adapter_instance = MagicMock()
        mock_adapter_instance.is_available.return_value = True
        mock_adapter_instance.create_static_video.return_value = {
            'success': False,
            'error': 'FFmpeg error'
        }
        mock_ffmpeg_adapter.return_value = mock_adapter_instance
        
        # Execute use case
        use_case = CreateStaticVideoUseCase()
        result = use_case.execute(
            project_id='test_project',
            text='Test text for video'
        )
        
        # Assertions
        assert result['ok'] is False
        assert 'FFmpeg failed to create static video: FFmpeg error' in result['error']
        mock_adapter_instance.is_available.assert_called_once()
        mock_adapter_instance.create_static_video.assert_called_once()
    
    def test_validate_input(self):
        """Test input validation."""
        use_case = CreateStaticVideoUseCase()
        
        # Valid input
        assert use_case._validate(project_id='test', text='Some text') is True
        
        # Invalid project_id
        assert use_case._validate(project_id='', text='Some text') is False
        assert use_case._validate(project_id=None, text='Some text') is False
        
        # Invalid text
        assert use_case._validate(project_id='test', text='') is False
        assert use_case._validate(project_id='test', text=None) is False
        assert use_case._validate(project_id='test', text='   ') is False