from __future__ import annotations

import csv
import html
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "Dashboards_Offline"
HTML_OUT = OUT_DIR / "daylight_demo_control_center.html"
REPORT_OUT = ROOT / "demo-control-center-report.txt"

CAPTURE_DIR = ROOT / "Annexes_Captures"
CAPTURE_CHECKLIST = ROOT / "config" / "captures" / "daylight_capture_checklist.csv"
SHOTLIST = ROOT / "config" / "video" / "daylight_video_shotlist.csv"
VIDEO_LINK = ROOT / "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt"
PREFLIGHT_REPORT = ROOT / "preflight-demo-report.txt"
ZIP_PATH = ROOT / "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip"
ZIP_HASH = ROOT / "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip.sha256"
PDF_DIR = ROOT / "Rendus_PDF"

MP4_CANDIDATES = [
    ROOT / "PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4",
    ROOT / "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4",
    ROOT / "Video" / "PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4",
    ROOT / "Video" / "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4",
]

if not CAPTURE_CHECKLIST.exists():
    CAPTURE_CHECKLIST = ROOT / "Config_Captures" / "daylight_capture_checklist.csv"
if not SHOTLIST.exists():
    SHOTLIST = ROOT / "Config_Video" / "daylight_video_shotlist.csv"
if not VIDEO_LINK.exists():
    VIDEO_LINK = ROOT / "Video" / "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt"
if not PREFLIGHT_REPORT.exists():
    PREFLIGHT_REPORT = ROOT / "Rapports_Preflight" / "preflight-demo-report.txt"
if not ZIP_PATH.exists():
    ZIP_PATH = ROOT.parent / "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip"
if not ZIP_HASH.exists():
    ZIP_HASH = ROOT.parent / "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip.sha256"

TOOL_DIR_NAME = "tools" if (ROOT / "tools").exists() else "Outils"

KEY_LINKS = [
    ("Teleprompteur video", "Dashboards_Offline/daylight_video_teleprompter.html"),
    ("Overlays nom/role video", "Dashboards_Offline/daylight_video_overlays.html"),
    ("Pack enregistrement video", "Dashboards_Offline/daylight_video_recording_pack.html"),
    ("Scenes OBS video", "config/video/daylight_video_obs_scenes.csv"),
    ("README overlays video", "Video_Overlays/README_VIDEO_OVERLAYS.md"),
    ("Revue firewall pfSense", "Dashboards_Offline/daylight_pfsense_firewall_review.html"),
    ("Guide import pfSense", "config/pfsense/README_IMPORT_PFSENSE_DAYLIGHT.md"),
    ("Plan tests pfSense", "config/pfsense/pfsense_demo_test_plan.csv"),
    ("Pack defense jury", "Dashboards_Offline/daylight_jury_defense_pack.html"),
    ("Matrice conformite", "Dashboards_Offline/daylight_compliance_matrix.html"),
    ("CSV conformite", "config/compliance/daylight_compliance_matrix.csv"),
    ("Cartes reponses jury", "config/video/daylight_jury_response_cards.csv"),
    ("Dashboard SOC offline", "Dashboards_Offline/daylight_soc_dashboard.html"),
    ("Dashboard statut preuves", "Dashboards_Offline/daylight_final_evidence_status.html"),
    ("Rapport relance CAP-25", "lab-cap25-recovery-report.txt"),
    ("Rapport groupe PDF", "Rendus_PDF/PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_RapportGroupe.pdf"),
    ("Dossier groupe complet PDF", "Rendus_PDF/PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_DossierGroupeComplet.pdf"),
    ("Presentation PowerPoint", "Presentation_Daylight_CyberTrust.pptx"),
    ("Matrice pfSense", "config/pfsense/pfsense_firewall_rules.csv"),
    ("Regles Wazuh custom", "config/wazuh/local_rules_daylight_pfsense.xml"),
    ("Matrice qualification alertes", "config/wazuh/daylight_alert_qualification_matrix.csv"),
    ("Runbook lab VM", "config/lab/daylight_lab_runbook.csv"),
    ("Logs pfSense demo", "Demo_Logs/pfsense.log"),
    ("Logs applicatifs demo", "Demo_Logs/daylight_app.log"),
]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return list(csv.DictReader(path.read_text(encoding="utf-8-sig").splitlines()))


