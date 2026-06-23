param(
    [switch]$AllowWarnings
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$ps = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
$report = Join-Path $root "post-capture-finalize-report.txt"
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
        if ($AllowNonZero -or $AllowWarnings) {
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

Add-Line "=== Finalisation apres captures reelles - Daylight / Cyber Trust ==="
Add-Line "Racine : $root"
Add-Line "Date   : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Add-Line "Usage  : a lancer apres ajout de CAP-01, CAP-02, CAP-03, CAP-25 et du lien video/MP4."

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
Run-Step "Controle captures" { python .\tools\check_capture_pack.py } -AllowNonZero
Run-Step "Controle video" { python .\tools\check_video_ready.py } -AllowNonZero
Run-Step "Reconstruction annexe captures" { python .\tools\build_capture_annex.py }
Run-Step "Generation manifeste depot" { python .\tools\build_delivery_manifest.py }
Run-Step "Export PDF Markdown" { python .\tools\export_markdown_to_pdf.py } -AllowNonZero
Run-Step "Export PDF fallback Pillow" { python .\tools\export_markdown_to_pdf_pillow.py }
Run-Step "Fusion dossier groupe complet" { python .\tools\build_group_dossier_pdf.py }
Run-Step "Generation manifeste apres PDF" { python .\tools\build_delivery_manifest.py }
Run-Step "Reconstruction rendu final" { & $ps -ExecutionPolicy Bypass -File .\tools\rebuild_rendu_final.ps1 }
Run-Step "Validation rendu final" { python .\tools\validate_rendu_final.py } -AllowNonZero
Run-Step "Reconstruction finale avec rapport validation" { & $ps -ExecutionPolicy Bypass -File .\tools\rebuild_rendu_final.ps1 }

$zip = Join-Path $root "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip"
$zipHashPath = Join-Path $root "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip.sha256"
if (Test-Path -LiteralPath $zip) {
    $zipHash = Get-FileHash -Algorithm SHA256 -LiteralPath $zip
    Set-Content -LiteralPath $zipHashPath -Value "$($zipHash.Hash.ToLower())  PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip" -Encoding UTF8
    Add-Line ""
    Add-Line "ZIP      : $zip"
    Add-Line "SHA-256  : $($zipHash.Hash.ToLower())"
    Add-Line "Hash txt : $zipHashPath"
}

$pdfCount = 0
$captureCount = 0
if (Test-Path -LiteralPath ".\Rendu_Final\Rendus_PDF") {
    $pdfCount = @(Get-ChildItem -LiteralPath ".\Rendu_Final\Rendus_PDF" -Filter "*.pdf" -File -ErrorAction SilentlyContinue).Count
}
if (Test-Path -LiteralPath ".\Rendu_Final\Annexes_Captures") {
    $captureCount = @(Get-ChildItem -LiteralPath ".\Rendu_Final\Annexes_Captures" -Filter "CAP-*.png" -File -ErrorAction SilentlyContinue).Count
}
Add-Line "PDF      : $pdfCount"
Add-Line "Captures : $captureCount"
Add-Line "Rapport  : $report"

Set-Content -LiteralPath $report -Value $lines -Encoding UTF8
$finalReportDir = Join-Path $root "Rendu_Final\Rapports_Finalisation"
if (!(Test-Path -LiteralPath $finalReportDir)) {
    New-Item -ItemType Directory -Path $finalReportDir | Out-Null
}
Copy-Item -LiteralPath $report -Destination (Join-Path $finalReportDir "post-capture-finalize-report.txt") -Force
Compress-Archive -Path (Join-Path $root "Rendu_Final\*") -DestinationPath $zip -Force
$zipHash = Get-FileHash -Algorithm SHA256 -LiteralPath $zip
Set-Content -LiteralPath $zipHashPath -Value "$($zipHash.Hash.ToLower())  PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip" -Encoding UTF8






