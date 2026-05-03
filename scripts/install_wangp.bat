@echo off
REM Instala e configura WanGP para FlowForgeAI
REM Destinado para GTX 1660 Super (6GB VRAM) - Modelo 1.3B apenas

setlocal EnableDelayedExpansion

set BASE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO
set ENGINES_DIR=%BASE_DIR%\engines
set WAN_GP_DIR=%ENGINES_DIR%\Wan2GP
set MODELS_DIR=%BASE_DIR%\models\wan
set STUDIO_ENV=%BASE_DIR%\envs\studio

echo ================================
echo   INSTALAR WAN2GP - FlowForgeAI
echo   GTX 1660 Super (6GB VRAM)
echo ================================
echo.

REM ========== Criar diretórios ==========
if not exist "%ENGINES_DIR%" mkdir "%ENGINES_DIR%"
if not exist "%MODELS_DIR%" mkdir "%MODELS_DIR%"

REM ========== Verificar Git ==========
where git >nul 2>&1
if errorlevel 1 (
    echo ✗ Git não encontrado! Instale o Git primeiro.
    pause
    exit /b 1
)
echo ✓ Git encontrado

REM ========== Clonar Wan2GP ==========
echo.
echo [1/4] Clonando Wan2GP...
if exist "%WAN_GP_DIR%" (
    echo Wan2GP já existe. Atualizando...
    cd /d "%WAN_GP_DIR%"
    git pull
) else (
    cd /d "%ENGINES_DIR%"
    git clone https://github.com/deepbeepmeep/Wan2GP.git
)

if not exist "%WAN_GP_DIR%" (
    echo ✗ Falha ao clonar Wan2GP
    pause
    exit /b 1
)
echo ✓ Wan2GP clonado

REM ========== Instalar dependências ==========
echo.
echo [2/4] Instalando dependências...
cd /d "%WAN_GP_DIR%"

REM Usa Python do ambiente studio se existir
set PYTHON_EXE=python
if exist "%STUDIO_ENV%\Scripts\python.exe" (
    set PYTHON_EXE=%STUDIO_ENV%\Scripts\python.exe
    echo Usando Python do ambiente studio
)

REM Atualiza pip
"%PYTHON_EXE%" -m pip install --upgrade pip

REM Instala requirements
if exist "requirements.txt" (
    "%PYTHON_EXE%" -m pip install -r requirements.txt
) else (
    echo ⚠ requirements.txt não encontrado, instalando deps básicas...
    "%PYTHON_EXE%" -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    "%PYTHON_EXE%" -m pip install gradio transformers accelerate diffusers pillow numpy
)

echo ✓ Dependências instaladas

REM ========== Baixar modelo 1.3B ==========
echo.
echo [3/4] Modelo 1.3B será baixado no primeiro uso...
echo O Wan2GP baixa automaticamente os modelos necessários.
echo Modelo 1.3B é ideal para GTX 1660 Super (6GB VRAM).
echo.

REM ========== Testar instalação ==========
echo [4/4] Testando instalação...
cd /d "%WAN_GP_DIR%"

REM Verifica se arquivos principais existem
if exist "main.py" (
    echo ✓ main.py encontrado
) else if exist "gradio.py" (
    echo ✓ gradio.py encontrado
) else (
    echo ⚠ Arquivo principal não encontrado
)

echo.
echo ================================
echo   INSTALAÇÃO CONCLUÍDA!
echo ================================
echo.
echo Próximos passos:
echo 1. Execute: scripts\test_wangp_integration.bat
echo 2. Inicie FlowForgeAI: scripts\start_app_debug.bat
echo 3. Acesse: http://127.0.0.1:7860
echo 4. Na tab "Gerar Vídeo", o sistema usará WanGP automaticamente se disponível.
echo.
echo Dica: Para testar WanGP isolado:
echo   cd %WAN_GP_DIR%
echo   %PYTHON_EXE% main.py
echo.

pause
exit /b 0
