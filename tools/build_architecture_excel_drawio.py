from __future__ import annotations

import csv
import html
import os
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Architecture_DayLight_CyberTrust"


def read_csv(rel_path: str) -> list[dict[str, str]]:
    path = ROOT / rel_path
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def safe_text(value: object) -> str:
    if value is None:
        return ""
    return str(value).replace("\r\n", "\n").replace("\r", "\n")


def xml_text(value: object) -> str:
    return html.escape(safe_text(value), quote=False)


def xml_attr(value: object) -> str:
    return html.escape(safe_text(value), quote=True)


def col_name(index: int) -> str:
    name = ""
    while index:
        index, rem = divmod(index - 1, 26)
        name = chr(65 + rem) + name
    return name


def cell_xml(row: int, col: int, value: object, style: int = 0) -> str:
    ref = f"{col_name(col)}{row}"
    text = xml_text(value)
    return f'<c r="{ref}" t="inlineStr" s="{style}"><is><t>{text}</t></is></c>'


def worksheet_xml(rows: list[list[object]], style_rows: dict[int, int] | None = None) -> str:
    style_rows = style_rows or {}
    max_cols = max((len(r) for r in rows), default=1)
    max_rows = max(len(rows), 1)
    dim = f"A1:{col_name(max_cols)}{max_rows}"

    widths = []
    for c in range(max_cols):
        width = 12
        for row in rows:
            if c < len(row):
                width = max(width, min(55, len(safe_text(row[c])) + 2))
        widths.append(width)

    cols_xml = "".join(
        f'<col min="{i + 1}" max="{i + 1}" width="{w}" customWidth="1"/>'
        for i, w in enumerate(widths)
    )

    sheet_rows = []
    for r_idx, row in enumerate(rows, start=1):
        style = style_rows.get(r_idx, 0)
        cells = []
        for c_idx in range(1, max_cols + 1):
            value = row[c_idx - 1] if c_idx - 1 < len(row) else ""
            cells.append(cell_xml(r_idx, c_idx, value, style))
        sheet_rows.append(f'<row r="{r_idx}">{"".join(cells)}</row>')

    filter_xml = f'<autoFilter ref="{dim}"/>' if len(rows) > 1 and max_cols > 1 else ""
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <dimension ref="{dim}"/>
  <sheetViews>
    <sheetView workbookViewId="0">
      <pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>
      <selection pane="bottomLeft"/>
    </sheetView>
  </sheetViews>
  <cols>{cols_xml}</cols>
  <sheetData>{"".join(sheet_rows)}</sheetData>
  {filter_xml}
</worksheet>'''


def styles_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="2">
    <font><sz val="10"/><color theme="1"/><name val="Aptos"/></font>
    <font><b/><sz val="10"/><color rgb="FFFFFFFF"/><name val="Aptos"/></font>
  </fonts>
  <fills count="4">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF1F4E78"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFE2F0D9"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border><left style="thin"><color rgb="FFD9E2F3"/></left><right style="thin"><color rgb="FFD9E2F3"/></right><top style="thin"><color rgb="FFD9E2F3"/></top><bottom style="thin"><color rgb="FFD9E2F3"/></bottom><diagonal/></border>
  </borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="3">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="3" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
  </cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>'''


def write_xlsx(path: Path, sheets: list[tuple[str, list[list[object]]]]) -> None:
    workbook_sheets = []
    workbook_rels = []
    content_overrides = [
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
    ]

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("_rels/.rels", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>''')
        z.writestr("xl/styles.xml", styles_xml())
        for idx, (name, rows) in enumerate(sheets, start=1):
            filename = f"worksheets/sheet{idx}.xml"
            z.writestr(f"xl/{filename}", worksheet_xml(rows, {1: 1}))
            sheet_name = name[:31]
            workbook_sheets.append(
                f'<sheet name="{xml_attr(sheet_name)}" sheetId="{idx}" r:id="rId{idx}"/>'
            )
            workbook_rels.append(
                f'<Relationship Id="rId{idx}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="{filename}"/>'
            )
            content_overrides.append(
                f'<Override PartName="/xl/{filename}" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            )
        workbook_rels.append(
            f'<Relationship Id="rId{len(sheets) + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        )
        z.writestr("xl/workbook.xml", f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>{"".join(workbook_sheets)}</sheets>
</workbook>''')
        z.writestr("xl/_rels/workbook.xml.rels", f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {"".join(workbook_rels)}
</Relationships>''')
        z.writestr("[Content_Types].xml", f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  {"".join(content_overrides)}
</Types>''')


