@echo off
REM FlowForgeAI - Start with ALL required environment variables (AGENTS.md compliant)
echo Iniciando FlowForgeAI com configuracao padrao K:...

REM Configurar variaveis obrigatorias
set PIP_CACHE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip
set HF_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\huggingface
set TORCH_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\torch
set XDG_CACHE_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache
set TEMP=K:\AI_VIDEO_COMERCIAL_STUDIO\temp
set TMP=K:\AI_VIDEO_COMERCIAL_STUDIO\temp
set OLLAMA_MODELS=K:\AI_VIDEO_COMERCIAL_STUDIO\models\ollama
set GIT_PYTHON_GIT_EXECUTABLE=K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Library\bin\git.exe

REM Verificar se estamos no diretorio correto
cd /d K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta

REM Ativar ambiente virtual
call K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\activate.bat

REM Iniciar Gradio UI
echo.
echo FlowForgeAI - Gradio UI
echo Acesse: http://127.0.0.1:7860
echo.
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe app/main.py

pause
