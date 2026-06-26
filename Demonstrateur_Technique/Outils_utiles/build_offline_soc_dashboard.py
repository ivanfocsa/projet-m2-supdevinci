from __future__ import annotations

import csv
import html
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "Demo_Logs"
MATRIX = ROOT / "config" / "wazuh" / "daylight_alert_qualification_matrix.csv"
OUT_DIR = ROOT / "Dashboards_Offline"
CAPTURE_DIR = ROOT / "Annexes_Captures"
HTML_OUT = OUT_DIR / "daylight_soc_dashboard.html"
CAP_ALERT = CAPTURE_DIR / "CAP-06_alerte-100120-acces-patient.png"
CAP_TECH = CAPTURE_DIR / "CAP-07_dashboard-technique.png"
CAP_EXEC = CAPTURE_DIR / "CAP-08_dashboard-executif.png"
CAP_QUALIF = CAPTURE_DIR / "CAP-23_qualification-alerte-100120.png"

SEVERITY_LEVEL = {"Critical": 12, "High": 10, "Medium": 7, "Low": 3}
SEVERITY_COLOR = {"Critical": "#b42318", "High": "#c85120", "Medium": "#b7791f", "Low": "#475467"}


@dataclass
class Event:
    timestamp: str
    source: str
    source_file: str
    rule_id: str
    title: str
    severity: str
    category: str
    raw: str


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def draw_wrapped(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt: ImageFont.ImageFont, fill: str, width: int, gap: int = 4) -> int:
    x, y = xy
    for line in wrap(str(text), width=width) or [""]:
        draw.text((x, y), line, font=fnt, fill=fill)
        _, h = text_size(draw, line or "A", fnt)
        y += h + gap
    return y


def card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, value: str, subtitle: str, accent: str) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=12, fill="#ffffff", outline="#d0d5dd", width=2)
    draw.rectangle((x1, y1, x2, y1 + 8), fill=accent)
    draw.text((x1 + 20, y1 + 24), title, font=font(18, True), fill="#475467")
    draw.text((x1 + 20, y1 + 54), value, font=font(42, True), fill="#172033")
    draw_wrapped(draw, (x1 + 20, y1 + 110), subtitle, font(15), "#667085", 36)


def parse_kv(line: str) -> dict[str, str]:
    pattern = r'(\w+)=((?:"[^"]+")|(?:[^\s]+))'
    result: dict[str, str] = {}
    for key, value in re.findall(pattern, line):
        result[key] = value.strip('"')
    return result


def classify_line(source_file: str, line: str) -> Event | None:
    if not line.strip():
        return None
    parts = line.split(maxsplit=2)
    if len(parts) < 3:
        return None
    timestamp, source, rest = parts
    kv = parse_kv(line)

    if source_file == "pfsense.log":
        if "WAN scan blocked" in line:
            return Event(timestamp, source, source_file, "110010", "Scan WAN bloque", "Medium", "Firewall", line)
        if "User VLAN to management denied" in line:
            return Event(timestamp, source, source_file, "110020", "Inter-VLAN vers MGMT bloque", "Critical", "Firewall", line)
        if "WAN_EXFIL_DEMO" in line:
            return Event(timestamp, source, source_file, "110050", "Flux sortant volumineux", "Critical", "Firewall", line)
        if "HTTPS to Daylight portal" in line:
            return Event(timestamp, source, source_file, "110000", "Flux HTTPS DMZ autorise", "Low", "Firewall", line)
        if "vpn_login" in line:
            return Event(timestamp, source, source_file, "110060", "Connexion VPN admin MFA", "Low", "Firewall", line)

    event = kv.get("event", "")
    risk = kv.get("risk", "").lower()
    if event == "auth_failure":
        return Event(timestamp, source, source_file, "100110", "Brute force applicatif Daylight", "High", "Application", line)
    if event == "patient_record_access":
        return Event(timestamp, source, source_file, "100120", "Acces anormal dossier patient", "Critical", "Application", line)
    if event == "appointment_export":
        return Event(timestamp, source, source_file, "100125", "Export rendez-vous a surveiller", "Medium", "Application", line)
    if event == "privileged_group_change":
        return Event(timestamp, source, source_file, "100130", "Modification groupe privilegie", "Critical", "AD", line)
    if event == "patient_share_access":
        return Event(timestamp, source, source_file, "100120", "Acces partage patient refuse", "High", "Files", line)
    if event == "password_spray":
        return Event(timestamp, source, source_file, "100110", "Password spray", "High", "AD", line)
    if event == "phishing_reported":
        return Event(timestamp, source, source_file, "100150", "Phishing signale", "High", "Mail", line)
    if event == "url_rewrite_click":
        return Event(timestamp, source, source_file, "100150", "Clic URL bloque", "Medium" if risk == "medium" else "High", "Mail", line)
    if event == "usb_insert":
        return Event(timestamp, source, source_file, "100140", "USB non autorise", "High", "Endpoint", line)
    if event == "process_start":
        return Event(timestamp, source, source_file, "100140", "Execution binaire non signe", "Medium", "Endpoint", line)
    return Event(timestamp, source, source_file, "000000", "Evenement collecte", "Low", "Autre", line)


