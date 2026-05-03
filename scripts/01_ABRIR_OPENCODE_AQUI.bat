@echo off
setlocal
cd /d %~dp0..
if not exist AGENTS.md (
  echo [ERRO] AGENTS.md nao encontrado. Rode 00_PREPARAR_OPENCODEGALPASTA.bat primeiro.
  pause
  exit /b 1
)
echo Abrindo OpenCode em: %CD%
echo Use a ordem: /inicio, /analise, /fundacao, /ui, /projeto, /roteiro, /storyboard, /fila, /wangp, /ffmpeg, /tts, /testes, /docs, /qa
opencode --dir %CD%
endlocal
