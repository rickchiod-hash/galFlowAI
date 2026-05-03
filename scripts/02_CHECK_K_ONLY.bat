@echo off
setlocal
set ROOT=K:\AI_VIDEO_COMMERCIAL_STUDIO
set PIP_CACHE_DIR=%ROOT%\cache\pip
set HF_HOME=%ROOT%\cache\huggingface
set TORCH_HOME=%ROOT%\cache\torch
set XDG_CACHE_HOME=%ROOT%\cache
set TEMP=%ROOT%\temp
set TMP=%ROOT%\temp
set OLLAMA_MODELS=%ROOT%\models\ollama
set GIT_PYTHON_GIT_EXECUTABLE=%ROOT%\envs\studio\Library\bin\git.exe

echo ROOT=%ROOT%
echo PIP_CACHE_DIR=%PIP_CACHE_DIR%
echo HF_HOME=%HF_HOME%
echo TORCH_HOME=%TORCH_HOME%
echo XDG_CACHE_HOME=%XDG_CACHE_HOME%
echo TEMP=%TEMP%
echo TMP=%TMP%
echo OLLAMA_MODELS=%OLLAMA_MODELS%
echo GIT_PYTHON_GIT_EXECUTABLE=%GIT_PYTHON_GIT_EXECUTABLE%
echo.
echo Espaco em K:
powershell -NoProfile -Command "$d=Get-PSDrive K; Write-Host ('Livre GB: {0:N2}' -f ($d.Free/1GB)); Write-Host ('Usado GB: {0:N2}' -f ($d.Used/1GB))"
pause
endlocal
