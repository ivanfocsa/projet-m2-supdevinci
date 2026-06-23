param(
    [switch]$WriteReport
)

$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $PSScriptRoot
$reportLines = New-Object System.Collections.Generic.List[string]

function Add-Line {
    param([string]$Line)
    $reportLines.Add($Line) | Out-Null
    Write-Host $Line
}

function Test-Command {
    param([string]$Name)
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    return [bool]$cmd
}

function Test-WazuhDashboard {
    $lastError = ""
    try {
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
        [System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }
        $response = Invoke-WebRequest -UseBasicParsing -Uri "https://localhost" -TimeoutSec 8 -ErrorAction Stop
        if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) {
            return @{ Ok = $true; Detail = "repond avec statut $($response.StatusCode)" }
        }
    } catch {
        $lastError = $_.Exception.Message
        if ($_.Exception.InnerException) {
            $lastError = "$lastError / $($_.Exception.InnerException.Message)"
        }
    }

    if (Test-Command "python") {
        try {
            $pythonCode = "import ssl, urllib.request; ctx=ssl._create_unverified_context(); r=urllib.request.urlopen('https://localhost', context=ctx, timeout=8); print(r.status)"
            $status = & python -c $pythonCode 2>$null
            if ($LASTEXITCODE -eq 0 -and "$status" -match "^\d+") {
                $code = [int]("$status".Trim())
                if ($code -ge 200 -and $code -lt 500) {
                    return @{ Ok = $true; Detail = "repond avec statut $code via Python TLS lab" }
                }
            }
        } catch {
            if (!$lastError) { $lastError = $_.Exception.Message }
        }
    }

    if (!$lastError) { $lastError = "aucune reponse HTTP valide" }
    return @{ Ok = $false; Detail = "inaccessible : $lastError" }
}
function Add-Check {
    param(
        [string]$Name,
        [bool]$Ok,
        [string]$OkText,
        [string]$FailText
    )
    if ($Ok) {
        Add-Line "[OK]   $Name - $OkText"
    } else {
        Add-Line "[WARN] $Name - $FailText"
    }
}

Set-Location $root
Add-Line "=== Preflight demo Daylight / Cyber Trust ==="
Add-Line "Racine projet : $root"
Add-Line "Date controle : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Add-Line ""

$requiredFiles = @(
    "Presentation_Daylight_CyberTrust.pptx",
    "04_SCRIPT_VIDEO_DEMO.md",
    "07_DOSSIER_PREUVES_CAPTURES.md",
    "09_NOTES_ORATEUR_SOUTENANCE.md",
    "Youssef GUERNIOU\setup-siem-lab.ps1",
    "Youssef GUERNIOU\Documentation_SIEM_Youssef_GUERNIOU.pdf",
    "tools\rebuild_rendu_final.ps1",
    "tools\export_markdown_to_pdf_pillow.py",
    "16_ANNEXE_CAPTURES_WAZUH.md",
    "17_DOSSIER_GROUPE_COMPLET_INDEX.md",
    "tools\build_group_dossier_pdf.py",
    "tools\validate_rendu_final.py",
    "tools\finalize_project.ps1",
    "18_SOLUTIONS_CONCRETES_DEMO.md",
    "config\pfsense\pfsense_firewall_rules.csv",
    "config\pfsense\pfsense_syslog_wazuh.md",
    "config\wazuh\local_rules_daylight_pfsense.xml",
    "tools\generate_demo_logs.py",
    "tools\send_demo_logs_to_syslog.py",
    "19_ROLES_CONTRIBUTIONS_PREUVES.md",
    "20_MODE_OPERATOIRE_PFSENSE_WAZUH_LAB.md",
    "config\pfsense\pfsense_lab_topology.csv",
    "21_DASHBOARDS_ALERTES_QUALIFICATION.md",
    "config\wazuh\daylight_dashboard_queries.csv",
    "config\wazuh\daylight_alert_qualification_matrix.csv",
    "22_EXPLOITATION_VM_RUNBOOK_REX.md",
    "config\lab\daylight_vm_inventory.csv",
    "config\lab\daylight_lab_runbook.csv",
    "config\lab\daylight_rex_scenarios.csv",
    "23_PREUVES_FINALES_CAPTURES_VIDEO_DEPOT.md",
    "24_DASHBOARD_SOC_OFFLINE.md",
    "config\captures\daylight_capture_checklist.csv",
    "config\video\daylight_video_shotlist.csv",
    "tools\check_capture_pack.py",
    "tools\render_static_proof_images.py",
    "tools\build_offline_soc_dashboard.py",
    "tools\render_preflight_evidence.py",
    "tools\prepare_capture_session.ps1",
    "25_MODE_OPERATOIRE_CAPTURE_WAZUH_PREUVES.md",
    "26_MODE_OPERATOIRE_VIDEO_DEPOT.md",
    "27_MANIFESTE_DEPOT_ET_INTEGRITE.md",
    "28_RUNBOOK_EXPRESS_PREUVES_RESTANTES.md",
    "29_IMPORT_PREUVES_FINALES.md",
    "30_TABLEAU_BORD_STATUT_FINAL.md",
    "tools\check_video_ready.py",
    "tools\build_delivery_manifest.py",
    "tools\post_capture_finalize.ps1",
    "tools\import_final_evidence.ps1",
    "tools\build_final_evidence_dashboard.py",
    "tools\extract_youssef_wazuh_proofs.py",
    "tools\render_documentary_proof_images.py",
    "tools\build_video_teleprompter.py",
    "tools\build_video_overlays.py",
    "tools\build_demo_control_center.py",
    "tools\open_demo_control_center.ps1",
    "tools\repair_lab_and_capture_cap25.ps1",
    "MANIFEST_DEPOT.md",
    "MANIFEST_DEPOT.json",
    "config\video\daylight_video_recording_checklist.csv",
    "config\video\youtube_description_daylight.txt",
    "config\captures\daylight_remaining_priority_captures.csv"
)

