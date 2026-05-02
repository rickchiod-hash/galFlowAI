@echo off
REM galFlowAI Launcher - Versao simples
cd /d K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta

REM Configurar ambiente
set PIP_CACHE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip
set HF_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\huggingface
set TORCH_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\torch
set XDG_CACHE_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache
set TEMP=K:\AI_VIDEO_COMERCIAL_STUDIO\temp
set TMP=K:\AI_VIDEO_COMERCIAL_STUDIO\temp

echo Iniciando galFlowAI...
echo Servidor estara disponivel em http://127.0.0.1:7860
echo.

REM Executar com Python do caminho correto (double L)
"K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\python.exe" run_galFlowAI.py
