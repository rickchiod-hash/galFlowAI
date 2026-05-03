@echo off
echo ===============================================
echo  EXEMPLO: INICIAR LLAMA.CPP
echo ===============================================
echo.

set GGUFDIR=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\models\gguf

REM Verificar se tem llama.cpp Python ou executavel
pip show llama-cpp-python >nul 2>&1
if errorlevel 1 (
    echo [!] llama-cpp-python nao instalado.
    echo Execute: pip install llama-cpp-python
    pause
    exit /b 1
)

REM Procurar modelo GGUF
dir /b "%GGUFDIR%\*.gguf" 2>nul
if errorlevel 1 (
    echo [X] Nenhum modelo GGUF encontrado em: %GGUFDIR%
    pause
    exit /b 1
)

echo [OK] Modelos encontrados. Iniciando servidor...
echo.
echo Servidor sera iniciado em: http://localhost:8080
echo.
echo Teste: curl http://localhost:8080/v1/models
echo.

python -m llama_cpp.server --model "%GGUFDIR%\*.gguf" --port 8080 --n_ctx 2048