def load_events() -> list[Event]:
    events: list[Event] = []
    for path in sorted(LOG_DIR.glob("*.log")):
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            event = classify_line(path.name, line)
            if event:
                events.append(event)
    return sorted(events, key=lambda e: e.timestamp)


def load_matrix() -> dict[str, dict[str, str]]:
    return {row["rule_id"]: row for row in csv.DictReader(MATRIX.read_text(encoding="utf-8").splitlines())}


def html_row(cells: list[str]) -> str:
    return "<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in cells) + "</tr>"


def render_html(events: list[Event], matrix: dict[str, dict[str, str]]) -> None:
    sev = Counter(e.severity for e in events)
    rules = Counter(e.rule_id for e in events)
    sources = Counter(e.category for e in events)
    critical = sev["Critical"]
    patient = sum(1 for e in events if e.rule_id == "100120")
    blocked_network = sum(1 for e in events if e.rule_id in {"110010", "110020"})

    rows = "\n".join(
        html_row([e.timestamp, e.rule_id, e.severity, e.category, e.title, e.source_file]) for e in events
    )
    qual_rows = "\n".join(
        html_row([
            rid,
            matrix[rid].get("scenario", "Hors matrice"),
            matrix[rid].get("severity", "-"),
            matrix[rid].get("sla_triage", "-"),
            matrix[rid].get("immediate_action", "A qualifier"),
        ])
        for rid in sorted({e.rule_id for e in events if e.rule_id in matrix})
    )
    severity_blocks = "\n".join(
        f'<div class="bar"><span>{html.escape(k)}</span><strong style="width:{max(8, v * 24)}px;background:{SEVERITY_COLOR.get(k, "#475467")}"></strong><em>{v}</em></div>'
        for k, v in sev.most_common()
    )
    rule_blocks = "\n".join(
        f'<div class="pill"><b>{html.escape(k)}</b><span>{v}</span></div>' for k, v in rules.most_common()
    )
    source_blocks = "\n".join(
        f'<div class="pill"><b>{html.escape(k)}</b><span>{v}</span></div>' for k, v in sources.most_common()
    )

    html_text = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Daylight SOC Offline Dashboard</title>
