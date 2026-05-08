import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logger

logger = setup_logger()
REPO_ROOT = Path(__file__).parent.parent


def test_wangp_unavailable_ffmpeg_fallback():
    """Test E2E fallback: WanGP indisponível → FFmpeg usado"""
    logger.info("Testando fallback WanGP → FFmpeg (WanGP indisponível)")
    
    with patch('app.pipeline.video_generation_pipeline.WanGPAdapter') as mock_wangp, \
         patch('app.pipeline.video_generation_pipeline.TTSAdapter') as mock_tts, \
         patch('app.pipeline.video_generation_pipeline.FFmpegAdapter') as mock_ffmpeg, \
         patch('app.services.script_service.generate_script_with_llm') as mock_script:
        
        # Configure mocks - WanGP indisponível, FFmpeg disponível
        mock_wangp_instance = MagicMock()
        mock_wangp_instance.is_available.return_value = False  # WanGP indisponível
        mock_wangp.return_value = mock_wangp_instance
        
        mock_tts_instance = MagicMock()
        mock_tts_instance.is_available.return_value = True
        mock_tts_instance.generate_audio.return_value = {'success': True, 'audio_path': 'test.wav'}
        mock_tts.return_value = mock_tts_instance
        
        mock_ffmpeg_instance = MagicMock()
        mock_ffmpeg_instance.is_available.return_value = True
        mock_ffmpeg_instance.create_static_video.return_value = {'success': True, 'video_path': 'scene_001.mp4'}
        mock_ffmpeg_instance.concat_videos.return_value = {'success': True, 'video_path': 'final.mp4'}
        mock_ffmpeg.return_value = mock_ffmpeg_instance
        
        mock_script.return_value = {'script': 'Cena 1: Teste de fallback\nCena 2: Segunda cena'}
        
        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
        
        pipeline = VideoGenerationPipeline()
        logger.info("  OK: Pipeline instanciado")
        
        # Execute pipeline
        result = pipeline.generate_commercial(
            project_id='test_e2e_wangp_fallback',
            product='Teste Produto',
            target_audience='Teste Audiência',
            progress_callback=None
        )
        
        # Verify success
        assert result.get('success') is True, f"Pipeline falhou: {result.get('error')}"
        logger.info("  SUCESSO! Pipeline executado com fallback para FFmpeg")
        
        # Verify FFmpeg was called (fallback used)
        assert mock_ffmpeg_instance.create_static_video.called, "FFmpeg.create_static_video não foi chamado"
        assert mock_ffmpeg_instance.concat_videos.called, "FFmpeg.concat_videos não foi chamado"
        logger.info("  ✓ FFmpeg foi usado como fallback (create_static_video e concat_videos chamados)")
        
        # Verify WanGP was NOT called for video generation
        assert not mock_wangp_instance.generate_video.called, "WanGP.generate_video foi chamado inesperadamente"
        logger.info("  ✓ WanGP não foi chamado para geração de vídeo (corretamente indisponível)")
        
        # Verify provider used in result
        provider_used = result.get('provider_used', '')
        assert 'FFmpeg' in provider_used or 'Fallback' in provider_used, f"Provider usado incorreto: {provider_used}"
        logger.info(f"  ✓ Provider usado correto: {provider_used}")
        
        return True


def test_ffmpeg_unavailable_graceful_failure():
    """Test E2E graceful failure: FFmpeg indisponível → falha controlada"""
    logger.info("Testando falha graciosa FFmpeg indisponível")
    
    with patch('app.pipeline.video_generation_pipeline.WanGPAdapter') as mock_wangp, \
         patch('app.pipeline.video_generation_pipeline.TTSAdapter') as mock_tts, \
         patch('app.pipeline.video_generation_pipeline.FFmpegAdapter') as mock_ffmpeg, \
         patch('app.services.script_service.generate_script_with_llm') as mock_script:
        
        # Configure mocks - WanGP disponível, FFmpeg indisponível
        mock_wangp_instance = MagicMock()
        mock_wangp_instance.is_available.return_value = True
        mock_wangp_instance.generate_video.return_value = {'success': True, 'video_path': 'scene_001.mp4'}
        mock_wangp.return_value = mock_wangp_instance
        
        mock_tts_instance = MagicMock()
        mock_tts_instance.is_available.return_value = True
        mock_tts_instance.generate_audio.return_value = {'success': True, 'audio_path': 'test.wav'}
        mock_tts.return_value = mock_tts_instance
        
        mock_ffmpeg_instance = MagicMock()
        mock_ffmpeg_instance.is_available.return_value = False  # FFmpeg indisponível
        mock_ffmpeg_instance.concat_videos.return_value = {'success': False, 'error': 'FFmpeg not available for concatenation'}
        mock_ffmpeg.return_value = mock_ffmpeg_instance
        
        mock_script.return_value = {'script': 'Cena 1: Teste\nCena 2: Outro teste'}
        
        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
        
        pipeline = VideoGenerationPipeline()
        
        # Execute pipeline
        result = pipeline.generate_commercial(
            project_id='test_e2e_ffmpeg_fail',
            product='Teste Produto',
            target_audience='Teste Audiência',
            progress_callback=None
        )
        
        # Should fail gracefully (not crash)
        assert result.get('success') is False, "Pipeline deveria ter falhado mas succeeded"
        error_msg = result.get('error', '').lower()
        assert 'ffmpeg' in error_msg or 'video' in error_msg or 'falha' in error_msg, \
            f"Erro não relacionado a FFmpeg/video: {error_msg}"
        logger.info("  ✓ Pipeline falhou graciosamente (sem crash)")
        logger.info(f"  Erro reportado: {result.get('error')}")
        
        return True


