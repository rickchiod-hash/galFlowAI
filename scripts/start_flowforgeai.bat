@echo off
REM FlowForgeAI - Corrigir, Configurar e Subir Aplicação
setlocal EnableDelayedExpansion

set BASE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
set STUDIO_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio

echo ================================
echo   FlowForgeAI - Inicialização
echo ================================
echo.

REM ========== Encontrar Python ==========
set PYTHON_EXE=
if exist "%STUDIO_DIR%\Scripts\python.exe" (
    set PYTHON_EXE=%STUDIO_DIR%\Scripts\python.exe
    echo ✓ Python encontrado no ambiente studio
) else (
    echo Procurando Python...
    for /f "delims=" %%i in ('where python 2^>nul') do (
        if exist "%%i" set PYTHON_EXE=%%i
    )
    if "!PYTHON_EXE!"=="" (
        echo ✗ Python não encontrado!
        pause
        exit /b 1
    )
    echo ✓ Python encontrado: !PYTHON_EXE!
)

echo.

REM ========== Configurar Variáveis de Ambiente ==========
set PIP_CACHE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip
set HF_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\huggingface
set TORCH_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\torch
set XDG_CACHE_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache
set TEMP=K:\AI_VIDEO_COMERCIAL_STUDIO\temp
set TMP=K:\AI_VIDEO_COMERCIAL_STUDIO\temp
set OLLAMA_MODELS=K:\AI_VIDEO_COMERCIAL_STUDIO\models\ollama
set GIT_PYTHON_GIT_EXECUTABLE=K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Library\bin\git.exe

echo Variáveis de ambiente configuradas.
echo.

REM ========== Criar diretórios necessários ==========
if not exist "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip" mkdir "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip"
if not exist "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\huggingface" mkdir "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\huggingface"
if not exist "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\torch" mkdir "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\torch"
if not exist "K:\AI_VIDEO_COMERCIAL_STUDIO\temp" mkdir "K:\AI_VIDEO_COMERCIAL_STUDIO\temp"
if not exist "K:\AI_VIDEO_COMERCIAL_STUDIO\models\ollama" mkdir "K:\AI_VIDEO_COMERCIAL_STUDIO\models\ollama"
if not exist "%BASE_DIR%\projects" mkdir "%BASE_DIR%\projects"

REM ========== Corrigir erros de sintaxe ==========
echo [1/4] Corrigindo erros de sintaxe...
cd /d "%BASE_DIR%"

REM Corrigir api.py - trocar ; por , em dicionários
powershell -Command "(Get-Content 'app\api.py') -replace '; ', ', ' -replace ';}', '}' | Set-Content 'app\api.py'"

REM Verificar se main.py tem erros similares
powershell -Command "(Get-Content 'app\main.py') -replace '; ', ', ' -replace ';}', '}' | Set-Content 'app\main.py'"

echo ✓ Arquivos corrigidos
echo.

REM ========== Verificar sintaxe ==========
echo [2/4] Verificando sintaxe Python...
"%PYTHON_EXE%" -m py_compile app/api.py 2>&1
if errorlevel 1 (
    echo ✗ Erro de sintaxe em api.py
    "%PYTHON_EXE%" -m py_compile app/api.py
    pause
    exit /b 1
)

"%PYTHON_EXE%" -m py_compile app/main.py 2>&1
if errorlevel 1 (
    echo ✗ Erro de sintaxe em main.py
    "%PYTHON_EXE%" -m py_compile app/main.py
    pause
    exit /b 1
)

echo ✓ Sintaxe OK
echo.

REM ========== Instalar dependências básicas se necessário ==========
echo [3/4] Verificando dependências...
"%PYTHON_EXE%" -c "import gradio, fastapi, uvicorn" 2>&1
if errorlevel 1 (
    echo Instalando dependências básicas...
    "%PYTHON_EXE%" -m pip install gradio fastapi uvicorn httpx pydantic
)

echo.

REM ========== Subir Aplicação ==========
echo [4/4] Iniciando FlowForgeAI...
echo.
echo ================================
echo   ACESSO:
echo   Gradio UI: http://127.0.0.1:7860
echo   FastAPI:    http://127.0.0.1:8000
echo   Docs API:   http://127.0.0.1:8000/docs
echo ================================
echo.

REM Inicia Gradio UI (padrão)
"%PYTHON_EXE%" app/main.py

pause
