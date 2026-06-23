from __future__ import annotations

import csv
import html
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "video"
if not CONFIG_DIR.exists():
    CONFIG_DIR = ROOT / "Config_Video"

OUT_DIR = ROOT / "Dashboards_Offline"
OVERLAY_DIR = ROOT / "Video_Overlays"
if not OVERLAY_DIR.exists():
    OVERLAY_DIR = ROOT / "Video_Overlays"

SHOTLIST = CONFIG_DIR / "daylight_video_shotlist.csv"
CHECKLIST = CONFIG_DIR / "daylight_video_recording_checklist.csv"
SCENES_OUT = CONFIG_DIR / "daylight_video_obs_scenes.csv"
EVIDENCE_OUT = CONFIG_DIR / "daylight_video_evidence_map.csv"
HTML_OUT = OUT_DIR / "daylight_video_recording_pack.html"
REPORT_OUT = ROOT / "video-recording-pack-report.txt"

TOOL_DIR_NAME = "tools" if (ROOT / "tools").exists() else "Outils"

SPEAKER_META = {
    "Kilyan": {
        "full_name": "Kilyan FELIX",
        "role": "Chef de projet SOC / detection, alertes, dashboards, qualification",
        "overlay": "overlay_kilyan_felix.png",
    },
    "Yvan": {
        "full_name": "Yvan FOCSA",
        "role": "Architecte solution / pfSense, segmentation, architecture",
        "overlay": "overlay_yvan_focsa.png",
    },
    "Youssef": {
        "full_name": "Youssef GUERNIOU",
        "role": "Ingenieur SIEM / Wazuh, agents, regles, RBAC",
        "overlay": "overlay_youssef_guerniou.png",
    },
    "Mahamadou": {
        "full_name": "Mahamadou DIACOUMBA",
        "role": "Exploitation lab / VM, playbooks, procedures, REX",
        "overlay": "overlay_mahamadou_diacoumba.png",
    },
    "Equipe": {
        "full_name": "Equipe Cyber Trust",
        "role": "Conclusion, depot final et prochaines etapes Daylight",
        "overlay": "overlay_equipe_cyber_trust.png",
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return list(csv.DictReader(path.read_text(encoding="utf-8-sig").splitlines()))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def esc(value: object) -> str:
    return html.escape(str(value or ""))


def rel(path: Path) -> str:
    return (".." / path.relative_to(ROOT)).as_posix()


def first_file_reference(value: str) -> str:
    for part in value.replace(";", "/").split("/"):
        part = part.strip()
        if "." in part or part.startswith("CAP-"):
            return part
    return value.strip()


def source_for_screen(screen: str, proof: str) -> str:
    combined_raw = f"{screen} {proof}"
    cap_match = re.search(r"CAP-\d+", combined_raw, flags=re.IGNORECASE)
    if cap_match:
        token = cap_match.group(0).upper()
        capture_dir = ROOT / "Annexes_Captures"
        matches = sorted(capture_dir.glob(f"{token}*.png")) if capture_dir.exists() else []
        if matches:
            return f"Annexes_Captures/{matches[0].name}"
        return token

    combined = combined_raw.lower()
    if "pfsense" in combined:
        return "Dashboards_Offline/daylight_pfsense_firewall_review.html"
    if "wazuh" in combined or "cap-01" in combined or "cap-02" in combined or "cap-03" in combined:
        return "Annexes_Captures/CAP-01_wazuh-dashboard-login.png"
    if "dashboard" in combined and "offline" not in combined:
        return "Dashboards_Offline/daylight_soc_dashboard.html"
    if "qualification" in combined:
        return "21_DASHBOARDS_ALERTES_QUALIFICATION.md"
    if "runbook" in combined:
        return "22_EXPLOITATION_VM_RUNBOOK_REX.md"
    if "rex" in combined or "playbook" in combined:
        return "03_PLAYBOOKS_PROCEDURES_REX.md"
    if "presentation" in combined or "intro" in combined:
        return "Presentation/Presentation_Daylight_CyberTrust.pptx"
    if "architecture" in combined:
        return "Annexes_Captures/CAP-12_architecture-solution.png"
    if "final" in combined or "checklist" in combined:
        return "11_CHECKLIST_DEPOT_FINAL.md"
    ref = first_file_reference(proof)
    return ref or screen


def build_scenes(shotlist: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for index, shot in enumerate(shotlist, start=1):
        speaker = shot.get("speaker", "")
        meta = SPEAKER_META.get(speaker, SPEAKER_META["Equipe"])
        rows.append(
            {
                "scene_id": f"SCENE-{index:02d}",
                "start": shot.get("start", ""),
                "end": shot.get("end", ""),
                "speaker": meta["full_name"],
                "role": meta["role"],
                "overlay_png": meta["overlay"],
                "source_to_open": source_for_screen(shot.get("screen", ""), shot.get("proof_or_file", "")),
                "proof_or_file": shot.get("proof_or_file", ""),
                "screen_label": shot.get("screen", ""),
                "talking_point": shot.get("talking_point", ""),
                "obs_action": "Afficher partage ecran + overlay intervenant + micro actif",
            }
        )
    return rows


def build_evidence_map(scenes: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for scene in scenes:
        rows.append(
            {
                "scene_id": scene["scene_id"],
                "speaker": scene["speaker"],
                "file_to_show": scene["source_to_open"],
                "evidence": scene["proof_or_file"],
                "why_it_matters": scene["talking_point"],
            }
        )
    return rows


def status_for_file(project_path: str) -> str:
    if not project_path:
        return "a verifier"
    candidates = [
        ROOT / project_path,
        ROOT / project_path.replace("config/video/", "Config_Video/"),
        ROOT / project_path.replace("config/pfsense/", "Config_PfSense/"),
        ROOT / project_path.replace("config/wazuh/", "Config_Wazuh/"),
    ]
    if project_path.startswith("CAP-"):
        candidates.append(ROOT / "Annexes_Captures" / project_path)
    return "pret" if any(path.exists() for path in candidates) else "a verifier"


def render_scene_rows(scenes: list[dict[str, str]]) -> str:
    rendered = []
    for scene in scenes:
        overlay_path = OVERLAY_DIR / scene["overlay_png"]
        source_status = status_for_file(scene["source_to_open"])
        rendered.append(
            "<tr>"
            f"<td><code>{esc(scene['scene_id'])}</code><br>{esc(scene['start'])}-{esc(scene['end'])}</td>"
            f"<td><b>{esc(scene['speaker'])}</b><br><span>{esc(scene['role'])}</span></td>"
            f"<td>{esc(scene['screen_label'])}<br><code>{esc(scene['source_to_open'])}</code></td>"
            f"<td><code>{esc(scene['overlay_png'])}</code><br>{'OK' if overlay_path.exists() else 'a verifier'}</td>"
            f"<td>{esc(scene['talking_point'])}</td>"
            f"<td><span class=\"pill {'ok' if source_status == 'pret' else 'warn'}\">{esc(source_status)}</span></td>"
            "</tr>"
        )
    return "\n".join(rendered)


def render_checklist(checklist: list[dict[str, str]]) -> str:
    rows = []
    for item in checklist:
        rows.append(
            "<tr>"
            f"<td>{esc(item.get('phase'))}</td>"
            f"<td>{esc(item.get('item'))}</td>"
            f"<td>{esc(item.get('owner'))}</td>"
            f"<td>{esc(item.get('expected_evidence'))}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_html(scenes: list[dict[str, str]], checklist: list[dict[str, str]]) -> str:
    generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Daylight / Cyber Trust - Pack enregistrement video</title>
<style>
:root {{
  --ink:#182230;
  --muted:#667085;
  --line:#d0d5dd;
  --bg:#f6f7fb;
  --paper:#fff;
  --green:#067647;
  --red:#b42318;
  --blue:#184e77;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:Arial, sans-serif; background:var(--bg); color:var(--ink); }}
header {{ background:#172033; color:white; padding:26px 34px; border-bottom:4px solid #22a699; }}
header h1 {{ margin:0; font-size:28px; letter-spacing:0; }}
header p {{ margin:8px 0 0; color:#d7e3f4; max-width:1060px; line-height:1.45; }}
main {{ padding:24px 34px 42px; }}
section {{ background:var(--paper); border:1px solid var(--line); border-radius:8px; padding:18px; margin-top:16px; overflow-x:auto; }}
h2 {{ margin:0 0 12px; font-size:20px; }}
table {{ width:100%; border-collapse:collapse; font-size:14px; }}
th, td {{ border-bottom:1px solid #e4e7ec; padding:9px; text-align:left; vertical-align:top; }}
th {{ background:#eef2f7; color:#344054; }}
code {{ background:#f2f4f7; border:1px solid #e4e7ec; border-radius:5px; padding:2px 5px; }}
span {{ color:var(--muted); }}
pre {{ white-space:pre-wrap; background:#111827; color:#f9fafb; border-radius:8px; padding:14px; line-height:1.45; }}
.grid {{ display:grid; grid-template-columns:repeat(4, 1fr); gap:12px; }}
.step {{ border:1px solid #d8dee9; border-radius:8px; background:#fbfcff; padding:12px; min-height:96px; }}
.step b {{ display:block; margin-bottom:7px; }}
.pill {{ display:inline-block; border-radius:999px; padding:4px 9px; font-size:12px; font-weight:700; }}
.ok {{ background:#ecfdf3; color:var(--green); }}
.warn {{ background:#fff1f0; color:var(--red); }}
@media (max-width: 1050px) {{ .grid {{ grid-template-columns:1fr; }} main, header {{ padding-left:18px; padding-right:18px; }} }}
</style>
</head>
<body>
<header>
  <h1>Daylight / Cyber Trust - Pack enregistrement video</h1>
  <p>Regie concrete pour enregistrer la video 15-20 minutes : scenes, intervenants, overlays, fichiers a ouvrir et controles apres export. Genere le {esc(generated)}.</p>
</header>
<main>
  <section>
    <h2>Mode operatoire ultra-court</h2>
    <div class="grid">
      <div class="step"><b>1. Ouvrir</b>PowerPoint, centre de controle, revue pfSense, dashboard SOC, teleprompteur.</div>
      <div class="step"><b>2. Enregistrer</b>Un partage ecran lisible, micro clair, overlay nom/role visible a chaque prise de parole.</div>
      <div class="step"><b>3. Exporter</b>MP4 ou YouTube non repertorie. La video doit durer entre 15 et 20 minutes.</div>
      <div class="step"><b>4. Finaliser</b>Importer le lien/MP4 puis relancer validation, ZIP et hash.</div>
    </div>
  </section>

  <section>
    <h2>Scenes a creer dans OBS ou a suivre en partage ecran</h2>
    <table>
      <thead><tr><th>Scene</th><th>Intervenant</th><th>Ecran/fichier</th><th>Overlay</th><th>Message</th><th>Etat source</th></tr></thead>
      <tbody>{render_scene_rows(scenes)}</tbody>
    </table>
  </section>

  <section>
    <h2>Commandes apres enregistrement</h2>
    <pre># Option lien YouTube non repertorie
C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -ExecutionPolicy Bypass -File .\\{esc(TOOL_DIR_NAME)}\\import_final_evidence.ps1 -Item VIDEO-LINK -YoutubeUrl "https://youtu.be/xxxx" -RunChecks

# Option MP4 local
C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -ExecutionPolicy Bypass -File .\\{esc(TOOL_DIR_NAME)}\\import_final_evidence.ps1 -Item VIDEO-MP4 -SourcePath "C:\\chemin\\vers\\video.mp4" -RunChecks

# Reconstruction finale
C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -ExecutionPolicy Bypass -File .\\{esc(TOOL_DIR_NAME)}\\post_capture_finalize.ps1 -AllowWarnings</pre>
  </section>

  <section>
    <h2>Checklist enregistrement</h2>
    <table><thead><tr><th>Phase</th><th>Item</th><th>Owner</th><th>Preuve attendue</th></tr></thead><tbody>
    {render_checklist(checklist)}
    </tbody></table>
  </section>
</main>
</body>
</html>
"""


def render_report(scenes: list[dict[str, str]], checklist: list[dict[str, str]]) -> str:
    lines = [
        "=== Pack enregistrement video Daylight / Cyber Trust ===",
        f"Generation : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"HTML : {HTML_OUT}",
        f"Scenes OBS : {SCENES_OUT}",
        f"Evidence map : {EVIDENCE_OUT}",
        f"Scenes : {len(scenes)}",
        f"Checklist : {len(checklist)}",
        "Usage : ouvrir le HTML avant l'enregistrement et suivre les scenes dans l'ordre.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shotlist = read_csv(SHOTLIST)
    checklist = read_csv(CHECKLIST)
    scenes = build_scenes(shotlist)
    evidence = build_evidence_map(scenes)
    write_csv(SCENES_OUT, scenes)
    write_csv(EVIDENCE_OUT, evidence)
    HTML_OUT.write_text(render_html(scenes, checklist), encoding="utf-8")
    REPORT_OUT.write_text(render_report(scenes, checklist), encoding="utf-8")
    print(REPORT_OUT.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

