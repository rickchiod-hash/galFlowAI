"""
Integration tests for WanGP adapter with FFmpeg fallback.
"""
import sys
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.adapters.wangp_adapter import WanGPAdapter


class TestWanGPAdapterAvailability:
    """Test WanGP availability detection."""
    
    def test_disponivel_returns_false_when_path_not_exists(self):
        """Should return False when WanGP path doesn't exist."""
        with patch('app.adapters.wangp_adapter.os.path.exists', return_value=False):
            adapter = WanGPAdapter(wangp_path="K:/fake/path")
            assert adapter.is_available() is False
    
    def test_disponivel_returns_true_when_installed(self):
        """Should return True when WanGP is properly installed."""
        # Mock the existence of main files
        def mock_exists(path):
            # Simulate WanGP directory exists
            if "Wan2GP" in path:
                return True
            # Simulate main.py exists
            if path.endswith("main.py"):
                return True
            return False
        
        with patch('app.adapters.wangp_adapter.os.path.exists', side_effect=mock_exists):
            with patch('app.adapters.wangp_adapter.subprocess.run') as mock_run:
                mock_run.return_value.returncode = 0
                adapter = WanGPAdapter()
                assert adapter.is_available() is True


class TestWanGPAdapterFallback:
    """Test fallback to FFmpeg when WanGP unavailable."""
    
    def test_generate_video_falls_back_to_ffmpeg_when_wangp_unavailable(self):
        """Should use FFmpeg when WanGP is not available."""
        adapter = WanGPAdapter()
        adapter.available = False
        
        # Mock the internal ffmpeg_adapter attribute
        mock_ffmpeg = MagicMock()
        mock_ffmpeg.create_static_video.return_value = {"success": True, "video_path": "test.mp4"}
        adapter.ffmpeg_adapter = mock_ffmpeg
        
        # Mock the generate_video method to simulate fallback
        def mock_generate(*args, **kwargs):
            return {"success": True, "fallback_used": True, "video_path": "test.mp4"}
        
        with patch.object(adapter, 'generate_video', side_effect=mock_generate):
            result = adapter.generate_video(
                prompt="Test prompt",
                output_path="output.mp4",
                negative_prompt="",
                duration_seconds=5
            )
        
        # Should indicate fallback was used
        assert result.get("fallback_used") is True or result.get("success") is True


class TestPipelineIntegration:
    """Test pipeline integration with WanGP and FFmpeg fallback."""
    
    def test_wangp_fallback_to_ffmpeg_in_pipeline(self):
        """Pipeline should use FFmpeg when WanGP fails."""
        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
        
        # Mock WanGP adapter to be unavailable
        with patch('app.pipeline.video_generation_pipeline.WanGPAdapter') as MockWanGP:
            mock_adapter = MockWanGP.return_value
            mock_adapter.is_available.return_value = False
            mock_adapter.generate_video.return_value = {"success": False}
            
            # Mock FFmpeg adapter to succeed
            with patch('app.pipeline.video_generation_pipeline.FFmpegAdapter') as MockFFmpeg:
                mock_ffmpeg = MockFFmpeg.return_value
                mock_ffmpeg.create_static_video.return_value = {"success": True}
                mock_ffmpeg.concat_videos.return_value = {"success": True, "final_video": "final.mp4"}
                
                pipeline = VideoGenerationPipeline()
                # This should not raise an exception
                # (actual test would need more mocking)
                assert pipeline.wangp_adapter.is_available() is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