def relative_candidates(project_relative: str) -> list[str]:
    candidates = [project_relative]
    prefix_map = {
        "config/pfsense/": "Config_PfSense/",
        "config/wazuh/": "Config_Wazuh/",
        "config/lab/": "Config_Lab/",
        "config/captures/": "Config_Captures/",
        "config/video/": "Config_Video/",
    }
    for source_prefix, final_prefix in prefix_map.items():
        if project_relative.startswith(source_prefix):
            candidates.append(project_relative.replace(source_prefix, final_prefix, 1))
    if project_relative == "lab-cap25-recovery-report.txt":
        candidates.append("Rapports_Preflight/lab-cap25-recovery-report.txt")
    if project_relative == "Presentation_Daylight_CyberTrust.pptx":
        candidates.append("Presentation/Presentation_Daylight_CyberTrust.pptx")
    if project_relative.endswith(".md") and "/" not in project_relative:
        candidates.append(f"Sources_Markdown/{project_relative}")
    return candidates


def resolve_relative(project_relative: str) -> tuple[str, Path]:
    for candidate in relative_candidates(project_relative):
        target = ROOT / candidate
        if target.exists():
            return candidate, target
    return project_relative, ROOT / project_relative


def href_for(project_relative: str) -> str:
    _, target = resolve_relative(project_relative)
    href = Path("..") / target.relative_to(ROOT)
    return href.as_posix()


def status_pill(ok: bool, label_ok: str = "OK", label_warn: str = "A faire") -> str:
    cls = "ok" if ok else "warn"
    label = label_ok if ok else label_warn
    return f'<span class="pill {cls}">{html.escape(label)}</span>'


def file_link(label: str, project_relative: str) -> str:
    _, target = resolve_relative(project_relative)
    label_html = html.escape(label)
    if not target.exists():
        return f'<span class="missing">{label_html}</span>'
    return f'<a href="{html.escape(href_for(project_relative))}">{label_html}</a>'


def command_block(commands: list[str]) -> str:
    return "<pre>" + html.escape("\n".join(commands)) + "</pre>"


def video_status() -> tuple[bool, str]:
    text = read_text(VIDEO_LINK)
    if ("http://" in text or "https://" in text) and "Coller ici" not in text:
        urls = re.findall(r"https?://\S+", text)
        return True, urls[0] if urls else "Lien detecte"
    for mp4 in MP4_CANDIDATES:
        if mp4.exists() and mp4.stat().st_size > 10_000_000:
            return True, mp4.name
    return False, "Lien YouTube ou MP4 final absent"


def preflight_line(pattern: str) -> str:
    for line in read_text(PREFLIGHT_REPORT).splitlines():
        if pattern in line:
            return line.strip()
    return "Non controle"


def build_state() -> dict[str, object]:
    captures = csv_rows(CAPTURE_CHECKLIST)
    shotlist = csv_rows(SHOTLIST)
    present = {path.name for path in CAPTURE_DIR.glob("CAP-*.png")} if CAPTURE_DIR.exists() else set()
    required = [row for row in captures if row.get("required_for_deposit", "").lower() == "yes"]
    missing_required = [row for row in required if row.get("filename") not in present]
    video_ok, video_detail = video_status()

    return {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "captures": captures,
        "shotlist": shotlist,
        "present": present,
        "required_total": len(required),
        "required_present": len(required) - len(missing_required),
        "missing_required": missing_required,
        "video_ok": video_ok,
        "video_detail": video_detail,
        "pdf_count": len(list(PDF_DIR.glob("*.pdf"))) if PDF_DIR.exists() else 0,
        "zip_ok": ZIP_PATH.exists(),
        "zip_hash": read_text(ZIP_HASH).strip(),
        "docker_line": preflight_line("Docker daemon"),
        "wazuh_line": preflight_line("https://localhost"),
    }


