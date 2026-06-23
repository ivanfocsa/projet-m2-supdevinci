from __future__ import annotations

import csv
import html
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPTURE_DIR = ROOT / "Annexes_Captures"
CHECKLIST = ROOT / "config" / "captures" / "daylight_capture_checklist.csv"
VIDEO_LINK = ROOT / "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt"
ZIP_PATH = ROOT / "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip"
ZIP_HASH = ROOT / "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip.sha256"
PDF_DIR = ROOT / "Rendus_PDF"
OUT_DIR = ROOT / "Dashboards_Offline"
HTML_OUT = OUT_DIR / "daylight_final_evidence_status.html"
REPORT_OUT = ROOT / "evidence-status-report.txt"
MP4_CANDIDATES = [
    ROOT / "PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4",
    ROOT / "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4",
]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def video_status() -> tuple[bool, str]:
    link_text = read_text(VIDEO_LINK)
    has_link = ("http://" in link_text or "https://" in link_text) and "Coller ici" not in link_text
    if has_link:
        return True, "Lien YouTube detecte"
    for path in MP4_CANDIDATES:
        if path.exists() and path.stat().st_size > 10_000_000:
            return True, f"MP4 detecte : {path.name}"
    return False, "Lien YouTube ou MP4 final absent"


def load_capture_rows() -> list[dict[str, str]]:
    return list(csv.DictReader(CHECKLIST.read_text(encoding="utf-8").splitlines()))


def status_badge(ok: bool) -> str:
    cls = "ok" if ok else "warn"
    label = "OK" if ok else "A faire"
    return f'<span class="badge {cls}">{label}</span>'


def row_html(cells: list[str]) -> str:
    return "<tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>"


def command_block(lines: list[str]) -> str:
    return "<pre>" + html.escape("\n".join(lines)) + "</pre>"


def build() -> dict[str, object]:
    rows = load_capture_rows()
    present_files = {path.name for path in CAPTURE_DIR.glob("CAP-*.png")} if CAPTURE_DIR.exists() else set()
    required = [row for row in rows if row["required_for_deposit"].lower() == "yes"]
    required_missing = [row for row in required if row["filename"] not in present_files]
    required_present = len(required) - len(required_missing)
    video_ok, video_detail = video_status()
    pdf_count = len(list(PDF_DIR.glob("*.pdf"))) if PDF_DIR.exists() else 0
    zip_ok = ZIP_PATH.exists()
    zip_hash_text = read_text(ZIP_HASH).strip()
    ready = required_present == len(required) and video_ok and zip_ok

    return {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ready": ready,
        "rows": rows,
        "present_files": present_files,
        "required_total": len(required),
        "required_present": required_present,
        "required_missing": required_missing,
        "video_ok": video_ok,
        "video_detail": video_detail,
        "pdf_count": pdf_count,
        "zip_ok": zip_ok,
        "zip_hash_text": zip_hash_text,
    }


def render_html(state: dict[str, object]) -> str:
    rows: list[dict[str, str]] = state["rows"]  # type: ignore[assignment]
    present_files: set[str] = state["present_files"]  # type: ignore[assignment]
    required_rows = [row for row in rows if row["required_for_deposit"].lower() == "yes"]

    capture_rows = "\n".join(
        row_html(
            [
                html.escape(row["id"]),
                f"<code>{html.escape(row['filename'])}</code>",
                html.escape(row["responsible"]),
                html.escape(row["evidence"]),
                status_badge(row["filename"] in present_files),
            ]
        )
        for row in required_rows
    )

    missing_commands = []
    for row in state["required_missing"]:  # type: ignore[union-attr]
        missing_commands.append(
            f'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -ExecutionPolicy Bypass -File .\\tools\\import_final_evidence.ps1 -Item {row["id"]} -SourcePath "C:\\Temp\\{row["filename"]}" -RunChecks'
        )
    if any(row["id"] == "CAP-25" for row in state["required_missing"]):  # type: ignore[union-attr]
        missing_commands.append(
            "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -ExecutionPolicy Bypass -File .\\tools\\preflight_demo.ps1 -WriteReport"
        )
        missing_commands.append(
            "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -ExecutionPolicy Bypass -File .\\tools\\import_final_evidence.ps1 -Item CAP-25 -RunChecks"
        )

    video_command = (
        'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -ExecutionPolicy Bypass -File .\\tools\\import_final_evidence.ps1 -Item VIDEO-LINK -YoutubeUrl "https://youtu.be/xxxx" -RunChecks'
    )
    final_command = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -ExecutionPolicy Bypass -File .\\tools\\post_capture_finalize.ps1"

    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Daylight - Statut final des preuves</title>
