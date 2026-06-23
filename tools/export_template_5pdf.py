from __future__ import annotations

import base64
import html
import re
import subprocess
from pathlib import Path
from zipfile import ZipFile

import markdown


ROOT = Path(__file__).resolve().parents[1]
LOCAL_TEMPLATE = ROOT / "templates" / "Tempalte.docx"
DOWNLOAD_TEMPLATE = Path(r"C:\Users\Ivan\Downloads\Tempalte.docx")
TEMPLATE = LOCAL_TEMPLATE if LOCAL_TEMPLATE.exists() else DOWNLOAD_TEMPLATE
HTML_DIR = ROOT / "Rendus_HTML_Template"
OUT_DIR = ROOT / "Rendu_Simple_5PDF"


GROUP_PARTS = [
    "17_DOSSIER_GROUPE_COMPLET_INDEX.md",
    "14_SYNTHESE_EXECUTIVE_CLIENT.md",
    "01_RAPPORT_TECHNIQUE_GROUPE.md",
    "18_SOLUTIONS_CONCRETES_DEMO.md",
    "19_ROLES_CONTRIBUTIONS_PREUVES.md",
    "Yvan FOCSA/PE-2526_M2CS_YvanFOCSA.md",
    "Youssef GUERNIOU/PE-2526_M2CS_YoussefGUERNIOU.md",
    "Kilyan FELIX/PE-2526_M2CS_KilyanFELIX.md",
    "Mahamadou DIACOUMBA/PE-2526_M2CS_MahamadouDIACOUMBA.md",
    "20_MODE_OPERATOIRE_PFSENSE_WAZUH_LAB.md",
    "21_DASHBOARDS_ALERTES_QUALIFICATION.md",
    "24_DASHBOARD_SOC_OFFLINE.md",
    "22_EXPLOITATION_VM_RUNBOOK_REX.md",
    "23_PREUVES_FINALES_CAPTURES_VIDEO_DEPOT.md",
    "25_MODE_OPERATOIRE_CAPTURE_WAZUH_PREUVES.md",
    "26_MODE_OPERATOIRE_VIDEO_DEPOT.md",
    "33_RUNBOOK_ENREGISTREMENT_VIDEO_IMMEDIAT.md",
    "27_MANIFESTE_DEPOT_ET_INTEGRITE.md",
    "28_RUNBOOK_EXPRESS_PREUVES_RESTANTES.md",
    "29_IMPORT_PREUVES_FINALES.md",
    "30_TABLEAU_BORD_STATUT_FINAL.md",
    "00_REGISTRE_EXIGENCES_ET_SYNTHESE.md",
    "02_GUIDE_DEPLOIEMENT_UTILISATION.md",
    "03_PLAYBOOKS_PROCEDURES_REX.md",
    "12_RISQUES_RGPD_CONFORMITE.md",
    "13_PLAN_RECETTE_ACCEPTATION.md",
    "07_DOSSIER_PREUVES_CAPTURES.md",
    "16_ANNEXE_CAPTURES_WAZUH.md",
    "08_AUDIT_FINAL_CONSIGNES.md",
    "05_BACKLOG_PLANNING.md",
    "10_MODE_OPERATOIRE_DEMO_JOUR_J.md",
    "11_CHECKLIST_DEPOT_FINAL.md",
]


DOCUMENTS = [
    {
        "kind": "Projet de groupe",
        "title": "Projet Daylight",
        "subtitle": "Dossier complet Cyber Trust",
        "author": "Équipe Cyber Trust",
        "role": "SOC externalise · Wazuh · pfSense · Playbooks",
        "output": "00_PROJET_COMPLET_Daylight_CyberTrust.pdf",
        "parts": GROUP_PARTS,
    },
    {
        "kind": "Rendu individuel",
        "title": "Yvan FOCSA",
        "subtitle": "Architecture de la solution",
        "author": "Yvan FOCSA",
        "role": "Architecte solution · pfSense · segmentation",
        "output": "01_Yvan_FOCSA_Architecte_Solution_pfSense.pdf",
        "parts": ["Yvan FOCSA/PE-2526_M2CS_YvanFOCSA.md"],
    },
    {
        "kind": "Rendu individuel",
        "title": "Youssef GUERNIOU",
        "subtitle": "SIEM Wazuh et collecte",
        "author": "Youssef GUERNIOU",
        "role": "Ingénieur SIEM · Wazuh · agents · RBAC",
        "output": "02_Youssef_GUERNIOU_SIEM_Wazuh.pdf",
        "parts": ["Youssef GUERNIOU/PE-2526_M2CS_YoussefGUERNIOU.md"],
    },
    {
        "kind": "Rendu individuel",
        "title": "Kilyan FELIX",
        "subtitle": "Détection, dashboards et qualification",
        "author": "Kilyan FELIX",
        "role": "Chef de projet SOC · détection · pilotage",
        "output": "03_Kilyan_FELIX_Detection_Dashboards_Qualification.pdf",
        "parts": ["Kilyan FELIX/PE-2526_M2CS_KilyanFELIX.md"],
    },
    {
        "kind": "Rendu individuel",
        "title": "Mahamadou DIACOUMBA",
        "subtitle": "Exploitation lab, playbooks et REX",
        "author": "Mahamadou DIACOUMBA",
        "role": "Exploitation VM · procédures · REX incidents",
        "output": "04_Mahamadou_DIACOUMBA_Playbooks_VM_REX.pdf",
        "parts": ["Mahamadou DIACOUMBA/PE-2526_M2CS_MahamadouDIACOUMBA.md"],
    },
]


