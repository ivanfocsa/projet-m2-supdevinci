from __future__ import annotations

import csv
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
CAPTURE_DIR = ROOT / "Annexes_Captures"
TOPOLOGY_CSV = ROOT / "config" / "pfsense" / "pfsense_lab_topology.csv"
RULES_CSV = ROOT / "config" / "pfsense" / "pfsense_firewall_rules.csv"
ARCH_OUT = CAPTURE_DIR / "CAP-12_architecture-solution.png"
PFSENSE_OUT = CAPTURE_DIR / "CAP-13_pfsense-regles-firewall.png"


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


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.ImageFont,
    fill: str,
    width_chars: int,
    line_gap: int = 4,
) -> int:
    x, y = xy
    if not text:
        return y
    lines: list[str] = []
    for part in str(text).split("\n"):
        lines.extend(wrap(part, width=width_chars) or [""])
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        _, h = text_size(draw, line or "A", fnt)
        y += h + line_gap
    return y


def rounded_box(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    fill: str,
    outline: str,
    title: str,
    body: list[str],
    accent: str,
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=12, fill=fill, outline=outline, width=2)
    draw.rectangle((x1, y1, x2, y1 + 42), fill=accent)
    draw.text((x1 + 18, y1 + 10), title, font=font(22, True), fill="white")
    y = y1 + 58
    for line in body:
        y = draw_wrapped(draw, (x1 + 18, y), line, font(18), "#172033", 34, 5)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str, label: str = "") -> None:
    draw.line((start, end), fill=color, width=4)
    sx, sy = start
    ex, ey = end
    if ex >= sx:
        head = [(ex, ey), (ex - 14, ey - 8), (ex - 14, ey + 8)]
    else:
        head = [(ex, ey), (ex + 14, ey - 8), (ex + 14, ey + 8)]
    draw.polygon(head, fill=color)
    if label:
        mx, my = (sx + ex) // 2, (sy + ey) // 2
        tw, th = text_size(draw, label, font(16, True))
        draw.rounded_rectangle((mx - tw // 2 - 8, my - th - 10, mx + tw // 2 + 8, my + 8), radius=6, fill="#ffffff", outline=color)
        draw.text((mx - tw // 2, my - th - 4), label, font=font(16, True), fill=color)


def read_csv(path: Path) -> list[dict[str, str]]:
    return list(csv.DictReader(path.read_text(encoding="utf-8").splitlines()))


def render_architecture() -> None:
    rows = read_csv(TOPOLOGY_CSV)
    by_node = {row["node"]: row for row in rows}
    zones = [row for row in rows if row["node"] == "pfsense-fw-01" and row["interface"] != "WAN"]

    image = Image.new("RGB", (1800, 1120), "#f7f9fc")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1800, 104), fill="#172033")
    draw.text((48, 28), "Daylight / Cyber Trust - Architecture SOC cible", font=font(36, True), fill="white")
    draw.text((48, 70), "Segmentation pfSense, collecte Wazuh et flux de supervision", font=font(20), fill="#d5e3ff")

    rounded_box(draw, (70, 180, 330, 330), "#ffffff", "#9fb2d6", "Internet / WAN", ["NAT hyperviseur", "Flux entrants limites", "VPN admin OpenVPN"], "#425caa")
    rounded_box(draw, (520, 165, 820, 350), "#ffffff", "#7e8da8", "pfSense FW-01", ["Routeur / firewall", "Default deny journalise", "Remote logging vers SOC"], "#2e7d72")
    arrow(draw, (330, 255), (520, 255), "#425caa", "WAN")

    zone_boxes = {
        "USERS": (1060, 140, 1345, 285, "#4f6fb5"),
        "SERVERS": (1430, 140, 1715, 285, "#7a5da8"),
        "DMZ": (1060, 365, 1345, 510, "#b15f3c"),
        "MGMT": (1430, 365, 1715, 510, "#57646f"),
        "SOC": (1245, 650, 1535, 820, "#1f7a4f"),
    }

    for zone in zones:
        interface = zone["interface"]
        if interface not in zone_boxes:
            continue
        x1, y1, x2, y2, accent = zone_boxes[interface]
        role_lines = [zone["network"], zone["ip_address"], zone["role"]]
        rounded_box(draw, (x1, y1, x2, y2), "#ffffff", "#a7b3c5", interface, role_lines, accent)
        arrow(draw, (820, 255), (x1, (y1 + y2) // 2), accent)

    endpoints = [
        ("poste-01", "Poste utilisateur", (1075, 300, 1328, 340), "#4f6fb5"),
        ("serveur-01", "Serveur interne", (1445, 300, 1698, 340), "#7a5da8"),
        ("daylight-app-01", "Application metier", (1075, 525, 1328, 565), "#b15f3c"),
        ("admin-01", "Poste administrateur", (1445, 525, 1698, 565), "#57646f"),
        ("wazuh-manager", "SIEM Cyber Trust", (1260, 835, 1520, 875), "#1f7a4f"),
    ]
    for node, label, box, color in endpoints:
        row = by_node.get(node, {})
        draw.rounded_rectangle(box, radius=8, fill="#fffdf8", outline=color, width=2)
        draw.text((box[0] + 12, box[1] + 8), f"{node} - {row.get('ip_address', '')}", font=font(15, True), fill="#172033")
        draw.text((box[0] + 12, box[1] + 24), label, font=font(13), fill="#4b5563")

    arrow(draw, (1328, 545), (1260, 850), "#1f7a4f", "logs app 1514")
    arrow(draw, (1570, 320), (1500, 835), "#1f7a4f", "agent 1514/1515")
    arrow(draw, (1190, 320), (1280, 835), "#1f7a4f", "agent endpoint")
    arrow(draw, (670, 350), (1245, 735), "#1f7a4f", "syslog UDP 514")
    arrow(draw, (1445, 545), (1515, 735), "#57646f", "admin")

    legend = [
        ("Collecte", "Agents Wazuh + syslog pfSense/serveurs vers SOC"),
        ("Segmentation", "USERS, SERVERS, DMZ, MGMT et SOC separes"),
        ("Controle", "Default deny, journalisation, escalade SOC Cyber Trust"),
    ]
    x, y = 72, 890
    for title, body in legend:
        rounded_box(draw, (x, y, x + 500, y + 120), "#ffffff", "#c8d0dc", title, [body], "#172033")
        x += 560

    footer = f"Genere depuis {TOPOLOGY_CSV.relative_to(ROOT)} - preuve statique architecture, non capture Wazuh"
    draw.text((48, 1070), footer, font=font(16), fill="#667085")
    image.save(ARCH_OUT)


def render_firewall_matrix() -> None:
    rows = read_csv(RULES_CSV)
    columns = ["order", "interface", "action", "protocol", "source", "destination", "port", "log", "description"]
    widths = [75, 115, 90, 95, 180, 185, 110, 70, 630]
    row_h = 54
    header_h = 155
    margin = 34
    width = margin * 2 + sum(widths)
    height = header_h + row_h * (len(rows) + 1) + 70
    image = Image.new("RGB", (width, height), "#f7f9fc")
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, width, 112), fill="#172033")
    draw.text((margin, 26), "CAP-13 - Matrice firewall pfSense Daylight", font=font(34, True), fill="white")
    draw.text((margin, 68), "Regles concretes de segmentation et journalisation pour la demonstration Cyber Trust", font=font(18), fill="#d5e3ff")

    y = header_h
    x = margin
    for col, col_w in zip(columns, widths):
        draw.rectangle((x, y, x + col_w, y + row_h), fill="#2e7d72", outline="#ffffff")
        draw_wrapped(draw, (x + 8, y + 12), col.upper(), font(15, True), "white", max(8, col_w // 10), 2)
        x += col_w

    for idx, row in enumerate(rows):
        y = header_h + row_h * (idx + 1)
        action = row["action"].lower()
        if action == "block":
            stripe = "#fff1f0"
            action_fill = "#b42318"
        elif action == "pass":
            stripe = "#eefbf3"
            action_fill = "#027a48"
        else:
            stripe = "#ffffff"
            action_fill = "#475467"
        x = margin
        for col, col_w in zip(columns, widths):
            fill = action_fill if col == "action" else ("#ffffff" if idx % 2 else stripe)
            text_fill = "white" if col == "action" else "#172033"
            draw.rectangle((x, y, x + col_w, y + row_h), fill=fill, outline="#d0d5dd")
            value = row[col]
            chars = max(7, col_w // 9)
            draw_wrapped(draw, (x + 7, y + 8), value, font(13, col in {"order", "interface", "action"}), text_fill, chars, 1)
            x += col_w

    footer = f"Source : {RULES_CSV.relative_to(ROOT)} - image generee depuis le CSV, verifiable et reproductible"
    draw.text((margin, height - 48), footer, font=font(15), fill="#667085")
    image.save(PFSENSE_OUT)


def main() -> None:
    CAPTURE_DIR.mkdir(exist_ok=True)
    render_architecture()
    render_firewall_matrix()
    print(f"Image generee : {ARCH_OUT}")
    print(f"Image generee : {PFSENSE_OUT}")


if __name__ == "__main__":
    main()
