from __future__ import annotations

import csv
import html
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "video"
if not CONFIG_DIR.exists():
    CONFIG_DIR = ROOT / "Config_Video"

OUT_DIR = ROOT / "Dashboards_Offline"
MARKDOWN_OUT = ROOT / "31_PACK_SOUTENANCE_JURY.md"
HTML_OUT = OUT_DIR / "daylight_jury_defense_pack.html"
CARDS_OUT = CONFIG_DIR / "daylight_jury_response_cards.csv"
PATH_OUT = CONFIG_DIR / "daylight_jury_demo_path.csv"
REPORT_OUT = ROOT / "jury-defense-pack-report.txt"

TOOL_DIR_NAME = "tools" if (ROOT / "tools").exists() else "Outils"


RESPONSE_CARDS = [
    {
        "theme": "Besoin client",
        "question": "Pourquoi Daylight a besoin d'un SOC externalise ?",
        "answer": "Daylight manipule des donnees patients sur plusieurs centres. Cyber Trust apporte une surveillance centralisee, des alertes qualifiees, des dashboards et des procedures sans imposer a Daylight de creer tout de suite un SOC interne.",
        "speaker": "Kilyan FELIX",
        "proof": "14_SYNTHESE_EXECUTIVE_CLIENT.md",
        "show": "Synthese executive client",
    },
    {
        "theme": "Architecture",
        "question": "Pourquoi pfSense dans votre solution ?",
        "answer": "pfSense apporte une brique concrete de segmentation : VLAN, NAT, refus par defaut, journalisation des flux et envoi syslog vers Wazuh. La revue firewall montre exactement les regles et les tests attendus.",
        "speaker": "Yvan FOCSA",
        "proof": "Dashboards_Offline/daylight_pfsense_firewall_review.html",
        "show": "Revue firewall pfSense",
    },
    {
        "theme": "Architecture",
        "question": "Votre lab est-il une architecture de production ?",
        "answer": "Non. Le lab prouve la faisabilite. En production, nous separons manager, indexer, dashboard, stockage, sauvegarde, haute disponibilite, supervision et gestion des secrets.",
        "speaker": "Yvan FOCSA",
        "proof": "01_RAPPORT_TECHNIQUE_GROUPE.md",
        "show": "Rapport technique groupe",
    },
    {
        "theme": "SIEM",
        "question": "Pourquoi Wazuh ?",
        "answer": "Wazuh est open-source, compatible agents et syslog, et assez complet pour couvrir endpoint, serveur, application, firewall, RBAC et dashboards dans un demonstrateur realiste sans cout de licence SIEM.",
        "speaker": "Youssef GUERNIOU",
        "proof": "Youssef GUERNIOU/Documentation_SIEM_Youssef_GUERNIOU.pdf",
        "show": "Documentation SIEM Youssef",
    },
    {
        "theme": "Detection",
        "question": "Quelles alertes sont vraiment demontrees ?",
        "answer": "Nous montrons 5712 pour brute force SSH, 100120 pour acces anormal a un dossier patient, 110020 pour mouvement lateral firewall, et les regles Daylight autour de l'application, des privileges, du phishing et des endpoints.",
        "speaker": "Kilyan FELIX",
        "proof": "21_DASHBOARDS_ALERTES_QUALIFICATION.md",
        "show": "Matrice qualification alertes",
    },
    {
        "theme": "Dashboards",
        "question": "Pourquoi deux dashboards ?",
        "answer": "Le dashboard technique aide l'analyste a investiguer. Le dashboard executif aide Daylight a piloter le service. Les deux vues servent des publics differents.",
        "speaker": "Kilyan FELIX",
        "proof": "Dashboards_Offline/daylight_soc_dashboard.html",
        "show": "Dashboard SOC offline",
    },
    {
        "theme": "Exploitation",
        "question": "Que faire si Docker ou Wazuh ne demarre pas pendant la soutenance ?",
        "answer": "On ne simule pas une preuve live. On montre le preflight, le rapport d'echec, la commande de relance, les captures deja extraites du dossier SIEM, le dashboard offline et la procedure CAP-25.",
        "speaker": "Mahamadou DIACOUMBA",
        "proof": "Rapports_Preflight/preflight-demo-report.txt",
        "show": "Rapport preflight / repair CAP-25",
    },
    {
        "theme": "Playbooks",
        "question": "Comment passez-vous d'une alerte a une action ?",
        "answer": "Chaque alerte a une qualification, un SLA, des verifications, une action immediate, une escalade et un REX. Les playbooks evitent que l'analyste improvise.",
        "speaker": "Mahamadou DIACOUMBA",
        "proof": "03_PLAYBOOKS_PROCEDURES_REX.md",
        "show": "Playbooks et REX",
    },
    {
        "theme": "RGPD",
        "question": "Comment limitez-vous les risques RGPD ?",
        "answer": "Nous appliquons minimisation, RBAC, retention limitee, journalisation des consultations et dashboards qui evitent d'exposer des donnees patients completes au public executif.",
        "speaker": "Yvan FOCSA",
        "proof": "12_RISQUES_RGPD_CONFORMITE.md",
        "show": "Risques RGPD et conformite",
    },
    {
        "theme": "Video",
        "question": "Comment prouver que toute l'equipe a participe ?",
        "answer": "Le shotlist, le pack d'enregistrement, les overlays nom/role et les rapports individuels associent chaque sequence a un intervenant et a une preuve ouverte a l'ecran.",
        "speaker": "Equipe Cyber Trust",
        "proof": "Dashboards_Offline/daylight_video_recording_pack.html",
        "show": "Pack enregistrement video",
    },
]


