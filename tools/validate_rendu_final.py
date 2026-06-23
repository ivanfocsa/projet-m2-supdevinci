import csv
from pathlib import Path
from zipfile import ZipFile

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
ZIP_NAME = "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip"
ZIP_PATH = ROOT / ZIP_NAME
REPORT_PATH = ROOT / "validation-rendu-final.txt"
PDF_DIR = ROOT / "Rendu_Final" / "Rendus_PDF"
CAPTURE_DIR = ROOT / "Rendu_Final" / "Annexes_Captures"
VIDEO_LINK = ROOT / "Rendu_Final" / "Video" / "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt"
CHECKLIST = ROOT / "Rendu_Final" / "Config_Captures" / "daylight_capture_checklist.csv"
MP4_CANDIDATES = [
    ROOT / "Rendu_Final" / "Video" / "PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4",
    ROOT / "Rendu_Final" / "Video" / "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4",
]

EXPECTED_PDF_MIN = 37
EXPECTED_COMBINED_PAGES = 90

REQUIRED_ZIP_ENTRIES = [
    "README_A_LIRE.md",
    "Rendus_PDF\\PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_RapportGroupe.pdf",
    "Rendus_PDF\\PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_DossierGroupeComplet.pdf",
    "Rendus_PDF\\PE-2526_M2CS_YvanFOCSA.pdf",
    "Rendus_PDF\\PE-2526_M2CS_YoussefGUERNIOU.pdf",
    "Rendus_PDF\\PE-2526_M2CS_KilyanFELIX.pdf",
    "Rendus_PDF\\PE-2526_M2CS_MahamadouDIACOUMBA.pdf",
    "Presentation\\Presentation_Daylight_CyberTrust.pptx",
    "Preuves_SIEM_Youssef\\Documentation_SIEM_Youssef_GUERNIOU.pdf",
    "Preuves_SIEM_Youssef\\setup-siem-lab.ps1",
    "Outils\\preflight_demo.ps1",
    "Outils\\rebuild_rendu_final.ps1",
    "Outils\\export_markdown_to_pdf_pillow.py",
    "Outils\\build_capture_annex.py",
    "Outils\\build_group_dossier_pdf.py",
    "Outils\\validate_rendu_final.py",
    "Outils\\finalize_project.ps1",
    "Outils\\generate_demo_logs.py",
    "Outils\\send_demo_logs_to_syslog.py",
    "Outils\\render_static_proof_images.py",
    "Outils\\build_offline_soc_dashboard.py",
    "Outils\\render_preflight_evidence.py",
    "Outils\\prepare_capture_session.ps1",
    "Outils\\check_capture_pack.py",
    "Outils\\check_video_ready.py",
    "Outils\\build_delivery_manifest.py",
    "Outils\\post_capture_finalize.ps1",
    "Outils\\import_final_evidence.ps1",
    "Outils\\build_final_evidence_dashboard.py",
    "Outils\\extract_youssef_wazuh_proofs.py",
    "Outils\\render_documentary_proof_images.py",
    "Outils\\build_video_teleprompter.py",
    "Outils\\build_video_overlays.py",
    "Outils\\build_video_recording_pack.py",
    "Outils\\build_jury_defense_pack.py",
    "Outils\\build_compliance_matrix.py",
    "Outils\\build_pfsense_demo_pack.py",
    "Outils\\build_demo_control_center.py",
    "Outils\\open_demo_control_center.ps1",
    "Outils\\launch_video_recording_session.ps1",
    "Outils\\repair_lab_and_capture_cap25.ps1",
    "Rendus_PDF\\18_SOLUTIONS_CONCRETES_DEMO.pdf",
    "Rendus_PDF\\19_ROLES_CONTRIBUTIONS_PREUVES.pdf",
    "Rendus_PDF\\20_MODE_OPERATOIRE_PFSENSE_WAZUH_LAB.pdf",
    "Rendus_PDF\\21_DASHBOARDS_ALERTES_QUALIFICATION.pdf",
    "Rendus_PDF\\22_EXPLOITATION_VM_RUNBOOK_REX.pdf",
    "Rendus_PDF\\23_PREUVES_FINALES_CAPTURES_VIDEO_DEPOT.pdf",
    "Rendus_PDF\\24_DASHBOARD_SOC_OFFLINE.pdf",
    "Rendus_PDF\\25_MODE_OPERATOIRE_CAPTURE_WAZUH_PREUVES.pdf",
    "Rendus_PDF\\26_MODE_OPERATOIRE_VIDEO_DEPOT.pdf",
    "Rendus_PDF\\27_MANIFESTE_DEPOT_ET_INTEGRITE.pdf",
    "Rendus_PDF\\28_RUNBOOK_EXPRESS_PREUVES_RESTANTES.pdf",
    "Rendus_PDF\\29_IMPORT_PREUVES_FINALES.pdf",
    "Rendus_PDF\\30_TABLEAU_BORD_STATUT_FINAL.pdf",
    "Rendus_PDF\\31_PACK_SOUTENANCE_JURY.pdf",
    "Rendus_PDF\\32_MATRICE_CONFORMITE_CAHIER_DES_CHARGES.pdf",
    "Rendus_PDF\\33_RUNBOOK_ENREGISTREMENT_VIDEO_IMMEDIAT.pdf",
    "Sources_Markdown\\18_SOLUTIONS_CONCRETES_DEMO.md",
    "Sources_Markdown\\19_ROLES_CONTRIBUTIONS_PREUVES.md",
    "Sources_Markdown\\20_MODE_OPERATOIRE_PFSENSE_WAZUH_LAB.md",
    "Sources_Markdown\\21_DASHBOARDS_ALERTES_QUALIFICATION.md",
    "Sources_Markdown\\22_EXPLOITATION_VM_RUNBOOK_REX.md",
    "Sources_Markdown\\23_PREUVES_FINALES_CAPTURES_VIDEO_DEPOT.md",
    "Sources_Markdown\\24_DASHBOARD_SOC_OFFLINE.md",
    "Sources_Markdown\\25_MODE_OPERATOIRE_CAPTURE_WAZUH_PREUVES.md",
    "Sources_Markdown\\26_MODE_OPERATOIRE_VIDEO_DEPOT.md",
    "Sources_Markdown\\27_MANIFESTE_DEPOT_ET_INTEGRITE.md",
    "Sources_Markdown\\28_RUNBOOK_EXPRESS_PREUVES_RESTANTES.md",
    "Sources_Markdown\\29_IMPORT_PREUVES_FINALES.md",
    "Sources_Markdown\\30_TABLEAU_BORD_STATUT_FINAL.md",
    "Sources_Markdown\\31_PACK_SOUTENANCE_JURY.md",
    "Sources_Markdown\\32_MATRICE_CONFORMITE_CAHIER_DES_CHARGES.md",
    "Sources_Markdown\\33_RUNBOOK_ENREGISTREMENT_VIDEO_IMMEDIAT.md",
    "Manifeste_Depot\\MANIFEST_DEPOT.md",
    "Manifeste_Depot\\MANIFEST_DEPOT.json",
    "Solutions_Concretes\\18_SOLUTIONS_CONCRETES_DEMO.md",
    "Solutions_Concretes\\19_ROLES_CONTRIBUTIONS_PREUVES.md",
    "Solutions_Concretes\\20_MODE_OPERATOIRE_PFSENSE_WAZUH_LAB.md",
    "Solutions_Concretes\\21_DASHBOARDS_ALERTES_QUALIFICATION.md",
    "Solutions_Concretes\\22_EXPLOITATION_VM_RUNBOOK_REX.md",
    "Solutions_Concretes\\23_PREUVES_FINALES_CAPTURES_VIDEO_DEPOT.md",
    "Solutions_Concretes\\24_DASHBOARD_SOC_OFFLINE.md",
    "Solutions_Concretes\\25_MODE_OPERATOIRE_CAPTURE_WAZUH_PREUVES.md",
    "Solutions_Concretes\\26_MODE_OPERATOIRE_VIDEO_DEPOT.md",
    "Solutions_Concretes\\28_RUNBOOK_EXPRESS_PREUVES_RESTANTES.md",
    "Solutions_Concretes\\29_IMPORT_PREUVES_FINALES.md",
    "Solutions_Concretes\\30_TABLEAU_BORD_STATUT_FINAL.md",
    "Solutions_Concretes\\31_PACK_SOUTENANCE_JURY.md",
    "Solutions_Concretes\\32_MATRICE_CONFORMITE_CAHIER_DES_CHARGES.md",
    "Solutions_Concretes\\33_RUNBOOK_ENREGISTREMENT_VIDEO_IMMEDIAT.md",
    "Config_PfSense\\README_PFSENSE_DAYLIGHT.md",
    "Config_PfSense\\pfsense_firewall_rules.csv",
    "Config_PfSense\\pfsense_aliases.csv",
    "Config_PfSense\\pfsense_nat_port_forward.csv",
    "Config_PfSense\\pfsense_lab_topology.csv",
    "Config_PfSense\\pfsense_syslog_wazuh.md",
    "Config_PfSense\\README_IMPORT_PFSENSE_DAYLIGHT.md",
    "Config_PfSense\\pfsense_demo_test_plan.csv",
    "Config_Wazuh\\local_rules_daylight_pfsense.xml",
    "Config_Wazuh\\daylight_dashboard_queries.csv",
    "Config_Wazuh\\daylight_alert_qualification_matrix.csv",
    "Config_Lab\\daylight_vm_inventory.csv",
    "Config_Lab\\daylight_lab_runbook.csv",
    "Config_Lab\\daylight_rex_scenarios.csv",
    "Config_Captures\\daylight_capture_checklist.csv",
    "Config_Captures\\daylight_remaining_priority_captures.csv",
    "Config_Video\\daylight_video_shotlist.csv",
    "Config_Video\\daylight_video_recording_checklist.csv",
    "Config_Video\\daylight_video_obs_scenes.csv",
    "Config_Video\\daylight_video_evidence_map.csv",
    "Config_Video\\daylight_video_open_order.csv",
    "Config_Video\\daylight_jury_response_cards.csv",
    "Config_Video\\daylight_jury_demo_path.csv",
    "Config_Video\\youtube_description_daylight.txt",
    "Config_Compliance\\daylight_compliance_matrix.csv",
    "Demo_Logs\\pfsense.log",
    "Demo_Logs\\daylight_app.log",
    "Demo_Logs\\ad_files.log",
    "Demo_Logs\\mail_phishing.log",
    "Demo_Logs\\endpoint_usb.log",
    "Rapports_Captures\\capture-pack-report.txt",
    "Rapports_Captures\\youssef-wazuh-proof-extraction-report.txt",
    "Rapports_Captures\\documentary-proof-images-report.txt",
    "Rapports_Captures\\log-replay-dry-run-report.txt",
    "Rapports_Captures\\preflight-evidence-report.txt",
    "Rapports_Video\\video-readiness-report.txt",
    "Rapports_Video\\video-teleprompter-report.txt",
    "Rapports_Video\\video-overlays-report.txt",
    "Rapports_Video\\video-recording-pack-report.txt",
    "Rapports_Video\\video-recording-launcher-report.txt",
    "Rapports_Video\\jury-defense-pack-report.txt",
    "Rapports_Validation\\demo-control-center-report.txt",
    "Rapports_Validation\\pfsense-demo-pack-report.txt",
    "Rapports_Validation\\compliance-matrix-report.txt",
    "Dashboards_Offline\\daylight_soc_dashboard.html",
    "Dashboards_Offline\\daylight_final_evidence_status.html",
    "Dashboards_Offline\\daylight_video_teleprompter.html",
    "Dashboards_Offline\\daylight_video_overlays.html",
    "Dashboards_Offline\\daylight_video_recording_pack.html",
    "Dashboards_Offline\\daylight_jury_defense_pack.html",
    "Dashboards_Offline\\daylight_compliance_matrix.html",
    "Dashboards_Offline\\daylight_pfsense_firewall_review.html",
    "Dashboards_Offline\\daylight_demo_control_center.html",
    "Rapports_Validation\\evidence-status-report.txt",
    "Rapports_Preflight\\preflight-demo-report.txt",
    "Rapports_Preflight\\lab-cap25-recovery-report.txt",
    "Rapports_Finalisation\\pdf-pillow-export-report.txt",
    "Rapports_Validation\\validation-rendu-final.txt",
    "Video\\PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt",
    "Video_Overlays\\README_VIDEO_OVERLAYS.md",
    "Video_Overlays\\overlay_kilyan_felix.png",
    "Video_Overlays\\overlay_yvan_focsa.png",
    "Video_Overlays\\overlay_youssef_guerniou.png",
    "Video_Overlays\\overlay_mahamadou_diacoumba.png",
    "Video_Overlays\\overlay_equipe_cyber_trust.png",
    "Annexes_Captures\\CAP-01_wazuh-dashboard-login.png",
    "Annexes_Captures\\CAP-02_agents-poste01-serveur01.png",
    "Annexes_Captures\\CAP-03_alerte-5712-brute-force-ssh.png",
    "Annexes_Captures\\README_PREUVES_WAZUH_EXTRAITES.md",
    "Annexes_Captures\\CAP-10_playbook-brute-force.png",
    "Annexes_Captures\\CAP-11_rex-incident-acces-patient.png",
    "Annexes_Captures\\CAP-14_pfsense-syslog-wazuh.png",
    "Annexes_Captures\\CAP-15_script-setup-siem-lab.png",
    "Annexes_Captures\\CAP-17_compte-supervision-dashboard.png",
    "Annexes_Captures\\CAP-18_export-dashboard-report.png",
    "Annexes_Captures\\CAP-19_wazuh-pfsense-alertes.png",
    "Annexes_Captures\\CAP-20_wazuh-rejeu-logs-demo.png",
    "Annexes_Captures\\CAP-24_qualification-alerte-110020.png",
    "Annexes_Captures\\CAP-27_rejeu-logs-dry-run.png",
    "Annexes_Captures\\CAP-28_rex-incident-rempli.png",
    "Annexes_Captures\\CAP-12_architecture-solution.png",
    "Annexes_Captures\\CAP-13_pfsense-regles-firewall.png",
    "Annexes_Captures\\CAP-06_alerte-100120-acces-patient.png",
    "Annexes_Captures\\CAP-07_dashboard-technique.png",
    "Annexes_Captures\\CAP-08_dashboard-executif.png",
    "Annexes_Captures\\CAP-23_qualification-alerte-100120.png",
]


