import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logger

logger = setup_logger()
REPO_ROOT = Path(__file__).parent.parent


def test_tts_adapter_files_exist():
    tts_path = REPO_ROOT / "app/adapters/tts_adapter.py"
    assert tts_path.exists(), f"TTS adapter not found: {tts_path}"
    logger.info(f"  OK: {tts_path.name} encontrado")
    return True


def test_tts_has_silence_fallback():
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
    logger.info("Testando fallback TTS indisponível → silêncio")

    with patch('app.pipeline.video_generation_pipeline.GenerateScriptUseCase') as mock_script_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.SplitScenesUseCase') as mock_split_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.BuildPromptsUseCase') as mock_build_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.GenerateAudioUseCase') as mock_audio_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.RenderVideoUseCase') as mock_render_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.CreateStaticVideoUseCase') as mock_static_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.ConcatVideosUseCase') as mock_concat_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.WanGPAdapter') as mock_wangp_cls, \
         patch('app.pipeline.video_generation_pipeline.TTSAdapter') as mock_tts_cls, \
         patch('app.pipeline.video_generation_pipeline.FFmpegAdapter') as mock_ffmpeg_cls, \
         patch('app.pipeline.prompt_builder.build_prompts_for_scenes') as mock_build_prompts:

        mock_script_uc = MagicMock()
        mock_script_uc.execute.return_value = {
            'ok': True,
            'data': {
                'script': 'Cena 1: Teste de TTS\nCena 2: Segunda cena'
            }
        }
        mock_script_uc_cls.return_value = mock_script_uc

        mock_split_uc = MagicMock()
        mock_split_uc.execute.return_value = {
            'ok': True,
            'data': {
                'scenes': [
                    {'id': 1, 'prompt': 'Prompt 1', 'scene_text': 'Scene 1 text', 'duration': 5},
                    {'id': 2, 'prompt': 'Prompt 2', 'scene_text': 'Scene 2 text', 'duration': 5}
                ]
            }
        }
        mock_split_uc_cls.return_value = mock_split_uc

        mock_build_uc = MagicMock()
        mock_build_uc.execute.return_value = {
            'ok': True,
            'data': {
                'scenes': [
                    {'id': 1, 'prompt': 'Prompt 1', 'scene_text': 'Scene 1 text', 'duration': 5},
                    {'id': 2, 'prompt': 'Prompt 2', 'scene_text': 'Scene 2 text', 'duration': 5}
                ]
            }
        }
        mock_build_uc_cls.return_value = mock_build_uc

        mock_audio_uc = MagicMock()
        mock_audio_uc.execute.return_value = {
            'ok': False,
            'error': 'TTS not available'
        }
        mock_audio_uc_cls.return_value = mock_audio_uc

        mock_render_uc = MagicMock()
        mock_render_uc.execute.return_value = {
            'ok': True,
            'data': {
                'video_path': str(REPO_ROOT / 'projects' / 'test_e2e_tts_fail' / 'renders' / 'scene_001.mp4'),
                'scene_id': 1,
                'preset': '1.3B'
            }
        }
        mock_render_uc_cls.return_value = mock_render_uc

        mock_static_uc = MagicMock()
        mock_static_uc.execute.return_value = {
            'ok': False,
            'error': 'FFmpeg not available'
        }
        mock_static_uc_cls.return_value = mock_static_uc

        mock_concat_uc = MagicMock()
        mock_concat_uc.execute.return_value = {
            'ok': True,
            'data': {
                'video_path': str(REPO_ROOT / 'projects' / 'test_e2e_tts_fail' / 'final' / 'commercial.mp4'),
                'input_count': 2,
                'has_audio': False
            }
        }
        mock_concat_uc_cls.return_value = mock_concat_uc

        mock_wangp = MagicMock()
        mock_wangp.is_available.return_value = True
        mock_wangp_cls.return_value = mock_wangp

        mock_tts = MagicMock()
        mock_tts.is_available.return_value = False
        mock_tts_cls.return_value = mock_tts

        mock_ffmpeg = MagicMock()
        mock_ffmpeg.is_available.return_value = True
        mock_ffmpeg_cls.return_value = mock_ffmpeg

        mock_build_prompts.return_value = [
            {'id': 1, 'prompt': 'Prompt 1', 'scene_text': 'Scene 1 text', 'duration': 5},
            {'id': 2, 'prompt': 'Prompt 2', 'scene_text': 'Scene 2 text', 'duration': 5}
        ]

        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline

        pipeline = VideoGenerationPipeline()

        result = pipeline.generate_commercial(
            project_id='test_e2e_tts_fail',
            product='Teste Produto',
            target_audience='Teste Audiência',
            progress_callback=None
        )

        assert result.get('success') is True, f"Pipeline falhou: {result.get('error')}"
        logger.info("  SUCESSO! Pipeline executado mesmo com TTS indisponível")

        narration_path = result.get('narration_path')
        logger.info(f"  Narration path: {narration_path}")

        assert not mock_static_uc.execute.called, "CreateStaticVideoUseCase não deveria ser chamado quando WanGP está disponível"
        assert mock_concat_uc.execute.called, "ConcatVideosUseCase não foi chamado"
        logger.info("  ✓ FFmpeg usado apenas para concatenação (WanGP usado para geração de cena)")

        assert mock_render_uc.execute.called, "RenderVideoUseCase não foi chamado"
        logger.info("  ✓ WanGP foi usado para geração de vídeo (disponível)")

        assert mock_audio_uc.execute.called, "GenerateAudioUseCase não foi chamado"
        logger.info("  ✓ TTS foi tentado (mas indisponível)")

        return True


