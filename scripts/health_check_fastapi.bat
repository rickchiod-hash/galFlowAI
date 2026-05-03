@echo off
echo Testando FastAPI em http://127.0.0.1:8000...
echo.

echo [1/4] Testando /api/health...
curl -s http://127.0.0.1:8000/api/health
if errorlevel 1 (
    echo [X] FastAPI nao esta rodando.
    echo Execute: scripts\start_fastapi.bat
    pause
    exit /b 1
) else (
    echo [OK] Health check passou.
)
echo.

echo [2/4] Testando /api/llm/providers...
curl -s http://127.0.0.1:8000/api/llm/providers
if errorlevel 1 (
    echo [X] Erro ao testar providers.
) else (
    echo [OK] Providers disponiveis.
)
echo.

echo [3/4] Testando geracao de roteiro (Template)...
curl -s -X POST http://127.0.0.1:8000/api/llm/script ^
  -H "Content-Type: application/json" ^
  -d "{\"briefing\": \"comercial teste\", \"provider\": \"template\"}"
if errorlevel 1 (
    echo [X] Erro ao gerar roteiro.
) else (
    echo [OK] Roteiro gerado.
)
echo.

echo [4/4] Testando hardware...
curl -s http://127.0.0.1:8000/api/hardware
if errorlevel 1 (
    echo [X] Erro ao testar hardware.
) else (
    echo [OK] Hardware detectado.
)
echo.

echo ==============================================
echo  TODOS OS TESTES CONCLUIDOS
echo ==============================================
echo.
pause
