@echo off
setlocal EnableDelayedExpansion
set BASE=K:\AI_VIDEO_COMMERCIAL_STUDIO
set WORKSPACE=%BASE%\opencodegalpasta

:: Set K-only environment variables
set PIP_CACHE_DIR=%BASE%\cache\pip
set HF_HOME=%BASE%\cache\huggingface
set TORCH_HOME=%BASE%\cache\torch
set XDG_CACHE_HOME=%BASE%\cache
set TEMP=%BASE%\temp
set TMP=%BASE%\temp
set OLLAMA_MODELS=%BASE%\models\ollama
set GIT_PYTHON_GIT_EXECUTABLE=%BASE%\envs\studio\Library\bin\git.exe
set PYTHONPATH=%WORKSPACE%

echo Starting FlowForgeAI on http://127.0.0.1:7860...
cd /d %WORKSPACE%
%BASE%\envs\studio\python.exe -m app.main
endlocal