<style>
:root {{ --ink:#172033; --muted:#667085; --line:#d0d5dd; --bg:#f7f9fc; --green:#1f7a4f; --red:#b42318; --orange:#c85120; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:Arial, sans-serif; color:var(--ink); background:var(--bg); }}
header {{ background:#172033; color:#fff; padding:28px 42px; }}
header p {{ margin:6px 0 0; color:#d5e3ff; }}
main {{ padding:28px 42px 48px; }}
.grid {{ display:grid; grid-template-columns:repeat(4, 1fr); gap:16px; }}
.card, section {{ background:#fff; border:1px solid var(--line); border-radius:10px; padding:18px; }}
.card small {{ color:var(--muted); display:block; }}
.card strong {{ font-size:42px; display:block; margin-top:8px; }}
section {{ margin-top:18px; }}
h2 {{ margin:0 0 14px; font-size:22px; }}
table {{ width:100%; border-collapse:collapse; font-size:14px; }}
th, td {{ border-bottom:1px solid #e4e7ec; text-align:left; padding:9px; vertical-align:top; }}
th {{ background:#eef2f7; }}
.bar {{ display:flex; align-items:center; gap:12px; margin:10px 0; }}
.bar span {{ width:90px; }}
.bar strong {{ display:inline-block; height:22px; border-radius:5px; }}
.bar em {{ color:var(--muted); font-style:normal; }}
.pills {{ display:flex; flex-wrap:wrap; gap:10px; }}
.pill {{ border:1px solid var(--line); border-radius:999px; padding:8px 12px; background:#fff; }}
.pill span {{ margin-left:10px; color:var(--muted); }}
.note {{ color:var(--muted); font-size:13px; }}
</style>
</head>
<body>
<header>
<h1>Daylight / Cyber Trust - Dashboard SOC offline</h1>
<p>Vue demonstrable generee depuis les logs du projet. Elle aide la video si Wazuh n'est pas accessible, sans remplacer les captures Wazuh finales.</p>
</header>
<main>
<div class="grid">
<div class="card"><small>Total evenements</small><strong>{len(events)}</strong></div>
<div class="card"><small>Alertes critiques</small><strong>{critical}</strong></div>
<div class="card"><small>Donnees patients</small><strong>{patient}</strong></div>
<div class="card"><small>Blocages reseau</small><strong>{blocked_network}</strong></div>
</div>
<section><h2>Repartition par severite</h2>{severity_blocks}</section>
<section><h2>Top regles detectees</h2><div class="pills">{rule_blocks}</div></section>
<section><h2>Sources collectees</h2><div class="pills">{source_blocks}</div></section>
<section><h2>Timeline des alertes</h2><table><thead><tr><th>Heure</th><th>Regle</th><th>Severite</th><th>Source</th><th>Scenario</th><th>Fichier</th></tr></thead><tbody>{rows}</tbody></table></section>
<section><h2>Qualification SOC</h2><table><thead><tr><th>Regle</th><th>Scenario</th><th>Severite</th><th>SLA</th><th>Action immediate</th></tr></thead><tbody>{qual_rows}</tbody></table></section>
<p class="note">Sources : Demo_Logs/*.log, config/wazuh/daylight_alert_qualification_matrix.csv, config/wazuh/daylight_dashboard_queries.csv.</p>
</main>
</body>
</html>
"""
    OUT_DIR.mkdir(exist_ok=True)
    HTML_OUT.write_text(html_text, encoding="utf-8")


def header(draw: ImageDraw.ImageDraw, title: str, subtitle: str, width: int) -> None:
    draw.rectangle((0, 0, width, 110), fill="#172033")
    draw.text((42, 24), title, font=font(34, True), fill="white")
    draw.text((42, 68), subtitle, font=font(18), fill="#d5e3ff")


def render_executive(events: list[Event]) -> None:
    width, height = 1600, 1000
    image = Image.new("RGB", (width, height), "#f7f9fc")
    draw = ImageDraw.Draw(image)
    header(draw, "CAP-08 - Dashboard executif Daylight", "KPI SOC offline generes depuis les logs demo", width)
    sev = Counter(e.severity for e in events)
    patient = sum(1 for e in events if e.rule_id == "100120")
    blocked_network = sum(1 for e in events if e.rule_id in {"110010", "110020"})
    critical = sev["Critical"]
    card(draw, (55, 155, 405, 315), "Total alertes", str(len(events)), "Tous les evenements collectes demo", "#425caa")
    card(draw, (435, 155, 785, 315), "Critiques", str(critical), "A traiter sous 15 minutes", "#b42318")
    card(draw, (815, 155, 1165, 315), "Donnees patients", str(patient), "Acces patient ou partage sensible", "#c85120")
    card(draw, (1195, 155, 1545, 315), "Blocages reseau", str(blocked_network), "WAN/inter-VLAN bloques", "#1f7a4f")

    draw.rounded_rectangle((55, 365, 745, 760), radius=12, fill="#ffffff", outline="#d0d5dd", width=2)
    draw.text((80, 390), "Repartition par severite", font=font(24, True), fill="#172033")
    y = 450
    max_count = max(sev.values() or [1])
    for label in ["Critical", "High", "Medium", "Low"]:
        value = sev[label]
        bar_w = int(460 * value / max_count) if value else 12
        draw.text((85, y), label, font=font(18, True), fill="#475467")
        draw.rounded_rectangle((210, y - 2, 210 + bar_w, y + 24), radius=7, fill=SEVERITY_COLOR[label])
        draw.text((690, y), str(value), font=font(18, True), fill="#172033")
        y += 62

    draw.rounded_rectangle((795, 365, 1545, 760), radius=12, fill="#ffffff", outline="#d0d5dd", width=2)
    draw.text((820, 390), "Incidents a commenter au client", font=font(24, True), fill="#172033")
    y = 445
    for event in [e for e in events if e.severity in {"Critical", "High"}][:6]:
        draw.rounded_rectangle((820, y, 1515, y + 42), radius=8, fill="#fff7ed" if event.severity == "High" else "#fff1f0", outline="#f2d0c8")
        draw.text((835, y + 11), f"{event.timestamp[11:16]}  {event.rule_id}  {event.title}", font=font(17, True), fill="#172033")
        y += 52

    draw.text((55, 910), "Note : dashboard de secours base sur Demo_Logs ; les captures Wazuh reelles CAP-01/02/03 restent a produire.", font=font(16), fill="#667085")
    CAP_EXEC.parent.mkdir(exist_ok=True)
    image.save(CAP_EXEC)


def render_technical(events: list[Event]) -> None:
    width, height = 1800, 1120
    image = Image.new("RGB", (width, height), "#f7f9fc")
    draw = ImageDraw.Draw(image)
    header(draw, "CAP-07 - Dashboard technique SOC", "Severite, sources, top regles et timeline offline", width)
    sev = Counter(e.severity for e in events)
    rules = Counter(e.rule_id for e in events)
    sources = Counter(e.category for e in events)

    draw.rounded_rectangle((45, 150, 550, 500), radius=12, fill="#ffffff", outline="#d0d5dd", width=2)
    draw.text((70, 178), "Top regles", font=font(24, True), fill="#172033")
    y = 230
    for rid, value in rules.most_common(7):
        draw.text((75, y), rid, font=font(19, True), fill="#172033")
        draw.rounded_rectangle((170, y, 170 + value * 70, y + 24), radius=6, fill="#425caa")
        draw.text((485, y), str(value), font=font(18, True), fill="#475467")
        y += 38

    draw.rounded_rectangle((595, 150, 1120, 500), radius=12, fill="#ffffff", outline="#d0d5dd", width=2)
    draw.text((620, 178), "Sources", font=font(24, True), fill="#172033")
    y = 230
    for src, value in sources.most_common():
        draw.text((625, y), src, font=font(18, True), fill="#172033")
        draw.rounded_rectangle((770, y, 770 + value * 62, y + 24), radius=6, fill="#1f7a4f")
        draw.text((1050, y), str(value), font=font(18, True), fill="#475467")
        y += 38

    draw.rounded_rectangle((1165, 150, 1755, 500), radius=12, fill="#ffffff", outline="#d0d5dd", width=2)
    draw.text((1190, 178), "Severite", font=font(24, True), fill="#172033")
    y = 235
    for label in ["Critical", "High", "Medium", "Low"]:
        value = sev[label]
        draw.ellipse((1190, y, 1216, y + 26), fill=SEVERITY_COLOR[label])
        draw.text((1230, y), f"{label}: {value}", font=font(20, True), fill="#172033")
        y += 52

    draw.rounded_rectangle((45, 545, 1755, 985), radius=12, fill="#ffffff", outline="#d0d5dd", width=2)
    draw.text((70, 575), "Timeline des evenements", font=font(24, True), fill="#172033")
    y = 630
    for event in events[:10]:
        color = SEVERITY_COLOR.get(event.severity, "#475467")
        draw.text((75, y), event.timestamp[11:16], font=font(17, True), fill="#475467")
        draw.rounded_rectangle((150, y - 4, 230, y + 24), radius=6, fill=color)
        draw.text((163, y), event.rule_id, font=font(15, True), fill="white")
        draw.text((250, y), event.severity, font=font(17, True), fill=color)
        draw.text((370, y), event.category, font=font(17), fill="#475467")
        draw_wrapped(draw, (500, y), event.title, font(17, True), "#172033", 70, 2)
        y += 36

    draw.text((45, 1045), "Source : Demo_Logs/*.log + matrice qualification Wazuh. Dashboard offline, pas une capture Wazuh native.", font=font(16), fill="#667085")
    CAP_TECH.parent.mkdir(exist_ok=True)
    image.save(CAP_TECH)


def render_alert_100120(events: list[Event], matrix: dict[str, dict[str, str]]) -> None:
    width, height = 1550, 1000
    image = Image.new("RGB", (width, height), "#f7f9fc")
    draw = ImageDraw.Draw(image)
    header(draw, "CAP-06 - Alerte 100120 acces patient", "Detail et qualification SOC depuis logs Daylight", width)
    target = next((e for e in events if e.rule_id == "100120" and "patient_record_access" in e.raw), next(e for e in events if e.rule_id == "100120"))
    kv = parse_kv(target.raw)
    qual = matrix.get("100120", {})

    draw.rounded_rectangle((55, 155, 720, 455), radius=12, fill="#ffffff", outline="#d0d5dd", width=2)
    draw.text((85, 185), "Detail alerte", font=font(26, True), fill="#172033")
    fields = [
        ("Regle", "100120 - Acces anormal dossier patient"),
        ("Severite", "Critical"),
        ("Horodatage", target.timestamp),
        ("Utilisateur", kv.get("user", "stagiaire.demo")),
        ("Patient", kv.get("patient_id", "DL-PT-88421")),
        ("Centre", kv.get("center", "Lyon")),
    ]
    y = 235
    for key, value in fields:
        draw.text((90, y), key, font=font(17, True), fill="#667085")
        draw_wrapped(draw, (240, y), value, font(18, True), "#172033", 36, 2)
        y += 38

    draw.rounded_rectangle((760, 155, 1495, 455), radius=12, fill="#fff1f0", outline="#f2b8ae", width=2)
    draw.text((790, 185), "Decision SOC", font=font(26, True), fill="#b42318")
    y = 238
    for label, value in [
        ("SLA", qual.get("sla_triage", "15 min")),
        ("Checks", qual.get("first_checks", "role; patient; centre; heure")),
        ("Action", qual.get("immediate_action", "Suspendre session si suspect")),
        ("Escalade", qual.get("escalation", "SOC + referent Daylight + DPO")),
    ]:
        draw.text((795, y), label, font=font(17, True), fill="#667085")
        y = draw_wrapped(draw, (920, y), value, font(18), "#172033", 48, 3) + 10

    draw.rounded_rectangle((55, 505, 1495, 825), radius=12, fill="#ffffff", outline="#d0d5dd", width=2)
    draw.text((85, 535), "Log source", font=font(24, True), fill="#172033")
    draw_wrapped(draw, (90, 590), target.raw, font(20), "#172033", 118, 8)
    draw.text((85, 770), "Preuve associee : Wazuh alert + patient access log. Cette image est une fiche offline exploitable si le dashboard Wazuh n'est pas disponible.", font=font(17), fill="#667085")

    image.save(CAP_ALERT)
    image.save(CAP_QUALIF)


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    CAPTURE_DIR.mkdir(exist_ok=True)
    events = load_events()
    matrix = load_matrix()
    render_html(events, matrix)
    render_executive(events)
    render_technical(events)
    render_alert_100120(events, matrix)
    print(f"Dashboard HTML genere : {HTML_OUT}")
    print(f"Capture generee : {CAP_ALERT}")
    print(f"Capture generee : {CAP_TECH}")
    print(f"Capture generee : {CAP_EXEC}")
    print(f"Capture generee : {CAP_QUALIF}")
    print(f"Evenements traites : {len(events)}")


if __name__ == "__main__":
    main()
