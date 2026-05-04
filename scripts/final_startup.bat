@echo off
REM Final solution for FlowForgeAI startup
setlocal EnableDelayedExpansion

set BASE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
set PYTHON_PORTABLE_DIR=%BASE_DIR%\python_portable
set PYTHON_EXE=%PYTHON_PORTABLE_DIR%\python.exe

echo ================================
echo   FlowForgeAI - Final Startup
echo ================================
echo.

REM ========== Step 1: Get Python ==========
if not exist "%PYTHON_EXE%" (
    echo [1/4] Python not found. Downloading portable Python...
    
    set PYTHON_URL=https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-amd64.zip
    set ZIP_FILE=%BASE_DIR%\python.zip
    
    powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%ZIP_FILE%'"
    
    if exist "%ZIP_FILE%" (
        echo Extracting Python...
        powershell -Command "Expand-Archive -Path '%ZIP_FILE%' -DestinationPath '%PYTHON_PORTABLE_DIR%' -Force"
        del "%ZIP_FILE%"
        echo ✓ Portable Python downloaded
    ) else (
        echo ✗ Failed to download Python
        echo Please install Python manually in: %PYTHON_PORTABLE_DIR%
        pause
        exit /b 1
    )
) else (
    echo [1/4] ✓ Python found: %PYTHON_EXE%
)

REM ========== Step 2: Fix api.py syntax ==========
echo [2/4] Fixing api.py syntax errors...

powershell -Command "
$content = Get-Content '%BASE_DIR%\app\api.py' -Raw

# Fix 1: allow_origins -> allow_origins
$content = $content -replace 'allow_origins', 'allow_origins'

# Fix 2: CORSMiddleware -> CORSMiddleware  
$content = $content -replace 'CORSMiddleware', 'CORSMiddleware'

# Fix 3: Add missing commas in dictionaries
# Pattern: 'True \"key\"' -> 'True, \"key\"'
$content = $content -replace '(\"ok\"\s*:\s*True)(\s+\"[a-z_]+)', '\$1,\$2'
$content = $content -replace '(\"ok\"\s*:\s*False)(\s+\"[a-z_]+)', '\$1,\$2'
$content = $content -replace '(\"success\"\s*:\s*True)(\s+\"[a-z_]+)', '\$1,\$2'
$content = $content -replace '(\"job_id\"\s*:\s*job_id)(\s+\"progress\")', '\$1,\$2'

# Fix 4: __file__ -> __file__
$content = $content -replace '_file__', '_file__'

# Fix 5: GRADIO -> GRADIO (if wrong)
$content = $content -replace 'GRADIO_HOST', 'GRADIO_HOST'
$content = $content -replace 'GRADIO_PORT', 'GRADIO_PORT'

Set-Content '%BASE_DIR%\app\api.py' $content
Write-Host 'api.py syntax fixed'
"

REM ========== Step 3: Verify syntax ==========
echo [3/4] Verifying syntax...
"%PYTHON_EXE%" -m py_compile "%BASE_DIR%\app\api.py" 2>&1 | findstr /i "error" && (
    echo ✗ Syntax errors still exist in api.py
    pause
    exit /b 1
)
echo ✓ Syntax OK

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
"%PYTHON_EXE%" app/main.py

pause
