@echo off
REM Setup LM Studio for GalFlowAI
REM Guide: https://lmstudio.ai

echo ================================
echo   GalFlowAI - Setup LM Studio
echo ================================
echo.

echo [1/3] Checking if LM Studio is installed...
where lmstudio.exe 2>nul
if %errorlevel%==0 (
    echo ✓ LM Studio found
) else (
    echo ✗ LM Studio not found
    echo Download from: https://lmstudio.ai
    echo Install and open LM Studio
    pause
    exit /b 1
)

echo.
echo [2/3] Instructions to start LM Studio server:
echo   1. Open LM Studio
echo   2. Go to "Developer" tab (left sidebar)
echo   3. Select "Local Server"
echo   4. Load a model (recommended: Llama 3.2 3B or similar)
echo   5. Make sure port is 1234
echo   6. Click "Start Server"
echo.

echo [3/3] Testing connection...
curl -s http://localhost:1234/v1/models >nul 2>&1
if %errorlevel%==0 (
    echo ✓ LM Studio server is running!
    echo GalFlowAI will detect it automatically.
) else (
    echo ✗ LM Studio server not responding on port 1234
    echo Please start the server following instructions above.
)

echo.
echo Setup complete! Now restart GalFlowAI and select "LM Studio local"
pause