def test_both_available_wangp_used():
    """Test normal case: ambos disponíveis → WanGP usado (preferência)"""
    logger.info("Testando caso normal: WanGP e FFmpeg disponíveis → WanGP usado")
    
    with patch('app.pipeline.video_generation_pipeline.WanGPAdapter') as mock_wangp, \
         patch('app.pipeline.video_generation_pipeline.TTSAdapter') as mock_tts, \
         patch('app.pipeline.video_generation_pipeline.FFmpegAdapter') as mock_ffmpeg, \
         patch('app.services.script_service.generate_script_with_llm') as mock_script:
        
        # Configure mocks - ambos disponíveis
        mock_wangp_instance = MagicMock()
        mock_wangp_instance.is_available.return_value = True
        mock_wangp_instance.generate_video.return_value = {'success': True, 'video_path': 'scene_001.mp4'}
        mock_wangp.return_value = mock_wangp_instance
        
        mock_tts_instance = MagicMock()
        mock_tts_instance.is_available.return_value = True
        mock_tts_instance.generate_audio.return_value = {'success': True, 'audio_path': 'test.wav'}
        mock_tts.return_value = mock_tts_instance
        
        mock_ffmpeg_instance = MagicMock()
        mock_ffmpeg_instance.is_available.return_value = True
        mock_ffmpeg_instance.create_static_video.return_value = {'success': True, 'video_path': 'scene_001.mp4'}
        mock_ffmpeg_instance.concat_videos.return_value = {'success': True, 'video_path': 'final.mp4'}
        mock_ffmpeg.return_value = mock_ffmpeg_instance
        
        mock_script.return_value = {'script': 'Cena 1: Teste normal\nCena 2: Segunda cena'}
        
        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
        
        pipeline = VideoGenerationPipeline()
        
        # Execute pipeline
        result = pipeline.generate_commercial(
            project_id='test_e2e_both_available',
            product='Teste Produto',
            target_audience='Teste Audiência',
            progress_callback=None
        )
        
        # Should succeed
        assert result.get('success') is True, f"Pipeline falhou: {result.get('error')}"
        logger.info("  SUCESSO! Pipeline executado com WanGP (preferido)")
        
        # Verify WanGP WAS called for video generation (preferred)
        assert mock_wangp_instance.generate_video.called, "WanGP.generate_video não foi chamado"
        logger.info("  ✓ WanGP foi usado para geração de vídeo (preferido quando disponível)")
        
        # FFmpeg might still be called for concatenation or other tasks
        # but video generation should use WanGP
        
        return True


def test_files_exist():
    """Verify that the adapter files exist"""
    wangp_path = REPO_ROOT / "app/adapters/wangp_adapter.py"
    ffmpeg_path = REPO_ROOT / "app/adapters/ffmpeg_adapter.py"
    
    assert wangp_path.exists(), f"WanGP adapter not found: {wangp_path}"
    assert ffmpeg_path.exists(), f"FFmpeg adapter not found: {ffmpeg_path}"
    
    logger.info(f"  OK: {wangp_path.name} encontrado")
    logger.info(f"  OK: {ffmpeg_path.name} encontrado")
    
    return True


if __name__ == "__main__":
    results = []
    for name, fn in [
        ("Arquivos de adapter existem", test_files_exist),
        ("WanGP indisponível → FFmpeg fallback", test_wangp_unavailable_ffmpeg_fallback),
        ("FFmpeg indisponível → falha graciosa", test_ffmpeg_unavailable_graceful_failure),
        ("Ambos disponíveis → WanGP usado (preferido)", test_both_available_wangp_used),
    ]:
        try:
            result = fn()
            results.append((name, result))
            if result:
                logger.info(f"✅ {name}: PASSOU")
            else:
                logger.error(f"❌ {name}: FALHOU")
        except Exception as e:
            logger.error(f"❌ {name}: FALHOU com exceção: {e}")
            results.append((name, False))

    print("\n" + "="*60)
    print("RESULTADOS QA-1003: Teste E2E WanGP falha → FFmpeg")
    print("="*60)
    for name, result in results:
        status = "PASSOU" if result else "FALHOU"
        print(f"{name:<45} {status}")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nPASSOU: {passed}/{total}")
    
    if passed == total:
        print("🎉 TODOS OS TESTES QA-1003 PASSARAM!")
        sys.exit(0)
    else:
        print("💥 ALGUNS TESTES QA-1003 FALHARAM!")
        sys.exit(1)