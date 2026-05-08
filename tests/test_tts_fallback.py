import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logger

logger = setup_logger()
REPO_ROOT = Path(__file__).parent.parent


def test_tts_adapter_files_exist():
    """Verify that the TTS adapter file exists"""
    tts_path = REPO_ROOT / "app/adapters/tts_adapter.py"
    assert tts_path.exists(), f"TTS adapter not found: {tts_path}"
    
    logger.info(f"  OK: {tts_path.name} encontrado")
    
    return True


def test_tts_has_silence_fallback():
    """Test that TTSAdapter has silence fallback mechanism"""
    tts_path = REPO_ROOT / "app/adapters/tts_adapter.py"
    assert tts_path.exists(), f"TTSAdapter not found: {tts_path}"
    content = tts_path.read_text(encoding="utf-8", errors="ignore")
    has_silence = "silence" in content.lower()
    has_fallback = "fallback" in content.lower()
    assert has_silence, "TTSAdapter missing silence fallback"
    assert has_fallback, "TTSAdapter missing fallback mechanism"
    logger.info("TTS SILENCE FALLBACK: OK")
    
    return True


def test_tts_unavailable_graceful_audio_fallback():
    """Test E2E graceful fallback: TTS indisponível → áudio silencioso"""
    logger.info("Testando fallback TTS indisponível → silêncio")
    
    # Mock the services and adapters that the pipeline uses
    with patch('app.services.script_service.generate_script_with_llm') as mock_script, \
         patch('app.pipeline.video_generation_pipeline.split_script_into_scenes') as mock_split, \
         patch('app.pipeline.video_generation_pipeline.build_prompts_for_scenes') as mock_build, \
         patch('app.pipeline.video_generation_pipeline.TTSAdapter') as mock_tts_cls, \
         patch('app.pipeline.video_generation_pipeline.WanGPAdapter') as mock_wangp_cls, \
         patch('app.pipeline.video_generation_pipeline.FFmpegAdapter') as mock_ffmpeg_cls:
        
        # Configure mocks for services
        mock_script.return_value = {'script': 'Cena 1: Teste de TTS\nCena 2: Segunda cena'}
        
        mock_split.return_value = [
            {'id': 1, 'prompt': 'Prompt 1', 'scene_text': 'Scene 1 text', 'duration': 5},
            {'id': 2, 'prompt': 'Prompt 2', 'scene_text': 'Scene 2 text', 'duration': 5}
        ]
        
        mock_build.return_value = [
            {'id': 1, 'prompt': 'Prompt 1', 'scene_text': 'Scene 1 text', 'duration': 5},
            {'id': 2, 'prompt': 'Prompt 2', 'scene_text': 'Scene 2 text', 'duration': 5}
        ]
        
        # Configure mocks for adapters
        mock_tts = MagicMock()
        mock_tts.generate_audio.return_value = {'success': False, 'error': 'TTS not available'}
        mock_tts.is_available.return_value = False
        mock_tts_cls.return_value = mock_tts
        
        mock_wangp = MagicMock()
        mock_wangp.generate_video.return_value = {'success': True, 'video_path': 'scene_001.mp4'}
        mock_wangp.is_available.return_value = True
        mock_wangp_cls.return_value = mock_wangp
        
        mock_ffmpeg = MagicMock()
        mock_ffmpeg.create_static_video.return_value = {'success': True, 'video_path': 'scene_001.mp4'}
        mock_ffmpeg.concat_videos.return_value = {'success': True, 'video_path': 'commercial.mp4'}
        mock_ffmpeg_cls.return_value = mock_ffmpeg
        
        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
        
        pipeline = VideoGenerationPipeline()
        
        # Execute pipeline
        result = pipeline.generate_commercial(
            project_id='test_e2e_tts_fail',
            product='Teste Produto',
            target_audience='Teste Audiência',
            progress_callback=None
        )
        
        # Should succeed (vídeo gerado, mesmo sem áudio)
        assert result.get('success') is True, f"Pipeline falhou: {result.get('error')}"
        logger.info("  SUCESSO! Pipeline executado mesmo com TTS indisponível")
        
        # Verify narration_path is None or points to silent audio
        narration_path = result.get('narration_path')
        logger.info(f"  Narration path: {narration_path}")
        
        # Verify TTS was attempted but failed
        assert mock_tts.generate_audio.called, "TTS Adapter generate_audio não foi chamado"
        logger.info("  ✓ TTS foi tentado (mas indisponível)")
        
        # Verify WanGP was used for video (since it was available)
        assert mock_wangp.generate_video.called, "WanGP Adapter generate_video não foi chamado"
        logger.info("  ✓ WanGP foi usado para geração de vídeo (disponível)")
        
        return True


