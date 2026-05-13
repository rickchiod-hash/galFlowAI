"""tests/integration/test_pipeline_completa.py — Testa fluxo end-to-end."""

import pytest
from pathlib import Path
from app.logging_config import setup_logger

logger = setup_logger()

class TestPipelineCompleta:
    """Testa fluxo completo: briefing → roteiro → cenas → prompts → video."""
    
    def setup_method(self):
        self.project_id = "test_integration_001"
        self.logger = logger
    
    def test_fluxo_completo_mock(self):
        """Testa pipeline completo com mocks."""
        from app.pipeline.script_generator import generate_script
        from app.pipeline.scene_splitter import split_script_into_scenes
        from app.pipeline.prompt_builder import build_prompts_for_scenes
        from app.adapters.ffmpeg_adapter import create_storyboard_video
        
        # Mock para não gerar vídeo real
        from unittest.mock import patch, MagicMock
        
        # Mockar generate_script_with_llm para retornar um roteiro de template
        with patch('app.pipeline.script_generator.generate_script_with_llm') as mock_llm:
            mock_llm.return_value = {
                "ok": True,
                "script": "Cena 1: Apresentação do produto\nCena 2: Demonstração\nCena 3: Chamada para ação",
                "provider": "template",
                "time": 0.1,
                "quality": "basic"
            }
            
            # 1. Gerar roteiro  
            script = generate_script("Teste de pipeline completo", self.project_id)
            assert script is not None
            assert len(script) > 20
            
            # 2. Dividir em cenas
            scenes = split_script_into_scenes(script, self.project_id)
            assert len(scenes) >= 3
            
            # 3. Build prompts
            scenes = build_prompts_for_scenes(scenes)
            for scene in scenes:
                assert "prompt" in scene  # Chave correta é prompt
                
            # 4. FFmpeg fallback (mock)  
            with patch('app.adapters.ffmpeg_adapter.FFmpegAdapter._check_availability', return_value=False):
                video = create_storyboard_video(self.project_id, scenes)
                # Como FFmpeg não está disponível, deve retornar None
                assert video is None
    
    def test_fallback_wangp(self):
        """Testa fallback WanGP → FFmpeg."""
        from app.adapters.wangp_adapter import WanGPAdapter
        from unittest.mock import patch, MagicMock
        
        # Mockar _check_availability para retornar False
        with patch.object(WanGPAdapter, '_check_availability', return_value=False):
            adapter = WanGPAdapter(self.logger)
            
            result = adapter.generate_video(
                prompt="test scene",
                duration_seconds=5,
                output_path="test_output.mp4"
            )
            assert result["success"] is False  # Deve retornar dict com success False
    
    def test_fallback_tts(self):
        """Testa fallback TTS: Kokoro → pyttsx3 → silêncio."""
        from app.adapters.tts_adapter import TTSAdapter
        from unittest.mock import patch, MagicMock
        
        # Mockar para kokoro e pyttsx3 não estarem disponíveis
        with patch.dict('sys.modules', {'kokoro': None, 'pyttsx3': None, 'win32com': None}):
            adapter = TTSAdapter(self.logger)
            assert adapter.selected_engine == "silence"
            
            # Testa geração de áudio (silêncio)
            result = adapter.generate_audio("Teste", "test_audio.wav")
            # Deve retornar dict com success
            assert result is not None
            assert "success" in result
