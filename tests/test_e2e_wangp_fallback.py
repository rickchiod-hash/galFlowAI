import shutil
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from contextlib import ExitStack

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import PROJECTS_DIR
from app.logging_config import setup_logger

logger = setup_logger()
REPO_ROOT = Path(__file__).parent.parent


def _ensure_approved_script(project_id: str, script_text: str) -> None:
    """Create script_approved.md so pipeline passes the approval gate."""
    approved_dir = PROJECTS_DIR / project_id / "script"
    approved_dir.mkdir(parents=True, exist_ok=True)
    (approved_dir / "script_approved.md").write_text(script_text, encoding="utf-8")


def _setup_use_case_adapter_patches(mock_wangp, mock_tts, mock_ffmpeg, mock_script):
    """Apply adapter patches at use case module level so use cases see the same mocks."""
    return [
        patch('app.application.use_cases.render_video_use_case.WanGPAdapter', mock_wangp),
        patch('app.application.use_cases.create_static_video_use_case.FFmpegAdapter', mock_ffmpeg),
        patch('app.application.use_cases.concat_videos_use_case.FFmpegAdapter', mock_ffmpeg),
        patch('app.application.use_cases.generate_audio_use_case.TTSAdapter', mock_tts),
        patch('app.application.use_cases.generate_script_use_case.generate_script_with_llm', mock_script),
    ]

def _base_patches(mock_wangp, mock_tts, mock_ffmpeg, mock_script):
    """Base pipeline-level patches."""
    return [
        patch('app.pipeline.video_generation_pipeline.WanGPAdapter', mock_wangp),
        patch('app.pipeline.video_generation_pipeline.TTSAdapter', mock_tts),
        patch('app.pipeline.video_generation_pipeline.FFmpegAdapter', mock_ffmpeg),
        patch('app.services.script_service.generate_script_with_llm', mock_script),
    ]

def _pipeline_test_setup(wangp_available=False, ffmpeg_available=True):
    """Shared mock setup for E2E pipeline tests."""
    mock_wangp = MagicMock()
    mock_tts = MagicMock()
    mock_ffmpeg = MagicMock()
    mock_script = MagicMock()

    mock_wangp_instance = MagicMock()
    mock_wangp_instance.is_available.return_value = wangp_available
    mock_wangp_instance.disponivel.return_value = wangp_available
    mock_wangp_instance.render_scene.return_value = {"video_path": "scene_001.mp4", "success": True}
    mock_wangp.return_value = mock_wangp_instance

    mock_tts_instance = MagicMock()
    mock_tts_instance.is_available.return_value = True
    mock_tts_instance.generate_audio.return_value = {'success': True, 'audio_path': 'test.wav'}
    mock_tts.return_value = mock_tts_instance

    mock_ffmpeg_instance = MagicMock()
    mock_ffmpeg_instance.is_available.return_value = ffmpeg_available
    mock_ffmpeg_instance.create_static_video.return_value = {'success': True, 'video_path': 'scene_001.mp4'}
    mock_ffmpeg_instance.concat_videos.return_value = {'success': True, 'video_path': 'final.mp4'}
    mock_ffmpeg.return_value = mock_ffmpeg_instance

    mock_script.return_value = {
        'ok': True,
        'script': 'Cena 1: Teste de fallback\nCena 2: Segunda cena',
        'provider': 'TemplateProvider',
        'time': 0.01,
        'quality': 'fast',
    }

    return mock_wangp, mock_wangp_instance, mock_tts, mock_tts_instance, mock_ffmpeg, mock_ffmpeg_instance, mock_script


def test_wangp_unavailable_ffmpeg_fallback():
    """Test E2E fallback: WanGP indisponível → FFmpeg usado"""
    logger.info("Testando fallback WanGP → FFmpeg (WanGP indisponível)")
    
    mocks = _pipeline_test_setup(wangp_available=False, ffmpeg_available=True)
    mock_wangp, mock_wangp_instance, mock_tts, mock_tts_instance, mock_ffmpeg, mock_ffmpeg_instance, mock_script = mocks
    
    base_patches = _base_patches(mock_wangp, mock_tts, mock_ffmpeg, mock_script)
    use_case_patches = _setup_use_case_adapter_patches(mock_wangp, mock_tts, mock_ffmpeg, mock_script)
    
    with ExitStack() as stack:
        for p in base_patches + use_case_patches:
            stack.enter_context(p)
        
        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
        
        pipeline = VideoGenerationPipeline()
        logger.info("  OK: Pipeline instanciado")
        
        script_text = mock_script.return_value['script']
        _ensure_approved_script('test_e2e_wangp_fallback', script_text)

        # Execute pipeline
        result = pipeline.generate_commercial(
            project_id='test_e2e_wangp_fallback',
            product='Teste Produto',
            target_audience='Teste Audiência',
            progress_callback=None
        )
        
        shutil.rmtree(PROJECTS_DIR / 'test_e2e_wangp_fallback', ignore_errors=True)

        # Verify success
        assert result.get('success') is True, f"Pipeline falhou: {result.get('error')}"
        logger.info("  SUCESSO! Pipeline executado com fallback para FFmpeg")
        
        # Verify FFmpeg was called (fallback used)
        assert mock_ffmpeg_instance.create_static_video.called, "FFmpeg.create_static_video não foi chamado"
        assert mock_ffmpeg_instance.concat_videos.called, "FFmpeg.concat_videos não foi chamado"
        logger.info("  ✓ FFmpeg foi usado como fallback (create_static_video e concat_videos chamados)")
        
        # Verify WanGP was NOT called for video generation
        assert not mock_wangp_instance.render_scene.called, "WanGP.render_scene foi chamado inesperadamente"
        logger.info("  ✓ WanGP não foi chamado para geração de vídeo (corretamente indisponível)")
        
        # Verify provider used in result
        provider_used = result.get('provider_used', '')
        assert 'FFmpeg' in provider_used or 'Fallback' in provider_used, f"Provider usado incorreto: {provider_used}"
        logger.info(f"  ✓ Provider usado correto: {provider_used}")
        



