from pathlib import Path

from pypdf import PdfReader, PdfWriter


ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "Rendus_PDF"
OUTPUT = PDF_DIR / "PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_DossierGroupeComplet.pdf"

PARTS = [
    ("Index du dossier complet", "17_DOSSIER_GROUPE_COMPLET_INDEX.pdf"),
    ("Synthese executive client", "14_SYNTHESE_EXECUTIVE_CLIENT.pdf"),
    ("Rapport technique groupe", "PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_RapportGroupe.pdf"),
    ("Solutions concretes demonstrables", "18_SOLUTIONS_CONCRETES_DEMO.pdf"),
    ("Roles contributions et preuves", "19_ROLES_CONTRIBUTIONS_PREUVES.pdf"),
    ("Rendu individuel - Yvan FOCSA", "PE-2526_M2CS_YvanFOCSA.pdf"),
    ("Rendu individuel - Youssef GUERNIOU", "PE-2526_M2CS_YoussefGUERNIOU.pdf"),
    ("Rendu individuel - Kilyan FELIX", "PE-2526_M2CS_KilyanFELIX.pdf"),
    ("Rendu individuel - Mahamadou DIACOUMBA", "PE-2526_M2CS_MahamadouDIACOUMBA.pdf"),
    ("Mode operatoire pfSense Wazuh lab", "20_MODE_OPERATOIRE_PFSENSE_WAZUH_LAB.pdf"),
    ("Dashboards alertes et qualification", "21_DASHBOARDS_ALERTES_QUALIFICATION.pdf"),
    ("Dashboard SOC offline", "24_DASHBOARD_SOC_OFFLINE.pdf"),
    ("Exploitation VM runbook et REX", "22_EXPLOITATION_VM_RUNBOOK_REX.pdf"),
    ("Preuves finales captures video depot", "23_PREUVES_FINALES_CAPTURES_VIDEO_DEPOT.pdf"),
    ("Mode operatoire captures Wazuh et preflight", "25_MODE_OPERATOIRE_CAPTURE_WAZUH_PREUVES.pdf"),
    ("Mode operatoire video et depot", "26_MODE_OPERATOIRE_VIDEO_DEPOT.pdf"),
    ("Runbook enregistrement video immediat", "33_RUNBOOK_ENREGISTREMENT_VIDEO_IMMEDIAT.pdf"),
    ("Manifeste depot et integrite", "27_MANIFESTE_DEPOT_ET_INTEGRITE.pdf"),
    ("Runbook express preuves restantes", "28_RUNBOOK_EXPRESS_PREUVES_RESTANTES.pdf"),
    ("Import des preuves finales", "29_IMPORT_PREUVES_FINALES.pdf"),
    ("Tableau de bord statut final", "30_TABLEAU_BORD_STATUT_FINAL.pdf"),
    ("Registre exigences et synthese", "00_REGISTRE_EXIGENCES_ET_SYNTHESE.pdf"),
    ("Guide de deploiement et utilisation", "02_GUIDE_DEPLOIEMENT_UTILISATION.pdf"),
    ("Playbooks, procedures et REX", "03_PLAYBOOKS_PROCEDURES_REX.pdf"),
    ("Risques, RGPD et conformite", "12_RISQUES_RGPD_CONFORMITE.pdf"),
    ("Plan de recette et acceptation", "13_PLAN_RECETTE_ACCEPTATION.pdf"),
    ("Dossier de preuves et captures", "07_DOSSIER_PREUVES_CAPTURES.pdf"),
    ("Annexe captures Wazuh", "16_ANNEXE_CAPTURES_WAZUH.pdf"),
    ("Audit final des consignes", "08_AUDIT_FINAL_CONSIGNES.pdf"),
    ("Backlog et planning", "05_BACKLOG_PLANNING.pdf"),
    ("Mode operatoire demo jour J", "10_MODE_OPERATOIRE_DEMO_JOUR_J.pdf"),
    ("Checklist depot final", "11_CHECKLIST_DEPOT_FINAL.pdf"),
]


def main() -> int:
    PDF_DIR.mkdir(exist_ok=True)
    writer = PdfWriter()
    missing: list[str] = []
    total_pages = 0

    for title, filename in PARTS:
        path = PDF_DIR / filename
        if not path.exists():
            missing.append(filename)
            continue

        reader = PdfReader(str(path))
        start_page = len(writer.pages)
        for page in reader.pages:
            writer.add_page(page)
        writer.add_outline_item(title, start_page)
        total_pages += len(reader.pages)

    if missing:
        print("PDF manquants pour le dossier consolide :")
        for filename in missing:
            print(f"- {filename}")
        return 1

    metadata = {
        "/Title": "Dossier groupe complet - Daylight / Cyber Trust",
        "/Author": "Cyber Trust",
        "/Subject": "Projet M2 CybersÃ©curitÃ© - SOC externalisÃ© Daylight",
        "/Creator": "tools/build_group_dossier_pdf.py",
    }
    writer.add_metadata(metadata)

    with OUTPUT.open("wb") as fh:
        writer.write(fh)

    print(f"Dossier groupe complet genere : {OUTPUT}")
    print(f"Documents fusionnes : {len(PARTS)}")
    print(f"Pages totales : {total_pages}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())







