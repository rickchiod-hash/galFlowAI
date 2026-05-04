@echo off
REM Setup GPT4All for FlowForgeAI
REM Python package already installed, need model files

echo ================================
echo   FlowForgeAI - Setup GPT4All
echo ================================
echo.

echo [1/3] Checking GPT4All Python package...
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe -c "import gpt4all; print('✓ gpt4all installed')" 2>&1
if %errorlevel%==0 (
    echo ✓ GPT4All package is installed
) else (
    echo ✗ GPT4All not installed, installing...
    K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\pip.exe install gpt4all
)

echo.
echo [2/3] Checking model directory...
set MODEL_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\models\gpt4all
mkdir "%MODEL_DIR%" 2>nul
echo Model directory: %MODEL_DIR%
echo.

echo [3/3] Downloading a small model for testing...
echo Note: You need to download GGUF model files.
echo Recommended (small models for 6GB VRAM):
echo   - orca-mini-3b-gguf (3B parameters)
echo   - llama-2-7b-chat-gguf (7B, might be tight)
echo.
echo Manual download:
echo   1. Go to: https://gpt4all.io
echo   2. Download a small GGUF model
echo   3. Save to: %MODEL_DIR%
echo.
echo Or use gpt4all command (if available):
echo   gpt4all list
echo   gpt4all download orca-mini-3b
echo.

echo Setup complete! After downloading a model, restart FlowForgeAI and select "GPT4All local"
pause
