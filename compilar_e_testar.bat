@echo off
echo ===================================
echo  COMPILANDO E TESTANDO - galFlowAI
echo ===================================
echo.

set PYTHON=K:\AI_VIDEO_COMMERCIAL_STUDIO\envs\studio\python.exe
set PROJECT=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta

echo 1. Verificando Python...
if not exist "%PYTHON%" (
    echo [ERRO] Python nao encontrado: %PYTHON%
    pause
    exit /b 1
)
echo    [OK] Python encontrado.
echo.

echo 2. Compilando arquivos Python...
set ERROR=0

call :compile_file "%PROJECT%\app\main.py"
call :compile_file "%PROJECT%\app\hardware.py"
call :compile_file "%PROJECT%\app\project_manager.py"
call :compile_file "%PROJECT%\app\config.py"
call :compile_file "%PROJECT%\app\logging_config.py"
call :compile_file "%PROJECT%\app\pipeline\script_generator.py"
call :compile_file "%PROJECT%\app\pipeline\scene_splitter.py"
call :compile_file "%PROJECT%\app\adapters\ffmpeg_adapter.py"
call :compile_file "%PROJECT%\app\adapters\tts_adapter.py"
call :compile_file "%PROJECT%\app\adapters\wangp_adapter.py"

echo.
if %ERROR% NEQ 0 (
    echo [AVISO] Alguns arquivos tem erros de sintaxe.
    echo Verifique os erros acima.
    pause
    exit /b 1
) else (
    echo [SUCESSO] Todos os arquivos compilados com sucesso!
)
echo.

echo 3. Executando teste do pipeline de video...
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
exit /b 0

:compile_file
set FILE=%~1
if not exist "%FILE%" (
    echo [NAO ENCONTRADO] %FILE%
    exit /b 1
)
"%PYTHON%" -m py_compile "%FILE%" 2>&1
if errorlevel 1 (
    echo [ERRO SINTAXE] %FILE%
    set /a ERROR+=1
) else (
    echo [OK] %FILE%
)
exit /b 0
