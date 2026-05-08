@echo off
REM GalFlowAI - Start Direct (avoiding Microsoft Store Python)

set BASE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
set STUDIO_PYTHON=K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe

echo ================================
echo   GalFlowAI - Inicializacao
echo ================================
echo.

REM verifica se Python do studio existe
if not exist "%STUDIO_PYTHON%" (
    echo ERRO: Python nao encontrado em:
    echo   %STUDIO_PYTHON%
    echo.
    echo Instale o ambiente studio primeiro.
    pause
    exit /b 1
)

echo ✓ Python encontrado: %STUDIO_PYTHON%
echo.

REM Configura variaveis de ambiente
set PIP_CACHE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip
set HF_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\huggingface
set TORCH_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\torch
set XDG_CACHE_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache
set TEMP=K:\AI_VIDEO_COMERCIAL_STUDIO\temp
set TMP=K:\AI_VIDEO_COMERCIAL_STUDIO\temp

echo Variaveis de ambiente configuradas.
echo.

REM Corrige sintaxe dos arquivos (troca ; por ,)
echo Corrigindo sintaxe em api.py e main.py...
cd /d "%BASE_DIR%"

REM Corrige api.py
powershell -Command "(Get-Content 'app\api.py') -replace '; ', ', ' | Set-Content 'app\api_backup.py'"
powershell -Command "(Get-Content 'app\api_backup.py') -replace ';}', '}' | Set-Content 'app\api.py'"
del "app\api_backup.py"

REM Corrige main.py se necessario
powershell -Command "(Get-Content 'app\main.py') -replace '; ', ', ' | Set-Content 'app\main.py'"

echo ✓ Sintaxe corrigida
echo.

REM Verifica sintaxe
echo Verificando sintaxe Python...
"%STUDIO_PYTHON%" -m py_compile "app\api.py" 2>&1
if errorlevel 1 (
    echo.
    echo ✗ Erro de sintaxe em api.py
    "%STUDIO_PYTHON%" -m py_compile "app\api.py"
    pause
    exit /b 1
)

"%STUDIO_PYTHON%" -m py_compile "app\main.py" 2>&1
if errorlevel 1 (
    echo.
    echo ✗ Erro de sintaxe em main.py
    "%STUDIO_PYTHON%" -m py_compile "app\main.py"
    pause
    exit /b 1
)

echo ✓ Sintaxe OK
echo.

REM Cria diretorios necessarios
if not exist "projects" mkdir projects
if not exist "K:\AI_VIDEO_COMERCIAL_STUDIO\temp" mkdir "K:\AI_VIDEO_COMERCIAL_STUDIO\temp"

echo ================================
echo   INICIANDO GalFlowAI
echo ================================
echo.
echo URLs de acesso:
echo   Gradio UI: http://127.0.0.1:7860
echo   FastAPI:   http://127.0.0.1:8000
echo   API Docs:  http://127.0.0.1:8000/docs
echo.
echo Pressione Ctrl+C para parar.
echo.

REM Inicia a aplicacao
"%STUDIO_PYTHON%" "app\main.py"

pause