def chrome_path() -> Path:
    candidates = [
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Chrome ou Edge introuvable pour l'export PDF.")


def template_assets() -> dict[str, str]:
    assets: dict[str, str] = {}
    with ZipFile(TEMPLATE) as zf:
        for name in zf.namelist():
            if name.startswith("word/media/") and name.lower().endswith(".png"):
                key = Path(name).stem
                encoded = base64.b64encode(zf.read(name)).decode("ascii")
                assets[key] = f"data:image/png;base64,{encoded}"
    return assets


def convert_mermaid_fences(text: str) -> str:
    return re.sub(
        r"```mermaid\n(.*?)```",
        lambda match: "<pre><code>" + html.escape(match.group(1).strip()) + "</code></pre>",
        text,
        flags=re.DOTALL,
    )


def local_image_uris(markdown_text: str, source: Path) -> str:
    pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

    def repl(match: re.Match[str]) -> str:
        alt, target = match.group(1), match.group(2).strip()
        if target.startswith(("http://", "https://", "data:", "#")):
            return match.group(0)
        clean_target = target.split()[0].strip("<>")
        resolved = (source.parent / clean_target).resolve()
        if not resolved.exists():
            resolved = (ROOT / clean_target).resolve()
        if resolved.exists():
            return f"![{alt}]({resolved.as_uri()})"
        return match.group(0)

    return pattern.sub(repl, markdown_text)


def pretty_markdown(source: Path, drop_first_h1: bool = False) -> str:
    raw = source.read_text(encoding="utf-8", errors="ignore")
    raw = local_image_uris(raw, source)
    raw = convert_mermaid_fences(raw)
    if drop_first_h1:
        raw = re.sub(r"^# .+?\n+", "", raw, count=1)
    return raw


def toc_for_parts(parts: list[str]) -> str:
    items = []
    for index, part in enumerate(parts, start=1):
        source = ROOT / part
        title = source.stem.replace("_", " ")
        if source.exists():
            first = re.search(r"^#\s+(.+)$", source.read_text(encoding="utf-8", errors="ignore"), re.MULTILINE)
            if first:
                title = first.group(1)
        items.append(f"<li><span>{index:02d}</span>{html.escape(title)}</li>")
    return "<ol class=\"toc\">" + "\n".join(items) + "</ol>"


def section_html(part: str, single: bool) -> str:
    source = ROOT / part
    body_md = pretty_markdown(source, drop_first_h1=single)
    body = markdown.markdown(body_md, extensions=["extra", "sane_lists", "tables", "fenced_code"])
    if single:
        return body

    heading = source.stem.replace("_", " ")
    first = re.search(r"^#\s+(.+)$", source.read_text(encoding="utf-8", errors="ignore"), re.MULTILINE)
    if first:
        heading = first.group(1)
    return f"<section class=\"document-section\"><h1>{html.escape(heading)}</h1>{body}</section>"


def css(primary: str = "#1F3864", secondary: str = "#2E4D7B", pale: str = "#F2F5FA") -> str:
    return f"""
@page {{
  size: A4;
  margin: 17mm 15mm 18mm 15mm;
}}
* {{ box-sizing: border-box; }}
html {{ color-scheme: light; }}
body {{
  margin: 0;
  color: #172033;
  font-family: Arial, "Segoe UI", sans-serif;
  font-size: 10.2pt;
  line-height: 1.48;
  background: white;
}}
.print-header {{
  position: fixed;
  top: -11mm;
  left: 0;
  right: 0;
  height: 9mm;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #6B7280;
  font-size: 8pt;
}}
.print-footer {{
  position: fixed;
  bottom: -12mm;
  left: 0;
  right: 0;
  color: #6B7280;
  font-size: 8pt;
  text-align: center;
}}
.cover {{
  min-height: 246mm;
  page-break-after: always;
  display: grid;
  grid-template-rows: auto 1fr auto;
}}
.cover-top {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 18mm;
}}
.brand {{
  color: {primary};
  font-size: 10pt;
  line-height: 1.4;
}}
.brand strong {{
  display: block;
  color: #111827;
  font-size: 11pt;
  margin-top: 2mm;
}}
.logos {{
  display: flex;
  align-items: center;
  gap: 8mm;
}}
.logos img {{
  width: 23mm;
  height: 23mm;
  object-fit: contain;
}}
.cover-main {{
  align-self: center;
  padding: 20mm 0 10mm;
}}
.kicker {{
  color: {secondary};
  font-size: 11pt;
  letter-spacing: 0;
  text-transform: uppercase;
  font-weight: 700;
  margin-bottom: 8mm;
}}
.cover h1 {{
  margin: 0;
  color: {primary};
  font-size: 35pt;
  line-height: 1.05;
  font-weight: 800;
}}
.cover h2 {{
  margin: 7mm 0 0;
  color: #253047;
  font-size: 18pt;
  font-weight: 500;
}}
.cover-meta {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4mm;
  margin-top: 15mm;
}}
.meta-card {{
  background: {pale};
  border-radius: 4mm;
  padding: 5mm;
  min-height: 20mm;
}}
.meta-card span {{
  display: block;
  color: #6B7280;
  font-size: 8.5pt;
  margin-bottom: 2mm;
}}
.meta-card strong {{
  color: #172033;
  font-size: 10.5pt;
}}
.cover-bottom {{
  color: #4B5563;
  font-size: 9.5pt;
  display: flex;
  justify-content: space-between;
  gap: 10mm;
}}
.intro-page {{
  page-break-after: always;
}}
.intro-page h1 {{
  color: {primary};
  font-size: 23pt;
  margin: 0 0 8mm;
}}
.intro-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 5mm;
  margin: 8mm 0 10mm;
}}
.toc {{
  margin: 0;
  padding: 0;
  list-style: none;
  counter-reset: toc;
}}
.toc li {{
  display: grid;
  grid-template-columns: 15mm 1fr;
  gap: 4mm;
  padding: 2.5mm 0;
  border-bottom: 0.4pt solid #E7ECF4;
}}
.toc li span {{
  color: {secondary};
  font-weight: 700;
}}
.content {{
  page-break-before: always;
}}
.document-section {{
  page-break-before: always;
}}
.document-section:first-child {{
  page-break-before: auto;
}}
h1 {{
  color: {primary};
  font-size: 22pt;
  line-height: 1.15;
  margin: 0 0 9mm;
  font-weight: 800;
}}
h2 {{
  color: {primary};
  font-size: 15pt;
  line-height: 1.25;
  margin: 10mm 0 4mm;
  font-weight: 750;
}}
h3 {{
  color: {secondary};
  font-size: 12pt;
  line-height: 1.25;
  margin: 7mm 0 3mm;
  font-weight: 700;
}}
h4, h5, h6 {{
  color: #27364F;
  font-size: 10.5pt;
  margin: 5mm 0 2mm;
}}
p {{
  margin: 0 0 3.2mm;
}}
ul, ol {{
  margin: 0 0 4mm 0;
  padding-left: 7mm;
}}
li {{
  margin: 0 0 1.8mm;
  padding-left: 1mm;
}}
ul li::marker {{
  color: {primary};
  font-size: 0.8em;
}}
ol li::marker {{
  color: {primary};
  font-weight: 700;
}}
table {{
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin: 4mm 0 7mm;
  font-size: 8.7pt;
  page-break-inside: avoid;
}}
th, td {{
  border: 0.4pt solid #DCE3EE;
  padding: 2.6mm 2.8mm;
  vertical-align: top;
}}
th {{
  background: {pale};
  color: {primary};
  font-weight: 700;
}}
tr:nth-child(even) td {{
  background: #FAFBFD;
}}
code {{
  font-family: Consolas, "Courier New", monospace;
  font-size: 8.8pt;
  color: #1F2937;
  background: #F4F6FA;
  border-radius: 2mm;
  padding: 0.2mm 1mm;
}}
pre {{
  background: #F4F6FA;
  border-radius: 3mm;
  padding: 4mm;
  white-space: pre-wrap;
  word-break: break-word;
  page-break-inside: avoid;
  margin: 4mm 0 6mm;
}}
pre code {{
  background: transparent;
  padding: 0;
}}
blockquote {{
  margin: 5mm 0;
  padding: 4mm 5mm;
  background: {pale};
  border-radius: 3mm;
  color: #253047;
}}
img {{
  max-width: 100%;
  height: auto;
  display: block;
  margin: 4mm auto 6mm;
  border-radius: 2mm;
}}
a {{
  color: {primary};
  text-decoration: none;
}}
hr {{
  display: none;
}}
"""


def cover(doc: dict[str, object], assets: dict[str, str]) -> str:
    sup = assets.get("image1", "")
    cyber = assets.get("image2", "")
    return f"""
<section class="cover">
  <div class="cover-top">
    <div class="brand">
      Mastère 2 Cybersécurité · Année 2025-2026
      <strong>Projet de groupe · Cyber Trust</strong>
    </div>
    <div class="logos">
      <img src="{sup}" alt="Sup de Vinci">
      <img src="{cyber}" alt="Cyber Trust">
    </div>
  </div>
  <div class="cover-main">
    <div class="kicker">{html.escape(str(doc["kind"]))}</div>
    <h1>{html.escape(str(doc["title"]))}</h1>
    <h2>{html.escape(str(doc["subtitle"]))}</h2>
    <div class="cover-meta">
      <div class="meta-card"><span>Établissement</span><strong>Sup de Vinci · Mastère 2 Cybersécurité</strong></div>
      <div class="meta-card"><span>Client</span><strong>Daylight</strong></div>
      <div class="meta-card"><span>Auteur</span><strong>{html.escape(str(doc["author"]))}</strong></div>
      <div class="meta-card"><span>Rôle</span><strong>{html.escape(str(doc["role"]))}</strong></div>
      <div class="meta-card"><span>Équipe</span><strong>Y. FOCSA · Y. GUERNIOU · K. FELIX · M. DIACOUMBA</strong></div>
      <div class="meta-card"><span>Version</span><strong>1.1 · Mise en page finale</strong></div>
    </div>
  </div>
  <div class="cover-bottom">
    <span>Prestataire fictif : Cyber Trust</span>
    <span>Date de rendu : 26/06/2026</span>
  </div>
</section>
"""


def html_document(doc: dict[str, object], assets: dict[str, str]) -> str:
    parts = list(doc["parts"])  # type: ignore[index]
    single = len(parts) == 1
    body = "\n".join(section_html(part, single=single) for part in parts)
    intro_cards = f"""
<section class="intro-page">
  <h1>Sommaire</h1>
  <p>Rendu structuré pour la correction, la soutenance et la consultation rapide des preuves.</p>
  <div class="intro-grid">
    <div class="meta-card"><span>Type de rendu</span><strong>{html.escape(str(doc["kind"]))}</strong></div>
    <div class="meta-card"><span>Périmètre</span><strong>{html.escape(str(doc["role"]))}</strong></div>
  </div>
  {toc_for_parts(parts)}
</section>
"""
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>{html.escape(str(doc["title"]))}</title>
  <style>{css()}</style>
</head>
<body>
  <div class="print-header"><span>Projet Daylight · Cyber Trust</span><span>{html.escape(str(doc["kind"]))}</span></div>
  <div class="print-footer">Sup de Vinci · Mastère 2 Cybersécurité · Année 2025-2026</div>
  {cover(doc, assets)}
  {intro_cards}
  <main class="content">{body}</main>
</body>
</html>
"""


def print_pdf(chrome: Path, html_path: Path, pdf_path: Path) -> None:
    command = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--allow-file-access-from-files",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ]
    subprocess.run(command, check=True, timeout=90)


def main() -> int:
    if not TEMPLATE.exists():
        raise FileNotFoundError(f"Template introuvable : {TEMPLATE}")
    HTML_DIR.mkdir(exist_ok=True)
    OUT_DIR.mkdir(exist_ok=True)
    assets = template_assets()
    chrome = chrome_path()
    for doc in DOCUMENTS:
        stem = Path(str(doc["output"])).stem
        html_path = HTML_DIR / f"{stem}.html"
        pdf_path = OUT_DIR / str(doc["output"])
        html_path.write_text(html_document(doc, assets), encoding="utf-8")
        print_pdf(chrome, html_path, pdf_path)
        print(f"[OK] {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
