@echo off
setlocal EnableDelayedExpansion

REM Configurar variaveis de ambiente
set PIP_CACHE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip
set HF_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\huggingface
set TORCH_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\torch
set XDG_CACHE_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache
set TEMP=K:\AI_VIDEO_COMERCIAL_STUDIO\temp
set TMP=K:\AI_VIDEO_COMERCIAL_STUDIO\temp
set OLLAMA_MODELS=K:\AI_VIDEO_COMERCIAL_STUDIO\models\ollama
set GIT_PYTHON_GIT_EXECUTABLE=K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Library\bin\git.exe

REM Mudar para o diretorio do projeto
cd /d K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta

REM Iniciar galFlowAI e salvar logs
echo Iniciando galFlowAI em http://127.0.0.1:7860 > logs\galFlowAI.log 2>&1
echo Data: %date% %time% >> logs\galFlowAI.log 2>&1

"K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\python.exe" "K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\run_galFlowAI.py" >> logs\galFlowAI.log 2>&1

pause
