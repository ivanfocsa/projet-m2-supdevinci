from __future__ import annotations

import csv
import html
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "compliance"
if not CONFIG_DIR.exists() and (ROOT / "Config_Compliance").exists():
    CONFIG_DIR = ROOT / "Config_Compliance"

OUT_DIR = ROOT / "Dashboards_Offline"
CSV_OUT = CONFIG_DIR / "daylight_compliance_matrix.csv"
HTML_OUT = OUT_DIR / "daylight_compliance_matrix.html"
MARKDOWN_OUT = ROOT / "32_MATRICE_CONFORMITE_CAHIER_DES_CHARGES.md"
REPORT_OUT = ROOT / "compliance-matrix-report.txt"


REQUIREMENTS = [
    {
        "id": "PED-01",
        "source": "Cadre pedagogique",
        "requirement": "Video 15-20 minutes presentant le MVP avec prise de parole individuelle",
        "evidence": "Dashboards_Offline/daylight_video_recording_pack.html; Config_Video/daylight_video_obs_scenes.csv; Video/PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt",
        "owner": "Equipe",
        "status": "A_FINALISER",
        "note": "Script, teleprompteur, overlays et scene pack prets ; lien YouTube/MP4 reel encore absent.",
    },
    {
        "id": "PED-02",
        "source": "Cadre pedagogique",
        "requirement": "Rapport technique complet avec architecture, configuration, logs, roles, procedures et REX",
        "evidence": "Rendus_PDF/PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_RapportGroupe.pdf; Rendus_PDF/PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_DossierGroupeComplet.pdf",
        "owner": "Equipe",
        "status": "OK",
        "note": "Rapport groupe et dossier groupe consolide generes.",
    },
    {
        "id": "PED-03",
        "source": "Cadre pedagogique",
        "requirement": "Contribution individuelle de chaque membre",
        "evidence": "Rendus_PDF/PE-2526_M2CS_YvanFOCSA.pdf; Rendus_PDF/PE-2526_M2CS_YoussefGUERNIOU.pdf; Rendus_PDF/PE-2526_M2CS_KilyanFELIX.pdf; Rendus_PDF/PE-2526_M2CS_MahamadouDIACOUMBA.pdf",
        "owner": "Equipe",
        "status": "OK",
        "note": "Un rendu individuel PDF par membre.",
    },
    {
        "id": "PED-04",
        "source": "Cadre pedagogique",
        "requirement": "Gestion de projet, planning, roles et methodologie",
        "evidence": "05_BACKLOG_PLANNING.md; 19_ROLES_CONTRIBUTIONS_PREUVES.md; 31_PACK_SOUTENANCE_JURY.md",
        "owner": "Kilyan FELIX",
        "status": "OK",
        "note": "Backlog, roles et parcours de soutenance disponibles.",
    },
    {
        "id": "SOC-01",
        "source": "Cahier des charges",
        "requirement": "Analyse initiale du besoin client Daylight",
        "evidence": "14_SYNTHESE_EXECUTIVE_CLIENT.md; 01_RAPPORT_TECHNIQUE_GROUPE.md",
        "owner": "Kilyan FELIX",
        "status": "OK",
        "note": "Contexte client, risques et objectifs formalises.",
    },
    {
        "id": "SOC-02",
        "source": "Cahier des charges",
        "requirement": "Document architecture technique",
        "evidence": "01_RAPPORT_TECHNIQUE_GROUPE.md; Annexes_Captures/CAP-12_architecture-solution.png",
        "owner": "Yvan FOCSA",
        "status": "OK",
        "note": "Architecture de demonstration et cible documentees.",
    },
    {
        "id": "SOC-03",
        "source": "Cahier des charges",
        "requirement": "Demonstrateur operationnel",
        "evidence": "Youssef GUERNIOU/setup-siem-lab.ps1; Preuves_SIEM_Youssef/Documentation_SIEM_Youssef_GUERNIOU.pdf; Rapports_Preflight/preflight-demo-report.txt; Annexes_Captures/CAP-25_preflight-demo-ok.png",
        "owner": "Youssef GUERNIOU / Mahamadou DIACOUMBA",
        "status": "OK",
        "note": "Lab Wazuh operationnel : Docker daemon OK, 3 conteneurs Wazuh UP, dashboard https://localhost en statut 200 via preflight CAP-25.",
    },
    {
        "id": "SOC-04",
        "source": "Cahier des charges",
        "requirement": "Collecte multi-source agents, syslog ou API",
        "evidence": "Youssef GUERNIOU/Documentation_SIEM_Youssef_GUERNIOU.pdf; Demo_Logs/pfsense.log; Demo_Logs/daylight_app.log; Config_PfSense/pfsense_syslog_wazuh.md",
        "owner": "Youssef GUERNIOU",
        "status": "OK",
        "note": "Endpoint, serveur, logs applicatifs, pfSense/syslog et logs demo couverts.",
    },
    {
        "id": "SOC-05",
        "source": "Cahier des charges",
        "requirement": "SIEM open-source centralise",
        "evidence": "Youssef GUERNIOU/Documentation_SIEM_Youssef_GUERNIOU.pdf; 02_GUIDE_DEPLOIEMENT_UTILISATION.md",
        "owner": "Youssef GUERNIOU",
        "status": "OK",
        "note": "Wazuh retenu et documente.",
    },
    {
        "id": "SOC-06",
        "source": "Cahier des charges",
        "requirement": "Regles de detection et alerting personnalisables",
        "evidence": "Config_Wazuh/local_rules_daylight_pfsense.xml; Config_Wazuh/daylight_alert_qualification_matrix.csv; Annexes_Captures/CAP-03_alerte-5712-brute-force-ssh.png",
        "owner": "Kilyan FELIX / Youssef GUERNIOU",
        "status": "OK",
        "note": "Regles 5712, 100xxx et 110xxx referencees et qualifiees.",
    },
    {
        "id": "SOC-07",
        "source": "Cahier des charges",
        "requirement": "Dashboards lisibles et segmentes",
        "evidence": "Dashboards_Offline/daylight_soc_dashboard.html; Annexes_Captures/CAP-07_dashboard-technique.png; Annexes_Captures/CAP-08_dashboard-executif.png",
        "owner": "Kilyan FELIX",
        "status": "OK",
        "note": "Vue analyste et executive disponibles.",
    },
    {
        "id": "SOC-08",
        "source": "Cahier des charges",
        "requirement": "Playbooks de reponse semi-automatises",
        "evidence": "03_PLAYBOOKS_PROCEDURES_REX.md; Annexes_Captures/CAP-10_playbook-brute-force.png; Annexes_Captures/CAP-28_rex-incident-rempli.png",
        "owner": "Mahamadou DIACOUMBA",
        "status": "OK",
        "note": "Playbooks et REX documentes avec preuves visuelles.",
    },
    {
        "id": "SOC-09",
        "source": "Cahier des charges",
        "requirement": "Reporting simple et exportable",
        "evidence": "Rendus_PDF/; Dashboards_Offline/daylight_final_evidence_status.html; MANIFEST_DEPOT.md",
        "owner": "Kilyan FELIX",
        "status": "OK",
        "note": "PDF, dashboards offline, manifeste et hash disponibles.",
    },
    {
        "id": "SOC-10",
        "source": "Cahier des charges",
        "requirement": "Interface web accessible et segmentee par roles supervision, analyste, admin",
        "evidence": "Annexes_Captures/CAP-01_wazuh-dashboard-login.png; Annexes_Captures/CAP-09_rbac-analyste-lecture-seule.png",
        "owner": "Youssef GUERNIOU",
        "status": "OK",
        "note": "Preuves Wazuh et RBAC extraites du dossier SIEM.",
    },
    {
        "id": "SOC-11",
        "source": "Cahier des charges",
        "requirement": "Simulation d'un ou plusieurs sites clients avec VMs ou conteneurs",
        "evidence": "Config_Lab/daylight_vm_inventory.csv; Config_Lab/daylight_lab_runbook.csv; 22_EXPLOITATION_VM_RUNBOOK_REX.md",
        "owner": "Mahamadou DIACOUMBA",
        "status": "OK",
        "note": "Inventaire et runbook VM/conteneurs fournis.",
    },
    {
        "id": "SOC-12",
        "source": "Cahier des charges",
        "requirement": "Generation de logs realistes attaque et safe",
        "evidence": "tools/generate_demo_logs.py; Demo_Logs/; tools/send_demo_logs_to_syslog.py; Annexes_Captures/CAP-27_rejeu-logs-dry-run.png",
        "owner": "Mahamadou DIACOUMBA",
        "status": "OK",
        "note": "Logs pfSense, application, AD/fichiers, mail et endpoint generes.",
    },
    {
        "id": "SOC-13",
        "source": "Cahier des charges",
        "requirement": "Templates de deploiement client et solution industrialisable",
        "evidence": "02_GUIDE_DEPLOIEMENT_UTILISATION.md; Config_PfSense/README_IMPORT_PFSENSE_DAYLIGHT.md; Config_PfSense/pfsense_demo_test_plan.csv",
        "owner": "Yvan FOCSA",
        "status": "OK",
        "note": "Guide, imports pfSense, configs Wazuh et trajectoire cible documentes.",
    },
]


