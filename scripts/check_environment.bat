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

echo ==============================================
echo FlowForgeAI - Environment Check
echo ==============================================
echo Using Python: %WORKSPACE%\..\envs\studio\python.exe
echo.

:: Run Python check script
%BASE%\envs\studio\python.exe -c "
from app.config import setup_env_vars
from app.hardware import check_full_environment
from app.logging_config import setup_logger
import json

setup_env_vars()
logger = setup_logger()
env = check_full_environment()
logger.info(f'Environment check: {json.dumps(env, indent=2)}')
print(json.dumps(env, indent=2))
print('\nRecommended preset for your GPU:')
print(json.dumps(env['recommended_preset'], indent=2))
"

if errorlevel 1 (
    echo.
    echo [ERROR] Environment check failed. Check logs in %WORKSPACE%\logs
) else (
    echo.
    echo [SUCCESS] Environment check passed. No C: writes detected.
)
endlocal
pause
