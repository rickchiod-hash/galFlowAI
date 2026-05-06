"""Testes para VideoService"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))


class TestVideoService(unittest.TestCase):
    """Testes para o serviço de vídeo"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        # Mock dos adapters para evitar dependências reais
        self.mock_wangp = Mock()
        self.mock_wangp.is_available.return_value = True
        self.mock_wangp.generate_video.return_value = {"success": True}
        
        self.mock_ffmpeg = Mock()
        self.mock_ffmpeg.is_available.return_value = True
        self.mock_ffmpeg.create_static_video.return_value = {"success": True}
        self.mock_ffmpeg.concat_videos.return_value = {"success": True}
        
        # Patch os imports
        with patch('app.services.video_service.WanGPAdapter', return_value=self.mock_wangp), \
             patch('app.services.video_service.FFmpegAdapter', return_value=self.mock_ffmpeg):
            from app.services.video_service import VideoService
            self.service = VideoService()
    
    def test_service_initialization(self):
        """Testa inicialização do serviço"""
        self.assertIsNotNone(self.service)
        self.assertTrue(self.service.is_available())
    
    def test_service_status(self):
        """Testa retorno de status"""
        status = self.service.get_status()
        self.assertIn("available", status)
        self.assertIn("wangp_available", status)
        self.assertIn("ffmpeg_available", status)
    
    def test_generate_scene_video_wangp_success(self):
        """Testa geração de cena com WanGP com sucesso"""
        result = self.service.generate_scene_video(
            scene_id="scene_001",
            prompt="Um produto incrível",
            output_path="test_output.mp4"
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["scene_id"], "scene_001")
        self.assertEqual(result["provider"], "WanGP")
    
    def test_generate_scene_video_wangp_fallback_ffmpeg(self):
        """Testa fallback para FFmpeg quando WanGP falha"""
        # WanGP falha
        self.mock_wangp.generate_video.return_value = {"success": False, "error": "GPU error"}
        
        result = self.service.generate_scene_video(
            scene_id="scene_002",
            prompt="Teste",
            output_path="test_output2.mp4"
        )
        
        # Deve tentar FFmpeg como fallback
        self.assertTrue(result["success"])
        self.assertEqual(result["provider"], "FFmpeg")
    
    def test_generate_scene_video_no_motors(self):
        """Testa erro quando nenhum motor está disponível"""
        self.mock_wangp.is_available.return_value = False
        self.mock_ffmpeg.is_available.return_value = False
        
        with patch('app.services.video_service.WanGPAdapter', return_value=self.mock_wangp), \
             patch('app.services.video_service.FFmpegAdapter', return_value=self.mock_ffmpeg):
            from app.services.video_service import VideoService
            service = VideoService()
            
            result = service.generate_scene_video(
                scene_id="scene_003",
                prompt="Teste",
                output_path="test.mp4"
            )
            
            self.assertFalse(result["success"])
            self.assertIn("Nenhum motor", result["error"])


class TestVideoServiceIntegration(unittest.TestCase):
    """Testes de integração (podem baixar modelos ou acessar disco)"""
    
    def test_wangp_adapter_exists(self):
        """Testa se WanGPAdapter pode ser importado"""
        try:
            from app.adapters.wangp_adapter import WanGPAdapter
            self.assertTrue(True)
        except ImportError:
            self.fail("WanGPAdapter não pôde ser importado")
    
    def test_ffmpeg_adapter_exists(self):
        """Testa se FFmpegAdapter pode ser importado"""
        try:
            from app.adapters.ffmpeg_adapter import FFmpegAdapter
            self.assertTrue(True)
        except ImportError:
            self.fail("FFmpegAdapter não pôde ser importado")
    
    def test_video_service_import(self):
        """Testa se VideoService pode ser importado"""
        try:
            from app.services.video_service import VideoService
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"VideoService não pôde ser importado: {e}")


if __name__ == "__main__":
    unittest.main()
