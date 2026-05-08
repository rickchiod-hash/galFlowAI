@echo off
REM GalFlowAI - Standard Startup Script (ALL required env vars)
echo Iniciando GalFlowAI com configuracao padrao K:...

REM Required environment variables (from AGENTS.md context)
set PIP_CACHE_DIR=K:\AI_VIDEO_COMMERCIAL_STUDIO\cache\pip
set HF_HOME=K:\AI_VIDEO_COMMERCIAL_STUDIO\cache\huggingface
set TORCH_HOME=K:\AI_VIDEO_COMMERCIAL_STUDIO\cache\torch
set XDG_CACHE_HOME=K:\AI_VIDEO_COMMERCIAL_STUDIO\cache
set TEMP=K:\AI_VIDEO_COMMERCIAL_STUDIO\temp
set TMP=K:\AI_VIDEO_COMMERCIAL_STUDIO\temp
set OLLAMA_MODELS=K:\AI_VIDEO_COMMERCIAL_STUDIO\models\ollama
set GIT_PYTHON_GIT_EXECUTABLE=K:\AI_VIDEO_COMMERCIAL_STUDIO\envs\studio\Library\bin\git.exe

REM Verify we are in correct directory
cd /d K:\AI_VIDEO_COMMERCIAL_STUDIO\opencodegalpasta

REM Activate virtual environment
call K:\AI_VIDEO_COMMERCIAL_STUDIO\envs\studio\Scripts\activate.bat

REM Start Gradio UI
echo.
echo GalFlowAI - Gradio UI
echo Acesse: http://127.0.0.1:7860
echo.

REM Start the application
K:\AI_VIDEO_COMMERCIAL_STUDIO\envs\studio\Scripts\python.exe app/main.py

pause
