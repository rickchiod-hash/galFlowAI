@echo off
echo Instalando GPT4All SDK no ambiente do projeto...
echo.

set ENVS=K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\python.exe
set MODELDIR=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\models\gpt4all

%ENVS% -m pip install gpt4all --no-cache-dir

if exist "%MODELDIR%" (
    echo.
    echo Pasta de modelos ja existe: %MODELDIR%
) else (
    mkdir "%MODELDIR%"
    echo.
    echo Criada pasta para modelos: %MODELDIR%
)

echo.
echo ===============================================
echo  MODELOS NECESSARIOS
echo ===============================================
echo Baixe um modelo GGUF leve e salve em: %MODELDIR%
echo.
echo Modelos recomendados (leves para 6GB VRAM):
echo  - orca-mini-3.7-8b-gguf (Q4)
echo  - gpt4all-falcon-newbpe-q4 (2GB)
echo.
echo Link: https://gpt4all.io/index.html
echo (Va em "Download models")
echo.
echo Pressione qualquer tecla para sair...
pause >nul