def render_quick_links() -> str:
    rows = []
    for label, rel_path in KEY_LINKS:
        _, target = resolve_relative(rel_path)
        state = status_pill(target.exists(), "pret", "absent")
        rows.append(
            "<tr>"
            f"<td>{file_link(label, rel_path)}</td>"
            f"<td><code>{html.escape(rel_path)}</code></td>"
            f"<td>{state}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_capture_rows(state: dict[str, object]) -> str:
    present: set[str] = state["present"]  # type: ignore[assignment]
    rows: list[dict[str, str]] = state["captures"]  # type: ignore[assignment]
    priority_rows = [row for row in rows if row.get("priority") == "1" or row.get("required_for_deposit") == "yes"]
    rendered = []
    for row in priority_rows:
        filename = row.get("filename", "")
        is_present = filename in present
        capture_link = f"Annexes_Captures/{filename}"
        rendered.append(
            "<tr>"
            f"<td>{html.escape(row.get('id', ''))}</td>"
            f"<td>{file_link(filename, capture_link) if is_present else '<code>' + html.escape(filename) + '</code>'}</td>"
            f"<td>{html.escape(row.get('responsible', ''))}</td>"
            f"<td>{html.escape(row.get('evidence', ''))}</td>"
            f"<td>{status_pill(is_present, 'presente', 'manquante')}</td>"
            "</tr>"
        )
    return "\n".join(rendered)


def proof_reference(proof: str, state: dict[str, object]) -> str:
    if not proof:
        return ""
    resolved_proof, direct = resolve_relative(proof)
    if direct.exists():
        return file_link(proof, resolved_proof)

    present: set[str] = state["present"]  # type: ignore[assignment]
    parts = [part.strip() for part in proof.split("/") if part.strip()]
    linked_parts = []
    for part in parts:
        match = next((name for name in sorted(present) if name.startswith(part)), None)
        if match:
            linked_parts.append(file_link(part, f"Annexes_Captures/{match}"))
        else:
            linked_parts.append(html.escape(part))
    return " / ".join(linked_parts) if linked_parts else html.escape(proof)

def render_shotlist_rows(state: dict[str, object]) -> str:
    shotlist: list[dict[str, str]] = state["shotlist"]  # type: ignore[assignment]
    rendered = []
    for row in shotlist:
        proof = row.get("proof_or_file", "")
        proof_cell = proof_reference(proof, state)
        rendered.append(
            "<tr>"
            f"<td>{html.escape(row.get('start', ''))}-{html.escape(row.get('end', ''))}</td>"
            f"<td>{html.escape(row.get('speaker', ''))}</td>"
            f"<td>{html.escape(row.get('screen', ''))}</td>"
            f"<td>{proof_cell}</td>"
            f"<td>{html.escape(row.get('talking_point', ''))}</td>"
            "</tr>"
        )
    return "\n".join(rendered)


def render_html(state: dict[str, object]) -> str:
    missing = state["missing_required"]  # type: ignore[assignment]
    missing_commands = [
        fr"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\{TOOL_DIR_NAME}\repair_lab_and_capture_cap25.ps1 -WaitSeconds 30",
        fr"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\{TOOL_DIR_NAME}\repair_lab_and_capture_cap25.ps1 -StartDockerDesktop -StartKnownContainers -WaitSeconds 180",
        fr"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\{TOOL_DIR_NAME}\repair_lab_and_capture_cap25.ps1 -RunYoussefSetup -StartKnownContainers -WaitSeconds 180",
        fr"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\{TOOL_DIR_NAME}\post_capture_finalize.ps1 -AllowWarnings",
    ]
    if not state["video_ok"]:
        missing_commands.insert(
            2,
            fr'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\{TOOL_DIR_NAME}\import_final_evidence.ps1 -Item VIDEO-LINK -YoutubeUrl "https://youtu.be/xxxx" -RunChecks',
        )

    blockers = []
    if missing:
        blockers.append("CAP-25 preflight reel a produire apres relance Docker/Wazuh")
    if not state["video_ok"]:
        blockers.append("Lien YouTube non repertorie ou MP4 final a ajouter")
    blocker_text = " ; ".join(blockers) if blockers else "Aucun blocage detecte par le controle local"

    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Daylight / Cyber Trust - Centre de controle demo</title>
<style>
:root {{
  --ink:#182230;
  --muted:#667085;
  --line:#d0d5dd;
  --paper:#ffffff;
  --bg:#f6f7fb;
  --blue:#1d4e89;
  --green:#067647;
  --red:#b42318;
  --amber:#b54708;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:Arial, sans-serif; color:var(--ink); background:var(--bg); }}
header {{ background:#182230; color:white; padding:24px 34px; border-bottom:4px solid #22a699; }}
header h1 {{ margin:0; font-size:28px; letter-spacing:0; }}
header p {{ margin:8px 0 0; color:#d7e3f4; max-width:980px; line-height:1.45; }}
main {{ padding:24px 34px 40px; }}
.summary {{ display:grid; grid-template-columns:repeat(5, minmax(130px, 1fr)); gap:12px; margin-bottom:16px; }}
.metric, section {{ background:var(--paper); border:1px solid var(--line); border-radius:8px; }}
.metric {{ padding:14px; min-height:96px; }}
.metric span {{ color:var(--muted); font-size:13px; display:block; }}
.metric strong {{ display:block; margin-top:10px; font-size:30px; }}
section {{ padding:18px; margin-top:16px; }}
h2 {{ margin:0 0 12px; font-size:20px; }}
table {{ width:100%; border-collapse:collapse; font-size:14px; }}
th, td {{ border-bottom:1px solid #e4e7ec; padding:9px; text-align:left; vertical-align:top; }}
th {{ background:#eef2f7; color:#344054; }}
a {{ color:var(--blue); font-weight:700; text-decoration:none; }}
a:hover {{ text-decoration:underline; }}
code {{ background:#f2f4f7; border:1px solid #e4e7ec; border-radius:5px; padding:2px 5px; }}
pre {{ white-space:pre-wrap; background:#111827; color:#f9fafb; border-radius:8px; padding:14px; line-height:1.45; }}
.pill {{ display:inline-block; border-radius:999px; padding:4px 9px; font-size:12px; font-weight:700; }}
.ok {{ background:#ecfdf3; color:var(--green); }}
.warn {{ background:#fff1f0; color:var(--red); }}
.info {{ background:#eef4ff; color:var(--blue); }}
.missing {{ color:var(--red); font-weight:700; }}
.two {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }}
.note {{ color:var(--muted); line-height:1.45; }}
@media (max-width: 980px) {{ .summary, .two {{ grid-template-columns:1fr; }} main, header {{ padding-left:18px; padding-right:18px; }} }}
</style>
</head>
<body>
<header>
  <h1>Daylight / Cyber Trust - Centre de controle demo</h1>
  <p>Point unique pour lancer la soutenance, ouvrir les preuves concretes, suivre les captures restantes et retrouver les commandes de finalisation.</p>
</header>
<main>
  <div class="summary">
    <div class="metric"><span>Captures prioritaires</span><strong>{state['required_present']}/{state['required_total']}</strong></div>
    <div class="metric"><span>Video</span><strong>{'OK' if state['video_ok'] else 'A faire'}</strong></div>
    <div class="metric"><span>PDF</span><strong>{state['pdf_count']}</strong></div>
    <div class="metric"><span>ZIP</span><strong>{'OK' if state['zip_ok'] else 'Non'}</strong></div>
    <div class="metric"><span>Etat depot</span><strong>{'Pret' if not blockers else 'Partiel'}</strong></div>
  </div>

  <section>
    <h2>Decision rapide</h2>
    <p>{status_pill(not blockers, 'pret depot', 'a completer')} {html.escape(blocker_text)}</p>
    <p class="note">Docker : {html.escape(str(state['docker_line']))}<br>Wazuh : {html.escape(str(state['wazuh_line']))}</p>
  </section>

  <section>
    <h2>Ouvrir les supports a montrer</h2>
    <table><thead><tr><th>Support</th><th>Fichier</th><th>Etat</th></tr></thead><tbody>
    {render_quick_links()}
    </tbody></table>
  </section>

  <section>
    <h2>Captures prioritaires et preuves concretes</h2>
    <table><thead><tr><th>ID</th><th>Fichier</th><th>Responsable</th><th>Preuve</th><th>Etat</th></tr></thead><tbody>
    {render_capture_rows(state)}
    </tbody></table>
  </section>

  <section>
    <h2>Deroule video 15-20 minutes</h2>
    <table><thead><tr><th>Timing</th><th>Intervenant</th><th>Ecran</th><th>Preuve</th><th>Message</th></tr></thead><tbody>
    {render_shotlist_rows(state)}
    </tbody></table>
  </section>

  <div class="two">
    <section>
      <h2>Commandes jour J</h2>
      {command_block(missing_commands)}
    </section>
    <section>
      <h2>Hash archive</h2>
      {command_block([str(state['zip_hash']) or 'Hash non encore calcule'])}
      <p class="note">Le hash doit etre recalcule apres ajout de CAP-25 ou du lien video.</p>
    </section>
  </div>
</main>
</body>
</html>
"""


def render_report(state: dict[str, object]) -> str:
    missing = [row["filename"] for row in state["missing_required"]]  # type: ignore[index]
    lines = [
        "=== Centre de controle demo Daylight / Cyber Trust ===",
        f"Generation : {state['generated_at']}",
        f"HTML : {HTML_OUT}",
        f"Captures prioritaires : {state['required_present']}/{state['required_total']}",
        f"Video : {'OK' if state['video_ok'] else 'WARN'} - {state['video_detail']}",
        f"Docker : {state['docker_line']}",
        f"Wazuh : {state['wazuh_line']}",
        "",
    ]
    if missing:
        lines.append("Preuves prioritaires restantes :")
        lines.extend(f"- {name}" for name in missing)
    else:
        lines.append("Toutes les preuves prioritaires sont presentes.")
    return "\n".join(lines) + "\n"


def main() -> int:
    OUT_DIR.mkdir(exist_ok=True)
    state = build_state()
    HTML_OUT.write_text(render_html(state), encoding="utf-8")
    REPORT_OUT.write_text(render_report(state), encoding="utf-8")
    print(f"Centre de controle demo : {HTML_OUT}")
    print(f"Rapport : {REPORT_OUT}")
    print(f"Captures prioritaires : {state['required_present']}/{state['required_total']}")
    print(f"Video : {'OK' if state['video_ok'] else 'WARN'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())