Add-Line "## Fichiers projet"
foreach ($file in $requiredFiles) {
    Add-Check $file (Test-Path -LiteralPath $file) "present" "introuvable"
}
Add-Line ""

Add-Line "## Rendus"
$pdfCount = 0
if (Test-Path -LiteralPath "Rendus_PDF") {
    $pdfCount = @(Get-ChildItem -LiteralPath "Rendus_PDF" -Filter "*.pdf" -File -ErrorAction SilentlyContinue).Count
}
Add-Check "Rendus_PDF" ($pdfCount -ge 37) "$pdfCount PDF detectes" "$pdfCount PDF detectes, attendu au moins 37"
Add-Check "Archive ZIP" (Test-Path -LiteralPath "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip") "presente" "archive absente"
Add-Check "Rendu_Final" (Test-Path -LiteralPath "Rendu_Final") "present" "dossier absent"
Add-Line ""

Add-Line "## Captures et video"
if (!(Test-Path -LiteralPath "Annexes_Captures")) {
    New-Item -ItemType Directory -Path "Annexes_Captures" | Out-Null
}
$captureCount = @(Get-ChildItem -LiteralPath "Annexes_Captures" -Filter "CAP-*.png" -File -ErrorAction SilentlyContinue).Count
Add-Check "Captures CAP-*.png" ($captureCount -ge 8) "$captureCount captures detectees" "$captureCount captures detectees, verifier CAP-25 et la checklist captures"

$videoFile = "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt"
$videoReady = $false
if (Test-Path -LiteralPath $videoFile) {
    $videoText = Get-Content -Raw -LiteralPath $videoFile
    $videoReady = ($videoText -match "https?://") -and ($videoText -notmatch "Coller ici")
}
Add-Check "Lien video" $videoReady "lien detecte" "lien YouTube non repertorie pas encore renseigne"
Add-Check "Rapport video" (Test-Path -LiteralPath "video-readiness-report.txt") "rapport present" "lancer python .\tools\check_video_ready.py"
Add-Line "## Solutions concretes"
$demoLogCount = 0
if (Test-Path -LiteralPath "Demo_Logs") {
    $demoLogCount = @(Get-ChildItem -LiteralPath "Demo_Logs" -Filter "*.log" -File -ErrorAction SilentlyContinue).Count
}
Add-Check "Logs demo Daylight" ($demoLogCount -ge 5) "$demoLogCount fichiers .log detectes" "$demoLogCount fichiers .log detectes, lancer python .\tools\generate_demo_logs.py"
Add-Check "Regles pfSense" (Test-Path -LiteralPath "config\pfsense\pfsense_firewall_rules.csv") "matrice presente" "matrice firewall absente"
Add-Check "Regles Wazuh custom" (Test-Path -LiteralPath "config\wazuh\local_rules_daylight_pfsense.xml") "XML present" "XML absent"
Add-Check "Images preuves statiques" ((Test-Path -LiteralPath "Annexes_Captures\CAP-12_architecture-solution.png") -and (Test-Path -LiteralPath "Annexes_Captures\CAP-13_pfsense-regles-firewall.png")) "architecture et matrice pfSense presentes" "lancer python .\tools\render_static_proof_images.py"
Add-Check "Dashboard SOC offline" ((Test-Path -LiteralPath "Dashboards_Offline\daylight_soc_dashboard.html") -and (Test-Path -LiteralPath "Annexes_Captures\CAP-07_dashboard-technique.png") -and (Test-Path -LiteralPath "Annexes_Captures\CAP-08_dashboard-executif.png")) "HTML et captures dashboard presents" "lancer python .\tools\build_offline_soc_dashboard.py"
Add-Check "Overlays video nom/role" ((Test-Path -LiteralPath "Video_Overlays\overlay_yvan_focsa.png") -and (Test-Path -LiteralPath "Video_Overlays\overlay_youssef_guerniou.png") -and (Test-Path -LiteralPath "Video_Overlays\overlay_kilyan_felix.png") -and (Test-Path -LiteralPath "Video_Overlays\overlay_mahamadou_diacoumba.png")) "4 bandeaux membres presents" "lancer python .\tools\build_video_overlays.py"
Add-Line ""
Add-Line ""

