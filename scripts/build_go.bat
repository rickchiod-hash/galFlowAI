@echo off
echo ===================================
echo galFlowAI - Build Go Executables
echo ===================================

set GOOS=windows
set GOARCH=amd64

echo.
echo Building server...
go build -o galflowai-server.exe ./cmd/server/

echo Building worker...
go build -o galflowai-worker.exe ./cmd/worker/

echo Building CLI...
go build -o galflowai-cli.exe ./cmd/cli/

echo.
echo Build concluido:
dir *.exe 2>&1
echo.
echo ===================================
echo Build finalizado
echo ===================================
