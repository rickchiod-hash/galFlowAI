"""Tests for H10 - Application Layer Use Cases."""
import pytest
from unittest.mock import patch, MagicMock
from app.application.use_cases.base import UseCase, UseCaseError
from app.application.use_cases.script_generation import (
    GenerateScriptUseCase, SaveManualEditUseCase, 
    ImproveScriptUseCase, ApproveScriptUseCase
)
from app.application.use_cases.project_use_cases import CreateProjectUseCase, LoadProjectUseCase
from app.application.use_cases.pipeline_use_cases import (
    SplitScenesUseCase, BuildPromptsUseCase, CreateStoryboardUseCase
)
from app.application.use_cases.video_use_cases import RenderVideoUseCase, CheckWanGPAvailabilityUseCase

class TestBaseUseCase:
    """Test base use case class."""
    
    def test_usecase_is_abstract(self):
        """UseCase should be abstract."""
        with pytest.raises(TypeError):
            UseCase()
    
    def test_build_success(self):
        """Test _build_success method."""
        class ConcreteUseCase(UseCase):
            def execute(self, **kwargs):
                return self._build_success(data={"test": "value"}, extra="info")
        
        uc = ConcreteUseCase()
        result = uc.execute()
        assert result["ok"] is True
        assert result["data"]["test"] == "value"
        assert result["extra"] == "info"
    
    def test_build_error(self):
        """Test _build_error method."""
        class ConcreteUseCase(UseCase):
            def execute(self, **kwargs):
                return self._build_error("Test error", code=500)
        
        uc = ConcreteUseCase()
        result = uc.execute()
        assert result["ok"] is False
        assert "Test error" in result["error"]
        assert result["code"] == 500

class TestGenerateScriptUseCase:
    """Test generate script use case."""
    
    @patch('app.application.use_cases.script_generation.generate_script_with_llm')
    @patch('app.application.use_cases.script_generation.save_script')
    def test_execute_success(self, mock_save, mock_generate):
        """Test successful script generation."""
        mock_generate.return_value = {
            "script": "Test script content",
            "provider": "TemplateProvider",
            "time": 0.5,
            "quality": "fallback"
        }
        
        uc = GenerateScriptUseCase()
        result = uc.execute(briefing="Test briefing", project_id="proj_001", provider="auto")
        
        assert result["ok"] is True
        assert result["data"]["script"] == "Test script content"
        assert result["project_id"] == "proj_001"
        mock_save.assert_called_once_with("proj_001", "Test script content")
    
    def test_validate_invalid_briefing(self):
        """Test validation with invalid briefing."""
        uc = GenerateScriptUseCase()
        assert uc._validate(briefing="", project_id="proj_001") is False
        assert uc._validate(briefing="short", project_id="proj_001") is False
    
    def test_validate_invalid_project_id(self):
        """Test validation with invalid project_id."""
        uc = GenerateScriptUseCase()
        assert uc._validate(briefing="Valid briefing text here", project_id="") is False

class TestCreateProjectUseCase:
    """Test create project use case."""
    
    @patch('app.application.use_cases.project_use_cases.create_project')
    def test_execute_success(self, mock_create):
        """Test successful project creation."""
        mock_create.return_value = {"id": "proj_001", "name": "Test Project"}
        
        uc = CreateProjectUseCase()
        result = uc.execute(project_name="Test Project")
        
        assert result["ok"] is True
        assert result["data"]["id"] == "proj_001"
        mock_create.assert_called_once_with("Test Project")
    
    def test_validate_invalid_name(self):
        """Test validation with invalid name."""
        uc = CreateProjectUseCase()
        assert uc._validate(project_name="") is False
        assert uc._validate(project_name="   ") is False

class TestSplitScenesUseCase:
    """Test split scenes use case."""
    
    @patch('app.application.use_cases.pipeline_use_cases.split_script_into_scenes')
    @patch('app.application.use_cases.pipeline_use_cases.save_scenes')
    def test_execute_success(self, mock_save, mock_split):
        """Test successful scene splitting."""
        mock_split.return_value = [{"id": 1, "text": "Scene 1"}]
        
        uc = SplitScenesUseCase()
        result = uc.execute(script="Test script", project_id="proj_001")
        
        assert result["ok"] is True
        assert result["data"]["count"] == 1
        mock_split.assert_called_once()
        mock_save.assert_called_once()

class TestBuildPromptsUseCase:
    """Test build prompts use case."""
    
    @patch('app.application.use_cases.pipeline_use_cases.build_prompts_for_scenes')
    @patch('app.application.use_cases.pipeline_use_cases.save_prompts')
    def test_execute_success(self, mock_save, mock_build):
        """Test successful prompt building."""
        mock_build.return_value = [{"id": 1, "prompt": "test prompt"}]
        
        uc = BuildPromptsUseCase()
        scenes = [{"id": 1, "text": "Scene 1"}]
        result = uc.execute(scenes=scenes, style="modern", project_id="proj_001")
        
        assert result["ok"] is True
        assert result["data"]["count"] == 1

class TestCreateStoryboardUseCase:
    """Test create storyboard use case."""
    
    @patch('app.application.use_cases.pipeline_use_cases.create_storyboard_video')
    @patch('app.application.use_cases.pipeline_use_cases.get_gpu_info')
    @patch('app.application.use_cases.pipeline_use_cases.get_recommended_preset')
    def test_execute_success(self, mock_preset, mock_gpu, mock_create):
        """Test successful storyboard creation."""
        mock_create.return_value = "/path/to/video.mp4"
        mock_gpu.return_value = {"vram_gb": 6, "name": "GTX 1660 Super"}
        mock_preset.return_value = {"model": "1.3B"}
        
        uc = CreateStoryboardUseCase()
        result = uc.execute(project_id="proj_001", scenes=[{"id": 1}])
        
        assert result["ok"] is True
        assert result["data"]["video_path"] == "/path/to/video.mp4"

class TestRenderVideoUseCase:
    """Test render video use case."""
    
    @patch('app.application.use_cases.video_use_cases.WanGPAdapter')
    def test_execute_success(self, mock_adapter_class):
        """Test successful video rendering."""
        mock_adapter = MagicMock()
        mock_adapter.disponivel.return_value = True
        mock_adapter.render_scene.return_value = {"video_path": "/path/to/video.mp4"}
        mock_adapter_class.return_value = mock_adapter
        
        uc = RenderVideoUseCase()
        scene = {"id": "scene_001", "prompt": "test prompt"}
        result = uc.execute(project_id="proj_001", scene=scene)
        
        assert result["ok"] is True
        assert result["data"]["scene_id"] == "scene_001"
    
    def test_validate_invalid_scene(self):
        """Test validation with invalid scene."""
        uc = RenderVideoUseCase()
        assert uc._validate(project_id="proj_001", scene={}) is False

class TestCheckWanGPAvailabilityUseCase:
    """Test WanGP availability check use case."""
    
    @patch('app.application.use_cases.video_use_cases.WanGPAdapter')
    def test_execute_available(self, mock_adapter_class):
        """Test when WanGP is available."""
        mock_adapter = MagicMock()
        mock_adapter.disponivel.return_value = True
        mock_adapter_class.return_value = mock_adapter
        
        uc = CheckWanGPAvailabilityUseCase()
        result = uc.execute()
        
        assert result["ok"] is True
        assert result["data"]["available"] is True
