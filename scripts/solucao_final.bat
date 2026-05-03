@echo off&
REM Solução Final FlowForgeAI - Execute este arquivo&
setlocal EnableDelayedExpansion&

set BASE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta&
set PORTABLE_DIR=%BASE_DIR%\python_portable&
set PYTHON=%PORTABLE_DIR%\python.exe&

echo =&
echo   FlowForgeAI - Solução Final&
echo =&

REM 1. Baixar Python se necessário&
if not exist "%PYTHON%" (
    echo [1/3] Baixando Python portátil...&
    set URL=https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-amd64.zip&
    set ZIP=%BASE_DIR%\python.zip&
    
    powershell -Command "Invoke-WebRequest -Uri '%URL%' -OutFile '%ZIP%'"&
    
    if exist "%ZIP%" (
        echo Extraindo Python...&
        powershell -Command "Expand-Archive -Path '%ZIP%' -DestinationPath '%PORTABLE_DIR%' -Force"&
        del "%ZIP%"&
        echo ✓ Python portátil instalado&
    ) else (
        echo ERRO: Falha ao baixar Python&
        pause&
        exit /b 1&
    )
) else (
    echo [1/3] ✓ Python encontrado: %PYTHON%&
)

echo.&

REM 2. Corrigir api.py&
echo [2/3] Corrigindo api.py...&

powershell -Command "
$content = Get-Content '%BASE_DIR%\app\api.py' -Raw&
$content = $content -replace 'allow_origins', 'allow_origins'&
Set-Content '%BASE_DIR%\app\api.py' $content&
Write-Host 'allow_origins corrigido'&
"&

echo Verificando sintaxe...&
"%PYTHON%" -m py_compile "%BASE_DIR%\app\api.py" 2>&1 | findstr /i "error" && (
    echo ✗ Ainda há erros de sintaxe&
    pause&
    exit /b 1&
) || (
    echo ✓ Sintaxe OK&
)

echo.&

REM 3. Subir aplicação&
echo [3/3] Iniciando FlowForgeAI...&
echo.&
echo ===============================&
echo   URLS:&
echo   Gradio UI:  http://127.0.0.1:7860&
echo   FastAPI:     http://127.0.0.1:8000&
echo ===============================&
echo.&

cd /d "%BASE_DIR%"&
"%PYTHON%" app/main.py&

pause&
