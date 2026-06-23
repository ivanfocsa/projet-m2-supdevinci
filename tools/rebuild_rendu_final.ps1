param(
    [string]$ZipName = "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$final = Join-Path $root "Rendu_Final"

function Ensure-Dir {
    param([string]$Path)
    if (!(Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
    }
}

function Copy-ExistingLiteral {
    param(
        [string[]]$Paths,
        [string]$Destination
    )
    Ensure-Dir $Destination
    foreach ($path in $Paths) {
        $full = Join-Path $root $path
        if (Test-Path -LiteralPath $full) {
            Copy-Item -LiteralPath $full -Destination $Destination -Force
            Write-Host "[OK] Copie : $path"
        } else {
            Write-Host "[WARN] Introuvable : $path"
        }
    }
}

Set-Location $root

$folders = @(
    "Sources_Markdown",
    "Rendus_PDF",
    "Annexes_Captures",
    "Preuves_SIEM_Youssef",
    "Outils",
    "Config_PfSense",
    "Config_Wazuh",
    "Config_Lab",
    "Config_Captures",
    "Config_Video",
    "Config_Compliance",
    "Demo_Logs",
    "Dashboards_Offline",
    "Solutions_Concretes",
    "Manifeste_Depot",
    "Video",
    "Presentation",
    "Rapports_Preflight",
    "Rapports_Validation",
    "Rapports_Finalisation",
    "Rapports_Captures",
    "Rapports_Video",
    "Video_Overlays"
)

Ensure-Dir $final
foreach ($folder in $folders) {
    Ensure-Dir (Join-Path $final $folder)
}

Copy-ExistingLiteral @("README_LIVRABLES.md") $final
Copy-ExistingLiteral @("MANIFEST_DEPOT.md", "MANIFEST_DEPOT.json") (Join-Path $final "Manifeste_Depot")
if (Test-Path -LiteralPath (Join-Path $final "README_LIVRABLES.md")) {
    Copy-Item -LiteralPath (Join-Path $final "README_LIVRABLES.md") -Destination (Join-Path $final "README_A_LIRE.md") -Force
}

$groupSources = @(
    "00_REGISTRE_EXIGENCES_ET_SYNTHESE.md",
    "01_RAPPORT_TECHNIQUE_GROUPE.md",
    "02_GUIDE_DEPLOIEMENT_UTILISATION.md",
    "03_PLAYBOOKS_PROCEDURES_REX.md",
    "04_SCRIPT_VIDEO_DEMO.md",
    "05_BACKLOG_PLANNING.md",
    "06_SUPPORT_PRESENTATION.md",
    "07_DOSSIER_PREUVES_CAPTURES.md",
    "08_AUDIT_FINAL_CONSIGNES.md",
    "09_NOTES_ORATEUR_SOUTENANCE.md",
    "10_MODE_OPERATOIRE_DEMO_JOUR_J.md",
    "11_CHECKLIST_DEPOT_FINAL.md",
    "12_RISQUES_RGPD_CONFORMITE.md",
    "13_PLAN_RECETTE_ACCEPTATION.md",
    "14_SYNTHESE_EXECUTIVE_CLIENT.md",
    "15_QA_SOUTENANCE_JURY_CLIENT.md",
    "16_ANNEXE_CAPTURES_WAZUH.md",
    "17_DOSSIER_GROUPE_COMPLET_INDEX.md",
    "18_SOLUTIONS_CONCRETES_DEMO.md",
    "19_ROLES_CONTRIBUTIONS_PREUVES.md",
    "20_MODE_OPERATOIRE_PFSENSE_WAZUH_LAB.md",
    "21_DASHBOARDS_ALERTES_QUALIFICATION.md",
    "22_EXPLOITATION_VM_RUNBOOK_REX.md",
    "23_PREUVES_FINALES_CAPTURES_VIDEO_DEPOT.md",
    "24_DASHBOARD_SOC_OFFLINE.md",
    "25_MODE_OPERATOIRE_CAPTURE_WAZUH_PREUVES.md",
    "26_MODE_OPERATOIRE_VIDEO_DEPOT.md",
    "27_MANIFESTE_DEPOT_ET_INTEGRITE.md",
    "28_RUNBOOK_EXPRESS_PREUVES_RESTANTES.md",
    "29_IMPORT_PREUVES_FINALES.md",
    "30_TABLEAU_BORD_STATUT_FINAL.md",
    "31_PACK_SOUTENANCE_JURY.md",
    "32_MATRICE_CONFORMITE_CAHIER_DES_CHARGES.md",
    "33_RUNBOOK_ENREGISTREMENT_VIDEO_IMMEDIAT.md",
    "Yvan FOCSA\PE-2526_M2CS_YvanFOCSA.md",
    "Youssef GUERNIOU\PE-2526_M2CS_YoussefGUERNIOU.md",
    "Kilyan FELIX\PE-2526_M2CS_KilyanFELIX.md",
    "Mahamadou DIACOUMBA\PE-2526_M2CS_MahamadouDIACOUMBA.md"
)
Copy-ExistingLiteral $groupSources (Join-Path $final "Sources_Markdown")

if (Test-Path -LiteralPath (Join-Path $root "Rendus_PDF")) {
    Copy-Item -Path (Join-Path $root "Rendus_PDF\*.pdf") -Destination (Join-Path $final "Rendus_PDF") -Force
    Write-Host "[OK] PDF copies"
}

Copy-ExistingLiteral @("Presentation_Daylight_CyberTrust.pptx") (Join-Path $final "Presentation")
Copy-ExistingLiteral @(
    "Youssef GUERNIOU\Documentation_SIEM_Youssef_GUERNIOU.pdf",
    "Youssef GUERNIOU\setup-siem-lab.ps1"
) (Join-Path $final "Preuves_SIEM_Youssef")
Copy-ExistingLiteral @(
    "tools\export_markdown_to_pdf.py",
    "tools\export_markdown_to_pdf_pillow.py",
    "tools\build_presentation_pptx.py",
    "tools\preflight_demo.ps1",
    "tools\rebuild_rendu_final.ps1",
    "tools\build_capture_annex.py",
    "tools\build_group_dossier_pdf.py",
    "tools\validate_rendu_final.py",
    "tools\finalize_project.ps1",
    "tools\generate_demo_logs.py",
    "tools\send_demo_logs_to_syslog.py",
    "tools\render_static_proof_images.py",
    "tools\build_offline_soc_dashboard.py",
    "tools\render_preflight_evidence.py",
    "tools\prepare_capture_session.ps1",
    "tools\check_video_ready.py",
    "tools\check_capture_pack.py",
    "tools\build_delivery_manifest.py",
    "tools\post_capture_finalize.ps1",
    "tools\import_final_evidence.ps1",
    "tools\build_final_evidence_dashboard.py",
    "tools\extract_youssef_wazuh_proofs.py",
    "tools\render_documentary_proof_images.py",
    "tools\build_video_teleprompter.py",
    "tools\build_video_overlays.py",
    "tools\build_video_recording_pack.py",
    "tools\build_jury_defense_pack.py",
    "tools\build_compliance_matrix.py",
    "tools\build_pfsense_demo_pack.py",
    "tools\build_demo_control_center.py",
    "tools\open_demo_control_center.ps1",
    "tools\launch_video_recording_session.ps1",
    "tools\repair_lab_and_capture_cap25.ps1"
) (Join-Path $final "Outils")
Copy-ExistingLiteral @("18_SOLUTIONS_CONCRETES_DEMO.md") (Join-Path $final "Solutions_Concretes")
Copy-ExistingLiteral @("19_ROLES_CONTRIBUTIONS_PREUVES.md") (Join-Path $final "Solutions_Concretes")
Copy-ExistingLiteral @("20_MODE_OPERATOIRE_PFSENSE_WAZUH_LAB.md") (Join-Path $final "Solutions_Concretes")
Copy-ExistingLiteral @("21_DASHBOARDS_ALERTES_QUALIFICATION.md") (Join-Path $final "Solutions_Concretes")
Copy-ExistingLiteral @("22_EXPLOITATION_VM_RUNBOOK_REX.md") (Join-Path $final "Solutions_Concretes")
Copy-ExistingLiteral @("23_PREUVES_FINALES_CAPTURES_VIDEO_DEPOT.md") (Join-Path $final "Solutions_Concretes")
Copy-ExistingLiteral @("24_DASHBOARD_SOC_OFFLINE.md") (Join-Path $final "Solutions_Concretes")
Copy-ExistingLiteral @("25_MODE_OPERATOIRE_CAPTURE_WAZUH_PREUVES.md") (Join-Path $final "Solutions_Concretes")
Copy-ExistingLiteral @("26_MODE_OPERATOIRE_VIDEO_DEPOT.md") (Join-Path $final "Solutions_Concretes")
Copy-ExistingLiteral @("28_RUNBOOK_EXPRESS_PREUVES_RESTANTES.md") (Join-Path $final "Solutions_Concretes")
Copy-ExistingLiteral @("29_IMPORT_PREUVES_FINALES.md") (Join-Path $final "Solutions_Concretes")
Copy-ExistingLiteral @("30_TABLEAU_BORD_STATUT_FINAL.md") (Join-Path $final "Solutions_Concretes")
Copy-ExistingLiteral @("31_PACK_SOUTENANCE_JURY.md") (Join-Path $final "Solutions_Concretes")
Copy-ExistingLiteral @("32_MATRICE_CONFORMITE_CAHIER_DES_CHARGES.md") (Join-Path $final "Solutions_Concretes")
Copy-ExistingLiteral @("33_RUNBOOK_ENREGISTREMENT_VIDEO_IMMEDIAT.md") (Join-Path $final "Solutions_Concretes")

if (Test-Path -LiteralPath (Join-Path $root "config\pfsense")) {
    Copy-Item -Path (Join-Path $root "config\pfsense\*") -Destination (Join-Path $final "Config_PfSense") -Force
    Write-Host "[OK] Config pfSense copiee"
}

if (Test-Path -LiteralPath (Join-Path $root "config\wazuh")) {
    Copy-Item -Path (Join-Path $root "config\wazuh\*") -Destination (Join-Path $final "Config_Wazuh") -Force
    Write-Host "[OK] Config Wazuh copiee"
}

if (Test-Path -LiteralPath (Join-Path $root "config\lab")) {
    Copy-Item -Path (Join-Path $root "config\lab\*") -Destination (Join-Path $final "Config_Lab") -Force
    Write-Host "[OK] Config lab copiee"
}

if (Test-Path -LiteralPath (Join-Path $root "config\captures")) {
    Copy-Item -Path (Join-Path $root "config\captures\*") -Destination (Join-Path $final "Config_Captures") -Force
    Write-Host "[OK] Config captures copiee"
}

if (Test-Path -LiteralPath (Join-Path $root "config\video")) {
    Copy-Item -Path (Join-Path $root "config\video\*") -Destination (Join-Path $final "Config_Video") -Force
    Write-Host "[OK] Config video copiee"
}

if (Test-Path -LiteralPath (Join-Path $root "config\compliance")) {
    Copy-Item -Path (Join-Path $root "config\compliance\*") -Destination (Join-Path $final "Config_Compliance") -Force
    Write-Host "[OK] Config compliance copiee"
}


if (Test-Path -LiteralPath (Join-Path $root "Dashboards_Offline")) {
    Copy-Item -Path (Join-Path $root "Dashboards_Offline\*") -Destination (Join-Path $final "Dashboards_Offline") -Force -ErrorAction SilentlyContinue
    Write-Host "[OK] Dashboard offline copie"
}
if (Test-Path -LiteralPath (Join-Path $root "Video_Overlays")) {
    Copy-Item -Path (Join-Path $root "Video_Overlays\*") -Destination (Join-Path $final "Video_Overlays") -Force -ErrorAction SilentlyContinue
    Write-Host "[OK] Overlays video copies"
}
if (Test-Path -LiteralPath (Join-Path $root "Demo_Logs")) {
    Copy-Item -Path (Join-Path $root "Demo_Logs\*") -Destination (Join-Path $final "Demo_Logs") -Force -ErrorAction SilentlyContinue
    Write-Host "[OK] Logs demo copies"
}


if (Test-Path -LiteralPath (Join-Path $root "Annexes_Captures")) {
    Copy-Item -Path (Join-Path $root "Annexes_Captures\*") -Destination (Join-Path $final "Annexes_Captures") -Force -ErrorAction SilentlyContinue
    Write-Host "[OK] Annexes captures copiees"
}

$videoCandidates = @(
    "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt",
    "PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4",
    "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4"
)
Copy-ExistingLiteral $videoCandidates (Join-Path $final "Video")

if (Test-Path -LiteralPath (Join-Path $root "capture-pack-report.txt")) {
    Copy-Item -LiteralPath (Join-Path $root "capture-pack-report.txt") -Destination (Join-Path $final "Rapports_Captures\capture-pack-report.txt") -Force
    if (Test-Path -LiteralPath (Join-Path $root "preflight-evidence-report.txt")) { Copy-Item -LiteralPath (Join-Path $root "preflight-evidence-report.txt") -Destination (Join-Path $final "Rapports_Captures\preflight-evidence-report.txt") -Force }
    if (Test-Path -LiteralPath (Join-Path $root "youssef-wazuh-proof-extraction-report.txt")) { Copy-Item -LiteralPath (Join-Path $root "youssef-wazuh-proof-extraction-report.txt") -Destination (Join-Path $final "Rapports_Captures\youssef-wazuh-proof-extraction-report.txt") -Force }
    if (Test-Path -LiteralPath (Join-Path $root "documentary-proof-images-report.txt")) { Copy-Item -LiteralPath (Join-Path $root "documentary-proof-images-report.txt") -Destination (Join-Path $final "Rapports_Captures\documentary-proof-images-report.txt") -Force }
    if (Test-Path -LiteralPath (Join-Path $root "log-replay-dry-run-report.txt")) { Copy-Item -LiteralPath (Join-Path $root "log-replay-dry-run-report.txt") -Destination (Join-Path $final "Rapports_Captures\log-replay-dry-run-report.txt") -Force }
    if (Test-Path -LiteralPath (Join-Path $root "evidence-status-report.txt")) { Copy-Item -LiteralPath (Join-Path $root "evidence-status-report.txt") -Destination (Join-Path $final "Rapports_Validation\evidence-status-report.txt") -Force }
    if (Test-Path -LiteralPath (Join-Path $root "video-teleprompter-report.txt")) { Copy-Item -LiteralPath (Join-Path $root "video-teleprompter-report.txt") -Destination (Join-Path $final "Rapports_Video\video-teleprompter-report.txt") -Force }
    if (Test-Path -LiteralPath (Join-Path $root "video-overlays-report.txt")) { Copy-Item -LiteralPath (Join-Path $root "video-overlays-report.txt") -Destination (Join-Path $final "Rapports_Video\video-overlays-report.txt") -Force }
    if (Test-Path -LiteralPath (Join-Path $root "video-recording-pack-report.txt")) { Copy-Item -LiteralPath (Join-Path $root "video-recording-pack-report.txt") -Destination (Join-Path $final "Rapports_Video\video-recording-pack-report.txt") -Force }
    if (Test-Path -LiteralPath (Join-Path $root "video-recording-launcher-report.txt")) { Copy-Item -LiteralPath (Join-Path $root "video-recording-launcher-report.txt") -Destination (Join-Path $final "Rapports_Video\video-recording-launcher-report.txt") -Force }
    if (Test-Path -LiteralPath (Join-Path $root "jury-defense-pack-report.txt")) { Copy-Item -LiteralPath (Join-Path $root "jury-defense-pack-report.txt") -Destination (Join-Path $final "Rapports_Video\jury-defense-pack-report.txt") -Force }
    if (Test-Path -LiteralPath (Join-Path $root "compliance-matrix-report.txt")) { Copy-Item -LiteralPath (Join-Path $root "compliance-matrix-report.txt") -Destination (Join-Path $final "Rapports_Validation\compliance-matrix-report.txt") -Force }
    if (Test-Path -LiteralPath (Join-Path $root "pfsense-demo-pack-report.txt")) { Copy-Item -LiteralPath (Join-Path $root "pfsense-demo-pack-report.txt") -Destination (Join-Path $final "Rapports_Validation\pfsense-demo-pack-report.txt") -Force }
    if (Test-Path -LiteralPath (Join-Path $root "demo-control-center-report.txt")) { Copy-Item -LiteralPath (Join-Path $root "demo-control-center-report.txt") -Destination (Join-Path $final "Rapports_Validation\demo-control-center-report.txt") -Force }
    Write-Host "[OK] Rapport captures copie"
}


if (Test-Path -LiteralPath (Join-Path $root "video-readiness-report.txt")) {
    Copy-Item -LiteralPath (Join-Path $root "video-readiness-report.txt") -Destination (Join-Path $final "Rapports_Video\video-readiness-report.txt") -Force
    Write-Host "[OK] Rapport video copie"
}
if (Test-Path -LiteralPath (Join-Path $root "lab-cap25-recovery-report.txt")) {
    Copy-Item -LiteralPath (Join-Path $root "lab-cap25-recovery-report.txt") -Destination (Join-Path $final "Rapports_Preflight\lab-cap25-recovery-report.txt") -Force
    Write-Host "[OK] Rapport relance CAP-25 copie"
}
if (Test-Path -LiteralPath (Join-Path $root "preflight-demo-report.txt")) {
    Copy-Item -LiteralPath (Join-Path $root "preflight-demo-report.txt") -Destination (Join-Path $final "Rapports_Preflight\preflight-demo-report.txt") -Force
    Write-Host "[OK] Rapport preflight copie"
}


if (Test-Path -LiteralPath (Join-Path $root "validation-rendu-final.txt")) {
    Copy-Item -LiteralPath (Join-Path $root "validation-rendu-final.txt") -Destination (Join-Path $final "Rapports_Validation\validation-rendu-final.txt") -Force
    Write-Host "[OK] Rapport validation copie"
}

if (Test-Path -LiteralPath (Join-Path $root "pdf-pillow-export-report.txt")) {
    Copy-Item -LiteralPath (Join-Path $root "pdf-pillow-export-report.txt") -Destination (Join-Path $final "Rapports_Finalisation\pdf-pillow-export-report.txt") -Force
    Write-Host "[OK] Rapport export PDF Pillow copie"
}
if (Test-Path -LiteralPath (Join-Path $root "finalize-project-report.txt")) {
    Copy-Item -LiteralPath (Join-Path $root "finalize-project-report.txt") -Destination (Join-Path $final "Rapports_Finalisation\finalize-project-report.txt") -Force
    Write-Host "[OK] Rapport finalisation copie"
}
$finalComplianceBuilder = Join-Path $final "Outils\build_compliance_matrix.py"
if (Test-Path -LiteralPath $finalComplianceBuilder) {
    Push-Location $final
    try {
        python $finalComplianceBuilder
        $finalComplianceReport = Join-Path $final "compliance-matrix-report.txt"
        if (Test-Path -LiteralPath $finalComplianceReport) {
            Copy-Item -LiteralPath $finalComplianceReport -Destination (Join-Path $final "Rapports_Validation\compliance-matrix-report.txt") -Force
        }
        Write-Host "[OK] Matrice conformite regeneree dans Rendu_Final"
    } finally {
        Pop-Location
    }
}

$finalJuryBuilder = Join-Path $final "Outils\build_jury_defense_pack.py"
if (Test-Path -LiteralPath $finalJuryBuilder) {
    Push-Location $final
    try {
        python $finalJuryBuilder
        $finalJuryReport = Join-Path $final "jury-defense-pack-report.txt"
        if (Test-Path -LiteralPath $finalJuryReport) {
            Copy-Item -LiteralPath $finalJuryReport -Destination (Join-Path $final "Rapports_Video\jury-defense-pack-report.txt") -Force
        }
        Write-Host "[OK] Pack defense jury regenere dans Rendu_Final"
    } finally {
        Pop-Location
    }
}

$finalVideoPackBuilder = Join-Path $final "Outils\build_video_recording_pack.py"
if (Test-Path -LiteralPath $finalVideoPackBuilder) {
    Push-Location $final
    try {
        python $finalVideoPackBuilder
        $finalVideoPackReport = Join-Path $final "video-recording-pack-report.txt"
        if (Test-Path -LiteralPath $finalVideoPackReport) {
            Copy-Item -LiteralPath $finalVideoPackReport -Destination (Join-Path $final "Rapports_Video\video-recording-pack-report.txt") -Force
        }
        Write-Host "[OK] Pack enregistrement video regenere dans Rendu_Final"
    } finally {
        Pop-Location
    }
}

$finalPfsenseBuilder = Join-Path $final "Outils\build_pfsense_demo_pack.py"
if (Test-Path -LiteralPath $finalPfsenseBuilder) {
    Push-Location $final
    try {
        python $finalPfsenseBuilder
        $finalPfsenseReport = Join-Path $final "pfsense-demo-pack-report.txt"
        if (Test-Path -LiteralPath $finalPfsenseReport) {
            Copy-Item -LiteralPath $finalPfsenseReport -Destination (Join-Path $final "Rapports_Validation\pfsense-demo-pack-report.txt") -Force
        }
        Write-Host "[OK] Pack demo pfSense regenere dans Rendu_Final"
    } finally {
        Pop-Location
    }
}

$finalDemoBuilder = Join-Path $final "Outils\build_demo_control_center.py"
if (Test-Path -LiteralPath $finalDemoBuilder) {
    Push-Location $final
    try {
        python $finalDemoBuilder
        $finalDemoReport = Join-Path $final "demo-control-center-report.txt"
        if (Test-Path -LiteralPath $finalDemoReport) {
            Copy-Item -LiteralPath $finalDemoReport -Destination (Join-Path $final "Rapports_Validation\demo-control-center-report.txt") -Force
        }
        Write-Host "[OK] Centre de controle demo regenere dans Rendu_Final"
    } finally {
        Pop-Location
    }
}

$zipPath = Join-Path $root $ZipName
Compress-Archive -Path (Join-Path $final "*") -DestinationPath $zipPath -Force

$pdfCount = @(Get-ChildItem -LiteralPath (Join-Path $final "Rendus_PDF") -Filter "*.pdf" -File -ErrorAction SilentlyContinue).Count
$captureCount = @(Get-ChildItem -LiteralPath (Join-Path $final "Annexes_Captures") -Filter "CAP-*.png" -File -ErrorAction SilentlyContinue).Count
$zip = Get-Item -LiteralPath $zipPath

Write-Host ""
Write-Host "=== Rendu final reconstruit ==="
Write-Host "ZIP       : $($zip.FullName)"
Write-Host "Taille    : $($zip.Length) octets"
Write-Host "PDF       : $pdfCount"
Write-Host "Captures  : $captureCount"
Write-Host "Rendu dir : $final"
























