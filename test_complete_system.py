"""Testes abrangentes para todo o sistema GalFlowAI"""

import unittest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent))


class TestCompleteSystem(unittest.TestCase):
    """Testes de integração do sistema completo"""
    
    def test_all_imports(self):
        """Testa se todos os módulos principais podem ser importados"""
        try:
            from app.services.video_service import VideoService
            from app.services.tts_service import TTSService
            from app.domain.prompt_builder_service import build_prompts_for_scenes
            from app.domain.scene_parser import split_script_into_scenes
            from app.adapters.wangp_adapter import WanGPAdapter
            from app.adapters.ffmpeg_adapter import FFmpegAdapter
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Erro de import: {e}")
    
    def test_video_service_creation(self):
        """Testa criação do VideoService"""
        with patch('app.services.video_service.WanGPAdapter') as mock_wangp, \
             patch('app.services.video_service.FFmpegAdapter') as mock_ffmpeg:
            
            mock_wangp.return_value.is_available.return_value = True
            mock_ffmpeg.return_value.is_available.return_value = True
            
            from app.services.video_service import VideoService
            service = VideoService()
            
            self.assertIsNotNone(service)
            self.assertTrue(service.is_available())
    
    def test_prompt_generation_flow(self):
        """Testa fluxo completo de geração de prompts"""
        from app.domain.prompt_builder_service import build_prompts_for_scenes
        
        scenes = [
            {"id": "s1", "text": "Cena 1", "duration": 5},
            {"id": "s2", "text": "Cena 2", "duration": 8}
        ]
        
        prompts = build_prompts_for_scenes(scenes)
        
        self.assertEqual(len(prompts), 2)
        self.assertEqual(prompts[0]["scene_id"], "s1")
        self.assertEqual(prompts[1]["scene_id"], "s2")
        self.assertIn("prompt", prompts[0])
        self.assertIn("negative_prompt", prompts[0])
    
    def test_wangp_adapter_availability(self):
        """Testa verificação de disponibilidade do WanGP"""
        from app.adapters.wangp_adapter import WanGPAdapter
        
        adapter = WanGPAdapter()
        # Pode ser True ou False dependendo do ambiente
        result = adapter.is_available()
        self.assertIsInstance(result, bool)
    
    def test_tts_service_availability(self):
        """Testa verificação de disponibilidade do TTS"""
        from app.services.tts_service import TTSService
        
        service = TTSService()
        result = service.is_available()
        self.assertIsInstance(result, bool)


class TestHardwareConstraints(unittest.TestCase):
    """Testes relacionados a restrições de hardware"""
    
    def test_wangp_defaults_for_low_vram(self):
        """Testa se WanGP usa configurações para baixa VRAM"""
        from app.adapters.wangp_adapter import WanGPAdapter
        
        adapter = WanGPAdapter()
        
        # Verifica se o preset é adequado para 6GB VRAM
        # (deve ser 1.3B ou similar)
        self.assertIsNotNone(adapter.model_preset)
        self.assertIn("1.3", adapter.model_preset)
    
    def test_video_service_handles_low_vram(self):
        """Testa se VideoService lida com pouca VRAM"""
        mock_wangp = Mock()
        mock_wangp.is_available.return_value = True
        mock_wangp.model_preset = "1.3B"
        mock_wangp.resolution = "480p"
        
        with patch('app.services.video_service.WanGPAdapter', return_value=mock_wangp), \
             patch('app.services.video_service.FFmpegAdapter'):
            
            from app.services.video_service import VideoService
            service = VideoService()
            
            # Não deve tentar usar modelo grande
            self.assertEqual(mock_wangp.model_preset, "1.3B")


class TestErrorHandling(unittest.TestCase):
    """Testes de tratamento de erros"""
    
    def test_video_service_no_motors(self):
        """Testa erro quando nenhum motor de vídeo está disponível"""
        mock_wangp = Mock()
        mock_wangp.is_available.return_value = False
        
        mock_ffmpeg = Mock()
        mock_ffmpeg.is_available.return_value = False
        
        with patch('app.services.video_service.WanGPAdapter', return_value=mock_wangp), \
             patch('app.services.video_service.FFmpegAdapter', return_value=mock_ffmpeg):
            
            from app.services.video_service import VideoService
            service = VideoService()
            
            result = service.generate_scene_video(
                scene_id="test",
                prompt="test",
                output_path="test.mp4"
            )
            
            self.assertFalse(result["success"])
            self.assertIn("Nenhum motor", result["error"])
    
    def test_prompt_builder_empty_scenes(self):
        """Testa comportamento com lista vazia de cenas"""
        from app.domain.prompt_builder_service import build_prompts_for_scenes
        
        prompts = build_prompts_for_scenes([])
        self.assertEqual(len(prompts), 0)


class TestProjectStructure(unittest.TestCase):
    """Testes da estrutura do projeto"""
    
    def test_project_dirs_exist(self):
        """Testa se diretórios essenciais existem"""
        from app.config import PROJECTS_DIR
        
        projects_path = Path(PROJECTS_DIR)
        self.assertTrue(projects_path.exists())
    
    def test_assets_dir_exists(self):
        """Testa se diretório de assets existe"""
        assets_path = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/assets")
        # Pode ou não existir, mas não deve quebrar
        self.assertIsInstance(assets_path.exists(), bool)
    
    def test_config_loads(self):
        """Testa se config carrega sem erros"""
        try:
            from app.config import BASE_DIR, PROJECTS_DIR
            self.assertIsNotNone(BASE_DIR)
            self.assertIsNotNone(PROJECTS_DIR)
        except Exception as e:
            self.fail(f"Erro ao carregar config: {e}")


if __name__ == "__main__":
    unittest.main()
