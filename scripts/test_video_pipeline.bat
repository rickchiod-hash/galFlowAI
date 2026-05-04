@echo off
REM Testa pipeline de geração de vídeo FlowForgeAI

setlocal EnableDelayedExpansion

set BASE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
set PYTHON_EXE=python

echo ================================
echo   TESTE: PIPELINE VIDEO
echo ================================
echo.

cd /d "%BASE_DIR%"

echo [1/5] Verificando imports...
"%PYTHON_EXE%" -c "from app.pipeline.video_generation_pipeline import VideoGenerationPipeline; print('OK: VideoGenerationPipeline')"
if errorlevel 1 goto :error

echo [2/5] Verificando WanGP adapter...
"%PYTHON_EXE%" -c "from app.adapters.wangp_adapter import WanGPAdapter; w = WanGPAdapter(); print(f'WanGP disponivel: {w.is_available()}')"
if errorlevel 1 goto :error

echo [3/5] Verificando TTS adapter...
"%PYTHON_EXE%" -c "from app.adapters.tts_adapter import TTSAdapter; t = TTSAdapter(); print(f'TTS motor: {t.selected_engine}')"
if errorlevel 1 goto :error

echo [4/5] Verificando FFmpeg adapter...
"%PYTHON_EXE%" -c "from app.adapters.ffmpeg_adapter import FFmpegAdapter; f = FFmpegAdapter(); print(f'FFmpeg disponivel: {f.is_available()}')"
if errorlevel 1 goto :error

echo [5/5] Testando criação de pipeline...
"%PYTHON_EXE%" -c "from app.pipeline.video_generation_pipeline import VideoGenerationPipeline; p = VideoGenerationPipeline(); status = p.get_pipeline_status(); print('Pipeline status:'); import json; print(json.dumps(status, indent=2))"
if errorlevel 1 goto :error

echo.
echo ================================
echo   TODOS OS TESTES PASSARAM!
echo ================================
goto :end

:error
echo.
echo ================================
echo   ERRO NO TESTE
echo ================================
echo Verifique os erros acima.
pause
exit /b 1

:end
pause
exit /b 0
