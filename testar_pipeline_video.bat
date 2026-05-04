@echo off
echo ===================================
echo  TESTE DO PIPELINE DE VIDEO
echo ===================================
echo.

set PYTHON=K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\python.exe
set PROJECT=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta

echo 1. Verificando Python...
if exist "%PYTHON%" (
    echo    [OK] Python encontrado
) else (
    echo    [ERRO] Python nao encontrado em:
    echo    %PYTHON%
    pause
    exit /b 1
)

echo.
echo 2. Executando teste do pipeline...
cd /d "%PROJECT%"
"%PYTHON%" test_video_pipeline.py
if errorlevel 1 (
    echo.
    echo [ERRO] Teste falhou. Verifique os erros acima.
) else (
    echo.
    echo [SUCESSO] Teste concluido!
)

echo.
echo ===================================
pause
