@echo off
echo ===========================================
echo galFlowAI — Suite de Testes Completa
echo ===========================================
echo.

echo [1/4] Testes unitarios Python...
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\python.exe -m pytest tests/unit/ -v --tb=short --cov=app --cov-report=term-missing
if errorlevel 1 (
    echo FALHA nos testes unitarios
    exit /b 1
)

echo.
echo [2/4] Testes de integracao Python...
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\python.exe -m pytest tests/integration/ -v --tb=short
if errorlevel 1 (
    echo FALHA nos testes de integracao
    exit /b 1
)

echo.
echo [3/4] Testes Go...
K:\Go\bin\go.exe test ./... -v -cover
if errorlevel 1 (
    echo FALHA nos testes Go
    exit /b 1
)

echo.
echo [4/4] Relatorio de cobertura...
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\python.exe -m pytest tests/ --cov=app --cov-report=html:coverage_html
echo Relatorio gerado em: coverage_html/index.html

echo.
echo ===========================================
echo TODOS OS TESTES PASSARAM
echo ===========================================
