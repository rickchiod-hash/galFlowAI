@echo off
echo Detectando LLMs locais no K:...
echo.

REM Check LM Studio
curl -s http://localhost:1234/v1/models >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] LM Studio: ATIVO em http://localhost:1234
) else (
    echo [X] LM Studio: nao encontrado (instale em: K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\docs\INSTALAR_LM_STUDIO_K.md)
)

REM Check KoboldCpp
curl -s http://localhost:5001/api/v1/models >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] KoboldCpp: ATIVO em http://localhost:5001
) else (
    echo [X] KoboldCpp: nao encontrado (baixe para: K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\llm_engines\koboldcpp)
)

REM Check Llama.cpp
curl -s http://localhost:8080/v1/models >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Llama.cpp: ATIVO em http://localhost:8080
) else (
    echo [X] Llama.cpp: nao encontrado (veja: K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\docs\INSTALAR_LLAMACPP_K.md)
)

REM Check GPT4All
K:/AI_VIDEO_COMERCIAL_STUDIO/envs/studio/python.exe -c "import gpt4all" 2>nul
if %errorlevel% == 0 (
    echo [OK] GPT4All: INSTALADO
) else (
    echo [X] GPT4All: nao instalado (veja: K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\docs\INSTALAR_GPT4ALL_K.md)
)

echo.
echo [OK] TemplateProvider: SEMPRE DISPONIVEL (fallback)
echo.
echo Pressione qualquer tecla para sair...
pause >nul
