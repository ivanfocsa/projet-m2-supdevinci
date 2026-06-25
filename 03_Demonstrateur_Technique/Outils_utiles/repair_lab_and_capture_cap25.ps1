param(
    [switch]$StartDockerDesktop,
    [switch]$StartKnownContainers,
    [switch]$RunYoussefSetup,
    [switch]$FinalizeIfReady,
    [int]$WaitSeconds = 90
)

$ErrorActionPreference = "Continue"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$folderName = Split-Path -Leaf $scriptDir
if ($folderName -in @("tools", "Outils")) {
    $root = Split-Path -Parent $scriptDir
} else {
    $root = $scriptDir
}

$toolDir = if (Test-Path -LiteralPath (Join-Path $root "tools")) { "tools" } else { "Outils" }
$toolPath = Join-Path $root $toolDir
$ps = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
$report = Join-Path $root "lab-cap25-recovery-report.txt"
$capture = Join-Path $root "Annexes_Captures\CAP-25_preflight-demo-ok.png"
$retry = Join-Path $root "Annexes_Captures\PRE-25_preflight-a-reprendre.png"
$lines = New-Object System.Collections.Generic.List[string]

function Add-Line {
    param([string]$Line = "")
    $lines.Add($Line) | Out-Null
    Write-Host $Line
}

function Run-CaptureCommand {
    param(
        [string]$Title,
        [scriptblock]$Action
    )
    Add-Line ""
    Add-Line "### $Title"
    try {
        $output = & $Action 2>&1
        $code = $LASTEXITCODE
        if ($null -eq $code) { $code = 0 }
        foreach ($line in $output) {
            Add-Line "  $line"
        }
        Add-Line "  exit_code=$code"
        return $code -eq 0
    } catch {
        Add-Line "  ERROR: $($_.Exception.Message)"
        return $false
    }
}

