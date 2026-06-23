param(
    [switch]$NoOpen,
    [switch]$OpenAll,
    [switch]$OpenCoreOnly
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$folderName = Split-Path -Leaf $scriptDir
if ($folderName -in @("tools", "Outils")) {
    $root = Split-Path -Parent $scriptDir
} else {
    $root = $scriptDir
}

function Resolve-DaylightPath {
    param([string]$RelativePath)
    $candidates = @(
        (Join-Path $root $RelativePath),
        (Join-Path $root ($RelativePath -replace '^config/', 'Config_')),
        (Join-Path $root ($RelativePath -replace '^Rendus_PDF/', 'Rendus_PDF\')),
        (Join-Path $root ($RelativePath -replace '/', '\'))
    )
    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }
    return (Join-Path $root ($RelativePath -replace '/', '\'))
}

function Add-Line {
    param([string]$Line = "")
    $script:Lines.Add($Line) | Out-Null
    Write-Host $Line
}

Set-Location $root
$script:Lines = New-Object System.Collections.Generic.List[string]
$orderCsv = Join-Path $root "config\video\daylight_video_open_order.csv"
if (!(Test-Path -LiteralPath $orderCsv)) {
    $orderCsv = Join-Path $root "Config_Video\daylight_video_open_order.csv"
}
if (!(Test-Path -LiteralPath $orderCsv)) {
    throw "Ordre d'ouverture introuvable : config\video\daylight_video_open_order.csv"
}

$rows = Import-Csv -LiteralPath $orderCsv
$report = Join-Path $root "video-recording-launcher-report.txt"
$coreLabels = @("Centre controle demo", "Teleprompteur video", "Pack enregistrement video", "Runbook immediat", "Fichier lien video")

Add-Line "=== Lanceur session enregistrement video - Daylight / Cyber Trust ==="
Add-Line "Racine : $root"
Add-Line "Date   : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Add-Line "Mode   : NoOpen=$NoOpen ; OpenAll=$OpenAll ; OpenCoreOnly=$OpenCoreOnly"
Add-Line ""
Add-Line "## Ordre d'ouverture"

$missing = 0
foreach ($row in $rows) {
    $target = Resolve-DaylightPath $row.path
    $exists = Test-Path -LiteralPath $target
    if (!$exists) { $missing += 1 }
    $status = if ($exists) { "OK" } else { "WARN" }
    Add-Line ("[{0}] {1}. {2} - {3}" -f $status, $row.order, $row.label, $target)
    Add-Line ("     Usage : {0}" -f $row.why)
}

Add-Line ""
Add-Line "## Actions conseillees"
Add-Line "1. Lancer OBS/Teams et verifier le micro."
Add-Line "2. Ouvrir les supports ci-dessus dans l'ordre."
Add-Line "3. Enregistrer 15 a 20 minutes avec les 4 membres."
Add-Line "4. Publier YouTube non repertorie ou deposer le MP4 final."
Add-Line "5. Coller l'URL dans PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt."
Add-Line "6. Relancer tools\post_capture_finalize.ps1 -AllowWarnings."

if ($missing -gt 0) {
    Add-Line ""
    Add-Line "[WARN] $missing support(s) introuvable(s). Corriger avant tournage."
} else {
    Add-Line ""
    Add-Line "[OK] Tous les supports d'enregistrement attendus sont presents."
}

$shouldOpen = (!$NoOpen) -and ($OpenAll -or $OpenCoreOnly)
if ($shouldOpen) {
    $toOpen = if ($OpenAll) { $rows } else { @($rows | Where-Object { $coreLabels -contains $_.label }) }
    Add-Line ""
    Add-Line "## Ouverture des supports"
    foreach ($row in $toOpen) {
        $target = Resolve-DaylightPath $row.path
        if (Test-Path -LiteralPath $target) {
            Start-Process -FilePath $target
            Add-Line "[OPEN] $($row.label)"
        } else {
            Add-Line "[SKIP] $($row.label) introuvable"
        }
    }
} else {
    Add-Line ""
    Add-Line "[INFO] Aucun fichier ouvert. Relancer avec -OpenCoreOnly ou -OpenAll pour ouvrir les supports."
}

Set-Content -LiteralPath $report -Value $script:Lines -Encoding UTF8
Add-Line ""
Add-Line "Rapport ecrit : $report"
