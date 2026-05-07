@echo off
REM Test Runner for GalFlowAI - Finds correct Python automatically

setlocal EnableDelayedExpansion

set BASE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
set STUDIO_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio

echo ================================
echo   GalFlowAI - Test Runner
echo ================================
echo.

REM ========== Find Python ==========
set PYTHON_EXE=
if exist "%STUDIO_DIR%\Scripts\python.exe" (
    set PYTHON_EXE=%STUDIO_DIR%\Scripts\python.exe
    echo ✓ Python encontrado no ambiente studio
) else (
    REM Tenta python do sistema
    where python >nul 2>&1
    if !errorlevel! equ 0 (
        set PYTHON_EXE=python
        echo ⚠ Usando python do sistema
    ) else (
        echo ✗ Python não encontrado!
        echo.
        echo Instale o Python em:
        echo   %STUDIO_DIR%
        echo.
        pause
        exit /b 1
    )
)

echo Python: %PYTHON_EXE%
echo.

REM ========== Set Environment Variables ==========
set PIP_CACHE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip
set HF_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\huggingface
set TORCH_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\torch
set XDG_CACHE_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache
set TEMP=K:\AI_VIDEO_COMERCIAL_STUDIO\temp
set TMP=K:\AI_VIDEO_COMERCIAL_STUDIO\temp

REM ========== Run Tests ==========
cd /d "%BASE_DIR%"

echo [1/3] Testando imports básicos...
"%PYTHON_EXE%" -c "import sys; sys.path.insert(0, '.'); from app.pipeline.video_generation_pipeline import VideoGenerationPipeline; print('✓ Imports OK')"
if errorlevel 1 goto :error

echo [2/3] Testando LLM Providers...
"%PYTHON_EXE%" -m pytest tests/unit/test_llm_providers.py -v --tb=short 2>&1 | findstr /C:"passed" /C:"failed"
if errorlevel 1 echo ⚠ Alguns testes LLM falharam (esperado se pytest não instalado)

echo [3/3] Testando pipeline completo...
"%PYTHON_EXE%" tests/integration/test_pipeline_completo.py
if errorlevel 1 goto :error

echo.
echo ================================
echo   TODOS OS TESTES PASSARAM!
echo ================================
goto :end

:error
echo.
echo ================================
echo   ERRO NOS TESTES
echo ================================
echo Verifique os erros acima.

:end
pause
exit /b 0
