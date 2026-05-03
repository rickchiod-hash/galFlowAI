@echo off
echo ===============================================
echo  TESTAR PROVIDERS LLM
echo ===============================================
echo.

REM Testar LM Studio
echo [1/4] Testando LM Studio (localhost:1234)...
curl -s --connect-timeout 2 http://localhost:1234/v1/models >nul 2>&1
if not errorlevel 1 (
    echo [OK] LM Studio: ATIVO
) else (
    echo [X] LM Studio: Inativo
)

REM Testar KoboldCpp
echo [2/4] Testando KoboldCpp (localhost:5001)...
curl -s --connect-timeout 2 http://localhost:5001/api/v1/models >nul 2>&1
if not errorlevel 1 (
    echo [OK] KoboldCpp: ATIVO
) else (
    echo [X] KoboldCpp: Inativo
)

REM Testar Llama.cpp
echo [3/4] Testando Llama.cpp (localhost:8080)...
curl -s --connect-timeout 2 http://localhost:8080/v1/models >nul 2>&1
if not errorlevel 1 (
    echo [OK] Llama.cpp: ATIVO
) else (
    echo [X] Llama.cpp: Inativo
)

REM Testar GPT4All
echo [4/4] Testando GPT4All (Python package)...
K:/AI_VIDEO_COMERCIAL_STUDIO/envs/studio/python.exe -c "import gpt4all" >nul 2>&1
if not errorlevel 1 (
    echo [OK] GPT4All: INSTALADO
) else (
    echo [X] GPT4All: Nao instalado
)

echo.
echo [OK] TemplateProvider: SEMPRE DISPONIVEL (fallback)
echo.
echo Pressione qualquer tecla para sair...
pause >nul
