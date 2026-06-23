from __future__ import annotations

import csv
import html
from collections import defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "pfsense"
WAZUH_DIR = ROOT / "config" / "wazuh"
if not CONFIG_DIR.exists():
    CONFIG_DIR = ROOT / "Config_PfSense"
if not WAZUH_DIR.exists():
    WAZUH_DIR = ROOT / "Config_Wazuh"

DASHBOARD_DIR = ROOT / "Dashboards_Offline"
HTML_OUT = DASHBOARD_DIR / "daylight_pfsense_firewall_review.html"
TEST_PLAN_OUT = CONFIG_DIR / "pfsense_demo_test_plan.csv"
IMPORT_GUIDE_OUT = CONFIG_DIR / "README_IMPORT_PFSENSE_DAYLIGHT.md"
REPORT_OUT = ROOT / "pfsense-demo-pack-report.txt"

RULES_CSV = CONFIG_DIR / "pfsense_firewall_rules.csv"
ALIASES_CSV = CONFIG_DIR / "pfsense_aliases.csv"
NAT_CSV = CONFIG_DIR / "pfsense_nat_port_forward.csv"
TOPOLOGY_CSV = CONFIG_DIR / "pfsense_lab_topology.csv"
SYSLOG_MD = CONFIG_DIR / "pfsense_syslog_wazuh.md"
WAZUH_RULES = WAZUH_DIR / "local_rules_daylight_pfsense.xml"
TOOL_DIR_NAME = "tools" if (ROOT / "tools").exists() else "Outils"


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


def rel_from_dashboard(path: Path) -> str:
    return (".." / path.relative_to(ROOT)).as_posix()


def file_link(label: str, path: Path) -> str:
    if not path.exists():
        return f"<span class=\"missing\">{esc(label)} absent</span>"
    return f"<a href=\"{esc(rel_from_dashboard(path))}\">{esc(label)}</a>"


def action_class(action: str) -> str:
    normalized = action.lower()
    if normalized == "pass":
        return "pass"
    if normalized == "block":
        return "block"
    return "info"


