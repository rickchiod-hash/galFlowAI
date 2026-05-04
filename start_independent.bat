@echo off
cd /d K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta

set PIP_CACHE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip
set HF_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\huggingface
set TORCH_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\torch
set XDG_CACHE_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache
set TEMP=K:\AI_VIDEO_COMERCIAL_STUDIO\temp
set TMP=K:\AI_VIDEO_COMERCIAL_STUDIO\temp

echo Iniciando galFlowAI... > logs\galFlowAI.log
echo %date% %time% >> logs\galFlowAI.log

"K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\python.exe" run_galFlowAI.py >> logs\galFlowAI.log 2>&1
