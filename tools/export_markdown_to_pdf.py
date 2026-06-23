from pathlib import Path
import re
import subprocess
import sys

import markdown


ROOT = Path(__file__).resolve().parents[1]

DOCUMENTS = {
    "README_LIVRABLES.md": "README_LIVRABLES",
    "00_REGISTRE_EXIGENCES_ET_SYNTHESE.md": "00_REGISTRE_EXIGENCES_ET_SYNTHESE",
    "01_RAPPORT_TECHNIQUE_GROUPE.md": "PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_RapportGroupe",
    "02_GUIDE_DEPLOIEMENT_UTILISATION.md": "02_GUIDE_DEPLOIEMENT_UTILISATION",
    "03_PLAYBOOKS_PROCEDURES_REX.md": "03_PLAYBOOKS_PROCEDURES_REX",
    "04_SCRIPT_VIDEO_DEMO.md": "04_SCRIPT_VIDEO_DEMO",
    "05_BACKLOG_PLANNING.md": "05_BACKLOG_PLANNING",
    "06_SUPPORT_PRESENTATION.md": "06_SUPPORT_PRESENTATION",
    "07_DOSSIER_PREUVES_CAPTURES.md": "07_DOSSIER_PREUVES_CAPTURES",
    "08_AUDIT_FINAL_CONSIGNES.md": "08_AUDIT_FINAL_CONSIGNES",
    "09_NOTES_ORATEUR_SOUTENANCE.md": "09_NOTES_ORATEUR_SOUTENANCE",
    "10_MODE_OPERATOIRE_DEMO_JOUR_J.md": "10_MODE_OPERATOIRE_DEMO_JOUR_J",
    "11_CHECKLIST_DEPOT_FINAL.md": "11_CHECKLIST_DEPOT_FINAL",
    "12_RISQUES_RGPD_CONFORMITE.md": "12_RISQUES_RGPD_CONFORMITE",
    "13_PLAN_RECETTE_ACCEPTATION.md": "13_PLAN_RECETTE_ACCEPTATION",
    "14_SYNTHESE_EXECUTIVE_CLIENT.md": "14_SYNTHESE_EXECUTIVE_CLIENT",
    "15_QA_SOUTENANCE_JURY_CLIENT.md": "15_QA_SOUTENANCE_JURY_CLIENT",
    "16_ANNEXE_CAPTURES_WAZUH.md": "16_ANNEXE_CAPTURES_WAZUH",
    "17_DOSSIER_GROUPE_COMPLET_INDEX.md": "17_DOSSIER_GROUPE_COMPLET_INDEX",
    "18_SOLUTIONS_CONCRETES_DEMO.md": "18_SOLUTIONS_CONCRETES_DEMO",
    "19_ROLES_CONTRIBUTIONS_PREUVES.md": "19_ROLES_CONTRIBUTIONS_PREUVES",
    "20_MODE_OPERATOIRE_PFSENSE_WAZUH_LAB.md": "20_MODE_OPERATOIRE_PFSENSE_WAZUH_LAB",
    "21_DASHBOARDS_ALERTES_QUALIFICATION.md": "21_DASHBOARDS_ALERTES_QUALIFICATION",
    "22_EXPLOITATION_VM_RUNBOOK_REX.md": "22_EXPLOITATION_VM_RUNBOOK_REX",
    "23_PREUVES_FINALES_CAPTURES_VIDEO_DEPOT.md": "23_PREUVES_FINALES_CAPTURES_VIDEO_DEPOT",
    "24_DASHBOARD_SOC_OFFLINE.md": "24_DASHBOARD_SOC_OFFLINE",
    "25_MODE_OPERATOIRE_CAPTURE_WAZUH_PREUVES.md": "25_MODE_OPERATOIRE_CAPTURE_WAZUH_PREUVES",
    "26_MODE_OPERATOIRE_VIDEO_DEPOT.md": "26_MODE_OPERATOIRE_VIDEO_DEPOT",
    "27_MANIFESTE_DEPOT_ET_INTEGRITE.md": "27_MANIFESTE_DEPOT_ET_INTEGRITE",
    "28_RUNBOOK_EXPRESS_PREUVES_RESTANTES.md": "28_RUNBOOK_EXPRESS_PREUVES_RESTANTES",
    "29_IMPORT_PREUVES_FINALES.md": "29_IMPORT_PREUVES_FINALES",
    "30_TABLEAU_BORD_STATUT_FINAL.md": "30_TABLEAU_BORD_STATUT_FINAL",
    "31_PACK_SOUTENANCE_JURY.md": "31_PACK_SOUTENANCE_JURY",
    "32_MATRICE_CONFORMITE_CAHIER_DES_CHARGES.md": "32_MATRICE_CONFORMITE_CAHIER_DES_CHARGES",
    "33_RUNBOOK_ENREGISTREMENT_VIDEO_IMMEDIAT.md": "33_RUNBOOK_ENREGISTREMENT_VIDEO_IMMEDIAT",
    "Yvan FOCSA/PE-2526_M2CS_YvanFOCSA.md": "PE-2526_M2CS_YvanFOCSA",
    "Youssef GUERNIOU/PE-2526_M2CS_YoussefGUERNIOU.md": "PE-2526_M2CS_YoussefGUERNIOU",
    "Kilyan FELIX/PE-2526_M2CS_KilyanFELIX.md": "PE-2526_M2CS_KilyanFELIX",
    "Mahamadou DIACOUMBA/PE-2526_M2CS_MahamadouDIACOUMBA.md": "PE-2526_M2CS_MahamadouDIACOUMBA",
}