def render_table(rows: list[dict[str, str]], columns: list[tuple[str, str]]) -> str:
    head = "".join(f"<th>{esc(label)}</th>" for _, label in columns)
    body = []
    for row in rows:
        cells = "".join(f"<td>{esc(row.get(key, ''))}</td>" for key, _ in columns)
        body.append(f"<tr>{cells}</tr>")
    if not body:
        body.append(f"<tr><td colspan=\"{len(columns)}\" class=\"missing\">Aucune donnee</td></tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def test_plan_rows() -> list[dict[str, str]]:
    return [
        {
            "id": "PF-TEST-01",
            "objectif": "Prouver le refus par defaut depuis WAN",
            "source": "Poste externe / reseau hyperviseur",
            "commande_ou_action": "nmap -Pn -p 22,80,443 <IP_WAN_PFSENSE>",
            "resultat_attendu": "Seul 443 peut repondre si le NAT portail est active ; les autres ports sont bloques et journalises",
            "preuve_wazuh_attendue": "rule.id:110010 ou ligne filterlog block WAN",
            "capture_conseillee": "CAP-13_pfsense-regles-firewall.png / CAP-19_wazuh-pfsense-alertes.png",
        },
        {
            "id": "PF-TEST-02",
            "objectif": "Prouver le blocage lateral USERS vers MGMT",
            "source": "poste-01 10.10.10.54",
            "commande_ou_action": "Test-NetConnection 10.10.40.1 -Port 443",
            "resultat_attendu": "Connexion refusee ; pfSense journalise un block de USERS vers MGMT",
            "preuve_wazuh_attendue": "rule.id:110020",
            "capture_conseillee": "CAP-24_qualification-alerte-110020.png",
        },
        {
            "id": "PF-TEST-03",
            "objectif": "Prouver le flux metier DMZ vers base interne",
            "source": "daylight-app-01 10.10.30.20",
            "commande_ou_action": "Test-NetConnection 10.10.20.30 -Port 5432",
            "resultat_attendu": "Flux autorise uniquement vers DAYLIGHT_DB:5432",
            "preuve_wazuh_attendue": "Ligne filterlog pass DMZ ou absence d'alerte critique",
            "capture_conseillee": "CAP-13_pfsense-regles-firewall.png",
        },
        {
            "id": "PF-TEST-04",
            "objectif": "Prouver le NAT HTTPS vers la DMZ",
            "source": "Poste externe / navigateur",
            "commande_ou_action": "curl -k https://<IP_WAN_PFSENSE>/",
            "resultat_attendu": "Reponse du portail Daylight en DMZ, pas d'acces direct au LAN interne",
            "preuve_wazuh_attendue": "Log pass WAN vers DAYLIGHT_APP:443",
            "capture_conseillee": "CAP-13_pfsense-regles-firewall.png",
        },
        {
            "id": "PF-TEST-05",
            "objectif": "Prouver l'envoi syslog pfSense vers Wazuh",
            "source": "pfSense Status > System Logs > Settings",
            "commande_ou_action": "Activer Remote Logging vers 10.10.50.10:514 UDP puis provoquer PF-TEST-02",
            "resultat_attendu": "Evenement filterlog visible dans Wazuh Discover",
            "preuve_wazuh_attendue": "filterlog OR rule.id:(110010 OR 110020)",
            "capture_conseillee": "CAP-14_pfsense-syslog-wazuh.png / CAP-19_wazuh-pfsense-alertes.png",
        },
        {
            "id": "PF-TEST-06",
            "objectif": "Prouver l'exploitation SOC d'une alerte firewall",
            "source": "Kilyan / analyste SOC",
            "commande_ou_action": "Ouvrir la matrice de qualification, choisir l'alerte 110020, appliquer le playbook",
            "resultat_attendu": "Severite haute, qualification mouvement lateral, action containment/documentation",
            "preuve_wazuh_attendue": "rule.id:110020 + qualification dans le dashboard",
            "capture_conseillee": "CAP-24_qualification-alerte-110020.png / CAP-28_rex-incident-rempli.png",
        },
    ]


def render_import_guide() -> str:
    return """# Import pfSense Daylight - guide concret

Ce fichier sert de support direct pendant la demo. Il indique quoi creer dans pfSense et comment prouver que la configuration fonctionne.

## 1. Interfaces a creer ou renommer

| Interface pfSense | VLAN | Adresse | Role |
|---|---:|---|---|
| WAN | - | DHCP/FAI | Acces Internet, refus entrant par defaut |
| USERS | 10 | `10.10.10.1/24` | Postes utilisateurs Daylight |
| SERVERS | 20 | `10.10.20.1/24` | AD, fichiers, base interne |
| DMZ | 30 | `10.10.30.1/24` | Portail Daylight expose |
| MGMT | 40 | `10.10.40.1/24` | Administration reservee |
| SOC | 50 | `10.10.50.1/24` | Wazuh et supervision Cyber Trust |

## 2. Aliases

Dans `Firewall > Aliases`, creer les objets du fichier `pfsense_aliases.csv`.

Ordre conseille :

1. Hotes critiques : `SOC_WAZUH`, `SOC_DASHBOARD`, `DAYLIGHT_APP`, `DAYLIGHT_DB`.
2. Reseaux : `USERS_SUBNET`, `SERVERS_SUBNET`, `DMZ_SUBNET`, `ADMIN_SUBNET`, `SOC_SUBNET`.
3. Groupes de controle : `RFC1918`, `DNS_ALLOWED`, `BLOCKLIST_WAN_DEMO`.

## 3. NAT

Dans `Firewall > NAT > Port Forward`, creer les lignes de `pfsense_nat_port_forward.csv`.

Point important a dire au jury : seule la DMZ est exposee, jamais le LAN interne.

## 4. Regles firewall

Dans `Firewall > Rules`, creer les regles de `pfsense_firewall_rules.csv` par interface et dans l'ordre `order`.

Regles a montrer en priorite :

1. WAN block par defaut.
2. WAN NAT HTTPS vers `DAYLIGHT_APP`.
3. USERS autorise DNS/HTTPS et bloque MGMT/SERVERS.
4. DMZ autorise uniquement le flux applicatif vers `DAYLIGHT_DB`.
5. SOC autorise la collecte et l'administration Wazuh.

Activer la journalisation sur toutes les regles de blocage et sur les flux critiques.

## 5. Remote logging vers Wazuh

Aller dans `Status > System Logs > Settings` :

1. Cocher `Enable Remote Logging`.
2. Serveur distant : `10.10.50.10:514`.
3. Protocole : UDP pour le lab.
4. Categories : Firewall Events, System Events, DHCP Events, DNS Resolver, VPN.

Cote Wazuh, utiliser `local_rules_daylight_pfsense.xml` et rechercher :

```text
filterlog OR rule.id:(110010 OR 110020 OR 110040)
```

## 6. Tests a executer

Le plan de tests pret a montrer est dans `pfsense_demo_test_plan.csv`.

En soutenance, ouvrir d'abord `daylight_pfsense_firewall_review.html`, puis ouvrir ce guide pour montrer les chemins exacts dans pfSense.
"""


def render_rules_by_interface(rules: list[dict[str, str]]) -> str:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in sorted(rules, key=lambda item: int(item.get("order") or 0)):
        groups[row.get("interface", "UNKNOWN")].append(row)

    sections = []
    for interface, rows in groups.items():
        body = []
        for row in rows:
            action = row.get("action", "")
            body.append(
                "<tr>"
                f"<td><code>{esc(row.get('order'))}</code></td>"
                f"<td><span class=\"pill {action_class(action)}\">{esc(action)}</span></td>"
                f"<td>{esc(row.get('protocol'))}</td>"
                f"<td>{esc(row.get('source'))}</td>"
                f"<td>{esc(row.get('destination'))}</td>"
                f"<td>{esc(row.get('port'))}</td>"
                f"<td>{esc(row.get('log'))}</td>"
                f"<td>{esc(row.get('description'))}</td>"
                "</tr>"
            )
        sections.append(
            f"""
<section>
  <h2>Regles {esc(interface)}</h2>
  <table>
    <thead><tr><th>Ordre</th><th>Action</th><th>Proto</th><th>Source</th><th>Destination</th><th>Port</th><th>Log</th><th>But demo</th></tr></thead>
    <tbody>{''.join(body)}</tbody>
  </table>
</section>
"""
        )
    return "\n".join(sections)


def render_test_plan(rows: list[dict[str, str]]) -> str:
    body = []
    for row in rows:
        body.append(
            "<tr>"
            f"<td><code>{esc(row['id'])}</code></td>"
            f"<td>{esc(row['objectif'])}</td>"
            f"<td>{esc(row['source'])}</td>"
            f"<td><code>{esc(row['commande_ou_action'])}</code></td>"
            f"<td>{esc(row['resultat_attendu'])}</td>"
            f"<td>{esc(row['preuve_wazuh_attendue'])}</td>"
            "</tr>"
        )
    return "".join(body)


def render_html(
    rules: list[dict[str, str]],
    aliases: list[dict[str, str]],
    nat: list[dict[str, str]],
    topology: list[dict[str, str]],
    tests: list[dict[str, str]],
) -> str:
    interfaces = sorted({row.get("interface", "") for row in rules if row.get("interface")})
    logged = [row for row in rules if row.get("log", "").lower() == "yes"]
    blocks = [row for row in rules if row.get("action", "").lower() == "block"]
    passes = [row for row in rules if row.get("action", "").lower() == "pass"]
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Daylight / Cyber Trust - Revue pfSense concrete</title>
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
  --amber:#b54708;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:Arial, sans-serif; color:var(--ink); background:var(--bg); }}
header {{ background:#172033; color:white; padding:26px 34px; border-bottom:4px solid #22a699; }}
header h1 {{ margin:0; font-size:28px; letter-spacing:0; }}
header p {{ margin:8px 0 0; max-width:1050px; color:#d7e3f4; line-height:1.45; }}
main {{ padding:24px 34px 42px; }}
.metrics {{ display:grid; grid-template-columns:repeat(6, minmax(120px, 1fr)); gap:12px; margin-bottom:16px; }}
.metric, section {{ background:var(--paper); border:1px solid var(--line); border-radius:8px; }}
.metric {{ padding:14px; min-height:92px; }}
.metric span {{ display:block; font-size:13px; color:var(--muted); }}
.metric strong {{ display:block; margin-top:10px; font-size:28px; }}
section {{ padding:18px; margin-top:16px; overflow-x:auto; }}
h2 {{ margin:0 0 12px; font-size:20px; }}
h3 {{ margin:18px 0 8px; font-size:16px; }}
p {{ line-height:1.45; }}
table {{ width:100%; border-collapse:collapse; font-size:14px; }}
th, td {{ border-bottom:1px solid #e4e7ec; padding:9px; text-align:left; vertical-align:top; }}
th {{ background:#eef2f7; color:#344054; }}
code {{ background:#f2f4f7; border:1px solid #e4e7ec; border-radius:5px; padding:2px 5px; }}
a {{ color:var(--blue); font-weight:700; text-decoration:none; }}
a:hover {{ text-decoration:underline; }}
.pill {{ display:inline-block; border-radius:999px; padding:4px 9px; font-size:12px; font-weight:700; }}
.pass {{ background:#ecfdf3; color:var(--green); }}
.block {{ background:#fff1f0; color:var(--red); }}
.info {{ background:#eef4ff; color:var(--blue); }}
.warn {{ background:#fff7ed; color:var(--amber); }}
.missing {{ color:var(--red); font-weight:700; }}
.two {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }}
.flow {{ display:grid; grid-template-columns:repeat(4, 1fr); gap:10px; }}
.flow div {{ border:1px solid #d8dee9; border-radius:8px; padding:12px; background:#fbfcff; min-height:88px; }}
.flow strong {{ display:block; margin-bottom:6px; }}
pre {{ white-space:pre-wrap; background:#111827; color:#f9fafb; border-radius:8px; padding:14px; line-height:1.45; }}
@media (max-width: 1050px) {{ .metrics, .two, .flow {{ grid-template-columns:1fr; }} main, header {{ padding-left:18px; padding-right:18px; }} }}
</style>
</head>
<body>
<header>
  <h1>Daylight / Cyber Trust - Revue pfSense concrete</h1>
  <p>Surface de demonstration generee depuis les fichiers CSV du projet. Elle sert a montrer la segmentation, les regles firewall, le NAT, les tests et le raccordement Wazuh sans inventer de capture live.</p>
</header>
<main>
  <div class="metrics">
    <div class="metric"><span>Interfaces</span><strong>{len(interfaces)}</strong></div>
    <div class="metric"><span>Aliases</span><strong>{len(aliases)}</strong></div>
    <div class="metric"><span>Regles</span><strong>{len(rules)}</strong></div>
    <div class="metric"><span>Pass</span><strong>{len(passes)}</strong></div>
    <div class="metric"><span>Block</span><strong>{len(blocks)}</strong></div>
    <div class="metric"><span>Regles loguees</span><strong>{len(logged)}</strong></div>
  </div>

  <section>
    <h2>Ce qu'on montre au jury</h2>
    <div class="flow">
      <div><strong>1. Segmentation</strong>USERS, SERVERS, DMZ, MGMT et SOC sont separes avec des passerelles dediees.</div>
      <div><strong>2. Refus par defaut</strong>WAN et mouvements lateraux sont bloques et journalises.</div>
      <div><strong>3. Flux minimaux</strong>DMZ vers base uniquement, VPN admin controle, HTTPS public vers DMZ.</div>
      <div><strong>4. Detection SOC</strong>pfSense envoie filterlog vers Wazuh et les regles 110010/110020 qualifient les alertes.</div>
    </div>
  </section>

  <section>
    <h2>Fichiers sources ouvrables</h2>
    <table><thead><tr><th>Element</th><th>Fichier</th><th>Usage demo</th></tr></thead><tbody>
      <tr><td>Aliases</td><td>{file_link('pfsense_aliases.csv', ALIASES_CSV)}</td><td>Objets reseau a creer dans pfSense.</td></tr>
      <tr><td>Regles firewall</td><td>{file_link('pfsense_firewall_rules.csv', RULES_CSV)}</td><td>Matrice complete par interface.</td></tr>
      <tr><td>NAT</td><td>{file_link('pfsense_nat_port_forward.csv', NAT_CSV)}</td><td>Publication controlee du portail Daylight.</td></tr>
      <tr><td>Syslog Wazuh</td><td>{file_link('pfsense_syslog_wazuh.md', SYSLOG_MD)}</td><td>Procedure de collecte vers le SIEM.</td></tr>
      <tr><td>Guide import pfSense</td><td>{file_link('README_IMPORT_PFSENSE_DAYLIGHT.md', IMPORT_GUIDE_OUT)}</td><td>Mode operatoire concret dans l'interface pfSense.</td></tr>
      <tr><td>Plan de tests</td><td>{file_link('pfsense_demo_test_plan.csv', TEST_PLAN_OUT)}</td><td>Tests a executer et preuves attendues.</td></tr>
      <tr><td>Regles Wazuh</td><td>{file_link('local_rules_daylight_pfsense.xml', WAZUH_RULES)}</td><td>Detection des logs filterlog pfSense.</td></tr>
    </tbody></table>
  </section>

  <section>
    <h2>Topologie lab</h2>
    {render_table(topology, [('node', 'Noeud'), ('interface', 'Interface'), ('network', 'Reseau'), ('ip_address', 'IP'), ('gateway', 'Gateway'), ('role', 'Role')])}
  </section>

  <div class="two">
    <section>
      <h2>Aliases pfSense</h2>
      {render_table(aliases, [('name', 'Nom'), ('type', 'Type'), ('value', 'Valeur'), ('description', 'Description')])}
    </section>
    <section>
      <h2>NAT Port Forward</h2>
      {render_table(nat, [('order', 'Ordre'), ('interface', 'Interface'), ('protocol', 'Proto'), ('destination_port', 'Port'), ('redirect_target_ip', 'Cible'), ('redirect_target_port', 'Port cible'), ('description', 'Description')])}
    </section>
  </div>

  {render_rules_by_interface(rules)}

  <section>
    <h2>Plan de tests concret</h2>
    <table>
      <thead><tr><th>ID</th><th>Objectif</th><th>Source</th><th>Commande/action</th><th>Resultat attendu</th><th>Preuve Wazuh</th></tr></thead>
      <tbody>{render_test_plan(tests)}</tbody>
    </table>
  </section>

  <section>
    <h2>Commandes demo rapides</h2>
    <pre>python .\\{esc(TOOL_DIR_NAME)}\\generate_demo_logs.py
python .\\{esc(TOOL_DIR_NAME)}\\send_demo_logs_to_syslog.py --dry-run

# Recherche Wazuh a montrer
filterlog OR rule.id:(110010 OR 110020 OR 110040)</pre>
    <p>Generation : {esc(generated_at)}. Ce HTML est documentaire et reproductible depuis les CSV du projet.</p>
  </section>
</main>
</body>
</html>
"""


def render_report(rules: list[dict[str, str]], aliases: list[dict[str, str]], nat: list[dict[str, str]], topology: list[dict[str, str]], tests: list[dict[str, str]]) -> str:
    lines = [
        "=== Pack demo pfSense Daylight / Cyber Trust ===",
        f"Generation : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"HTML : {HTML_OUT}",
        f"Guide import : {IMPORT_GUIDE_OUT}",
        f"Plan tests : {TEST_PLAN_OUT}",
        f"Regles firewall : {len(rules)}",
        f"Aliases : {len(aliases)}",
        f"NAT : {len(nat)}",
        f"Topologie : {len(topology)}",
        f"Tests : {len(tests)}",
        "",
        "A montrer : ouvrir Dashboards_Offline/daylight_pfsense_firewall_review.html puis derouler pfsense_demo_test_plan.csv.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

    rules = read_csv(RULES_CSV)
    aliases = read_csv(ALIASES_CSV)
    nat = read_csv(NAT_CSV)
    topology = read_csv(TOPOLOGY_CSV)
    tests = test_plan_rows()

    write_csv(TEST_PLAN_OUT, tests)
    IMPORT_GUIDE_OUT.write_text(render_import_guide(), encoding="utf-8")
    HTML_OUT.write_text(render_html(rules, aliases, nat, topology, tests), encoding="utf-8")
    REPORT_OUT.write_text(render_report(rules, aliases, nat, topology, tests), encoding="utf-8")

    print(f"Pack pfSense HTML : {HTML_OUT}")
    print(f"Guide import      : {IMPORT_GUIDE_OUT}")
    print(f"Plan de tests     : {TEST_PLAN_OUT}")
    print(f"Rapport           : {REPORT_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


