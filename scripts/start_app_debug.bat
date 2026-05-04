@echo off
REM Start FlowForgeAI Gradio UI with required environment variables

setlocal EnableDelayedExpansion

REM ========== Required Environment Variables ==========
set PIP_CACHE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip
set HF_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\huggingface
set TORCH_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\torch
set XDG_CACHE_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache
set TEMP=K:\AI_VIDEO_COMERCIAL_STUDIO\temp
set TMP=K:\AI_VIDEO_COMERCIAL_STUDIO\temp
set OLLAMA_MODELS=K:\AI_VIDEO_COMERCIAL_STUDIO\models\ollama
set GIT_PYTHON_GIT_EXECUTABLE=K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Library\bin\git.exe

REM ========== Create directories if not exist ==========
if not exist "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip" mkdir "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip"
if not exist "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\huggingface" mkdir "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\huggingface"
if not exist "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\torch" mkdir "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\torch"
if not exist "K:\AI_VIDEO_COMERCIAL_STUDIO\cache" mkdir "K:\AI_VIDEO_COMERCIAL_STUDIO\cache"
if not exist "K:\AI_VIDEO_COMERCIAL_STUDIO\temp" mkdir "K:\AI_VIDEO_COMERCIAL_STUDIO\temp"
if not exist "K:\AI_VIDEO_COMERCIAL_STUDIO\models\ollama" mkdir "K:\AI_VIDEO_COMERCIAL_STUDIO\models\ollama"

REM ========== Change to working directory ==========
cd /d "K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta"

REM ========== Start Gradio UI ==========
echo ================================
echo   FlowForgeAI - Gradio UI
echo ================================
echo.
echo Environment variables set:
echo   PIP_CACHE_DIR=%PIP_CACHE_DIR%
echo   HF_HOME=%HF_HOME%
echo   TORCH_HOME=%TORCH_HOME%
echo   TEMP=%TEMP%
echo.
echo Starting Gradio UI at http://127.0.0.1:7860
echo.

python app/main.py

pause
