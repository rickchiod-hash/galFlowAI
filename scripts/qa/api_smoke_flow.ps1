#Requires -Version 7
<#
.SYNOPSIS
    GalFlowAI API Smoke Test — validates all critical endpoints and saves responses.
.DESCRIPTION
    Tests all API endpoints in sequence, saves JSON responses to artifacts/qa/curl/.
    Run after the app is started (scripts/start_GalFlowAI_standard.bat).
    Usage: pwsh scripts/qa/api_smoke_flow.ps1
#>

param(
    [string]$BaseUrl = "http://127.0.0.1:8000",
    [string]$OutputDir = "artifacts/qa/curl"
)

# Ensure output directory exists
if (-not (Test-Path -LiteralPath $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

$PASS = 0
$FAIL = 0

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$sessionLog = "$OutputDir/session-$timestamp.txt"

Write-Host "GalFlowAI API Smoke Test — Session $timestamp" -ForegroundColor Cyan
Write-Host "Base URL: $BaseUrl" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Save session header
@"
=== GalFlowAI API Smoke Test ===
Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss UTC")
Base URL: $BaseUrl
Output: $OutputDir
---
"@ | Out-File -FilePath $sessionLog -Encoding utf8

function Test-Step {
    param($Name, $Endpoint, $Method = "GET", $Body = $null, $ExpectedStatus = 200, $SaveFile = $null)

    $filePrefix = ($Name -replace '[^a-zA-Z0-9]', '_').Substring(0, [Math]::Min(60, $Name.Length))
    $responseFile = "$OutputDir/$filePrefix.json"
    $curlCommand = "curl -sk -w `"%{http_code}`" -o `"$responseFile`" -X $Method `"$BaseUrl$Endpoint`""

    if ($Body) {
        $bodyFile = "$OutputDir/${filePrefix}_request.json"
        $Body | Out-File -FilePath $bodyFile -Encoding utf8
        $curlCommand = "curl -sk -w `"%{http_code}`" -o `"$responseFile`" -X $Method -H `"Content-Type: application/json`" -d `"@$bodyFile`" `"$BaseUrl$Endpoint`""
    }

    try {
        $httpCode = & cmd /c $curlCommand 2>&1
        $actualStatus = if ($httpCode -match '^\d{3}') { [int]$httpCode } else { 0 }

        if ($actualStatus -eq $ExpectedStatus) {
            Write-Host "  PASS [$actualStatus]: $Name" -ForegroundColor Green
            $script:PASS++
            # Append to session log
            "PASS [$actualStatus] $Method $Endpoint → $responseFile" | Out-File -FilePath $sessionLog -Encoding utf8 -Append
        } elseif ($ExpectedStatus -in 200, 201 -and $actualStatus -eq 0) {
            Write-Host "  WARN [$actualStatus]: $Name (server may be down)" -ForegroundColor Yellow
            $script:FAIL++
            "WARN [$actualStatus] $Method $Endpoint — possible server down" | Out-File -FilePath $sessionLog -Encoding utf8 -Append
        } else {
            Write-Host "  FAIL [$actualStatus, expected $ExpectedStatus]: $Name" -ForegroundColor Red
            $script:FAIL++
            "FAIL [$actualStatus, expected $ExpectedStatus] $Method $Endpoint → $responseFile" | Out-File -FilePath $sessionLog -Encoding utf8 -Append
        }

        if ($SaveFile -and (Test-Path -LiteralPath $responseFile)) {
            Copy-Item -LiteralPath $responseFile -Destination "$OutputDir/$SaveFile" -Force
        }
    } catch {
        Write-Host "  FAIL: $Name — $_" -ForegroundColor Red
        $script:FAIL++
        "FAIL $Method $Endpoint — $_" | Out-File -FilePath $sessionLog -Encoding utf8 -Append
    }
}

Write-Host "--- Pre-Flight ---" -ForegroundColor Yellow

Test-Step "Health check" "/api/v1/health"
Test-Step "Provider list" "/api/v1/llm/providers"
Test-Step "Pipeline status" "/api/v1/pipeline/status"
Test-Step "Hardware info" "/api/v1/hardware"

Write-Host ""
Write-Host "--- Script & Approval (Script-Only) ---" -ForegroundColor Yellow

$projectId = "test_project_qa"

Test-Step "Generate script (template)" "/api/v1/llm/script" -Method POST -Body '{"briefing":"Produto teste para validacao de fluxo completo","provider":"template"}' -ExpectedStatus 200 -SaveFile "script_generate_response.json"

Test-Step "Save script" "/api/v1/projects/$projectId/script/save-manual-edit" -Method POST -Body '{"project_id":"test_project_qa","script_markdown":"# Roteiro Teste\n\n## Cena 1\nTexto da cena 1\n\n## Cena 2\nTexto da cena 2\n","version_note":"QA smoke test"}' -ExpectedStatus 200 -SaveFile "script_save_response.json"

Test-Step "Approve script" "/api/v1/projects/$projectId/script/approve" -Method POST -ExpectedStatus 200 -SaveFile "script_approve_response.json"

Test-Step "Load current script" "/api/v1/projects/$projectId/script/current" -ExpectedStatus 200 -SaveFile "script_current_response.json"

Test-Step "List versions" "/api/v1/projects/$projectId/script/versions" -ExpectedStatus 200 -SaveFile "script_versions_response.json"

Write-Host ""
Write-Host "--- Dashboard & Observability ---" -ForegroundColor Yellow

Test-Step "Metrics summary" "/api/v1/metrics"
Test-Step "Metrics operations" "/api/v1/metrics/operations"
Test-Step "Recent logs" "/api/v1/logs/recent?limit=10"
Test-Step "Logs summary" "/api/v1/logs/summary"
Test-Step "Last error" "/api/v1/logs/last-error"
Test-Step "Structured logs" "/api/v1/logs/structured"
Test-Step "Diagnostic bundle" "/api/v1/logs/diagnostic"

Write-Host ""
Write-Host "--- Jobs & Queue ---" -ForegroundColor Yellow

Test-Step "List jobs" "/api/v1/jobs"
Test-Step "Health dashboard" "/api/v1/health/dashboard"

Write-Host ""
Write-Host "=== Results ===" -ForegroundColor Cyan
Write-Host "$PASS passed, $FAIL failed" -ForegroundColor $(if ($FAIL -eq 0) { "Green" } else { "Red" })
Write-Host "Session log: $sessionLog"
Write-Host ""

"`n=== FINAL ===`n$PASS passed, $FAIL failed" | Out-File -FilePath $sessionLog -Encoding utf8 -Append

if ($FAIL -gt 0) { exit 1 } else { exit 0 }
