# Teste Autonomo Completo - galFlowAI
Write-Host "=== TESTE AUTONOMO galFlowAI ===" -ForegroundColor Cyan

# 1. Encontrar Python (caminho duplo L)
$pythonPath = "K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\python.exe"
Write-Host "`n1. Verificando Python em: $pythonPath"
if (Test-Path $pythonPath) {
    Write-Host "   [OK] Python encontrado" -ForegroundColor Green
} else {
    Write-Host "   [ERRO] Python nao encontrado, buscando..." -ForegroundColor Red
    $found = Get-ChildItem -Path "K:\AI_VIDEO_COMERCIAL_STUDIO" -Filter "python.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($found) {
        $pythonPath = $found.FullName
        Write-Host "   [OK] Python encontrado em: $pythonPath" -ForegroundColor Green
    } else {
        Write-Host "   [ERRO] Python nao encontrado em nenhum lugar!" -ForegroundColor Red
        exit 1
    }
}

# 2. Verificar projeto (caminho simples L)
$projectPath = "K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta"
Write-Host "`n2. Verificando projeto em: $projectPath"
if (Test-Path $projectPath) {
    Write-Host "   [OK] Projeto encontrado" -ForegroundColor Green
} else {
    Write-Host "   [ERRO] Projeto nao encontrado!" -ForegroundColor Red
    exit 1
}

# 3. Testar importacao
Write-Host "`n3. Testando importacao da aplicacao..."
$testCode = @"
import sys
sys.path.insert(0, r'$projectPath')
try:
    import gradio
    print('Gradio OK:', gradio.__version__)
    from app.main import demo
    print('App OK:', demo.title)
    print('IMPORT_SUCCESS')
except Exception as e:
    print('IMPORT_ERROR:', e)
    sys.exit(1)
"@
$testFile = "$projectPath\temp_test_import.py"
$testCode | Out-File -FilePath $testFile -Encoding UTF8
& $pythonPath $testFile
if ($LASTEXITCODE -ne 0) {
    Write-Host "   [ERRO] Falha na importacao" -ForegroundColor Red
    Remove-Item $testFile -Force -ErrorAction SilentlyContinue
    exit 1
}
Remove-Item $testFile -Force -ErrorAction SilentlyContinue
Write-Host "   [OK] Importacao bem sucedida" -ForegroundColor Green

# 4. Iniciar servidor em processo separado
Write-Host "`n4. Iniciando servidor galFlowAI..."
$logPath = "$projectPath\logs\galFlowAI_test.log"
if (-not (Test-Path "$projectPath\logs")) { New-Item -Path "$projectPath\logs" -ItemType Directory -Force | Out-Null }

$envVars = @(
    "PIP_CACHE_DIR=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip",
    "HF_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\huggingface",
    "TORCH_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache\torch",
    "XDG_CACHE_HOME=K:\AI_VIDEO_COMERCIAL_STUDIO\cache",
    "TEMP=K:\AI_VIDEO_COMERCIAL_STUDIO\temp",
    "TMP=K:\AI_VIDEO_COMERCIAL_STUDIO\temp"
)

$startInfo = New-Object System.Diagnostics.ProcessStartInfo
$startInfo.FileName = $pythonPath
$startInfo.Arguments = "run_galFlowAI.py"
$startInfo.WorkingDirectory = $projectPath
$startInfo.UseShellExecute = $false
$startInfo.RedirectStandardOutput = $true
$startInfo.RedirectStandardError = $true
foreach ($envVar in $envVars) {
    $name, $value = $envVar -split '=', 2
    $startInfo.EnvironmentVariables[$name] = $value
}

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $startInfo
$process.Start() | Out-Null
Write-Host "   [OK] Servidor iniciado (PID: $($process.Id))" -ForegroundColor Green

# 5. Aguardar servidor iniciar
Write-Host "`n5. Aguardando servidor iniciar (max 60s)..."
$maxWait = 60
$waited = 0
$serverUp = $false
while ($waited -lt $maxWait) {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:7860" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            $serverUp = $true
            Write-Host "   [OK] Servidor respondeu com status $($response.StatusCode)" -ForegroundColor Green
            break
        }
    } catch {
        # Servidor ainda nao subiu
    }
    Start-Sleep -Seconds 2
    $waited += 2
    Write-Host "   Aguardando... ($waited s)" -ForegroundColor Yellow
}

if (-not $serverUp) {
    Write-Host "   [ERRO] Servidor nao iniciou em $maxWait segundos" -ForegroundColor Red
    $process.Kill()
    $process.WaitForExit()
    exit 1
}

# 6. Fazer chamada de teste
Write-Host "`n6. Testando chamada a aplicacao..."
try {
    $testResponse = Invoke-WebRequest -Uri "http://127.0.0.1:7860" -UseBasicParsing -TimeoutSec 10
    Write-Host "   [OK] Pagina carregada: $($testResponse.Content.Length) bytes" -ForegroundColor Green
    if ($testResponse.Content -like "*galFlowAI*") {
        Write-Host "   [OK] Titulo galFlowAI encontrado na pagina" -ForegroundColor Green
    }
} catch {
    Write-Host "   [ERRO] Falha na chamada: $_" -ForegroundColor Red
}

# 7. Parar servidor
Write-Host "`n7. Parando servidor..."
try {
    $process.Kill()
    $process.WaitForExit(5000)
    Write-Host "   [OK] Servidor parado" -ForegroundColor Green
} catch {
    Write-Host "   [AVISO] Erro ao parar servidor: $_" -ForegroundColor Yellow
}

Write-Host "`n=== TESTE CONCLUIDO ===" -ForegroundColor Cyan
