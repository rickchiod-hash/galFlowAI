@echo off
echo Baixando KoboldCpp para K:...
echo.

set KOBOLDDIR=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\llm_engines\koboldcpp
set GGUFDIR=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\models\gguf

if not exist "%KOBOLDDIR%" mkdir "%KOBOLDDIR%"

echo.
echo Baixe o KoboldCpp de: https://github.com/LostRuins/KoboldCpp/releases
echo Procure por: koboldcpp.exe (versao Windows)
echo.
echo Salve o executavel em: %KOBOLDDIR%
echo.
echo ===============================================
echo  MODELOS GGUF NECESSARIOS
echo ===============================================
echo Crie a pasta: %GGUFDIR%
echo Baixe um modelo leve (ex: Llama 3.2 3B Q4) e salve em: %GGUFDIR%
echo.
echo Modelos recomendados (leves para 6GB VRAM):
echo  - Llama 3.2 3B Q4 (2GB)
echo  - Phi-3 mini Q4 (2GB)
echo  - Gemma 2 2B Q4 (1.5GB)
echo.
echo Link: https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads
echo (Procure por modelos GGUF)
echo.
echo Pressione qualquer tecla para sair...
pause >nul
