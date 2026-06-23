param(
    [switch]$SkipPowerPoint
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$ps = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
$report = Join-Path $root "finalize-project-report.txt"
$lines = New-Object System.Collections.Generic.List[string]

function Add-Line {
    param([string]$Line = "")
    $lines.Add($Line) | Out-Null
    Write-Host $Line
}

function Run-Step {
    param(
        [string]$Name,
        [scriptblock]$Action,
        [switch]$AllowNonZero
    )

    Add-Line ""
    Add-Line "=== $Name ==="
    $global:LASTEXITCODE = 0
    & $Action
    $code = $global:LASTEXITCODE
    if ($null -eq $code) { $code = 0 }

    if ($code -ne 0) {
        if ($AllowNonZero) {
            Add-Line "[WARN] $Name termine avec code $code, continuation autorisee."
        } else {
            Add-Line "[FAIL] $Name termine avec code $code."
            Set-Content -LiteralPath $report -Value $lines -Encoding UTF8
            throw "$Name a echoue avec code $code"
        }
    } else {
        Add-Line "[OK] $Name"
    }
}

Set-Location $root

Add-Line "=== Finalisation projet Daylight / Cyber Trust ==="
Add-Line "Racine : $root"
Add-Line "Date   : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Add-Line "Note   : les avertissements attendus avant depot officiel concernent les captures Wazuh/preflight et le lien video."

Run-Step "Generation logs demo concrets" { python .\tools\generate_demo_logs.py }
Run-Step "Generation images preuves statiques" { python .\tools\render_static_proof_images.py }
Run-Step "Generation dashboard SOC offline" { python .\tools\build_offline_soc_dashboard.py }
Run-Step "Extraction preuves Wazuh Youssef" { python .\tools\extract_youssef_wazuh_proofs.py }
Run-Step "Generation preuves documentaires" { python .\tools\render_documentary_proof_images.py }
Run-Step "Generation teleprompteur video" { python .\tools\build_video_teleprompter.py }
Run-Step "Generation overlays video" { python .\tools\build_video_overlays.py }
Run-Step "Generation pack enregistrement video" { python .\tools\build_video_recording_pack.py }
Run-Step "Controle lanceur enregistrement video" { & $ps -ExecutionPolicy Bypass -File .\tools\launch_video_recording_session.ps1 -NoOpen }
Run-Step "Generation pack defense jury" { python .\tools\build_jury_defense_pack.py }
Run-Step "Generation matrice conformite" { python .\tools\build_compliance_matrix.py }
Run-Step "Generation pack demo pfSense" { python .\tools\build_pfsense_demo_pack.py }
Run-Step "Generation dashboard statut preuves" { python .\tools\build_final_evidence_dashboard.py } -AllowNonZero
Run-Step "Generation centre controle demo" { python .\tools\build_demo_control_center.py }
Run-Step "Generation annexe captures" { python .\tools\build_capture_annex.py }
Run-Step "Verification pack captures" { python .\tools\check_capture_pack.py } -AllowNonZero
Run-Step "Generation manifeste depot" { python .\tools\build_delivery_manifest.py }
Run-Step "Export PDF Markdown" { python .\tools\export_markdown_to_pdf.py } -AllowNonZero
Run-Step "Export PDF fallback Pillow" { python .\tools\export_markdown_to_pdf_pillow.py }

if ($SkipPowerPoint) {
    Add-Line ""
    Add-Line "[INFO] Generation PowerPoint ignoree via -SkipPowerPoint."
} else {
    Run-Step "Generation PowerPoint" { python .\tools\build_presentation_pptx.py }
}

Run-Step "Fusion dossier groupe complet" { python .\tools\build_group_dossier_pdf.py }
Run-Step "Preflight demo" { & $ps -ExecutionPolicy Bypass -File .\tools\preflight_demo.ps1 -WriteReport }
Run-Step "Generation preuve preflight" { python .\tools\render_preflight_evidence.py } -AllowNonZero
Run-Step "Verification video" { python .\tools\check_video_ready.py } -AllowNonZero
Run-Step "Generation annexe captures apres preflight" { python .\tools\build_capture_annex.py }
Run-Step "Generation manifeste depot apres preflight" { python .\tools\build_delivery_manifest.py }
Run-Step "Export PDF Markdown apres preflight" { python .\tools\export_markdown_to_pdf.py } -AllowNonZero
Run-Step "Export PDF fallback Pillow apres preflight" { python .\tools\export_markdown_to_pdf_pillow.py }
Run-Step "Fusion dossier groupe complet apres preflight" { python .\tools\build_group_dossier_pdf.py }
Run-Step "Reconstruction rendu final avant validation" { & $ps -ExecutionPolicy Bypass -File .\tools\rebuild_rendu_final.ps1 }
Run-Step "Validation rendu final" { python .\tools\validate_rendu_final.py } -AllowNonZero
Run-Step "Reconstruction rendu final apres validation" { & $ps -ExecutionPolicy Bypass -File .\tools\rebuild_rendu_final.ps1 }
Run-Step "Generation manifeste depot final local" { python .\tools\build_delivery_manifest.py }

Add-Line ""
Add-Line "=== Synthese finale ==="
$zip = Join-Path $root "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip"
$pdfDir = Join-Path $root "Rendu_Final\Rendus_PDF"
$captureDir = Join-Path $root "Rendu_Final\Annexes_Captures"
$videoTxt = Join-Path $root "Rendu_Final\Video\PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt"

$pdfCount = 0
if (Test-Path -LiteralPath $pdfDir) {
    $pdfCount = @(Get-ChildItem -LiteralPath $pdfDir -Filter "*.pdf" -File -ErrorAction SilentlyContinue).Count
}

$captureCount = 0
if (Test-Path -LiteralPath $captureDir) {
    $captureCount = @(Get-ChildItem -LiteralPath $captureDir -Filter "CAP-*.png" -File -ErrorAction SilentlyContinue).Count
}

$videoReady = $false
if (Test-Path -LiteralPath $videoTxt) {
    $videoText = Get-Content -Raw -LiteralPath $videoTxt
    $videoReady = ($videoText -match "https?://") -and ($videoText -notmatch "Coller ici")
}

if (Test-Path -LiteralPath $zip) {
    $zipItem = Get-Item -LiteralPath $zip
    Add-Line "ZIP      : $($zipItem.FullName)"
    Add-Line "Taille   : $($zipItem.Length) octets"
} else {
    Add-Line "ZIP      : introuvable"
}
Add-Line "PDF      : $pdfCount"
Add-Line "Captures : $captureCount"
Add-Line "Video    : $(if ($videoReady) { 'lien detecte' } else { 'lien manquant' })"

Add-Line "Rapport  : $report"
Add-Line "[OK] Rapport finalisation inclus dans le ZIP"
Set-Content -LiteralPath $report -Value $lines -Encoding UTF8

$finalReportDir = Join-Path $root "Rendu_Final\Rapports_Finalisation"
if (!(Test-Path -LiteralPath $finalReportDir)) {
    New-Item -ItemType Directory -Path $finalReportDir | Out-Null
}
$manifestDir = Join-Path $root "Rendu_Final\Manifeste_Depot"
if (!(Test-Path -LiteralPath $manifestDir)) {
    New-Item -ItemType Directory -Path $manifestDir | Out-Null
}
Copy-Item -LiteralPath (Join-Path $root "MANIFEST_DEPOT.md") -Destination (Join-Path $manifestDir "MANIFEST_DEPOT.md") -Force
Copy-Item -LiteralPath (Join-Path $root "MANIFEST_DEPOT.json") -Destination (Join-Path $manifestDir "MANIFEST_DEPOT.json") -Force
Copy-Item -LiteralPath $report -Destination (Join-Path $finalReportDir "finalize-project-report.txt") -Force
Compress-Archive -Path (Join-Path $root "Rendu_Final\*") -DestinationPath $zip -Force
$zipHashPath = Join-Path $root "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip.sha256"
$zipHash = Get-FileHash -Algorithm SHA256 -LiteralPath $zip
Set-Content -LiteralPath $zipHashPath -Value "$($zipHash.Hash.ToLower())  PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip" -Encoding UTF8
Add-Line "Hash ZIP : $zipHashPath"












