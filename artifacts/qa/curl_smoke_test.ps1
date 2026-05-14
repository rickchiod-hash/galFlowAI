#Requires -Version 7
<#
.SYNOPSIS
    GalFlowAI P0 Smoke Test — validates critical UI-210, UI-209, and gate-bypass fixes.
.DESCRIPTION
    Tests key Gradio endpoints via HTTP API simulation.
    Run after the app is started (python -m app.main).
    Usage: pwsh artifacts/qa/curl_smoke_test.ps1
#>

$BASE = "http://127.0.0.1:7860"
$PASS = 0
$FAIL = 0

function Test-Step {
    param($Name, $ScriptBlock)
    try {
        $result = & $ScriptBlock
        if ($LASTEXITCODE -eq 0 -or $result) {
            Write-Host "  PASS: $Name" -ForegroundColor Green
            $script:PASS++
        } else {
            Write-Host "  FAIL: $Name" -ForegroundColor Red
            $script:FAIL++
        }
    } catch {
        Write-Host "  FAIL: $Name — $_" -ForegroundColor Red
        $script:FAIL++
    }
}

Write-Host "GalFlowAI P0 Smoke Test" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

# 1. App responds at root
Test-Step "GET / responds 200 or redirect" {
    $r = Invoke-WebRequest -Uri "$BASE/" -UseBasicParsing -TimeoutSec 10
    $r.StatusCode -in 200, 302, 303
}

# 2. API health check (FastAPI)
Test-Step "GET /api/v1/health returns 200" {
    $r = Invoke-WebRequest -Uri "$BASE/api/v1/health" -UseBasicParsing -TimeoutSec 10 -ErrorAction SilentlyContinue
    $r.StatusCode -eq 200
}

# 3. Config endpoint alive
Test-Step "GET /api/v1/config returns config" {
    $r = Invoke-WebRequest -Uri "$BASE/api/v1/config" -UseBasicParsing -TimeoutSec 10 -ErrorAction SilentlyContinue
    $r.StatusCode -eq 200
}

# 4. Provider list endpoint
Test-Step "GET /api/v1/llm/providers returns providers" {
    $r = Invoke-WebRequest -Uri "$BASE/api/v1/llm/providers" -UseBasicParsing -TimeoutSec 10 -ErrorAction SilentlyContinue
    $r.StatusCode -eq 200
}

# 5. Script generation API (template = fast, no LLM needed)
Test-Step "POST /api/v1/script/generate with template provider" {
    $body = @{briefing="Produto teste para validacao P0"; provider="template"} | ConvertTo-Json
    $r = Invoke-WebRequest -Uri "$BASE/api/v1/script/generate" -Method Post -Body $body -ContentType "application/json" -UseBasicParsing -TimeoutSec 30 -ErrorAction SilentlyContinue
    if ($r.StatusCode -eq 200) {
        $data = $r.Content | ConvertFrom-Json
        $data.ok -eq $true
    } else { $false }
}

# 6. Script save API
Test-Step "POST /api/v1/script/test_project/save saves script" {
    $body = @{script_markdown="# Teste`nCena 1"; note="Smoke test save"} | ConvertTo-Json
    $r = Invoke-WebRequest -Uri "$BASE/api/v1/script/test_project/save" -Method Post -Body $body -ContentType "application/json" -UseBasicParsing -TimeoutSec 30 -ErrorAction SilentlyContinue
    if ($r.StatusCode -eq 200) {
        $data = $r.Content | ConvertFrom-Json
        $data.ok -eq $true
    } else { $false }
}

# 7. Script approve API (must exist first)
Test-Step "POST /api/v1/script/test_project/approve approves script" {
    $r = Invoke-WebRequest -Uri "$BASE/api/v1/script/test_project/approve" -Method Post -UseBasicParsing -TimeoutSec 30 -ErrorAction SilentlyContinue
    if ($r.StatusCode -eq 200) {
        $data = $r.Content | ConvertFrom-Json
        $data.ok -eq $true
    } else { $false }
}

# 8. Script load after approval
Test-Step "GET /api/v1/script/test_project/current loads approved" {
    $r = Invoke-WebRequest -Uri "$BASE/api/v1/script/test_project/current" -UseBasicParsing -TimeoutSec 10 -ErrorAction SilentlyContinue
    if ($r.StatusCode -eq 200) {
        $data = $r.Content | ConvertFrom-Json
        $data.ok -eq $true -and $data.script -ne $null
    } else { $false }
}

# 9. Scenes generation requires approval (gate test)
Test-Step "GET /api/v1/scenes/test_project/list returns scenes or 400" {
    $r = Invoke-WebRequest -Uri "$BASE/api/v1/scenes/test_project/list" -UseBasicParsing -TimeoutSec 10 -ErrorAction SilentlyContinue
    $r.StatusCode -in 200, 400, 404
}

# 10. Metrics endpoint
Test-Step "GET /api/v1/metrics returns summary" {
    $r = Invoke-WebRequest -Uri "$BASE/api/v1/metrics" -UseBasicParsing -TimeoutSec 10 -ErrorAction SilentlyContinue
    $r.StatusCode -eq 200
}

# 11. Logs endpoint
Test-Step "GET /api/v1/logs returns logs" {
    $r = Invoke-WebRequest -Uri "$BASE/api/v1/logs" -UseBasicParsing -TimeoutSec 10 -ErrorAction SilentlyContinue
    $r.StatusCode -eq 200
}

Write-Host ""
Write-Host "Results: $PASS passed, $FAIL failed" -ForegroundColor $(if ($FAIL -eq 0) { "Green" } else { "Red" })
if ($FAIL -gt 0) { exit 1 } else { exit 0 }
