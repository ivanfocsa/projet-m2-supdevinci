from __future__ import annotations

import csv
import html
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHOTLIST = ROOT / "config" / "video" / "daylight_video_shotlist.csv"
CHECKLIST = ROOT / "config" / "video" / "daylight_video_recording_checklist.csv"
OUT_DIR = ROOT / "Dashboards_Offline"
HTML_OUT = OUT_DIR / "daylight_video_teleprompter.html"
REPORT_OUT = ROOT / "video-teleprompter-report.txt"


PROMPTS = {
    "00:00": "Bonjour, nous sommes Cyber Trust. Nous presentons le SOC externalise propose pour Daylight, reseau de centres d'audioprothesistes. L'objectif est de centraliser les evenements de securite, detecter les comportements suspects et fournir des procedures exploitables.",
    "01:30": "La solution repose sur Wazuh pour la supervision et pfSense pour la segmentation. Le demonstrateur couvre un endpoint, un serveur Linux simule, des logs applicatifs Daylight et une trajectoire cible multi-site.",
    "02:30": "Ici nous montrons la revue pfSense : interfaces, aliases, flux autorises, flux bloques, NAT, plan de tests et envoi syslog vers Wazuh. C'est la partie concrete firewall/routeur demandee par le cahier des charges.",
    "04:00": "Je presente la partie SIEM. Wazuh est deploye en lab, les preuves montrent le dashboard et la collecte multi-source. Les captures viennent de la documentation SIEM et peuvent etre recapturees en live si le lab repond.",
    "05:30": "Nous montrons maintenant les alertes SSH 5710, 5503, 5551 ou 5763, les regles metier Daylight 100110 a 100140, et l'acces anormal aux dossiers patients 100120.",
    "07:00": "Le RBAC separe les profils : admin complet, analyste et supervision en lecture. Le role soc_readonly evite qu'un profil de supervision modifie la plateforme.",
    "08:30": "Le dashboard technique sert aux analystes : severite, source, top regles et details de qualification. L'objectif est d'aller vite vers la bonne priorite.",
    "10:00": "La matrice de qualification associe chaque regle a une severite, un SLA de triage, des premieres verifications, une action immediate et une escalade.",
    "11:30": "Mon role est de rendre le lab exploitable : relance Docker/Wazuh, serveur-01, preflight, verification des services et preuves de redemarrage.",
    "13:00": "Une alerte ne suffit pas : les playbooks disent quoi verifier, qui prevenir, quoi bloquer et comment produire le REX. Exemple : brute force SSH ou acces patient.",
    "14:30": "Pour industrialiser, Cyber Trust propose un pilote, puis une extension progressive aux sites Daylight, avec retention, supervision, couts d'infrastructure et amelioration continue.",
    "16:00": "Pour conclure, le demonstrateur couvre les attentes : SIEM open-source, collecte multi-source, alertes, dashboards, RBAC, playbooks, REX, documentation et ZIP final controle.",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    return list(csv.DictReader(path.read_text(encoding="utf-8-sig").splitlines()))


def render_rows(rows: list[dict[str, str]]) -> str:
    cards = []
    for index, row in enumerate(rows, start=1):
        prompt = PROMPTS.get(row["start"], row["talking_point"])
        cards.append(
            f"""
<section class="segment" data-start="{html.escape(row['start'])}" data-end="{html.escape(row['end'])}">
  <div class="time">{html.escape(row['start'])} - {html.escape(row['end'])}</div>
  <div class="speaker">{html.escape(row['speaker'])}</div>
  <h2>{index}. {html.escape(row['talking_point'])}</h2>
  <div class="grid">
    <div><span>Ecran</span><strong>{html.escape(row['screen'])}</strong></div>
    <div><span>Preuve</span><strong>{html.escape(row['proof_or_file'])}</strong></div>
  </div>
  <p class="prompt">{html.escape(prompt)}</p>
</section>
"""
        )
    return "\n".join(cards)


def render_checklist(rows: list[dict[str, str]]) -> str:
    items = []
    for row in rows:
        items.append(
            f"<li><b>{html.escape(row['phase'])}</b> - {html.escape(row['item'])} <em>{html.escape(row['owner'])}</em><br><span>{html.escape(row['expected_evidence'])}</span></li>"
        )
    return "\n".join(items)


def render_html(shot_rows: list[dict[str, str]], checklist_rows: list[dict[str, str]]) -> str:
    generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Daylight / Cyber Trust - Teleprompteur video</title>
<style>
:root {{ --ink:#172033; --muted:#667085; --line:#d0d5dd; --bg:#f7f9fc; --accent:#175cd3; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:Arial, sans-serif; background:var(--bg); color:var(--ink); }}
header {{ position:sticky; top:0; z-index:3; padding:22px 34px; background:#172033; color:white; border-bottom:6px solid var(--accent); }}
header h1 {{ margin:0; font-size:28px; }}
header p {{ margin:8px 0 0; color:#d5e3ff; }}
main {{ display:grid; grid-template-columns:minmax(0, 1fr) 360px; gap:22px; padding:24px 34px 44px; }}
.segment {{ background:white; border:1px solid var(--line); border-radius:10px; padding:22px; margin-bottom:18px; }}
.time {{ color:var(--accent); font-weight:700; font-size:22px; }}
.speaker {{ display:inline-block; margin-top:8px; padding:7px 11px; border-radius:999px; background:#eef4ff; color:#1849a9; font-weight:700; }}
h2 {{ margin:14px 0 12px; font-size:24px; }}
.grid {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:12px 0 18px; }}
.grid div {{ border:1px solid #e4e7ec; border-radius:8px; padding:12px; background:#fcfcfd; }}
.grid span {{ display:block; color:var(--muted); font-size:13px; margin-bottom:5px; }}
.grid strong {{ font-size:16px; }}
.prompt {{ font-size:26px; line-height:1.35; margin:0; }}
aside {{ position:sticky; top:106px; align-self:start; background:white; border:1px solid var(--line); border-radius:10px; padding:18px; max-height:calc(100vh - 130px); overflow:auto; }}
aside h2 {{ font-size:19px; margin:0 0 12px; }}
ol, ul {{ padding-left:20px; }}
li {{ margin-bottom:11px; }}
li span {{ color:var(--muted); }}
code {{ background:#f2f4f7; border:1px solid #e4e7ec; border-radius:5px; padding:2px 5px; }}
.warning {{ background:#fff7ed; border:1px solid #fed7aa; border-radius:8px; padding:12px; margin:14px 0; }}
@media (max-width: 980px) {{ main {{ grid-template-columns:1fr; }} aside {{ position:static; }} .prompt {{ font-size:22px; }} }}
</style>
</head>
<body>
<header>
  <h1>Daylight / Cyber Trust - Teleprompteur video 15-20 min</h1>
  <p>Genere le {generated}. Afficher le nom de chaque intervenant a l'ecran pendant sa sequence.</p>
</header>
<main>
<div>
{render_rows(shot_rows)}
</div>
<aside>
  <h2>Checklist rapide</h2>
  <div class="warning"><b>Restes reels :</b> lien YouTube/MP4 final, et <code>CAP-25</code> seulement si Docker + Wazuh repondent.</div>
  <ul>
{render_checklist(checklist_rows)}
  </ul>
  <h2>Apres enregistrement</h2>
  <ol>
    <li>Publier en YouTube non repertorie ou deposer un MP4 final.</li>
    <li>Coller le lien dans <code>PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt</code>.</li>
    <li>Lancer <code>python .\\tools\\check_video_ready.py</code>.</li>
    <li>Lancer <code>powershell -ExecutionPolicy Bypass -File .\\tools\\post_capture_finalize.ps1</code>.</li>
  </ol>
</aside>
</main>
</body>
</html>
"""


def main() -> int:
    OUT_DIR.mkdir(exist_ok=True)
    shot_rows = read_csv(SHOTLIST)
    checklist_rows = read_csv(CHECKLIST)
    HTML_OUT.write_text(render_html(shot_rows, checklist_rows), encoding="utf-8")
    REPORT_OUT.write_text(
        "\n".join(
            [
                "=== Teleprompteur video Daylight / Cyber Trust ===",
                f"HTML : {HTML_OUT}",
                f"Segments : {len(shot_rows)}",
                f"Checklist : {len(checklist_rows)} items",
                "Usage : ouvrir le HTML pendant l'enregistrement de la video 15-20 minutes.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(REPORT_OUT.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


