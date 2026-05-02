@echo off
echo ===================================
echo  galFlowAI - Configurar GitHub
echo ===================================
echo.
echo Voce precisa autenticar no GitHub primeiro.
echo.
echo OPCOES:
echo 1. Executar: gh auth login
echo    (escolha GitHub.com, HTTPS, login com browser)
echo.
echo 2. Ou criar um token em:
echo    https://github.com/settings/tokens
echo    e executar:
echo    set GH_TOKEN=seu_token_aqui
echo.
echo Depois execute este script novamente.
echo.
pause

REM Tentar criar repo e fazer push
cd /d K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta

echo.
echo Verificando autenticacao...
gh auth status 2>&1
if errorlevel 1 (
    echo ERRO: Nao autenticado no GitHub
    pause
    exit /b 1
)

echo.
echo Criando repositorio galFlowAI no GitHub...
gh repo create galFlowAI --public --source=. --push --description "galFlowAI: Estudio local para comerciais curtos com IA" 2>&1
if errorlevel 1 (
    echo Tentando fazer push para repo existente...
    git remote -v | findstr origin || git remote add origin https://github.com/anomalyco/galFlowAI.git
    git push -u origin master 2>&1
)

echo.
echo ===================================
echo  PRONTO! Codigo enviado ao GitHub
echo ===================================
pause