def test_ffmpeg_unavailable_graceful_failure():
    """Test E2E graceful failure: FFmpeg indisponível → falha controlada"""
    logger.info("Testando falha graciosa FFmpeg indisponível")
    
    mocks = _pipeline_test_setup(wangp_available=True, ffmpeg_available=False)
    mock_wangp, mock_wangp_instance, mock_tts, mock_tts_instance, mock_ffmpeg, mock_ffmpeg_instance, mock_script = mocks
    
    base_patches = _base_patches(mock_wangp, mock_tts, mock_ffmpeg, mock_script)
    use_case_patches = _setup_use_case_adapter_patches(mock_wangp, mock_tts, mock_ffmpeg, mock_script)
    
    with ExitStack() as stack:
        for p in base_patches + use_case_patches:
            stack.enter_context(p)
        
        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
        
        pipeline = VideoGenerationPipeline()
        
        script_text = mock_script.return_value['script']
        _ensure_approved_script('test_e2e_ffmpeg_fail', script_text)

        # Execute pipeline
        result = pipeline.generate_commercial(
            project_id='test_e2e_ffmpeg_fail',
            product='Teste Produto',
            target_audience='Teste Audiência',
            progress_callback=None
        )
        
        shutil.rmtree(PROJECTS_DIR / 'test_e2e_ffmpeg_fail', ignore_errors=True)

        # Should fail gracefully (not crash)
        assert result.get('success') is False, "Pipeline deveria ter falhado mas succeeded"
        error_msg = result.get('error', '').lower()
        assert 'ffmpeg' in error_msg or 'video' in error_msg or 'falha' in error_msg, \
            f"Erro não relacionado a FFmpeg/video: {error_msg}"
        logger.info("  ✓ Pipeline falhou graciosamente (sem crash)")
        logger.info(f"  Erro reportado: {result.get('error')}")
        



def test_both_available_wangp_used():
    """Test normal case: ambos disponíveis → WanGP usado (preferência)"""
    logger.info("Testando caso normal: WanGP e FFmpeg disponíveis → WanGP usado")
    
    mocks = _pipeline_test_setup(wangp_available=True, ffmpeg_available=True)
    mock_wangp, mock_wangp_instance, mock_tts, mock_tts_instance, mock_ffmpeg, mock_ffmpeg_instance, mock_script = mocks
    
    base_patches = _base_patches(mock_wangp, mock_tts, mock_ffmpeg, mock_script)
    use_case_patches = _setup_use_case_adapter_patches(mock_wangp, mock_tts, mock_ffmpeg, mock_script)
    
    with ExitStack() as stack:
        for p in base_patches + use_case_patches:
            stack.enter_context(p)
        
        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
        
        pipeline = VideoGenerationPipeline()
        
        script_text = mock_script.return_value['script']
        _ensure_approved_script('test_e2e_both_available', script_text)

        # Execute pipeline
        result = pipeline.generate_commercial(
            project_id='test_e2e_both_available',
            product='Teste Produto',
            target_audience='Teste Audiência',
            progress_callback=None
        )
        
        shutil.rmtree(PROJECTS_DIR / 'test_e2e_both_available', ignore_errors=True)

        # Should succeed
        assert result.get('success') is True, f"Pipeline falhou: {result.get('error')}"
        logger.info("  SUCESSO! Pipeline executado com WanGP (preferido)")
        
        # Verify WanGP WAS called for video generation (preferred)
        assert mock_wangp_instance.render_scene.called, "WanGP.render_scene não foi chamado"
        logger.info("  ✓ WanGP foi usado para geração de vídeo (preferido quando disponível)")
        
        # FFmpeg might still be called for concatenation or other tasks
        # but video generation should use WanGP
        



def test_files_exist():
    """Verify that the adapter files exist"""
    wangp_path = REPO_ROOT / "app/adapters/wangp_adapter.py"
    ffmpeg_path = REPO_ROOT / "app/adapters/ffmpeg_adapter.py"
    
    assert wangp_path.exists(), f"WanGP adapter not found: {wangp_path}"
    assert ffmpeg_path.exists(), f"FFmpeg adapter not found: {ffmpeg_path}"
    
    logger.info(f"  OK: {wangp_path.name} encontrado")
    logger.info(f"  OK: {ffmpeg_path.name} encontrado")
    



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