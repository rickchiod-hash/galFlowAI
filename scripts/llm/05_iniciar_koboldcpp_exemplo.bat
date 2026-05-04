@echo off
echo ===============================================
echo  EXEMPLO: INICIAR KOBOLDCPP
echo ===============================================
echo.

set KOBOLDDIR=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\llm_engines\koboldcpp
set GGUFDIR=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\models\gguf
set EXE=%KOBOLDDIR%\koboldcpp.exe

if not exist "%EXE%" (
    echo [X] KoboldCpp nao encontrado em: %EXE%
    echo.
    echo Execute primeiro: scripts\llm\03_baixar_koboldcpp_k.bat
    pause
    exit /b 1
)

REM Procurar modelo GGUF
dir /b "%GGUFDIR%\*.gguf" 2>nul
if errorlevel 1 (
    echo [X] Nenhum modelo GGUF encontrado em: %GGUFDIR%
    echo.
    echo Baixe um modelo leve e coloque nesta pasta.
    pause
    exit /b 1
)

echo [OK] Modelos encontrados. Iniciando servidor...
echo.
echo Servidor sera iniciado em: http://localhost:5001
echo Deixe esta janela aberta!
echo.
echo Teste em outra janela: curl http://localhost:5001/api/v1/models
echo.

%EXE% --model "%GGUFDIR%\*.gguf" --port 5001 --threads 6