DEMO_PATH = [
    {
        "order": "01",
        "owner": "Kilyan FELIX",
        "open": "Presentation/Presentation_Daylight_CyberTrust.pptx",
        "message": "Contexte Daylight, objectif Cyber Trust, roles de l'equipe.",
        "fallback": "06_SUPPORT_PRESENTATION.md",
    },
    {
        "order": "02",
        "owner": "Yvan FOCSA",
        "open": "Annexes_Captures/CAP-12_architecture-solution.png",
        "message": "Architecture cible, segmentation et sources raccordees.",
        "fallback": "01_RAPPORT_TECHNIQUE_GROUPE.md",
    },
    {
        "order": "03",
        "owner": "Yvan FOCSA",
        "open": "Dashboards_Offline/daylight_pfsense_firewall_review.html",
        "message": "pfSense concret : interfaces, NAT, regles, logs et tests.",
        "fallback": "Config_PfSense/pfsense_firewall_rules.csv",
    },
    {
        "order": "04",
        "owner": "Youssef GUERNIOU",
        "open": "Annexes_Captures/CAP-01_wazuh-dashboard-login.png",
        "message": "Acces Wazuh, agents et preuves SIEM disponibles.",
        "fallback": "Preuves_SIEM_Youssef/Documentation_SIEM_Youssef_GUERNIOU.pdf",
    },
    {
        "order": "05",
        "owner": "Youssef GUERNIOU",
        "open": "Annexes_Captures/CAP-03_alerte-5712-brute-force-ssh.png",
        "message": "Detection brute force SSH et logique de regles.",
        "fallback": "Config_Wazuh/local_rules_daylight_pfsense.xml",
    },
    {
        "order": "06",
        "owner": "Kilyan FELIX",
        "open": "Dashboards_Offline/daylight_soc_dashboard.html",
        "message": "Dashboard technique, dashboard executif et qualification.",
        "fallback": "21_DASHBOARDS_ALERTES_QUALIFICATION.md",
    },
    {
        "order": "07",
        "owner": "Mahamadou DIACOUMBA",
        "open": "03_PLAYBOOKS_PROCEDURES_REX.md",
        "message": "Playbook, procedure, REX et exploitation VM/lab.",
        "fallback": "22_EXPLOITATION_VM_RUNBOOK_REX.md",
    },
    {
        "order": "08",
        "owner": "Equipe Cyber Trust",
        "open": "Dashboards_Offline/daylight_demo_control_center.html",
        "message": "Etat final, preuves restantes, ZIP, hash, limites honnetes.",
        "fallback": "30_TABLEAU_BORD_STATUT_FINAL.md",
    },
]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def esc(value: object) -> str:
    return html.escape(str(value or ""))


