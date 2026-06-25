from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PDF = ROOT / "Youssef GUERNIOU" / "Documentation_SIEM_Youssef_GUERNIOU.pdf"
CAPTURE_DIR = ROOT / "Annexes_Captures"
REPORT = ROOT / "youssef-wazuh-proof-extraction-report.txt"

EXPECTED_HASHES = {
    "endpoint_sca": "a4d9b01c1f5a",
    "serveur_ssh_events": "c490ccdff3b5",
    "ssh_5712": "28a82c9b1aef",
    "daylight_custom_rules": "4297c6550562",
    "dashboard_severity": "a577739ecb76",
    "dashboard_source": "2b4a7fa95f92",
    "dashboard_top_rules": "1ee9bcb63c16",
    "dashboard_tech_consolide": "4100845cce2e",
    "dashboard_exec_kpis": "fafce463cc3e",
    "dashboard_exec_sites": "f6ff7b68be9d",
    "wazuh_authenticated_dashboard": "fe1fed9e82ef",
    "rbac_admin_blocked": "73728f409249",
}

DIRECT_OUTPUTS = {
    "wazuh_authenticated_dashboard": "CAP-01_wazuh-dashboard-login.png",
    "ssh_5712": "CAP-03_alerte-5712-brute-force-ssh.png",
    "endpoint_sca": "CAP-04_source-endpoint-poste01-sca.png",
    "daylight_custom_rules": "CAP-05_daylight-alertes-metier.png",
    "rbac_admin_blocked": "CAP-09_rbac-analyste-lecture-seule.png",
    "serveur_ssh_events": "CAP-16_auth-log-serveur01.png",
    "dashboard_tech_consolide": "CAP-21_dashboard-technique-requetes.png",
    "dashboard_exec_sites": "CAP-22_dashboard-executif-daylight.png",
}


def extract_unique_images() -> dict[str, bytes]:
    reader = PdfReader(str(SOURCE_PDF))
    images: dict[str, bytes] = {}
    for page in reader.pages:
        for image in getattr(page, "images", []):
            data = image.data
            digest = hashlib.sha256(data).hexdigest()[:12]
            images.setdefault(digest, data)
    return images


def write_png(data: bytes, target: Path) -> None:
    target.parent.mkdir(exist_ok=True)
    tmp = target.with_suffix(".source")
    tmp.write_bytes(data)
    with Image.open(tmp) as image:
        image.convert("RGB").save(target, "PNG")
    tmp.unlink(missing_ok=True)


def load_capture(data: bytes) -> Image.Image:
    tmp = CAPTURE_DIR / "_source_capture.tmp"
    tmp.write_bytes(data)
    try:
        return Image.open(tmp).convert("RGB").copy()
    finally:
        tmp.unlink(missing_ok=True)


def make_multisource_board(images: dict[str, bytes], target: Path) -> None:
    panels = [
        ("Endpoint poste-01 / SCA", load_capture(images[EXPECTED_HASHES["endpoint_sca"]])),
        ("Serveur serveur-01 / SSH", load_capture(images[EXPECTED_HASHES["serveur_ssh_events"]])),
        ("Application Daylight / regles metier", load_capture(images[EXPECTED_HASHES["daylight_custom_rules"]])),
    ]

    try:
        title_font = ImageFont.truetype("arial.ttf", 34)
        label_font = ImageFont.truetype("arial.ttf", 24)
        note_font = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        note_font = ImageFont.load_default()

    width = 1500
    panel_h = 760
    margin = 34
    title_h = 62
    footer_h = 68
    board_h = margin + title_h + len(panels) * (panel_h + margin) + footer_h
    board = Image.new("RGB", (width, board_h), "white")
    draw = ImageDraw.Draw(board)
    draw.rectangle((0, 0, width, 96), fill=(23, 32, 51))
    draw.text((margin, 28), "CAP-02 - Collecte multi-source Wazuh", fill="white", font=title_font)
    y = 116
    for label, image in panels:
        image.thumbnail((width - 2 * margin, panel_h - 52), Image.LANCZOS)
        draw.text((margin, y), label, fill=(23, 32, 51), font=label_font)
        board.paste(image, (margin, y + 32))
        y += panel_h + margin
    draw.text(
        (margin, board_h - footer_h + 10),
        "Source : Documentation_SIEM_Youssef_GUERNIOU.pdf. Planche composee a partir de captures Wazuh reelles du document source.",
        fill=(80, 90, 110),
        font=note_font,
    )
    board.save(target, "PNG")


def main() -> int:
    lines = [
        "=== Extraction preuves Wazuh depuis la documentation SIEM Youssef ===",
        f"Source : {SOURCE_PDF}",
        f"Destination : {CAPTURE_DIR}",
        "",
    ]

    if not SOURCE_PDF.exists():
        lines.append("[WARN] PDF source introuvable.")
        REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("\n".join(lines))
        return 1

    CAPTURE_DIR.mkdir(exist_ok=True)
    images = extract_unique_images()
    missing = [name for name, digest in EXPECTED_HASHES.items() if digest not in images]
    if missing:
        lines.append("[WARN] Images attendues introuvables : " + ", ".join(missing))
        REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("\n".join(lines))
        return 1

    for key, filename in DIRECT_OUTPUTS.items():
        target = CAPTURE_DIR / filename
        write_png(images[EXPECTED_HASHES[key]], target)
        lines.append(f"[OK] {filename} depuis {key}")

    make_multisource_board(images, CAPTURE_DIR / "CAP-02_agents-poste01-serveur01.png")
    lines.append("[OK] CAP-02_agents-poste01-serveur01.png depuis endpoint, serveur et application")

    report_copy = CAPTURE_DIR / "README_PREUVES_WAZUH_EXTRAITES.md"
    report_copy.write_text(
        "\n".join(
            [
                "# Preuves Wazuh extraites",
                "",
                "Ces captures proviennent de `Youssef GUERNIOU/Documentation_SIEM_Youssef_GUERNIOU.pdf`.",
                "Elles ne remplacent pas une nouvelle capture live si le lab Wazuh est disponible, mais elles isolent des preuves deja presentes dans la documentation SIEM.",
                "",
                "- `CAP-01` : session Wazuh authentifiee, utilisee comme preuve d'acces dashboard.",
                "- `CAP-02` : planche multi-source endpoint / serveur / application Daylight.",
                "- `CAP-03` : alerte SSH brute force `5712` sur `serveur-01`.",
                "",
                "Commande de regeneration :",
                "",
                "```powershell",
                "python .\\tools\\extract_youssef_wazuh_proofs.py",
                "```",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    lines.append(f"[OK] Note de tracabilite : {report_copy.name}")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