CHROME_CANDIDATES = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
]

CSS = """
@page {
  size: A4;
  margin: 18mm 16mm;
}
* {
  box-sizing: border-box;
}
body {
  font-family: "Segoe UI", Arial, sans-serif;
  color: #111827;
  line-height: 1.45;
  font-size: 10.5pt;
}
h1 {
  font-size: 22pt;
  margin: 0 0 16px;
  color: #0f172a;
}
h2 {
  font-size: 15pt;
  margin: 26px 0 10px;
  padding-bottom: 4px;
  border-bottom: 1px solid #d1d5db;
  color: #1f2937;
}
h3 {
  font-size: 12.5pt;
  margin: 18px 0 8px;
  color: #374151;
}
p, li {
  margin: 0 0 7px;
}
ul, ol {
  margin-top: 0;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 10px 0 18px;
  page-break-inside: avoid;
}
th, td {
  border: 1px solid #d1d5db;
  padding: 6px 7px;
  vertical-align: top;
}
th {
  background: #eef2f7;
  font-weight: 650;
}
code {
  font-family: Consolas, "Courier New", monospace;
  font-size: 9.5pt;
}
pre {
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  padding: 10px;
  white-space: pre-wrap;
  page-break-inside: avoid;
}
blockquote {
  border-left: 4px solid #9ca3af;
  margin-left: 0;
  padding-left: 12px;
  color: #374151;
}
img {
  max-width: 100%;
  height: auto;
}
figure.capture {
  margin: 10px 0 18px;
  page-break-inside: avoid;
}
figcaption {
  color: #4b5563;
  font-size: 9pt;
  margin-top: 5px;
}
.footer {
  margin-top: 28px;
  padding-top: 8px;
  border-top: 1px solid #d1d5db;
  color: #6b7280;
  font-size: 9pt;
}
"""


def find_chrome() -> Path:
    for candidate in CHROME_CANDIDATES:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Chrome ou Edge introuvable pour l'export PDF.")


def html_document(title: str, body: str) -> str:
    safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>{safe_title}</title>
  <style>{CSS}</style>
</head>
<body>
  {body}
  <div class="footer">Projet 4 Daylight / Cyber Trust - source Markdown exportee localement</div>
</body>
</html>
"""


def convert_mermaid_fences(text: str) -> str:
    return re.sub(
        r"```mermaid\n(.*?)```",
        lambda match: "<pre><code>" + match.group(1).strip() + "</code></pre>",
        text,
        flags=re.DOTALL,
    )



def print_pdf_with_fallback(chrome: Path, html_path: Path, pdf_path: Path) -> str:
    command = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ]
    try:
        subprocess.run(command, check=True, timeout=60)
        return "generated"
    except subprocess.CalledProcessError as exc:
        if pdf_path.exists() and pdf_path.stat().st_size > 0:
            print(f"[WARN] Chrome a echoue pour {pdf_path.name} (code {exc.returncode}); PDF existant conserve.")
            return "kept-existing"
        print(f"[WARN] Chrome a echoue pour {pdf_path.name} (code {exc.returncode}); PDF fallback Pillow requis.")
        return "chrome-failed"
    except subprocess.TimeoutExpired:
        if pdf_path.exists() and pdf_path.stat().st_size > 0:
            print(f"[WARN] Chrome a expire pour {pdf_path.name}; PDF existant conserve.")
            return "kept-existing"
        print(f"[WARN] Chrome a expire pour {pdf_path.name}; PDF fallback Pillow requis.")
        return "chrome-timeout"
def main() -> int:
    html_dir = ROOT / "Rendus_HTML"
    pdf_dir = ROOT / "Rendus_PDF"
    html_dir.mkdir(exist_ok=True)
    pdf_dir.mkdir(exist_ok=True)

    chrome = find_chrome()
    generated = []

    for source_name, output_name in DOCUMENTS.items():
        source = ROOT / source_name
        if not source.exists():
            print(f"[SKIP] Introuvable: {source_name}")
            continue

        raw = source.read_text(encoding="utf-8")
        raw = convert_mermaid_fences(raw)
        body = markdown.markdown(raw, extensions=["extra", "sane_lists", "tables", "fenced_code"])

        html_path = html_dir / f"{output_name}.html"
        pdf_path = pdf_dir / f"{output_name}.pdf"
        html_path.write_text(html_document(output_name, body), encoding="utf-8")

        status = print_pdf_with_fallback(chrome, html_path, pdf_path)
        generated.append((pdf_path, status))

    print("PDF generes :")
    for path, status in generated:
        print(f"- {path} ({status})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())






















