param(
    [ValidateSet("", "CAP-01", "CAP-02", "CAP-03", "CAP-25", "VIDEO-LINK", "VIDEO-MP4")]
    [string]$Item = "",
    [string]$SourcePath = "",
    [string]$YoutubeUrl = "",
    [switch]$RunChecks,
    [switch]$Finalize
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$ps = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
Set-Location $root

$captureTargets = @{
    "CAP-01" = "CAP-01_wazuh-dashboard-login.png"
    "CAP-02" = "CAP-02_agents-poste01-serveur01.png"
    "CAP-03" = "CAP-03_alerte-5712-brute-force-ssh.png"
    "CAP-25" = "CAP-25_preflight-demo-ok.png"
}

function Show-Usage {
    Write-Host "=== Import preuves finales Daylight / Cyber Trust ==="
    Write-Host ""
    Write-Host "Captures :"
    Write-Host "  .\tools\import_final_evidence.ps1 -Item CAP-01 -SourcePath C:\Temp\capture.png -RunChecks"
    Write-Host "  .\tools\import_final_evidence.ps1 -Item CAP-02 -SourcePath C:\Temp\capture.png -RunChecks"
    Write-Host "  .\tools\import_final_evidence.ps1 -Item CAP-03 -SourcePath C:\Temp\capture.png -RunChecks"
    Write-Host "  .\tools\import_final_evidence.ps1 -Item CAP-25"
    Write-Host ""
    Write-Host "Video :"
    Write-Host "  .\tools\import_final_evidence.ps1 -Item VIDEO-LINK -YoutubeUrl https://youtu.be/xxxxx -RunChecks"
    Write-Host "  .\tools\import_final_evidence.ps1 -Item VIDEO-MP4 -SourcePath C:\Temp\demo.mp4 -RunChecks"
    Write-Host ""
    Write-Host "Finalisation complete apres toutes les preuves :"
    Write-Host "  .\tools\import_final_evidence.ps1 -Item VIDEO-LINK -YoutubeUrl https://youtu.be/xxxxx -Finalize"
}

function Ensure-Dir {
    param([string]$Path)
    if (!(Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
    }
}

function Import-Capture {
    param([string]$CapId, [string]$Path)
    $targetName = $captureTargets[$CapId]
    $captureDir = Join-Path $root "Annexes_Captures"
    $target = Join-Path $captureDir $targetName
    Ensure-Dir $captureDir

    if ($CapId -eq "CAP-25" -and [string]::IsNullOrWhiteSpace($Path)) {
        Write-Host "[INFO] CAP-25 demande sans SourcePath : tentative de generation depuis le preflight."
        & python .\tools\render_preflight_evidence.py
        if (!(Test-Path -LiteralPath $target)) {
            throw "CAP-25 non genere. Relancer Docker/Wazuh, executer preflight_demo.ps1 -WriteReport, puis reessayer."
        }
        return
    }

    if ([string]::IsNullOrWhiteSpace($Path)) {
        throw "SourcePath obligatoire pour $CapId."
    }
    if (!(Test-Path -LiteralPath $Path)) {
        throw "Fichier source introuvable : $Path"
    }
    $source = Get-Item -LiteralPath $Path
    if ($source.Extension.ToLowerInvariant() -ne ".png") {
        throw "Le fichier source doit etre un PNG pour rester coherent avec la checklist : $($source.Name)"
    }
    if ($source.Length -lt 10kb) {
        throw "Capture trop petite pour etre exploitable : $($source.Length) octets"
    }

    Copy-Item -LiteralPath $source.FullName -Destination $target -Force
    Write-Host "[OK] Capture importee : $target"
}

function Import-VideoLink {
    param([string]$Url)
    if ([string]::IsNullOrWhiteSpace($Url)) {
        throw "YoutubeUrl obligatoire pour VIDEO-LINK."
    }
    if ($Url -notmatch "^https?://") {
        throw "URL invalide : elle doit commencer par http:// ou https://"
    }
    if ($Url -notmatch "youtube\.com|youtu\.be") {
        throw "URL invalide : utiliser un lien YouTube non repertorie."
    }
    $target = Join-Path $root "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt"
    Set-Content -LiteralPath $target -Value $Url -Encoding UTF8
    Write-Host "[OK] Lien video ecrit : $target"
}

function Import-VideoMp4 {
    param([string]$Path)
    if ([string]::IsNullOrWhiteSpace($Path)) {
        throw "SourcePath obligatoire pour VIDEO-MP4."
    }
    if (!(Test-Path -LiteralPath $Path)) {
        throw "MP4 source introuvable : $Path"
    }
    $source = Get-Item -LiteralPath $Path
    if ($source.Extension.ToLowerInvariant() -ne ".mp4") {
        throw "Le fichier video doit etre un MP4 : $($source.Name)"
    }
    if ($source.Length -lt 10mb) {
        throw "MP4 trop petit pour etre accepte par le controle video : $($source.Length) octets"
    }
    $target = Join-Path $root "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4"
    Copy-Item -LiteralPath $source.FullName -Destination $target -Force
    Write-Host "[OK] MP4 final importe : $target"
}

if ([string]::IsNullOrWhiteSpace($Item)) {
    Show-Usage
    exit 0
}

if ($captureTargets.ContainsKey($Item)) {
    Import-Capture -CapId $Item -Path $SourcePath
} elseif ($Item -eq "VIDEO-LINK") {
    Import-VideoLink -Url $YoutubeUrl
} elseif ($Item -eq "VIDEO-MP4") {
    Import-VideoMp4 -Path $SourcePath
}

if ($RunChecks -or $Finalize) {
    Write-Host ""
    Write-Host "=== Controles apres import ==="
    & python .\tools\check_capture_pack.py
    & python .\tools\check_video_ready.py
}

if ($Finalize) {
    Write-Host ""
    Write-Host "=== Reconstruction finale ==="
    & $ps -ExecutionPolicy Bypass -File .\tools\post_capture_finalize.ps1
}