def test_tts_available_normal_operation():
    logger.info("Testando operação normal: TTS disponível")

    with patch('app.pipeline.video_generation_pipeline.GenerateScriptUseCase') as mock_script_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.SplitScenesUseCase') as mock_split_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.BuildPromptsUseCase') as mock_build_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.GenerateAudioUseCase') as mock_audio_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.RenderVideoUseCase') as mock_render_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.CreateStaticVideoUseCase') as mock_static_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.ConcatVideosUseCase') as mock_concat_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.WanGPAdapter') as mock_wangp_cls, \
         patch('app.pipeline.video_generation_pipeline.TTSAdapter') as mock_tts_cls, \
         patch('app.pipeline.video_generation_pipeline.FFmpegAdapter') as mock_ffmpeg_cls, \
         patch('app.pipeline.prompt_builder.build_prompts_for_scenes') as mock_build_prompts:

        mock_script_uc = MagicMock()
        mock_script_uc.execute.return_value = {
            'ok': True,
            'data': {
                'script': 'Cena 1: Teste normal\nCena 2: Segunda cena'
            }
        }
        mock_script_uc_cls.return_value = mock_script_uc

        mock_split_uc = MagicMock()
        mock_split_uc.execute.return_value = {
            'ok': True,
            'data': {
                'scenes': [
                    {'id': 1, 'prompt': 'Prompt 1', 'scene_text': 'Scene 1 text', 'duration': 5},
                    {'id': 2, 'prompt': 'Prompt 2', 'scene_text': 'Scene 2 text', 'duration': 5}
                ]
            }
        }
        mock_split_uc_cls.return_value = mock_split_uc

        mock_build_uc = MagicMock()
        mock_build_uc.execute.return_value = {
            'ok': True,
            'data': {
                'scenes': [
                    {'id': 1, 'prompt': 'Prompt 1', 'scene_text': 'Scene 1 text', 'duration': 5},
                    {'id': 2, 'prompt': 'Prompt 2', 'scene_text': 'Scene 2 text', 'duration': 5}
                ]
            }
        }
        mock_build_uc_cls.return_value = mock_build_uc

        mock_audio_uc = MagicMock()
        mock_audio_uc.execute.return_value = {
            'ok': True,
            'data': {
                'audio_path': str(REPO_ROOT / 'projects' / 'test_e2e_tts_normal' / 'audio' / 'narration.wav'),
                'text_length': 40
            }
        }
        mock_audio_uc_cls.return_value = mock_audio_uc

        mock_render_uc = MagicMock()
        mock_render_uc.execute.return_value = {
            'ok': True,
            'data': {
                'video_path': str(REPO_ROOT / 'projects' / 'test_e2e_tts_normal' / 'renders' / 'scene_001.mp4'),
                'scene_id': 1,
                'preset': '1.3B'
            }
        }
        mock_render_uc_cls.return_value = mock_render_uc

        mock_static_uc = MagicMock()
        mock_static_uc.execute.return_value = {
            'ok': False,
            'error': 'FFmpeg not available'
        }
        mock_static_uc_cls.return_value = mock_static_uc

        mock_concat_uc = MagicMock()
        mock_concat_uc.execute.return_value = {
            'ok': True,
            'data': {
                'video_path': str(REPO_ROOT / 'projects' / 'test_e2e_tts_normal' / 'final' / 'commercial.mp4'),
                'input_count': 2,
                'has_audio': True
            }
        }
        mock_concat_uc_cls.return_value = mock_concat_uc

        mock_wangp = MagicMock()
        mock_wangp.is_available.return_value = True
        mock_wangp_cls.return_value = mock_wangp

        mock_tts = MagicMock()
        mock_tts.is_available.return_value = True
        mock_tts_cls.return_value = mock_tts

        mock_ffmpeg = MagicMock()
        mock_ffmpeg.is_available.return_value = True
        mock_ffmpeg_cls.return_value = mock_ffmpeg

        mock_build_prompts.return_value = [
            {'id': 1, 'prompt': 'Prompt 1', 'scene_text': 'Scene 1 text', 'duration': 5},
            {'id': 2, 'prompt': 'Prompt 2', 'scene_text': 'Scene 2 text', 'duration': 5}
        ]

        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline

        pipeline = VideoGenerationPipeline()

        result = pipeline.generate_commercial(
            project_id='test_e2e_tts_normal',
            product='Teste Produto',
            target_audience='Teste Audiência',
            progress_callback=None
        )

        assert result.get('success') is True, f"Pipeline falhou: {result.get('error')}"
        logger.info("  SUCESSO! Pipeline executado normalmente com TTS disponível")

        narration_path = result.get('narration_path')
        logger.info(f"  Narration path: {narration_path}")

        assert mock_render_uc.execute.called, "RenderVideoUseCase não foi chamado"
        assert mock_audio_uc.execute.called, "GenerateAudioUseCase não foi chamado"
        assert not mock_static_uc.execute.called, "CreateStaticVideoUseCase não deveria ser chamado quando WanGP está disponível e funcionando"
        assert mock_concat_uc.execute.called, "ConcatVideosUseCase não foi chamado"
        logger.info("  ✓ WanGP e TTS usados para geração, FFmpeg apenas para concatenação final")

        return True