def render_response_rows() -> str:
    rows = []
    for card in RESPONSE_CARDS:
        rows.append(
            "<tr>"
            f"<td>{esc(card['theme'])}</td>"
            f"<td><b>{esc(card['question'])}</b><br>{esc(card['answer'])}</td>"
            f"<td>{esc(card['speaker'])}</td>"
            f"<td><code>{esc(card['proof'])}</code><br>{esc(card['show'])}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_demo_rows() -> str:
    rows = []
    for item in DEMO_PATH:
        rows.append(
            "<tr>"
            f"<td><code>{esc(item['order'])}</code></td>"
            f"<td>{esc(item['owner'])}</td>"
            f"<td><code>{esc(item['open'])}</code></td>"
            f"<td>{esc(item['message'])}</td>"
            f"<td><code>{esc(item['fallback'])}</code></td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_html() -> str:
    generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Daylight / Cyber Trust - Pack defense jury</title>
<style>
:root {{
  --ink:#182230;
  --muted:#667085;
  --line:#d0d5dd;
  --bg:#f6f7fb;
  --paper:#fff;
  --blue:#184e77;
  --green:#067647;
  --red:#b42318;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:Arial, sans-serif; color:var(--ink); background:var(--bg); }}
header {{ background:#172033; color:white; padding:26px 34px; border-bottom:4px solid #22a699; }}
header h1 {{ margin:0; font-size:28px; letter-spacing:0; }}
header p {{ margin:8px 0 0; color:#d7e3f4; max-width:1080px; line-height:1.45; }}
main {{ padding:24px 34px 42px; }}
section {{ background:var(--paper); border:1px solid var(--line); border-radius:8px; padding:18px; margin-top:16px; overflow-x:auto; }}
h2 {{ margin:0 0 12px; font-size:20px; }}
table {{ width:100%; border-collapse:collapse; font-size:14px; }}
th, td {{ border-bottom:1px solid #e4e7ec; padding:9px; text-align:left; vertical-align:top; }}
th {{ background:#eef2f7; color:#344054; }}
code {{ background:#f2f4f7; border:1px solid #e4e7ec; border-radius:5px; padding:2px 5px; }}
pre {{ white-space:pre-wrap; background:#111827; color:#f9fafb; border-radius:8px; padding:14px; line-height:1.45; }}
.grid {{ display:grid; grid-template-columns:repeat(4, 1fr); gap:12px; }}
.card {{ border:1px solid #d8dee9; border-radius:8px; padding:12px; background:#fbfcff; }}
.card b {{ display:block; margin-bottom:6px; }}
.warn {{ color:var(--red); font-weight:700; }}
@media (max-width: 1050px) {{ .grid {{ grid-template-columns:1fr; }} main, header {{ padding-left:18px; padding-right:18px; }} }}
</style>
</head>
<body>
<header>
  <h1>Daylight / Cyber Trust - Pack defense jury</h1>
  <p>Support oral genere le {esc(generated)} : parcours de demo, objections probables, reponses courtes et fichiers a ouvrir. Le but est de rester concret et honnete sur l'etat CAP-25/video.</p>
</header>
<main>
  <section>
    <h2>Regle d'or pendant la soutenance</h2>
    <div class="grid">
      <div class="card"><b>Montrer d'abord</b>Un fichier, une capture, un dashboard ou une commande avant d'expliquer.</div>
      <div class="card"><b>Ne pas maquiller</b>Si Docker/Wazuh est KO, dire que CAP-25 attend une relance reelle.</div>
      <div class="card"><b>Relier au role</b>Chaque membre parle sur son perimetre et cite sa preuve.</div>
      <div class="card"><b>Fermer proprement</b>Finir par ZIP, hash, limites et prochaines etapes.</div>
    </div>
  </section>

  <section>
    <h2>Parcours demo recommande</h2>
    <table><thead><tr><th>#</th><th>Owner</th><th>Ouvrir</th><th>Message</th><th>Plan B</th></tr></thead><tbody>
    {render_demo_rows()}
    </tbody></table>
  </section>

  <section>
    <h2>Questions jury : reponses courtes avec preuve</h2>
    <table><thead><tr><th>Theme</th><th>Question / reponse</th><th>Intervenant</th><th>Preuve a ouvrir</th></tr></thead><tbody>
    {render_response_rows()}
    </tbody></table>
  </section>

  <section>
    <h2>Phrase si le lab live ne repond pas</h2>
    <pre>Nous ne presentons pas une capture live fabriquee. Le preflight montre que Docker/Wazuh ne repond pas sur cette machine a cet instant. Nous avons donc deux preuves honnetes : les captures SIEM deja extraites du dossier de Youssef, et les supports reproductibles qui montrent comment relancer le lab et produire CAP-25 quand Docker/Wazuh sont disponibles.</pre>
  </section>

  <section>
    <h2>Commandes de cloture apres video/capture</h2>
    <pre>C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -ExecutionPolicy Bypass -File .\\{esc(TOOL_DIR_NAME)}\\repair_lab_and_capture_cap25.ps1 -StartDockerDesktop -StartKnownContainers -WaitSeconds 180
C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -ExecutionPolicy Bypass -File .\\{esc(TOOL_DIR_NAME)}\\import_final_evidence.ps1 -Item VIDEO-LINK -YoutubeUrl "https://youtu.be/xxxx" -RunChecks
C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -ExecutionPolicy Bypass -File .\\{esc(TOOL_DIR_NAME)}\\post_capture_finalize.ps1 -AllowWarnings</pre>
  </section>
</main>
</body>
</html>
"""


def render_markdown() -> str:
    lines = [
        "# Pack soutenance jury - Daylight / Cyber Trust",
        "",
        "## Objectif",
        "",
        "Ce document donne a l'equipe une fiche courte pour defendre le projet devant le jury : parcours de demonstration, questions probables, reponses courtes et preuves a ouvrir.",
        "",
        "## Parcours demo recommande",
        "",
        "| # | Owner | Ouvrir | Message | Plan B |",
        "|---|---|---|---|---|",
    ]
    for item in DEMO_PATH:
        lines.append(f"| {item['order']} | {item['owner']} | `{item['open']}` | {item['message']} | `{item['fallback']}` |")

    lines.extend(
        [
            "",
            "## Questions jury et reponses",
            "",
            "| Theme | Question | Reponse courte | Intervenant | Preuve |",
            "|---|---|---|---|---|",
        ]
    )
    for card in RESPONSE_CARDS:
        lines.append(
            f"| {card['theme']} | {card['question']} | {card['answer']} | {card['speaker']} | `{card['proof']}` |"
        )

    lines.extend(
        [
            "",
            "## Phrase si Docker/Wazuh ne repond pas",
            "",
            "> Nous ne presentons pas une capture live fabriquee. Le preflight montre que Docker/Wazuh ne repond pas sur cette machine a cet instant. Nous avons donc deux preuves honnetes : les captures SIEM deja extraites du dossier de Youssef, et les supports reproductibles qui montrent comment relancer le lab et produire CAP-25 quand Docker/Wazuh sont disponibles.",
            "",
            "## Commandes de cloture",
            "",
            "```powershell",
            f"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -ExecutionPolicy Bypass -File .\\{TOOL_DIR_NAME}\\repair_lab_and_capture_cap25.ps1 -StartDockerDesktop -StartKnownContainers -WaitSeconds 180",
            f"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -ExecutionPolicy Bypass -File .\\{TOOL_DIR_NAME}\\import_final_evidence.ps1 -Item VIDEO-LINK -YoutubeUrl \"https://youtu.be/xxxx\" -RunChecks",
            f"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -ExecutionPolicy Bypass -File .\\{TOOL_DIR_NAME}\\post_capture_finalize.ps1 -AllowWarnings",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def render_report() -> str:
    lines = [
        "=== Pack defense jury Daylight / Cyber Trust ===",
        f"Generation : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Markdown : {MARKDOWN_OUT}",
        f"HTML : {HTML_OUT}",
        f"Cartes questions : {CARDS_OUT}",
        f"Parcours demo : {PATH_OUT}",
        f"Questions : {len(RESPONSE_CARDS)}",
        f"Etapes demo : {len(DEMO_PATH)}",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(CARDS_OUT, RESPONSE_CARDS)
    write_csv(PATH_OUT, DEMO_PATH)
    MARKDOWN_OUT.write_text(render_markdown(), encoding="utf-8")
    HTML_OUT.write_text(render_html(), encoding="utf-8")
    REPORT_OUT.write_text(render_report(), encoding="utf-8")
    print(REPORT_OUT.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
