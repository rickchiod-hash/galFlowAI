@echo off
echo ===================================
echo  TESTE DO PIPELINE DE VIDEO - galFlowAI
echo ===================================
echo.

set PYTHON=K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\python.exe
set PROJECT=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta

echo Verificando Python...
if not exist "%PYTHON%" (
    echo [ERRO] Python nao encontrado em:
    echo %PYTHON%
    pause
    exit /b 1
)
echo [OK] Python encontrado.

echo.
echo Executando teste do pipeline...
cd /d "%PROJECT%"
"%PYTHON%" test_video_pipeline.py

echo.
echo ===================================
echo  TESTE CONCLUIDO
echo ===================================
echo Verifique os logs em:
echo %PROJECT%\projects\*\logs\
echo.
pause
