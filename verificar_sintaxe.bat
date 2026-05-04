@echo off
echo ===================================
echo  VERIFICADOR DE SINTAXE - galFlowAI
echo ===================================
echo.

set PYTHON=K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\python.exe
set PROJECT=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta

echo Verificando Python...
if not exist "%PYTHON%" (
    echo [ERRO] Python nao encontrado: %PYTHON%
    pause
    exit /b 1
)
echo [OK] Python encontrado.
echo.

echo Verificando arquivos...
set ERROR=0

call :check_file "%PROJECT%\app\main.py"
call :check_file "%PROJECT%\app\hardware.py"
call :check_file "%PROJECT%\app\project_manager.py"
call :check_file "%PROJECT%\app\config.py"
call :check_file "%PROJECT%\app\logging_config.py"
call :check_file "%PROJECT%\app\pipeline\script_generator.py"
call :check_file "%PROJECT%\app\pipeline\scene_splitter.py"
call :check_file "%PROJECT%\app\adapters\ffmpeg_adapter.py"
call :check_file "%PROJECT%\app\adapters\tts_adapter.py"
call :check_file "%PROJECT%\app\adapters\wangp_adapter.py"

echo.
if %ERROR% NEQ 0 (
    echo [AVISO] Alguns arquivos tem erros de sintaxe.
) else (
    echo [SUCESSO] Todos os arquivos tem sintaxe correta!
)
echo.
pause
exit /b %ERROR%

:check_file
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
