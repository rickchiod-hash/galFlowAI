@echo off
REM Final startup script for FlowForgeAI
setlocal EnableDelayedExpansion

set BASE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
set PORTABLE_PYTHON_DIR=%BASE_DIR%\python_portable
set PORTABLE_PYTHON=%PORTABLE_PYTHON_DIR%\python.exe

echo ================================
echo   FlowForgeAI - Final Startup
echo ================================
echo.

REM ========== Step 1: Get Python ==========
echo [1/4] Checking Python...
if exist "%PORTABLE_PYTHON%" (
    set PYTHON=%PORTABLE_PYTHON%
    echo ✓ Portable Python found: %PYTHON%
) else (
    echo Portable Python not found. Downloading...
    set PYTHON_URL=https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-amd64.zip
    set ZIP_FILE=%BASE_DIR%\python.zip
    
    powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%ZIP_FILE%'"
    
    if exist "%ZIP_FILE%" (
        echo Extracting Python...
        powershell -Command "Expand-Archive -Path '%ZIP_FILE%' -DestinationPath '%PORTABLE_PYTHON_DIR%' -Force"
        del "%ZIP_FILE%"
        set PYTHON=%PORTABLE_PYTHON%
        echo ✓ Portable Python downloaded
    ) else (
        echo ERROR: Failed to download Python
        echo Please install Python manually in: %PORTABLE_PYTHON_DIR%
        pause
        exit /b 1
    )
)

echo.

REM ========== Step 2: Fix api.py syntax ==========
echo [2/4] Fixing api.py syntax...

powershell -Command "
$content = Get-Content '%BASE_DIR%\app\api.py' -Raw

# Fix 1: allow_origins -> allow_origins
$content = $content -replace 'allow_origins', 'allow_origins'

# Fix 2: Add missing commas in dictionaries
# Pattern: 'True \"key\"' -> 'True, \"key\"'
$content = $content -replace '(\"ok\"\s*:\s*True)(\s+\"[a-z_]+)', '\$1,\$2'
$content = $content -replace '(\"ok\"\s*:\s*False)(\s+\"[a-z_]+)', '\$1,\$2'
$content = $content -replace '(\"success\"\s*:\s*True)(\s+\"[a-z_]+)', '\$1,\$2'
$content = $content -replace '(\"job_id\"\s*:\s*job_id)(\s+\"progress\")', '\$1,\$2'

# Fix 3: __file__ -> __file__
$content = $content -replace '_file__', '_file__'

# Fix 4: CORSMiddleware -> CORSMiddleware (if wrong)
$content = $content -replace 'CORSMiddleware', 'CORSMiddleware'

Set-Content '%BASE_DIR%\app\api_fixed.py' $content
Write-Host 'api.py fixed'
"

if exist "%BASE_DIR%\app\api_fixed.py" (
    copy "%BASE_DIR%\app\api_fixed.py" "%BASE_DIR%\app\api.py" /Y >nul
    del "%BASE_DIR%\app\api_fixed.py"
    echo ✓ api.py syntax fixed
) else (
    echo ✗ Failed to fix api.py
)

echo.

REM ========== Step 3: Verify syntax ==========
echo [3/4] Verifying syntax...
"%PYTHON%" -m py_compile "%BASE_DIR%\app\api.py" 2>&1 | findstr /i "error" && (
    echo ✗ Syntax errors still exist in api.py
    pause
    exit /b 1
)
echo ✓ Syntax OK

echo.

REM ========== Step 4: Start application ==========
echo [4/4] Starting FlowForgeAI...
echo.
echo ================================
echo   ACCESS URLS:
echo   Gradio UI:  http://127.0.0.1:7860
echo   FastAPI:    http://127.0.0.1:8000
echo   API Docs:   http://127.0.0.1:8000/docs
echo ================================
echo.

cd /d "%BASE_DIR%"
"%PYTHON%" app/main.py

pause
