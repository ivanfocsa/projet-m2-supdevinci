param(
    [switch]$StartLab,
    [switch]$RunYoussefSetup,
    [switch]$SendLogs,
    [string]$SyslogHost = "127.0.0.1",
    [int]$SyslogPort = 514,
    [ValidateSet("udp", "tcp")]
    [string]$SyslogProtocol = "udp",
    [switch]$OpenBrowser
)

$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $PSScriptRoot
$ps = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
Set-Location $root

function Step($Name) {
    Write-Host ""
    Write-Host "=== $Name ===" -ForegroundColor Cyan
}

function Run($Name, [scriptblock]$Action) {
    Step $Name
    $global:LASTEXITCODE = 0
    & $Action
    $code = $global:LASTEXITCODE
    if ($null -eq $code) { $code = 0 }
    if ($code -eq 0) {
        Write-Host "[OK] $Name" -ForegroundColor Green
    } else {
        Write-Host "[WARN] $Name termine avec code $code" -ForegroundColor Yellow
    }
}

Step "Preparation session captures Daylight / Cyber Trust"
Write-Host "Racine : $root"
Write-Host "Objectif : recapturer CAP-01/CAP-02/CAP-03 si Wazuh est disponible, puis produire CAP-25 sans inventer de preuve."

Run "Generation logs demo" { python .\tools\generate_demo_logs.py }
Run "Generation images architecture/pfSense" { python .\tools\render_static_proof_images.py }
Run "Generation dashboard SOC offline" { python .\tools\build_offline_soc_dashboard.py }

if ($StartLab) {
    Run "Demarrage lab npm si package.json existe" {
        if (Test-Path -LiteralPath ".\package.json") {
            npm run lab:start
        } else {
            Write-Host "[INFO] package.json introuvable dans cette racine. Demarrer le lab Wazuh depuis sa racine technique."
        }
    }
}

if ($RunYoussefSetup) {
    Run "Setup SIEM Youssef" { & $ps -ExecutionPolicy Bypass -File ".\Youssef GUERNIOU\setup-siem-lab.ps1" }
}

if ($SendLogs) {
    Run "Rejeu logs demo vers syslog" { python .\tools\send_demo_logs_to_syslog.py --host $SyslogHost --port $SyslogPort --protocol $SyslogProtocol }
} else {
    Run "Dry-run logs demo" { python .\tools\send_demo_logs_to_syslog.py --dry-run }
}

Run "Preflight demo" { & $ps -ExecutionPolicy Bypass -File .\tools\preflight_demo.ps1 -WriteReport }
Run "Rendu preuve preflight" { python .\tools\render_preflight_evidence.py }
Run "Controle pack captures" { python .\tools\check_capture_pack.py }

Step "Captures prioritaires Wazuh et preflight"
Write-Host "1. CAP-01_wazuh-dashboard-login.png (deja extractible depuis le PDF SIEM, recapture live recommandee si possible)"
Write-Host "   Ouvrir https://localhost, se connecter admin / SecretPassword, capturer la page Dashboard connectee."
Write-Host "2. CAP-02_agents-poste01-serveur01.png (deja extractible depuis le PDF SIEM, recapture live recommandee si possible)"
Write-Host "   Wazuh > Agents, montrer poste-01 et serveur-01 actifs."
Write-Host "3. CAP-03_alerte-5712-brute-force-ssh.png (deja extractible depuis le PDF SIEM, recapture live recommandee si possible)"
Write-Host "   Wazuh > Security events, requete rule.id:5712, ouvrir le detail de l'alerte."
Write-Host "4. CAP-25_preflight-demo-ok.png (preuve restante : uniquement si Docker + Wazuh repondent)"
Write-Host "   Produit automatiquement par render_preflight_evidence.py seulement si Docker + Wazuh repondent."

if ($OpenBrowser) {
    Step "Ouverture navigateur"
    Start-Process "https://localhost"
    Start-Process (Join-Path $root "Dashboards_Offline\daylight_soc_dashboard.html")
}

Step "Apres captures"
Write-Host "Relancer :"
Write-Host "  python .\tools\build_capture_annex.py"
Write-Host "  C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\post_capture_finalize.ps1"


