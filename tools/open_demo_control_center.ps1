param(
    [switch]$NoOpen
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$folderName = Split-Path -Leaf $scriptDir
if ($folderName -in @("tools", "Outils")) {
    $root = Split-Path -Parent $scriptDir
} else {
    $root = $scriptDir
}

$toolsDir = Join-Path $root "tools"
if (!(Test-Path -LiteralPath $toolsDir)) {
    $toolsDir = Join-Path $root "Outils"
}

$builder = Join-Path $toolsDir "build_demo_control_center.py"
$html = Join-Path $root "Dashboards_Offline\daylight_demo_control_center.html"

Write-Host "=== Daylight / Cyber Trust - ouverture centre de controle ==="
Write-Host "Racine : $root"

if (Test-Path -LiteralPath $builder) {
    Push-Location $root
    try {
        python $builder
    } finally {
        Pop-Location
    }
} else {
    Write-Host "[WARN] Generateur introuvable : $builder"
}

if (!(Test-Path -LiteralPath $html)) {
    throw "Centre de controle introuvable : $html"
}

Write-Host "[OK] Centre de controle : $html"
Write-Host ""
Write-Host "Supports utiles :"
Write-Host "- Dashboard demo : $html"
Write-Host "- Teleprompteur : $(Join-Path $root 'Dashboards_Offline\daylight_video_teleprompter.html')"
Write-Host "- Dashboard SOC : $(Join-Path $root 'Dashboards_Offline\daylight_soc_dashboard.html')"
Write-Host "- Dossier groupe : $(Join-Path $root 'Rendus_PDF\PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_DossierGroupeComplet.pdf')"
Write-Host ""
$toolCommandDir = if (Test-Path -LiteralPath (Join-Path $root "tools")) { "tools" } else { "Outils" }
Write-Host "Commandes finales apres preuves reelles :"
Write-Host "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\$toolCommandDir\repair_lab_and_capture_cap25.ps1 -StartDockerDesktop -StartKnownContainers -WaitSeconds 180"
Write-Host "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\$toolCommandDir\post_capture_finalize.ps1 -AllowWarnings"

if (!$NoOpen) {
    Start-Process -FilePath $html
}


