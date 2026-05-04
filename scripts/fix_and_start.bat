@echo off
REM Final Fix and Start Script for FlowForgeAI
setlocal EnableDelayedExpansion

set BASE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
set STUDIO_PYTHON=K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe

echo ================================
echo   FlowForgeAI - Fix and Start
echo ================================
echo.

REM Check Python
if exist "%STUDIO_PYTHON%" (
    set PYTHON=%STUDIO_PYTHON%
    echo ✓ Python found: %PYTHON%
) else (
    echo ✗ Python not found at: %STUDIO_PYTHON%
    echo Searching for Python...
    for /f "delims=" %%i in ('where python 2^>nul') do (
        echo Found: %%i
        if not "%%i"=="" set PYTHON=%%i
    )
    if "!PYTHON!"=="" (
        echo ✗ Python not found anywhere!
        pause
        exit /b 1
    )
)

echo.

REM ========== Fix api.py Syntax Errors ==========
echo [1/4] Fixing api.py syntax errors...
cd /d "%BASE_DIR%"

REM Create a clean api.py with correct syntax
REM This uses a simple approach: read line by line and fix common errors

echo Creating fixed api.py...
(
echo """
echo FastAPI V2 for FlowForgeAI - Local-first internal API.
echo """
echo from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
echo from fastapi.middleware.cors import CORSMiddleware
echo from pydantic import BaseModel
echo from typing import Dict, List, Optional, Any
echo import sys
echo from pathlib import Path
echo import time
echo.
echo # Add project root to path
echo sys.path.insert(0, str(Path(__file__).parent.parent^)^)
echo.
echo from app.config import GRADIO_HOST, GRADIO_PORT
echo from app.logging_config import setup_logger
echo.
echo logger = setup_logger(^)
echo.
echo app = FastAPI(
echo     title="FlowForgeAI API",
echo     description="Local-first API for commercial video generation",
echo     version="2.0"
echo ^)
echo.
echo # CORS for local access
echo app.add_middleware(
echo     CORSMiddleware,
echo     allow_origins=["http://127.0.0.1:7860", "http://localhost:7860"],
echo     allow_credentials=True,
echo     allow_methods=["*"],
echo     allow_headers=["*"],
echo ^)
) > api_part1.txt

echo Part 1 created...

REM Now we need to append the rest with correct syntax
REM Let me use a different approach - create the entire fixed file

echo.
echo [2/4] Creating complete fixed api.py...
echo This will take a moment...

REM Use PowerShell to create the file properly
powershell -Command "
$content = Get-Content 'app\api.py' -Raw
# Fix missing commas in dictionaries
$content = $content -replace '(\"ok\"\s*:\s*True)(\s+\"[a-z_]+)', '\$1,\$2'
$content = $content -replace '(\"ok\"\s*:\s*False)(\s+\"[a-z_]+)', '\$1,\$2'
$content = $content -replace '(\"job_id\"\s*:\s*job_id)(\s+\"progress\")', '\$1,\$2'
$content = $content -replace '(\"success\"\s*:\s*True)(\s+\"[a-z_]+)', '\$1,\$2'
# Fix __file__ to __file__
$content = $content -replace '_file__', '_file__'
# Fix Dict[str; Any] to Dict[str, Any]
$content = $content -replace 'Dict\[str; Any\]', 'Dict[str, Any]'
$content = $content -replace 'List\[str; Any\]', 'List[str, Any]'
Set-Content 'app\api_fixed.py' $content
Write-Host 'api.py syntax fixed'
"

if exist "app\api_fixed.py" (
    copy "app\api_fixed.py" "app\api.py" /Y >nul
    echo ✓ api.py fixed
) else (
    echo ✗ Failed to fix api.py
    pause
    exit /b 1
)

echo.
echo [3/4] Checking syntax...
"%PYTHON%" -m py_compile "app\api.py" 2>&1 | findstr /i "error" && (
    echo ✗ Syntax error still exists in api.py
    pause
    exit /b 1
)

echo ✓ Syntax OK
echo.
echo [4/4] Starting application...
echo.
echo ================================
echo   ACCESS URLS:
echo   Gradio UI: http://127.0.0.1:7860
echo   FastAPI:   http://127.0.0.1:8000
echo ================================
echo.

"%PYTHON%" "app\main.py"

pause