def add(lines: list[str], line: str = "") -> None:
    lines.append(line)


def ok_line(name: str, ok: bool, detail: str) -> str:
    return f"[{'OK' if ok else 'WARN'}] {name} - {detail}"


def has_video_link() -> bool:
    if not VIDEO_LINK.exists():
        return False
    text = VIDEO_LINK.read_text(encoding="utf-8", errors="ignore")
    return ("http://" in text or "https://" in text) and "Coller ici" not in text

def has_video_ready() -> bool:
    if has_video_link():
        return True
    return any(path.exists() and path.stat().st_size > 10_000_000 for path in MP4_CANDIDATES)


def main() -> int:
    lines: list[str] = []
    warnings = 0

    add(lines, "=== Validation rendu final Daylight / Cyber Trust ===")
    add(lines, f"Racine : {ROOT}")
    add(lines, f"Archive : {ZIP_PATH}")
    add(lines)

    add(lines, "## Dossier local")
    pdfs = sorted(PDF_DIR.glob("*.pdf")) if PDF_DIR.exists() else []
    pdf_count_ok = len(pdfs) >= EXPECTED_PDF_MIN
    warnings += 0 if pdf_count_ok else 1
    add(lines, ok_line("Nombre de PDF", pdf_count_ok, f"{len(pdfs)} detectes, attendu au moins {EXPECTED_PDF_MIN}"))

    combined = PDF_DIR / "PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_DossierGroupeComplet.pdf"
    if combined.exists():
        reader = PdfReader(str(combined))
        combined_ok = len(reader.pages) >= EXPECTED_COMBINED_PAGES
        warnings += 0 if combined_ok else 1
        add(lines, ok_line("Dossier groupe complet", combined_ok, f"{len(reader.pages)} pages, attendu au moins {EXPECTED_COMBINED_PAGES}"))
    else:
        warnings += 1
        add(lines, ok_line("Dossier groupe complet", False, "PDF introuvable"))

    present_files = {path.name for path in CAPTURE_DIR.glob("CAP-*.png")} if CAPTURE_DIR.exists() else set()
    capture_count = len(present_files)
    required_total = 8
    required_present = min(capture_count, required_total)
    missing_required: list[str] = []
    if CHECKLIST.exists():
        rows = list(csv.DictReader(CHECKLIST.read_text(encoding="utf-8").splitlines()))
        required = [row for row in rows if row["required_for_deposit"].lower() == "yes"]
        required_total = len(required)
        missing_required = [row["filename"] for row in required if row["filename"] not in present_files]
        required_present = required_total - len(missing_required)
    capture_ok = required_total > 0 and required_present == required_total
    warnings += 0 if capture_ok else 1
    add(lines, ok_line("Captures/preuves prioritaires", capture_ok, f"{required_present}/{required_total} prioritaires presentes, {capture_count} fichier(s) CAP-*.png"))
    if missing_required:
        add(lines, "Captures prioritaires manquantes : " + ", ".join(missing_required))

    video_ok = has_video_ready()
    warnings += 0 if video_ok else 1
    add(lines, ok_line("Video", video_ok, "lien YouTube ou MP4 detecte" if video_ok else "lien YouTube non repertorie ou MP4 final non renseigne"))
    add(lines)

    add(lines, "## Archive ZIP")
    if not ZIP_PATH.exists():
        warnings += 1
        add(lines, ok_line("Archive ZIP", False, "introuvable"))
    else:
        with ZipFile(ZIP_PATH) as z:
            names = {name.replace("/", "\\") for name in z.namelist()}
            pdf_entries = [name for name in names if name.startswith("Rendus_PDF\\") and name.endswith(".pdf")]
            zip_pdf_ok = len(pdf_entries) >= EXPECTED_PDF_MIN
            warnings += 0 if zip_pdf_ok else 1
            add(lines, ok_line("PDF dans ZIP", zip_pdf_ok, f"{len(pdf_entries)} detectes"))

            for entry in REQUIRED_ZIP_ENTRIES:
                exists = entry in names
                warnings += 0 if exists else 1
                add(lines, ok_line(entry, exists, "present" if exists else "manquant"))
    add(lines)

    add(lines, "## Decision")
    if warnings == 0:
        add(lines, "[OK] Rendu final complet selon les controles automatises.")
    else:
        add(lines, f"[WARN] {warnings} point(s) a traiter ou a justifier avant depot officiel.")
        add(lines, "L'avertissement attendu tant que la demo n'est pas enregistree est : lien YouTube ou MP4 video final.")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nRapport ecrit : {REPORT_PATH}")
    return 0 if warnings == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())








































