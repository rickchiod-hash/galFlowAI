@echo off
REM Setup KoboldCpp for FlowForgeAI
REM Download: https://github.com/LostRuins/KoboldCpp/releases

echo ================================
echo   FlowForgeAI - Setup KoboldCpp
echo ================================
echo.

set KOBOLD_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\engines\KoboldCpp
set KOBOLD_EXE=%KOBOLD_DIR%\koboldcpp.exe

echo [1/4] Checking if KoboldCpp exists...
if exist "%KOBOLD_EXE%" (
    echo ✓ KoboldCpp found at: %KOBOLD_EXE%
) else (
    echo ✗ KoboldCpp not found
    echo Download from: https://github.com/LostRuins/KoboldCpp/releases
    echo Download the latest koboldcpp_nocuda.exe (for GTX 1660 Super)
    echo Save to: %KOBOLD_DIR%
    echo.
    mkdir "%KOBOLD_DIR%" 2>nul
    echo After downloading, place koboldcpp.exe in: %KOBOLD_DIR%
    pause
    exit /b 1
)

echo.
echo [2/4] Checking model directory...
set MODEL_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\models\koboldcpp
mkdir "%MODEL_DIR%" 2>nul
echo Model directory: %MODEL_DIR%
echo Place your GGUF models there.
echo.

echo [3/4] Starting KoboldCpp server...
start /min "%KOBOLD_EXE%" --port 5001 --model "%MODEL_DIR%\your_model.gguf"

echo.
echo [4/4] Testing connection...
timeout /t 5 /nobreak >nul
curl -s http://localhost:5001/api/v1/models >nul 2>&1
if %errorlevel%==0 (
    echo ✓ KoboldCpp server is running!
    echo FlowForgeAI will detect it automatically.
) else (
    echo ✗ KoboldCpp server not responding on port 5001
    echo Check if a model is loaded.
)

echo.
echo Setup complete! Now restart FlowForgeAI and select "KoboldCpp local"
pause