Add-Line "## Outils locaux"
$hasDocker = Test-Command "docker"
$hasNpm = Test-Command "npm"
$hasPython = Test-Command "python"
$hasPackageJson = Test-Path -LiteralPath ".\package.json"
Add-Check "docker" $hasDocker "commande disponible" "commande introuvable"
Add-Check "npm" $hasNpm "commande disponible" "commande introuvable ou non necessaire si lab deja pret"
Add-Check "python" $hasPython "commande disponible" "commande introuvable"
Add-Check "package.json lab npm" $hasPackageJson "present dans cette racine" "absent ici, lancer Wazuh depuis sa racine technique"
Add-Line ""

Add-Line "## Docker et conteneurs"
if ($hasDocker) {
    $dockerInfoOk = $false
    try {
        docker info *> $null
        $dockerInfoOk = ($LASTEXITCODE -eq 0)
    } catch {
        $dockerInfoOk = $false
    }
    Add-Check "Docker daemon" $dockerInfoOk "repond" "ne repond pas, lancer Docker Desktop"

    if ($dockerInfoOk) {
        $containers = docker ps -a --format "{{.Names}}|{{.Status}}" 2>$null
        $wazuhContainers = @($containers | Select-String -Pattern "wazuh" -SimpleMatch)
        $server01 = @($containers | Select-String -Pattern "^serveur-01\|" )
        Add-Check "Conteneurs Wazuh" ($wazuhContainers.Count -gt 0) "$($wazuhContainers.Count) entree(s) detectee(s)" "aucun conteneur Wazuh detecte"
        Add-Check "Conteneur serveur-01" ($server01.Count -gt 0) "detecte" "non detecte, lancer setup-siem-lab.ps1"
        if ($wazuhContainers.Count -gt 0) {
            Add-Line "Conteneurs Wazuh detectes :"
            foreach ($c in $wazuhContainers) { Add-Line "  $($c.Line)" }
        }
        if ($server01.Count -gt 0) {
            Add-Line "Serveur simule :"
            foreach ($c in $server01) { Add-Line "  $($c.Line)" }
        }
    }
}
Add-Line ""

Add-Line "## Acces Wazuh Dashboard"
$dashboardResult = Test-WazuhDashboard
Add-Check "https://localhost" $dashboardResult.Ok $dashboardResult.Detail $dashboardResult.Detail
Add-Line ""

Add-Line "## Prochaines commandes conseillees"
if (!$hasDocker) {
    Add-Line "- Installer/lancer Docker Desktop avant la demo."
} else {
    if ($hasPackageJson) {
        Add-Line "- Si Wazuh est eteint dans cette racine : npm run lab:start"
    } else {
        Add-Line "- Aucun package.json ici : lancer/demarrer Wazuh depuis la racine technique du lab, puis revenir dans ce dossier."
    }
    Add-Line "- Si serveur-01 existe mais est eteint : docker start serveur-01"
    Add-Line "- Pour guider la relance CAP-25 : C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\repair_lab_and_capture_cap25.ps1 -StartDockerDesktop -StartKnownContainers -WaitSeconds 180"
    Add-Line "- Pour preparer le perimetre SIEM : C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File `".\Youssef GUERNIOU\setup-siem-lab.ps1`""
    Add-Line "- Pour finaliser apres captures/video : C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\post_capture_finalize.ps1"
}
Add-Line "- Capturer les ecrans listes dans 07_DOSSIER_PREUVES_CAPTURES.md"
Add-Line "- Controler le pack captures : python .\tools\check_capture_pack.py"
Add-Line "- Coller le lien YouTube dans $videoFile"

if ($WriteReport) {
    $reportPath = Join-Path $root "preflight-demo-report.txt"
    Set-Content -LiteralPath $reportPath -Value $reportLines -Encoding UTF8
    Add-Line ""
    Add-Line "Rapport ecrit : $reportPath"
}
