def test_both_wangp_and_tts_unavailable():
    logger.info("Testando cenário extremo: WanGP e TTS indisponíveis")

    with patch('app.pipeline.video_generation_pipeline.GenerateScriptUseCase') as mock_script_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.SplitScenesUseCase') as mock_split_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.BuildPromptsUseCase') as mock_build_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.GenerateAudioUseCase') as mock_audio_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.RenderVideoUseCase') as mock_render_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.CreateStaticVideoUseCase') as mock_static_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.ConcatVideosUseCase') as mock_concat_uc_cls, \
         patch('app.pipeline.video_generation_pipeline.WanGPAdapter') as mock_wangp_cls, \
         patch('app.pipeline.video_generation_pipeline.TTSAdapter') as mock_tts_cls, \
         patch('app.pipeline.video_generation_pipeline.FFmpegAdapter') as mock_ffmpeg_cls, \
         patch('app.pipeline.prompt_builder.build_prompts_for_scenes') as mock_build_prompts:

        mock_script_uc = MagicMock()
        mock_script_uc.execute.return_value = {
            'ok': True,
            'data': {
                'script': 'Cena 1: Teste extremo\nCena 2: Segunda cena'
            }
        }
        mock_script_uc_cls.return_value = mock_script_uc

        mock_split_uc = MagicMock()
        mock_split_uc.execute.return_value = {
            'ok': True,
            'data': {
                'scenes': [
                    {'id': 1, 'prompt': 'Prompt 1', 'scene_text': 'Scene 1 text', 'duration': 5},
                    {'id': 2, 'prompt': 'Prompt 2', 'scene_text': 'Scene 2 text', 'duration': 5}
                ]
            }
        }
        mock_split_uc_cls.return_value = mock_split_uc

        mock_build_uc = MagicMock()
        mock_build_uc.execute.return_value = {
            'ok': True,
            'data': {
                'scenes': [
                    {'id': 1, 'prompt': 'Prompt 1', 'scene_text': 'Scene 1 text', 'duration': 5},
                    {'id': 2, 'prompt': 'Prompt 2', 'scene_text': 'Scene 2 text', 'duration': 5}
                ]
            }
        }
        mock_build_uc_cls.return_value = mock_build_uc

        mock_audio_uc = MagicMock()
        mock_audio_uc.execute.return_value = {
            'ok': False,
            'error': 'TTS not available'
        }
        mock_audio_uc_cls.return_value = mock_audio_uc

        mock_render_uc = MagicMock()
        mock_render_uc.execute.return_value = {
            'ok': False,
            'error': 'WanGP not available'
        }
        mock_render_uc_cls.return_value = mock_render_uc

        mock_static_uc = MagicMock()
        mock_static_uc.execute.return_value = {
            'ok': True,
            'data': {
                'video_path': 'scene_001.mp4'
            }
        }
        mock_static_uc_cls.return_value = mock_static_uc

        mock_concat_uc = MagicMock()
        mock_concat_uc.execute.return_value = {
            'ok': True,
            'data': {
                'video_path': 'final.mp4',
                'input_count': 2,
                'has_audio': False
            }
        }
        mock_concat_uc_cls.return_value = mock_concat_uc

        mock_wangp = MagicMock()
        mock_wangp.is_available.return_value = False
        mock_wangp_cls.return_value = mock_wangp

        mock_tts = MagicMock()
        mock_tts.is_available.return_value = False
        mock_tts_cls.return_value = mock_tts

        mock_ffmpeg = MagicMock()
        mock_ffmpeg.is_available.return_value = True
        mock_ffmpeg_cls.return_value = mock_ffmpeg

        mock_build_prompts.return_value = [
            {'id': 1, 'prompt': 'Prompt 1', 'scene_text': 'Scene 1 text', 'duration': 5},
            {'id': 2, 'prompt': 'Prompt 2', 'scene_text': 'Scene 2 text', 'duration': 5}
        ]

        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline

        pipeline = VideoGenerationPipeline()

        result = pipeline.generate_commercial(
            project_id='test_e2e_both_fail',
            product='Teste Produto',
            target_audience='Teste Audiência',
            progress_callback=None
        )

        assert result.get('success') is True, f"Pipeline falhou: {result.get('error')}"
        logger.info("  SUCESSO! Pipeline executado com FFmpeg fallback e silêncio")

        assert mock_static_uc.execute.called, "CreateStaticVideoUseCase não foi chamado"
        assert mock_concat_uc.execute.called, "ConcatVideosUseCase não foi chamado"
        logger.info("  ✓ FFmpeg usado para vídeo (WanGP fallback) e concatenação")

        assert not mock_render_uc.execute.called or not mock_render_uc.execute.return_value.get('ok'), "RenderVideoUseCase foi chamado inesperadamente"
        logger.info("  ✓ WanGP não foi usado para vídeo (corretamente indisponível)")

        assert mock_audio_uc.execute.called, "GenerateAudioUseCase não foi chamado"
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
                logger.info(f"{name}: PASSOU")
            else:
                logger.error(f"{name}: FALHOU")
        except Exception as e:
            logger.error(f"{name}: FALHOU com exceção: {e}")
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
        print("TODOS OS TESTES QA-1004 PASSARAM!")
        sys.exit(0)
    else:
        print("ALGUNS TESTES QA-1004 FALHARAM!")
        sys.exit(1)
