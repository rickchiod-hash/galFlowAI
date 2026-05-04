@echo off
REM FlowForgeAI - Inicialização Direta (sem Microsoft Store)
REM Este script não usa a palavra "python" diretamente para evitar o redirecionamento

setlocal EnableDelayedExpansion

set BASE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
set STUDIO_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio

echo ================================
echo   FlowForgeAI - Inicialização
echo ================================
echo.

REM ========== Encontrar Python (evitando Microsoft Store) ==========
set PYTHON_EXE=

REM 1. Tenta ambiente studio primeiro
if exist "%STUDIO_DIR%\Scripts\python.exe" (
    set PYTHON_EXE=%STUDIO_DIR%\Scripts\python.exe
    echo ✓ Python encontrado: %PYTHON_EXE%
    goto :found_python
)

REM 2. Procura python.exe no PATH (que não seja da Microsoft Store)
for /f "delims=" %%i in ('where python 2^>nul') do (
    echo %%i | findstr /i "WindowsApps" >nul
    if errorlevel 1 (
        set PYTHON_EXE=%%i
        echo ✓ Python encontrado: !PYTHON_EXE!
        goto :found_python
    )
)

echo ✗ Python não encontrado!
echo Instale Python em: %STUDIO_DIR%
pause
exit /b 1

:found_python
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

REM ========== Criar diretórios ==========
if not exist "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip" mkdir "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip"
if not exist "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\huggingface" mkdir "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\huggingface"
if not exist "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\torch" mkdir "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\torch"
if not exist "K:\AI_VIDEO_COMERCIAL_STUDIO\temp" mkdir "K:\AI_VIDEO_COMERCIAL_STUDIO\temp"
if not exist "%BASE_DIR%\projects" mkdir "%BASE_DIR%\projects"

REM ========== Corrigir sintaxe dos arquivos ==========
echo [1/3] Corrigindo erros de sintaxe...
cd /d "%BASE_DIR%"

REM Corrigir api.py
powershell -Command "(Get-Content 'app\api.py') -replace '; ', ', ' | Set-Content 'app\api.py'"

REM Corrigir main.py se necessário
powershell -Command "(Get-Content 'app\main.py') -replace '; ', ', ' | Set-Content 'app\main.py'"

echo ✓ Arquivos corrigidos
echo.

REM ========== Verificar sintaxe ==========
echo [2/3] Verificando sintaxe Python...
"%PYTHON_EXE%" -m py_compile "app\api.py" 2>&1 | findstr /i "error" && (
    echo ✗ Erro de sintaxe em api.py
    pause
    exit /b 1
)

"%PYTHON_EXE%" -m py_compile "app\main.py" 2>&1 | findstr /i "error" && (
    echo ✗ Erro de sintaxe em main.py
    pause
    exit /b 1
)

echo ✓ Sintaxe OK
echo.

REM ========== Subir Aplicação ==========
echo [3/3] Iniciando FlowForgeAI...
echo.
echo ================================
echo   ACESSO:
echo   Gradio UI: http://127.0.0.1:7860
echo   FastAPI:    http://127.0.0.1:8000
echo   Docs API:   http://127.0.0.1:8000/docs
echo ================================
echo.

REM Inicia Gradio UI
"%PYTHON_EXE%" app/main.py

pause
