"""Integration tests for artifact cache with pipeline stages (PIPE-402)."""
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

from app.application.use_cases.generate_script_use_case import GenerateScriptUseCase
from app.application.use_cases.split_scenes_use_case import SplitScenesUseCase
from app.application.use_cases.build_prompts_use_case import BuildPromptsUseCase
from app.application.use_cases.generate_audio_use_case import GenerateAudioUseCase
from app.services.artifact_cache_service import artifact_cache


def test_script_generation_cache_integration():
    """Test that script generation properly uses artifact cache."""
    # Clear cache before test
    artifact_cache.clear()
    
    try:
        # Mock the LLM service to return a predictable result
        # Patch where it's used, not where it's defined
        with patch('app.application.use_cases.generate_script_use_case.generate_script_with_llm') as mock_llm:
            mock_llm.return_value = {
                'ok': True,
                'script': 'Test script content for caching',
                'provider': 'TemplateProvider',
                'time': 0.1,
                'quality': 'fast'
            }
            
            use_case = GenerateScriptUseCase()
            
            # First call - should go to LLM and cache result
            result1 = use_case.execute(
                briefing="Test product for caching",
                project_id="test_cache_integration",
                mode="fast"
            )
            
            print(f"DEBUG: result1 = {result1}")
            print(f"DEBUG: mock_llm.call_count = {mock_llm.call_count}")
            if mock_llm.call_count > 0:
                print(f"DEBUG: mock_llm.call_args = {mock_llm.call_args}")
            
            assert result1["ok"] is True
            assert result1["data"]["cache_hit"] is False
            # The mock returns exactly what we set it to return
            assert result1["data"]["script"] == 'Test script content for caching'
            assert result1["data"]["provider"] == "TemplateProvider"
            
            # Verify it was cached
            artifact_key = use_case._generate_artifact_key(
                "Test product for caching", 
                "test_cache_integration", 
                "fast"
            )
            cached = artifact_cache.contains(artifact_key)
            assert cached is True
            
            # Second call - should return cached result
            result2 = use_case.execute(
                briefing="Test product for caching",
                project_id="test_cache_integration",
                mode="fast"
            )
            
            print(f"DEBUG: result2 = {result2}")
            
            assert result2["ok"] is True
            assert result2["data"]["cache_hit"] is True
            # Cached result should be identical to the first
            assert result2["data"]["script"] == 'Test script content for caching'
            assert result2["data"]["provider"] == "CACHE"
            
            # Verify LLM was only called once
            assert mock_llm.call_count == 1
            
    finally:
        # Clean up
        artifact_cache.clear()


def test_different_scripts_different_cache_keys():
    """Test that different scripts generate different cache keys."""
    artifact_cache.clear()
    
    try:
        with patch('app.services.script_service.generate_script_with_llm') as mock_llm:
            mock_llm.return_value = {
                'ok': True,
                'script': 'Script content',
                'provider': 'TemplateProvider',
                'time': 0.1,
                'quality': 'fast'
            }
            
            use_case = GenerateScriptUseCase()
            
            # Generate two different scripts
            result1 = use_case.execute(
                briefing="First product description",
                project_id="test_project",
                mode="fast"
            )
            
            result2 = use_case.execute(
                briefing="Second product description",
                project_id="test_project", 
                mode="fast"
            )
            
            # Both should succeed
            assert result1["ok"] is True
            assert result2["ok"] is True
            
            # First should be cache miss, second should also be miss (different content)
            assert result1["data"]["cache_hit"] is False
            assert result2["data"]["cache_hit"] is False
            
            # But calling the same again should hit cache
            result3 = use_case.execute(
                briefing="First product description",
                project_id="test_project",
                mode="fast"
            )
            
            assert result3["ok"] is True
            assert result3["data"]["cache_hit"] is True
            
    finally:
        artifact_cache.clear()


def test_cache_persistence_across_instances():
    """Test that cache persists across different use case instances."""
    artifact_cache.clear()
    
    try:
        with patch('app.services.script_service.generate_script_with_llm') as mock_llm:
            mock_llm.return_value = {
                'ok': True,
                'script': 'Persistent script',
                'provider': 'TemplateProvider',
                'time': 0.1,
                'quality': 'fast'
            }
            
            # First use case instance
            use_case1 = GenerateScriptUseCase()
            result1 = use_case1.execute(
                briefing="Test for persistence",
                project_id="persistence_test",
                mode="fast"
            )
            
            assert result1["ok"] is True
            assert result1["data"]["cache_hit"] is False
            # The script service formats the script using TemplateProvider, which adds structure
            # We verify that our input briefing influenced the output
            assert "Test for persistence" in result1["data"]["script"]
            assert result1["data"]["provider"] == "TemplateProvider"
            
            # Second use case instance should find cached result
            use_case2 = GenerateScriptUseCase()
            result2 = use_case2.execute(
                briefing="Test for persistence",
                project_id="persistence_test",
                mode="fast"
            )
            
            assert result2["ok"] is True
            assert result2["data"]["cache_hit"] is True
            # Cached result should contain the original briefing influence
            assert "Test for persistence" in result2["data"]["script"]
            assert result2["data"]["provider"] == "CACHE"
            
    finally:
        artifact_cache.clear()


if __name__ == "__main__":
    # Run tests directly if executed as script
    try:
        test_script_generation_cache_integration()
        print("✓ test_script_generation_cache_integration passed")
    except Exception as e:
        print(f"✗ test_script_generation_cache_integration failed: {e}")
        
    try:
        test_different_scripts_different_cache_keys()
        print("✓ test_different_scripts_different_cache_keys passed")
    except Exception as e:
        print(f"✗ test_different_scripts_different_cache_keys failed: {e}")
        
    try:
        test_cache_persistence_across_instances()
        print("✓ test_cache_persistence_across_instances passed")
    except Exception as e:
        print(f"✗ test_cache_persistence_across_instances failed: {e}")
        
    print("Integration tests completed")