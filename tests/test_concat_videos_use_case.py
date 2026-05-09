"""Tests for ConcatVideosUseCase."""
import pytest
from unittest.mock import patch, MagicMock
from app.application.use_cases.concat_videos_use_case import ConcatVideosUseCase


class TestConcatVideosUseCase:
    """Test ConcatVideosUseCase."""
    
    def test_concat_videos_use_case_exists(self):
        """Test that the use case can be instantiated."""
        use_case = ConcatVideosUseCase()
        assert use_case is not None
    
    @patch('app.application.use_cases.concat_videos_use_case.FFmpegAdapter')
    def test_execute_success(self, mock_ffmpeg_adapter):
        """Test successful execution of the use case."""
        # Setup mock
        mock_adapter_instance = MagicMock()
        mock_adapter_instance.is_available.return_value = True
        mock_adapter_instance.concat_videos.return_value = {
            'success': True,
            'video_path': 'K:\\AI_VIDEO_COMMERCIAL_STUDIO\\opencodegalpasta\\projects\\test_project\\final\\commercial_test.mp4'
        }
        mock_ffmpeg_adapter.return_value = mock_adapter_instance
        
        # Execute use case
        use_case = ConcatVideosUseCase()
        result = use_case.execute(
            project_id='test_project',
            video_paths=['scene1.mp4', 'scene2.mp4'],
            output_name='commercial_test.mp4'
        )
        
        # Assertions
        assert result['ok'] is True
        assert result['data']['video_path'] == 'K:\\AI_VIDEO_COMMERCIAL_STUDIO\\opencodegalpasta\\projects\\test_project\\final\\commercial_test.mp4'
        assert result['data']['input_count'] == 2
        mock_adapter_instance.is_available.assert_called_once()
        mock_adapter_instance.concat_videos.assert_called_once()
    
    @patch('app.application.use_cases.concat_videos_use_case.FFmpegAdapter')
    def test_execute_success_with_audio(self, mock_ffmpeg_adapter):
        """Test successful execution with audio."""
        # Setup mock
        mock_adapter_instance = MagicMock()
        mock_adapter_instance.is_available.return_value = True
        mock_adapter_instance.concat_videos.return_value = {
            'success': True,
            'video_path': 'K:\\AI_VIDEO_COMMERCIAL_STUDIO\\opencodegalpasta\\projects\\test_project\\final\\commercial_test.mp4'
        }
        mock_ffmpeg_adapter.return_value = mock_adapter_instance
        
        # Execute use case
        use_case = ConcatVideosUseCase()
        result = use_case.execute(
            project_id='test_project',
            video_paths=['scene1.mp4', 'scene2.mp4'],
            output_name='commercial_test.mp4',
            audio_path='narration.wav'
        )
        
        # Assertions
        assert result['ok'] is True
        assert result['data']['video_path'] == 'K:\\AI_VIDEO_COMMERCIAL_STUDIO\\opencodegalpasta\\projects\\test_project\\final\\commercial_test.mp4'
        assert result['data']['input_count'] == 2
        assert result['data']['has_audio'] is True
        mock_adapter_instance.is_available.assert_called_once()
        mock_adapter_instance.concat_videos.assert_called_once()
    
    @patch('app.application.use_cases.concat_videos_use_case.FFmpegAdapter')
    def test_execute_ffmpeg_not_available(self, mock_ffmpeg_adapter):
        """Test execution when FFmpeg is not available."""
        # Setup mock
        mock_adapter_instance = MagicMock()
        mock_adapter_instance.is_available.return_value = False
        mock_ffmpeg_adapter.return_value = mock_adapter_instance
        
        # Execute use case
        use_case = ConcatVideosUseCase()
        result = use_case.execute(
            project_id='test_project',
            video_paths=['scene1.mp4', 'scene2.mp4']
        )
        
        # Assertions
        assert result['ok'] is False
        assert 'FFmpeg not available' in result['error']
        mock_adapter_instance.is_available.assert_called_once()
        mock_adapter_instance.concat_videos.assert_not_called()
    
    @patch('app.application.use_cases.concat_videos_use_case.FFmpegAdapter')
    def test_execute_concat_failure(self, mock_ffmpeg_adapter):
        """Test execution when FFmpeg fails to concatenate."""
        # Setup mock
        mock_adapter_instance = MagicMock()
        mock_adapter_instance.is_available.return_value = True
        mock_adapter_instance.concat_videos.return_value = {
            'success': False,
            'error': 'Concat error'
        }
        mock_ffmpeg_adapter.return_value = mock_adapter_instance
        
        # Execute use case
        use_case = ConcatVideosUseCase()
        result = use_case.execute(
            project_id='test_project',
            video_paths=['scene1.mp4', 'scene2.mp4']
        )
        
        # Assertions
        assert result['ok'] is False
        assert 'FFmpeg failed to concatenate videos: Concat error' in result['error']
        mock_adapter_instance.is_available.assert_called_once()
        mock_adapter_instance.concat_videos.assert_called_once()
    
    def test_validate_input(self):
        """Test input validation."""
        use_case = ConcatVideosUseCase()
        
        # Valid input
        assert use_case._validate(project_id='test', video_paths=['file1.mp4']) is True
        assert use_case._validate(project_id='test', video_paths=['file1.mp4', 'file2.mp4']) is True
        
        # Invalid project_id
        assert use_case._validate(project_id='', video_paths=['file1.mp4']) is False
        assert use_case._validate(project_id=None, video_paths=['file1.mp4']) is False
        
        # Invalid video_paths
        assert use_case._validate(project_id='test', video_paths=[]) is False
        assert use_case._validate(project_id='test', video_paths=None) is False
        assert use_case._validate(project_id='test', video_paths='not_a_list') is False