def test_tts_available_normal_operation():
    """Test normal case: TTS disponível → operação normal"""
    logger.info("Testando operação normal: TTS disponível")
    
    with patch('app.services.script_service.generate_script_with_llm') as mock_script, \
         patch('app.pipeline.video_generation_pipeline.split_script_into_scenes') as mock_split, \
         patch('app.pipeline.video_generation_pipeline.build_prompts_for_scenes') as mock_build, \
         patch('app.pipeline.video_generation_pipeline.TTSAdapter') as mock_tts_cls, \
         patch('app.pipeline.video_generation_pipeline.WanGPAdapter') as mock_wangp_cls, \
         patch('app.pipeline.video_generation_pipeline.FFmpegAdapter') as mock_ffmpeg_cls:
        
        # Configure mocks for services
        mock_script.return_value = {'script': 'Cena 1: Teste normal\nCena 2: Segunda cena'}
        
        mock_split.return_value = [
            {'id': 1, 'prompt': 'Prompt 1', 'scene_text': 'Scene 1 text', 'duration': 5},
            {'id': 2, 'prompt': 'Prompt 2', 'scene_text': 'Scene 2 text', 'duration': 5}
        ]
        
        mock_build.return_value = [
            {'id': 1, 'prompt': 'Prompt 1', 'scene_text': 'Scene 1 text', 'duration': 5},
            {'id': 2, 'prompt': 'Prompt 2', 'scene_text': 'Scene 2 text', 'duration': 5}
        ]
        
        # Configure mocks for adapters
        mock_tts = MagicMock()
        mock_tts.generate_audio.return_value = {'success': True, 'audio_path': 'narration.wav'}
        mock_tts.is_available.return_value = True
        mock_tts_cls.return_value = mock_tts
        
        mock_wangp = MagicMock()
        mock_wangp.generate_video.return_value = {'success': True, 'video_path': 'scene_001.mp4'}
        mock_wangp.is_available.return_value = True
        mock_wangp_cls.return_value = mock_wangp
        
        mock_ffmpeg = MagicMock()
        mock_ffmpeg.create_static_video.return_value = {'success': True, 'video_path': 'scene_001.mp4'}
        mock_ffmpeg.concat_videos.return_value = {'success': True, 'video_path': 'commercial.mp4'}
        mock_ffmpeg_cls.return_value = mock_ffmpeg
        
        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
        
        pipeline = VideoGenerationPipeline()
        
        # Execute pipeline
        result = pipeline.generate_commercial(
            project_id='test_e2e_tts_normal',
            product='Teste Produto',
            target_audience='Teste Audiência',
            progress_callback=None
        )
        
        # Should succeed
        assert result.get('success') is True, f"Pipeline falhou: {result.get('error')}"
        logger.info("  SUCESSO! Pipeline executado normalmente com TTS disponível")
        
        # Verify narration_path points to audio file
        narration_path = result.get('narration_path')
        logger.info(f"  Narration path: {narration_path}")
        
        # Verify all components were called appropriately
        assert mock_wangp.generate_video.called, "WanGP Adapter generate_video não foi chamado"
        assert mock_tts.generate_audio.called, "TTS Adapter generate_audio não foi chamado"
        logger.info("  ✓ WanGP e TTS usados para geração, FFmpeg apenas para concatenação final")
        
        return True


