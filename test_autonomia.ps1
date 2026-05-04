# Teste completo do galFlowAI - Autonomia total
Write-Host "=== VERIFICANDO CAMINHOS ==="

$pythonPath = "K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\python.exe"
$projectPath = "K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta"

if (Test-Path $pythonPath) {
    Write-Host "Python encontrado: $pythonPath"
} else {
    Write-Host "ERRO: Python nao encontrado em $pythonPath"
    exit 1
}

if (Test-Path $projectPath) {
    Write-Host "Projeto encontrado: $projectPath"
} else {
    Write-Host "ERRO: Projeto nao encontrado em $projectPath"
    exit 1
}

Write-Host "`n=== TESTANDO IMPORTS ==="
$testCmd = "& `"$pythonPath`" -c `"import sys; sys.path.insert(0, '$projectPath'); import gradio; print('Gradio OK:', gradio.__version__); from app.main import demo; print('App OK:', demo.title)`""
Invoke-Expression $testCmd

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO nos imports"
    exit 1
}

Write-Host "`n=== INICIANDO SERVIDOR ==="
$process = Start-Process -FilePath $pythonPath -ArgumentList "run_galFlowAI.py" -WorkingDirectory $projectPath -PassThru -WindowStyle Normal

Write-Host "Aguardando servidor iniciar (30s max)..."
$maxWait = 30
$waited = 0
$serverUp = $false

while ($waited -lt $maxWait) {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:7860" -UseBasicParsing -TimeoutSec 2
        if ($response.StatusCode -eq 200) {
            $serverUp = $true
            break
        }
    } catch {
        # Servidor ainda nao subiu
    }
    Start-Sleep -Seconds 2
    $waited += 2
    Write-Host "Aguardando... ($waited s)"
}

if ($serverUp) {
    Write-Host "`nSUCESSO: galFlowAI rodando em http://127.0.0.1:7860"
    Write-Host "Status HTTP: $($response.StatusCode)"
    Write-Host "Conteudo carregado: $($response.Content.Length) bytes"
    
    # Testar chamada a API (opcional)
    Write-Host "`n=== TESTANDO CHAMADA ==="
    try {
        $testResponse = Invoke-WebRequest -Uri "http://127.0.0.1:7860/run/predict" -Method POST -Body '{"data":["teste"]}' -ContentType "application/json" -UseBasicParsing -TimeoutSec 5
        Write-Host "Chamada API status: $($testResponse.StatusCode)"
    } catch {
        Write-Host "Chamada API (esperado para MVP mock): $_"
    }
} else {
    Write-Host "`nERRO: Servidor nao iniciou em $maxWait segundos"
    if (Test-Path "$projectPath\logs\galFlowAI.log") {
        Write-Host "`nUltimos logs:"
        Get-Content "$projectPath\logs\galFlowAI.log" | Select-Object -Last 20
    }
}

# Parar processo apos teste
if (-not $process.HasExited) {
    Write-Host "`nParando servidor..."
    $process.Kill()
    Write-Host "Servidor parado"
}