def path_exists(reference: str) -> bool:
    ref = reference.strip()
    if not ref:
        return False
    candidates = [ROOT / ref]
    if ref.startswith("Config_"):
        candidates.append(ROOT / ref.replace("Config_", "config/").replace("\\", "/"))
    if ref.endswith("/"):
        candidates.append(ROOT / ref.rstrip("/"))
    return any(path.exists() for path in candidates)


def evidence_state(evidence: str) -> str:
    refs = [part.strip() for part in evidence.split(";") if part.strip()]
    if not refs:
        return "aucune"
    present = sum(1 for ref in refs if path_exists(ref))
    if present == len(refs):
        return "preuves_presentes"
    if present:
        return f"partiel_{present}_{len(refs)}"
    return "preuves_absentes"


def rows() -> list[dict[str, str]]:
    out = []
    for req in REQUIREMENTS:
        row = dict(req)
        row["evidence_state"] = evidence_state(row["evidence"])
        out.append(row)
    return out


def write_csv(path: Path, data: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)


def esc(value: object) -> str:
    return html.escape(str(value or ""))


def render_html(data: list[dict[str, str]]) -> str:
    counts = Counter(row["status"] for row in data)
    generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body = []
    for row in data:
        cls = "ok" if row["status"] == "OK" else "warn"
        body.append(
            "<tr>"
            f"<td><code>{esc(row['id'])}</code></td>"
            f"<td>{esc(row['source'])}</td>"
            f"<td><b>{esc(row['requirement'])}</b><br><span>{esc(row['note'])}</span></td>"
            f"<td>{esc(row['owner'])}</td>"
            f"<td><code>{esc(row['evidence'])}</code><br><span>{esc(row['evidence_state'])}</span></td>"
            f"<td><span class=\"pill {cls}\">{esc(row['status'])}</span></td>"
            "</tr>"
        )

    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Daylight / Cyber Trust - Matrice conformite</title>
