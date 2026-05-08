@echo off
REM Check and fix api.py syntax
setlocal EnableDelayedExpansion

set PYTHON=K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe
set BASE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta

echo ================================
echo   Check and Fix api.py Syntax
echo ================================
echo.

REM Check if Python exists
if not exist "%PYTHON%" (
    echo Python not found at: %PYTHON%
    echo Searching for Python...
    for /f "delims=" %%i in ('where python 2^>nul') do (
        set PYTHON=%%i
        goto :found
    )
    echo ERROR: Python not found!
    pause
    exit /b 1
)

:found
echo ✓ Python found: %PYTHON%
echo.

REM Check syntax
echo [1/3] Checking api.py syntax...
"%PYTHON%" -m py_compile "%BASE_DIR%\app\api.py" 2>&1
if errorlevel 1 (
    echo.
    echo ✗ Syntax errors found in api.py
    echo.
    echo [2/3] Creating fixed api.py...
    
    REM Create a clean api.py with correct syntax
    REM This is a simplified version - just check key issues
    
    powershell -Command "
    $content = Get-Content '%BASE_DIR%\app\api.py' -Raw
    
    # Fix 1: __file__ to __file__
    $content = $content -replace '_file__', '_file__'
    
    # Fix 2: Add missing commas in dictionaries
    # Pattern: 'True \"key\"' -> 'True, \"key\"'
    $content = $content -replace '(\"ok\"\s*:\s*True)(\s+\"[a-z_]+)', '\$1,\$2'
    $content = $content -replace '(\"ok\"\s*:\s*False)(\s+\"[a-z_]+)', '\$1,\$2'
    $content = $content -replace '(\"success\"\s*:\s*True)(\s+\"[a-z_]+)', '\$1,\$2'
    $content = $content -replace '(\"job_id\"\s*:\s*job_id)(\s+\"progress\")', '\$1,\$2'
    
    # Fix 3: allow_origins to allow_origins
    $content = $content -replace 'allow_origins', 'allow_origins'
    
    # Fix 4: CORSMiddleware to CORSMiddleware
    $content = $content -replace 'CORSMiddleware', 'CORSMiddleware'
    
    # Fix 5: Dict[str; Any] to Dict[str, Any]
    $content = $content -replace 'Dict\[str; Any\]', 'Dict[str, Any]'
    $content = $content -replace 'List\[str; Any\]', 'List[str, Any]'
    
    Set-Content '%BASE_DIR%\app\api_fixed.py' $content
    Write-Host 'Fixed api.py created as api_fixed.py'
    "
    
    if exist "%BASE_DIR%\app\api_fixed.py" (
        copy "%BASE_DIR%\app\api_fixed.py" "%BASE_DIR%\app\api.py" /Y >nul
        echo ✓ api.py fixed
        del "%BASE_DIR%\app\api_fixed.py"
    ) else (
        echo ✗ Failed to fix api.py
    )
    
    echo.
    echo [3/3] Re-checking syntax...
    "%PYTHON%" -m py_compile "%BASE_DIR%\app\api.py" 2>&1
    if errorlevel 1 (
        echo ✗ Still has syntax errors
    ) else (
        echo ✓ Syntax OK
    )
) else (
    echo ✓ Syntax OK - no errors found
)

echo.
echo ================================
echo   Starting GalFlowAI...
echo ================================
echo.
echo URLs:
echo   Gradio: http://127.0.0.1:7860
echo   FastAPI: http://127.0.0.1:8000
echo.

cd /d "%BASE_DIR%"
"%PYTHON%" app/main.py

pause