<style>
:root {{ --ink:#172033; --muted:#667085; --line:#d0d5dd; --bg:#f7f9fc; --ok:#1f7a4f; --warn:#b42318; --blue:#234a7c; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:Arial, sans-serif; background:var(--bg); color:var(--ink); }}
header {{ padding:28px 42px; background:#172033; color:white; }}
header p {{ margin:6px 0 0; color:#d5e3ff; }}
main {{ padding:28px 42px 48px; }}
.grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:16px; }}
.card, section {{ background:white; border:1px solid var(--line); border-radius:10px; padding:18px; }}
.card small {{ color:var(--muted); display:block; }}
.card strong {{ font-size:38px; display:block; margin-top:8px; }}
section {{ margin-top:18px; }}
h2 {{ margin:0 0 14px; font-size:22px; }}
table {{ width:100%; border-collapse:collapse; font-size:14px; }}
th, td {{ border-bottom:1px solid #e4e7ec; text-align:left; padding:10px; vertical-align:top; }}
th {{ background:#eef2f7; }}
code {{ background:#f2f4f7; border:1px solid #e4e7ec; border-radius:5px; padding:2px 5px; }}
pre {{ white-space:pre-wrap; background:#101828; color:#f9fafb; padding:14px; border-radius:8px; line-height:1.45; }}
.badge {{ display:inline-block; border-radius:999px; padding:5px 10px; font-weight:700; font-size:12px; }}
.ok {{ background:#ecfdf3; color:#067647; }}
.warn {{ background:#fff1f0; color:#b42318; }}
.note {{ color:var(--muted); }}
</style>
</head>
<body>
<header>
<h1>Daylight / Cyber Trust - Statut final des preuves</h1>
<p>Dashboard local genere depuis la checklist, les captures presentes, la video et le ZIP. Aucune preuve Wazuh n'est inventee.</p>
</header>
<main>
<div class="grid">
<div class="card"><small>Captures prioritaires</small><strong>{state['required_present']}/{state['required_total']}</strong></div>
<div class="card"><small>Video</small><strong>{'OK' if state['video_ok'] else 'Non'}</strong></div>
<div class="card"><small>PDF</small><strong>{state['pdf_count']}</strong></div>
<div class="card"><small>ZIP</small><strong>{'OK' if state['zip_ok'] else 'Non'}</strong></div>
</div>
<section>
<h2>Captures prioritaires</h2>
<table><thead><tr><th>ID</th><th>Fichier</th><th>Responsable</th><th>Preuve attendue</th><th>Etat</th></tr></thead><tbody>{capture_rows}</tbody></table>
</section>
<section>
<h2>Video</h2>
<p>{status_badge(bool(state['video_ok']))} {html.escape(str(state['video_detail']))}</p>
</section>
<section>
<h2>Commandes restantes</h2>
<p class="note">Adapter seulement le chemin <code>C:\\Temp\\...</code> avec le fichier capture reel.</p>
{command_block(missing_commands + ([video_command] if not state['video_ok'] else []) + [final_command])}
</section>
<section>
<h2>Archive et integrite</h2>
<p>Hash ZIP courant :</p>
{command_block([str(state['zip_hash_text']) or 'Hash non encore calcule'])}
</section>
</main>
</body>
</html>
"""


def render_report(state: dict[str, object]) -> str:
    missing = [row["filename"] for row in state["required_missing"]]  # type: ignore[index]
    lines = [
        "=== Tableau de bord final des preuves Daylight / Cyber Trust ===",
        f"Generation : {state['generated_at']}",
        f"Captures prioritaires : {state['required_present']}/{state['required_total']}",
        f"Video : {'OK' if state['video_ok'] else 'WARN'} - {state['video_detail']}",
        f"PDF : {state['pdf_count']}",
        f"ZIP : {'OK' if state['zip_ok'] else 'WARN'}",
        "",
    ]
    if missing:
        lines.append("Captures prioritaires manquantes :")
        lines.extend(f"- {name}" for name in missing)
    else:
        lines.append("Toutes les captures prioritaires sont presentes.")
    lines.extend(
        [
            "",
            f"Dashboard HTML : {HTML_OUT}",
            "Commande finale apres preuves :",
            r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\post_capture_finalize.ps1",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    OUT_DIR.mkdir(exist_ok=True)
    state = build()
    HTML_OUT.write_text(render_html(state), encoding="utf-8")
    REPORT_OUT.write_text(render_report(state), encoding="utf-8")
    print(f"Dashboard final preuves : {HTML_OUT}")
    print(f"Rapport statut preuves : {REPORT_OUT}")
    print(f"Captures prioritaires : {state['required_present']}/{state['required_total']}")
    print(f"Video : {'OK' if state['video_ok'] else 'WARN'}")
    return 0 if state["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