function Test-DockerDaemon {
    try {
        docker info *> $null
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

function Test-WazuhDashboard {
    try {
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
        [System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }
        $response = Invoke-WebRequest -UseBasicParsing -Uri "https://localhost" -TimeoutSec 8 -ErrorAction Stop
        if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) {
            return $true
        }
    } catch {
    }

    if (Get-Command python -ErrorAction SilentlyContinue) {
        try {
            $pythonCode = "import ssl, urllib.request; ctx=ssl._create_unverified_context(); r=urllib.request.urlopen('https://localhost', context=ctx, timeout=8); print(r.status)"
            $status = & python -c $pythonCode 2>$null
            if ($LASTEXITCODE -eq 0 -and "$status" -match "^\d+") {
                $code = [int]("$status".Trim())
                return ($code -ge 200 -and $code -lt 500)
            }
        } catch {
        }
    }

    return $false
}

function Start-DockerDesktopIfRequested {
    if (!$StartDockerDesktop) {
        Add-Line "[INFO] StartDockerDesktop non demande. Aucun lancement GUI automatique."
        return
    }

    $candidates = @(
        "C:\Program Files\Docker\Docker\Docker Desktop.exe",
        "$env:LOCALAPPDATA\Docker\Docker Desktop.exe"
    )
    $dockerDesktop = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if (!$dockerDesktop) {
        Add-Line "[WARN] Docker Desktop introuvable dans les chemins standards."
        return
    }

    Add-Line "[ACTION] Lancement Docker Desktop : $dockerDesktop"
    Start-Process -FilePath $dockerDesktop -WindowStyle Minimized
}

function Wait-Docker {
    param([int]$Seconds)
    $deadline = (Get-Date).AddSeconds($Seconds)
    while ((Get-Date) -lt $deadline) {
        if (Test-DockerDaemon) {
            Add-Line "[OK] Docker daemon repond."
            return $true
        }
        Start-Sleep -Seconds 5
        Add-Line "[WAIT] Docker daemon pas encore disponible..."
    }
    Add-Line "[WARN] Docker daemon ne repond toujours pas apres $Seconds secondes."
    return $false
}

function Get-DockerRows {
    try {
        return @(docker ps -a --format "{{.Names}}|{{.Status}}" 2>$null)
    } catch {
        return @()
    }
}

function Start-KnownContainersIfRequested {
    if (!$StartKnownContainers) {
        Add-Line "[INFO] StartKnownContainers non demande. Aucun docker start automatique."
        return
    }

    $rows = Get-DockerRows
    if ($rows.Count -eq 0) {
        Add-Line "[WARN] Aucun conteneur detecte par docker ps -a."
        return
    }

    $namesToStart = New-Object System.Collections.Generic.List[string]
    foreach ($row in $rows) {
        $parts = $row -split "\|", 2
        if ($parts.Count -lt 2) { continue }
        $name = $parts[0]
        $status = $parts[1]
        $isKnown = ($name -match "wazuh") -or ($name -eq "serveur-01") -or ($name -match "daylight")
        $isStopped = $status -match "Exited|Created"
        if ($isKnown -and $isStopped) {
            $namesToStart.Add($name) | Out-Null
        }
    }

    if ($namesToStart.Count -eq 0) {
        Add-Line "[INFO] Aucun conteneur Wazuh/Daylight/serveur-01 arrete a demarrer."
        return
    }

    foreach ($name in $namesToStart) {
        Add-Line "[ACTION] docker start $name"
        docker start $name | ForEach-Object { Add-Line "  $_" }
    }
}

function Run-YoussefSetupIfRequested {
    if (!$RunYoussefSetup) {
        Add-Line "[INFO] RunYoussefSetup non demande. Le script SIEM de Youssef n'est pas execute automatiquement."
        return
    }

    $sourceSetup = Join-Path $root "Youssef GUERNIOU\setup-siem-lab.ps1"
    $finalSetup = Join-Path $root "Preuves_SIEM_Youssef\setup-siem-lab.ps1"
    $setup = if (Test-Path -LiteralPath $sourceSetup) { $sourceSetup } else { $finalSetup }
    if (!(Test-Path -LiteralPath $setup)) {
        Add-Line "[WARN] setup-siem-lab.ps1 introuvable."
        return
    }

    Add-Line "[ACTION] Execution setup SIEM : $setup"
    & $ps -ExecutionPolicy Bypass -File $setup
}

Set-Location $root
Add-Line "=== Relance lab et generation CAP-25 - Daylight / Cyber Trust ==="
Add-Line "Racine : $root"
Add-Line "Date   : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Add-Line "Mode   : StartDockerDesktop=$StartDockerDesktop ; StartKnownContainers=$StartKnownContainers ; RunYoussefSetup=$RunYoussefSetup ; FinalizeIfReady=$FinalizeIfReady"

$hasDocker = [bool](Get-Command docker -ErrorAction SilentlyContinue)
if (!$hasDocker) {
    Add-Line "[WARN] Commande docker introuvable. Installer/lancer Docker Desktop avant CAP-25."
} else {
    Add-Line "[OK] Commande docker disponible."
}

Start-DockerDesktopIfRequested
$dockerOk = $false
if ($hasDocker) {
    $dockerOk = Wait-Docker -Seconds $WaitSeconds
}

if ($dockerOk) {
    Run-CaptureCommand "docker ps -a" { docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" } | Out-Null
    Start-KnownContainersIfRequested
    Run-YoussefSetupIfRequested
    Run-CaptureCommand "docker ps -a apres actions" { docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" } | Out-Null
}

$wazuhOk = Test-WazuhDashboard
if ($wazuhOk) {
    Add-Line "[OK] Wazuh Dashboard repond sur https://localhost."
} else {
    Add-Line "[WARN] Wazuh Dashboard ne repond pas encore sur https://localhost."
}

$preflightScript = Join-Path $toolPath "preflight_demo.ps1"
$renderScript = Join-Path $toolPath "render_preflight_evidence.py"
$checkScript = Join-Path $toolPath "check_capture_pack.py"
$finalizeScript = Join-Path $toolPath "post_capture_finalize.ps1"

if (Test-Path -LiteralPath $preflightScript) {
    Run-CaptureCommand "Preflight officiel" { & $ps -ExecutionPolicy Bypass -File $preflightScript -WriteReport } | Out-Null
} else {
    Add-Line "[WARN] preflight_demo.ps1 introuvable : $preflightScript"
}

if (Test-Path -LiteralPath $renderScript) {
    Run-CaptureCommand "Generation image CAP-25 si preflight OK" { python $renderScript } | Out-Null
} else {
    Add-Line "[WARN] render_preflight_evidence.py introuvable : $renderScript"
}

if (Test-Path -LiteralPath $capture) {
    Add-Line "[OK] CAP-25 genere : $capture"
    if (Test-Path -LiteralPath $checkScript) {
        Run-CaptureCommand "Controle captures apres CAP-25" { python $checkScript } | Out-Null
    }
    if ($FinalizeIfReady -and (Test-Path -LiteralPath $finalizeScript)) {
        Run-CaptureCommand "Finalisation demandee" { & $ps -ExecutionPolicy Bypass -File $finalizeScript -AllowWarnings } | Out-Null
    }
} else {
    Add-Line "[WARN] CAP-25 non genere. Image d'attente possible : $retry"
    Add-Line ""
    Add-Line "Actions concretes restantes :"
    Add-Line "- Ouvrir Docker Desktop, attendre l'etat Running, puis relancer ce script avec -StartKnownContainers."
    Add-Line "- Si les conteneurs Wazuh existent mais sont arretes : utiliser -StartKnownContainers."
    Add-Line "- Si le lab de Youssef doit etre initialise : relancer avec -RunYoussefSetup."
    Add-Line "- Quand https://localhost repond, relancer ce script puis post_capture_finalize.ps1."
}

Set-Content -LiteralPath $report -Value $lines -Encoding UTF8
Add-Line ""
Add-Line "Rapport ecrit : $report"
Set-Content -LiteralPath $report -Value $lines -Encoding UTF8

if (Test-Path -LiteralPath $capture) {
    exit 0
}
exit 1