class Drawio:
    def __init__(self, title: str):
        self.title = title
        self.cells: list[str] = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
        self.next_id = 2

    def _id(self) -> str:
        value = str(self.next_id)
        self.next_id += 1
        return value

    def vertex(self, label: str, x: int, y: int, w: int, h: int, style: str) -> str:
        cid = self._id()
        self.cells.append(
            f'<mxCell id="{cid}" value="{xml_attr(label)}" style="{xml_attr(style)}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )
        return cid

    def edge(self, source: str, target: str, label: str, style: str) -> str:
        cid = self._id()
        self.cells.append(
            f'<mxCell id="{cid}" value="{xml_attr(label)}" style="{xml_attr(style)}" edge="1" parent="1" source="{source}" target="{target}">'
            '<mxGeometry relative="1" as="geometry"/></mxCell>'
        )
        return cid

    def xml(self) -> str:
        return f'''<mxfile host="app.diagrams.net" modified="2026-06-23T00:00:00.000Z" agent="Codex" version="24.7.17">
  <diagram id="{xml_attr(self.title)}" name="{xml_attr(self.title)}">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1000" math="0" shadow="0">
      <root>{"".join(self.cells)}</root>
    </mxGraphModel>
  </diagram>
</mxfile>'''


ZONE_STYLE = "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1"
DEVICE_STYLE = "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#666666"
PFSENSE_STYLE = "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1"
WAZUH_STYLE = "rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1"
ALLOW_EDGE = "endArrow=block;html=1;rounded=0;strokeColor=#2E7D32;fontColor=#2E7D32;strokeWidth=2"
BLOCK_EDGE = "endArrow=block;html=1;rounded=0;strokeColor=#C00000;fontColor=#C00000;dashed=1;strokeWidth=2"
LOG_EDGE = "endArrow=block;html=1;rounded=0;strokeColor=#6A1B9A;fontColor=#6A1B9A;strokeWidth=2"


def write_drawio(path: Path, drawio: Drawio) -> None:
    path.write_text(drawio.xml(), encoding="utf-8")


def build_global_drawio(path: Path) -> None:
    d = Drawio("Architecture globale")
    pf = d.vertex("pfSense fw 01\nFirewall central\nRoutage inter zones", 640, 360, 220, 90, PFSENSE_STYLE)
    wan = d.vertex("WAN\nInternet / NAT hyperviseur", 640, 80, 220, 80, ZONE_STYLE)
    users = d.vertex("USERS\n10.10.10.0/24\nposte 01 10.10.10.54", 90, 290, 260, 110, ZONE_STYLE)
    servers = d.vertex("SERVERS\n10.10.20.0/24\nserveur 01 10.10.20.20\nDB 10.10.20.30", 90, 560, 300, 130, ZONE_STYLE)
    dmz = d.vertex("DMZ\n10.10.30.0/24\nDaylight app 10.10.30.20", 500, 560, 300, 110, ZONE_STYLE)
    mgmt = d.vertex("MGMT\n10.10.40.0/24\nadmin 01 10.10.40.21", 980, 250, 280, 110, ZONE_STYLE)
    soc = d.vertex("SOC\n10.10.50.0/24\nWazuh 10.10.50.10", 980, 560, 280, 120, WAZUH_STYLE)
    d.edge(wan, pf, "WAN DHCP", ALLOW_EDGE)
    d.edge(pf, users, "GW 10.10.10.1", ALLOW_EDGE)
    d.edge(pf, servers, "GW 10.10.20.1", ALLOW_EDGE)
    d.edge(pf, dmz, "GW 10.10.30.1", ALLOW_EDGE)
    d.edge(mgmt, pf, "Admin pfSense 443", ALLOW_EDGE)
    d.edge(pf, soc, "GW 10.10.50.1", ALLOW_EDGE)
    d.edge(users, dmz, "HTTPS 443 autorise", ALLOW_EDGE)
    d.edge(users, servers, "Blocage lateral", BLOCK_EDGE)
    d.edge(users, mgmt, "Blocage admin", BLOCK_EDGE)
    d.edge(dmz, servers, "DB 5432 seulement", ALLOW_EDGE)
    d.edge(pf, soc, "Syslog UDP 514\nalertes 110010 110020", LOG_EDGE)
    write_drawio(path, d)


def build_pfsense_drawio(path: Path) -> None:
    d = Drawio("pfSense flux")
    pf = d.vertex("pfSense fw 01\nInterfaces WAN USERS SERVERS DMZ MGMT SOC\nDefault deny + logs", 610, 350, 270, 110, PFSENSE_STYLE)
    wan = d.vertex("WAN\nBlock RFC1918\nBlocklist demo\nNAT 443 vers Daylight app", 610, 80, 270, 100, ZONE_STYLE)
    users = d.vertex("USERS\n10.10.10.0/24\nAutorise app 443\nBloque MGMT SERVERS SOC", 100, 260, 320, 130, ZONE_STYLE)
    dmz = d.vertex("DMZ\n10.10.30.0/24\nApp vers DB 5432\nLogs vers Wazuh 1514", 100, 560, 320, 130, ZONE_STYLE)
    servers = d.vertex("SERVERS\n10.10.20.0/24\nAgents Wazuh 1514 1515\nSyslog 514", 1030, 260, 330, 130, ZONE_STYLE)
    soc = d.vertex("SOC Wazuh\n10.10.50.10\nManager Indexer Dashboard", 1030, 560, 330, 130, WAZUH_STYLE)
    mgmt = d.vertex("MGMT\n10.10.40.0/24\nAdmin pfSense Wazuh serveurs", 610, 720, 310, 100, ZONE_STYLE)
    d.edge(wan, pf, "HTTPS 443 NAT\nOpenVPN 1194", ALLOW_EDGE)
    d.edge(wan, pf, "Tout autre entrant bloque", BLOCK_EDGE)
    d.edge(users, pf, "DNS 53 / Web 80 443 / App 443", ALLOW_EDGE)
    d.edge(users, pf, "Vers MGMT SERVERS SOC bloque", BLOCK_EDGE)
    d.edge(dmz, pf, "App vers DB 5432", ALLOW_EDGE)
    d.edge(dmz, pf, "DMZ vers LAN/MGMT bloque", BLOCK_EDGE)
    d.edge(servers, pf, "Agents et syslog vers SOC", ALLOW_EDGE)
    d.edge(mgmt, pf, "Admin 443 22 3389 5985 5986", ALLOW_EDGE)
    d.edge(pf, soc, "Remote logging UDP 514\nfilterlog vers Wazuh", LOG_EDGE)
    d.edge(pf, soc, "Regles Wazuh 110010 110020 110050", LOG_EDGE)
    write_drawio(path, d)


def build_soc_drawio(path: Path) -> None:
    d = Drawio("Chaine SOC Wazuh")
    manager = d.vertex("Wazuh Manager\nCollecte + correlation", 620, 300, 260, 90, WAZUH_STYLE)
    indexer = d.vertex("Wazuh Indexer\nStockage alertes", 620, 470, 260, 80, WAZUH_STYLE)
    dash = d.vertex("Wazuh Dashboard\nQualification + dashboards", 620, 630, 260, 90, WAZUH_STYLE)
    pf = d.vertex("pfSense\nfilterlog syslog\n110010 110020 110050", 120, 130, 310, 110, PFSENSE_STYLE)
    srv = d.vertex("serveur 01\nSSH auth.log\n5710 5503 5551 5763", 120, 310, 310, 110, DEVICE_STYLE)
    app = d.vertex("Daylight app\nlogs metier\n100110 a 100150", 120, 500, 310, 110, DEVICE_STYLE)
    endpoint = d.vertex("poste 01\nagent endpoint\nUSB SCA events", 120, 690, 310, 90, DEVICE_STYLE)
    play = d.vertex("SOC Cyber Trust\nDashboards\nQualification\nPlaybooks REX", 1040, 430, 330, 170, DEVICE_STYLE)
    d.edge(pf, manager, "UDP 514", LOG_EDGE)
    d.edge(srv, manager, "Agent 1514/1515", LOG_EDGE)
    d.edge(app, manager, "Agent/syslog 1514/514", LOG_EDGE)
    d.edge(endpoint, manager, "Agent endpoint", LOG_EDGE)
    d.edge(manager, indexer, "Alertes normalisees", ALLOW_EDGE)
    d.edge(indexer, dash, "Recherche et visualisation", ALLOW_EDGE)
    d.edge(dash, play, "Tri + preuves video", ALLOW_EDGE)
    write_drawio(path, d)


def build_excel(path: Path) -> None:
    topology = read_csv("config/pfsense/pfsense_lab_topology.csv")
    aliases = read_csv("config/pfsense/pfsense_aliases.csv")
    rules = read_csv("config/pfsense/pfsense_firewall_rules.csv")
    nat = read_csv("config/pfsense/pfsense_nat_port_forward.csv")
    alerts = read_csv("config/wazuh/daylight_alert_qualification_matrix.csv")
    dashboards = read_csv("config/wazuh/daylight_dashboard_queries.csv")
    inventory = read_csv("config/lab/daylight_vm_inventory.csv")
    runbook = read_csv("config/lab/daylight_lab_runbook.csv")

    inventory_by_name = {r["name"]: r for r in inventory}
    zones = [
        ["Zone", "Reseau", "Passerelle", "Role securite", "Equipements principaux", "Regles cles"],
        ["WAN", "NAT hyperviseur", "DHCP", "Exposition externe limitee", "pfSense WAN", "Block par defaut, NAT 443, VPN 1194"],
        ["USERS", "10.10.10.0/24", "10.10.10.1", "Postes utilisateurs sans acces admin", "poste-01", "App 443 autorise, MGMT/SERVERS/SOC bloques"],
        ["SERVERS", "10.10.20.0/24", "10.10.20.1", "Serveurs internes proteges", "serveur-01, DAYLIGHT_DB", "Agents/syslog vers Wazuh, flux retour limites"],
        ["DMZ", "10.10.30.0/24", "10.10.30.1", "Application exposee controlee", "daylight-app-01", "DB 5432 seulement, logs vers SOC"],
        ["MGMT", "10.10.40.0/24", "10.10.40.1", "Administration isolee", "admin-01", "Admin pfSense/Wazuh/serveurs autorisee"],
        ["SOC", "10.10.50.0/24", "10.10.50.1", "Supervision Cyber Trust", "wazuh-manager", "Reception agents, syslog, dashboards"],
    ]

    equipements = [["Equipement", "Type", "Zone", "IP ou acces", "Services", "Proprietaire", "Preuve"]]
    for item in topology:
        inv = inventory_by_name.get(item["node"], {})
        equipements.append([
            item["node"],
            inv.get("type", "pfSense interface" if item["node"] == "pfsense-fw-01" else ""),
            item["interface"],
            item["ip_address"],
            inv.get("services", item["role"]),
            inv.get("owner", ""),
            inv.get("proof", ""),
        ])

    interfaces = [["Equipement", "Interface", "Reseau", "Adresse", "Gateway", "Role"]]
    for item in topology:
        interfaces.append([item["node"], item["interface"], item["network"], item["ip_address"], item["gateway"], item["role"]])

    aliases_rows = [["Alias", "Type", "Valeur", "Description"]]
    aliases_rows += [[r["name"], r["type"], r["value"], r["description"]] for r in aliases]

    rules_rows = [["Ordre", "Interface", "Action", "Proto", "Source", "Destination", "Port", "Log", "Description"]]
    rules_rows += [[r["order"], r["interface"], r["action"], r["protocol"], r["source"], r["destination"], r["port"], r["log"], r["description"]] for r in rules]

    nat_rows = [["Ordre", "Interface", "Proto", "Source", "Port externe", "Cible", "Port cible", "Description"]]
    nat_rows += [[r["order"], r["interface"], r["protocol"], r["source"], r["destination_port"], r["redirect_target_ip"], r["redirect_target_port"], r["description"]] for r in nat]

    flux = [
        ["Flux", "Source", "Destination", "Ports", "Decision", "Justification", "Preuve"],
        ["Acces metier", "USERS_SUBNET", "DAYLIGHT_APP", "443/tcp", "Autorise", "Les utilisateurs doivent acceder au portail Daylight", "Regle USERS 110"],
        ["Mouvement lateral", "USERS_SUBNET", "SERVERS_SUBNET", "any", "Bloque", "Un poste compromis ne doit pas atteindre les serveurs", "Regle USERS 140 + log"],
        ["Acces administration", "USERS_SUBNET", "ADMIN_SUBNET", "any", "Bloque", "Administration reservee a MGMT", "Regle USERS 130 + log"],
        ["App vers base", "DAYLIGHT_APP", "DAYLIGHT_DB", "5432/tcp", "Autorise", "Flux applicatif minimal", "Regle DMZ 200"],
        ["DMZ vers admin", "DMZ_SUBNET", "ADMIN_SUBNET", "any", "Bloque", "La DMZ ne doit jamais administrer le SI", "Regle DMZ 230 + log"],
        ["Serveurs vers SOC", "SERVERS_SUBNET", "SOC_WAZUH", "1514/1515 tcp, 514 udp", "Autorise", "Collecte agent et syslog", "Regles SERVERS 300 310"],
        ["pfSense vers SOC", "pfsense-fw-01", "SOC_WAZUH", "514/udp", "Autorise", "Remote logging firewall", "CAP-14"],
        ["WAN vers app", "Internet", "DAYLIGHT_APP", "443/tcp", "NAT autorise", "Publication HTTPS controlee", "NAT ordre 10"],
        ["WAN entrant", "Internet", "any", "any", "Bloque", "Refus entrant par defaut", "Regle WAN 50"],
    ]

    alert_rows = [["Regle", "Scenario", "Severite", "SLA", "Checks", "Action immediate", "Escalade", "Preuve"]]
    alert_rows += [[r["rule_id"], r["scenario"], r["severity"], r["sla_triage"], r["first_checks"], r["immediate_action"], r["escalation"], r["proof"]] for r in alerts]

    dash_rows = [["Dashboard", "Widget", "Type", "Requete", "Split", "Metric", "Owner"]]
    dash_rows += [[r["dashboard"], r["widget"], r["type"], r["query"], r["split_field"], r["metric"], r["owner"]] for r in dashboards]

    tests = [["Ordre", "Phase", "Action", "Commande ou ecran", "Resultat attendu", "Owner"]]
    tests += [[r["order"], r["phase"], r["action"], r["command_or_screen"], r["expected_result"], r["owner"]] for r in runbook]
    tests += [
        ["A", "Video", "Ouvrir Wazuh", "https://localhost", "Dashboard accessible admin / SecretPassword", "Youssef"],
        ["B", "Video", "Filtrer SSH serveur", "agent.name: serveur-01 AND (rule.id:5710 OR rule.id:5503 OR rule.id:5551 OR rule.id:5763)", "Alerte brute force visible", "Youssef"],
        ["C", "Video", "Filtrer pfSense", "rule.id:110010 OR rule.id:110020 OR pfsense-fw-01", "Blocages firewall visibles", "Yvan/Kilyan"],
    ]

    captures = [
        ["Capture", "Fichier", "Ce que le jury voit", "Responsable"],
        ["CAP-12", "Annexes_Captures/CAP-12_architecture-solution.png", "Schema architecture demo/cible", "Yvan"],
        ["CAP-13", "Annexes_Captures/CAP-13_pfsense-regles-firewall.png", "Regles firewall pfSense", "Yvan"],
        ["CAP-14", "Annexes_Captures/CAP-14_pfsense-syslog-wazuh.png", "Remote logging pfSense vers Wazuh", "Yvan"],
        ["CAP-19", "Annexes_Captures/CAP-19_wazuh-pfsense-alertes.png", "Alertes Wazuh venant de pfSense", "Yvan/Kilyan"],
        ["CAP-02", "Annexes_Captures/CAP-02_agents-poste01-serveur01.png", "Agents Wazuh visibles", "Youssef"],
        ["CAP-03", "Annexes_Captures/CAP-03_alerte-5712-brute-force-ssh.png", "Alerte SSH serveur-01", "Youssef"],
    ]

    synthese = [
        ["Champ", "Valeur"],
        ["Client", "Daylight"],
        ["Prestataire", "Cyber Trust"],
        ["Objectif", "Architecture SOC concrete avec pfSense, Wazuh, segmentation, alertes et preuves video"],
        ["Firewall", "pfSense fw 01, interfaces WAN USERS SERVERS DMZ MGMT SOC"],
        ["SIEM", "Wazuh 10.10.50.10 ou https://localhost en lab Docker"],
        ["Fichier Excel", str(path.name)],
        ["Schemas drawio", "01 architecture globale, 02 pfSense flux, 03 SOC Wazuh"],
        ["A montrer", "CAP-12 puis CAP-13/CAP-14 puis Wazuh avec les filtres"],
    ]

    roles = [
        ["Membre", "Role principal", "Ce qu'il presente", "Preuves"],
        ["Yvan FOCSA", "Architecte solution", "Segmentation, pfSense, flux autorises/bloques, architecture", "Excel, drawio, CAP-12/13/14"],
        ["Youssef GUERNIOU", "Ingenieur SIEM Wazuh", "Agents, collecte, alertes SSH, RBAC", "setup-siem-lab, Wazuh live"],
        ["Kilyan FELIX", "Chef projet detection", "Dashboards, qualification, SLA, synthese client", "Matrices alertes, dashboards"],
        ["Mahamadou DIACOUMBA", "Exploitation lab", "VM, runbook, playbooks, REX, relance demo", "Runbook, preflight, captures"],
    ]

    sheets = [
        ("00 Synthese", synthese),
        ("01 Zones", zones),
        ("02 Equipements", equipements),
        ("03 Interfaces pfSense", interfaces),
        ("04 Aliases", aliases_rows),
        ("05 Regles pfSense", rules_rows),
        ("06 NAT", nat_rows),
        ("07 Flux critiques", flux),
        ("08 Alertes Wazuh", alert_rows),
        ("09 Dashboards", dash_rows),
        ("10 Tests video", tests),
        ("11 Captures", captures),
        ("12 Roles", roles),
    ]
    write_xlsx(path, sheets)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    build_excel(OUT / "Daylight_CyberTrust_Architecture_Equipements_Zones.xlsx")
    build_global_drawio(OUT / "01_architecture_globale_daylight_cybertrust.drawio")
    build_pfsense_drawio(OUT / "02_architecture_pfsense_flux.drawio")
    build_soc_drawio(OUT / "03_architecture_soc_wazuh.drawio")
    index = OUT / "README_ARCHITECTURE.md"
    index.write_text(
        "\n".join(
            [
                "# Architecture Daylight / Cyber Trust",
                "",
                "Fichiers generes pour la presentation architecture et pfSense.",
                "",
                "| Fichier | Usage |",
                "|---|---|",
                "| Daylight_CyberTrust_Architecture_Equipements_Zones.xlsx | Excel complet : zones, equipements, aliases, regles, NAT, flux, alertes, tests. |",
                "| 01_architecture_globale_daylight_cybertrust.drawio | Schema global zones + pfSense + Wazuh. |",
                "| 02_architecture_pfsense_flux.drawio | Schema pfSense avec flux autorises/bloques et syslog Wazuh. |",
                "| 03_architecture_soc_wazuh.drawio | Chaine SOC : sources logs, manager, indexer, dashboard, playbooks. |",
                "",
                "A ouvrir avec Excel et https://app.diagrams.net/.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    for path in sorted(OUT.iterdir()):
        print(path)


if __name__ == "__main__":
    main()