<style>
:root {{ --ink:#182230; --muted:#667085; --line:#d0d5dd; --bg:#f6f7fb; --paper:#fff; --green:#067647; --red:#b42318; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:Arial, sans-serif; background:var(--bg); color:var(--ink); }}
header {{ background:#172033; color:white; padding:26px 34px; border-bottom:4px solid #22a699; }}
header h1 {{ margin:0; font-size:28px; letter-spacing:0; }}
header p {{ margin:8px 0 0; color:#d7e3f4; max-width:1080px; line-height:1.45; }}
main {{ padding:24px 34px 42px; }}
.metrics {{ display:grid; grid-template-columns:repeat(4, minmax(140px, 1fr)); gap:12px; }}
.metric, section {{ background:var(--paper); border:1px solid var(--line); border-radius:8px; }}
.metric {{ padding:14px; min-height:88px; }}
.metric span {{ display:block; color:var(--muted); font-size:13px; }}
.metric strong {{ display:block; margin-top:10px; font-size:28px; }}
section {{ margin-top:16px; padding:18px; overflow-x:auto; }}
h2 {{ margin:0 0 12px; font-size:20px; }}
table {{ width:100%; border-collapse:collapse; font-size:14px; }}
th, td {{ border-bottom:1px solid #e4e7ec; padding:9px; text-align:left; vertical-align:top; }}
th {{ background:#eef2f7; color:#344054; }}
code {{ background:#f2f4f7; border:1px solid #e4e7ec; border-radius:5px; padding:2px 5px; }}
span {{ color:var(--muted); }}
.pill {{ display:inline-block; border-radius:999px; padding:4px 9px; font-size:12px; font-weight:700; }}
.ok {{ background:#ecfdf3; color:var(--green); }}
.warn {{ background:#fff1f0; color:var(--red); }}
@media (max-width: 980px) {{ .metrics {{ grid-template-columns:1fr; }} main, header {{ padding-left:18px; padding-right:18px; }} }}
</style>
</head>
<body>
<header>
  <h1>Daylight / Cyber Trust - Matrice conformite cahier des charges</h1>
  <p>Exigences issues du cadre pedagogique et du cahier des charges, reliees aux preuves actuelles du rendu. Genere le {esc(generated)}.</p>
</header>
<main>
  <div class="metrics">
    <div class="metric"><span>Exigences</span><strong>{len(data)}</strong></div>
    <div class="metric"><span>OK</span><strong>{counts.get('OK', 0)}</strong></div>
    <div class="metric"><span>A finaliser</span><strong>{counts.get('A_FINALISER', 0)}</strong></div>
    <div class="metric"><span>Blocages reels</span><strong>1</strong></div>
  </div>
  <section>
    <h2>Lecture rapide</h2>
    <p>Le point a finaliser reste la video reelle. CAP-25 prouve maintenant Docker/Wazuh OK ; les autres exigences ont une preuve documentaire ou technique dans le ZIP.</p>
  </section>
  <section>
    <h2>Matrice</h2>
    <table><thead><tr><th>ID</th><th>Source</th><th>Exigence</th><th>Owner</th><th>Preuve</th><th>Statut</th></tr></thead><tbody>
    {''.join(body)}
    </tbody></table>
  </section>
</main>
</body>
</html>
"""


def render_markdown(data: list[dict[str, str]]) -> str:
    counts = Counter(row["status"] for row in data)
    lines = [
        "# Matrice conformite cahier des charges - Daylight / Cyber Trust",
        "",
        "## Objectif",
        "",
        "Ce document relie les exigences du cadre pedagogique et du cahier des charges aux preuves presentes dans le rendu final. Il sert de garde-fou pour verifier que l'equipe n'oublie pas un attendu.",
        "",
        "## Synthese",
        "",
        f"- Exigences suivies : {len(data)}.",
        f"- Exigences OK : {counts.get('OK', 0)}.",
        f"- Exigences a finaliser : {counts.get('A_FINALISER', 0)}.",
        "- Point reel restant : lien/MP4 video final.",
        "",
        "## Matrice",
        "",
        "| ID | Source | Exigence | Owner | Statut | Preuve | Note |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in data:
        lines.append(
            f"| {row['id']} | {row['source']} | {row['requirement']} | {row['owner']} | {row['status']} | `{row['evidence']}` | {row['note']} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_report(data: list[dict[str, str]]) -> str:
    counts = Counter(row["status"] for row in data)
    lines = [
        "=== Matrice conformite Daylight / Cyber Trust ===",
        f"Generation : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"CSV : {CSV_OUT}",
        f"HTML : {HTML_OUT}",
        f"Markdown : {MARKDOWN_OUT}",
        f"Exigences : {len(data)}",
        f"OK : {counts.get('OK', 0)}",
        f"A_FINALISER : {counts.get('A_FINALISER', 0)}",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = rows()
    write_csv(CSV_OUT, data)
    HTML_OUT.write_text(render_html(data), encoding="utf-8")
    MARKDOWN_OUT.write_text(render_markdown(data), encoding="utf-8")
    REPORT_OUT.write_text(render_report(data), encoding="utf-8")
    print(REPORT_OUT.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