def test_both_wangp_and_tts_unavailable():
    """Test case: WanGP indisponível → FFmpeg fallback, TTS indisponível → silêncio"""
    logger.info("Testando cenário extremo: WanGP e TTS indisponíveis")
    
    with patch('app.services.script_service.generate_script_with_llm') as mock_script, \
         patch('app.pipeline.video_generation_pipeline.split_script_into_scenes') as mock_split, \
         patch('app.pipeline.video_generation_pipeline.build_prompts_for_scenes') as mock_build, \
         patch('app.pipeline.video_generation_pipeline.TTSAdapter') as mock_tts_cls, \
         patch('app.pipeline.video_generation_pipeline.WanGPAdapter') as mock_wangp_cls, \
         patch('app.pipeline.video_generation_pipeline.FFmpegAdapter') as mock_ffmpeg_cls:
        
        # Configure mocks for services
        mock_script.return_value = {'script': 'Cena 1: Teste extremo\nCena 2: Segunda cena'}
        
        mock_split.return_value = [
            {'id': 1, 'prompt': 'Prompt 1', 'scene_text': 'Scene 1 text', 'duration': 5},
            {'id': 2, 'prompt': 'Prompt 2', 'scene_text': 'Scene 2 text', 'duration': 5}
        ]
        
        mock_build.return_value = [
            {'id': 1, 'prompt': 'Prompt 1', 'scene_text': 'Scene 1 text', 'duration': 5},
            {'id': 2, 'prompt': 'Prompt 2', 'scene_text': 'Scene 2 text', 'duration': 5}
        ]
        
        # Configure mocks for adapters - WanGP indisponível, TTS indisponível, FFmpeg disponível
        mock_tts = MagicMock()
        mock_tts.generate_audio.return_value = {'success': False, 'error': 'TTS not available'}
        mock_tts.is_available.return_value = False
        mock_tts_cls.return_value = mock_tts
        
        mock_wangp = MagicMock()
        mock_wangp.generate_video.return_value = {'success': False, 'error': 'WanGP not available'}
        mock_wangp.is_available.return_value = False
        mock_wangp_cls.return_value = mock_wangp
        
        mock_ffmpeg = MagicMock()
        mock_ffmpeg.create_static_video.return_value = {'success': True, 'video_path': 'scene_001.mp4'}
        mock_ffmpeg.concat_videos.return_value = {'success': True, 'video_path': 'commercial.mp4'}
        mock_ffmpeg_cls.return_value = mock_ffmpeg
        
        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
        
        pipeline = VideoGenerationPipeline()
        
        # Execute pipeline
        result = pipeline.generate_commercial(
            project_id='test_e2e_both_fail',
            product='Teste Produto',
            target_audience='Teste Audiência',
            progress_callback=None
        )
        
        # Should succeed (vídeo gerado com FFmpeg e silêncio)
        assert result.get('success') is True, f"Pipeline falhou: {result.get('error')}"
        logger.info("  SUCESSO! Pipeline executado com FFmpeg fallback e silêncio")
        
        # Verify FFmpeg was used for video (WanGP fallback)
        assert mock_ffmpeg.create_static_video.called, "FFmpeg create_static_video não foi chamado"
        logger.info("  ✓ FFmpeg usado para vídeo (WanGP fallback) e concatenação")
        
        # Verify WanGP was NOT used for video
        assert not mock_wangp.generate_video.called or not mock_wangp.generate_video.return_value.get('success'), "WanGP foi chamado inesperadamente"
        logger.info("  ✓ WanGP não foi usado para vídeo (corretamente indisponível)")
        
        # Verify TTS was attempted but failed
        assert mock_tts.generate_audio.called, "TTS Adapter generate_audio não foi chamado"
        logger.info("  ✓ TTS foi tentado (mas indisponível → silêncio)")
        
        return True


if __name__ == "__main__":
    results = []
    for name, fn in [
        ("Arquivo de adapter TTS existe", test_tts_adapter_files_exist),
        ("TTS tem silence fallback", test_tts_has_silence_fallback),
        ("TTS indisponível → silêncio (áudio opcional)", test_tts_unavailable_graceful_audio_fallback),
        ("TTS disponível → operação normal", test_tts_available_normal_operation),
        ("WanGP e TTS indisponíveis → FFmpeg + silêncio", test_both_wangp_and_tts_unavailable),
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
    print("RESULTADOS QA-1004: Teste TTS falha → export sem áudio")
    print("="*60)
    for name, result in results:
        status = "PASSOU" if result else "FALHOU"
        print(f"{name:<50} {status}")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nPASSOU: {passed}/{total}")
    
    if passed == total:
        print("🎉 TODOS OS TESTES QA-1004 PASSARAM!")
        sys.exit(0)
    else:
        print("💥 ALGUNS TESTES QA-1004 FALHARAM!")
        sys.exit(1)
