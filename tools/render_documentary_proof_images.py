from __future__ import annotations

import csv
import subprocess
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "Annexes_Captures"
REPORT = ROOT / "documentary-proof-images-report.txt"


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


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="ignore")


def extract_between(text: str, start_marker: str, end_marker: str | None = None, limit: int = 2200) -> str:
    start = text.find(start_marker)
    if start < 0:
        return text[:limit]
    end = text.find(end_marker, start + len(start_marker)) if end_marker else -1
    if end < 0:
        end = min(len(text), start + limit)
    return text[start:end].strip()[:limit]


def draw_wrapped(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt: ImageFont.ImageFont, fill: str, width: int, gap: int = 5) -> int:
    x, y = xy
    for paragraph in text.splitlines():
        if not paragraph.strip():
            y += 16
            continue
        for line in wrap(paragraph, width=width) or [""]:
            draw.text((x, y), line, font=fnt, fill=fill)
            box = draw.textbbox((0, 0), line or "A", font=fnt)
            y += box[3] - box[1] + gap
    return y


def wrap_lines(text: str, width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.splitlines():
        if not paragraph.strip():
            lines.append("")
            continue
        lines.extend(wrap(paragraph, width=width) or [""])
    return lines


def render_card(filename: str, title: str, subtitle: str, source: str, sections: list[tuple[str, str]], accent: str = "#234a7c") -> Path:
    width, height = 1500, 980
    image = Image.new("RGB", (width, height), "#f7f9fc")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 120), fill="#172033")
    draw.rectangle((0, 112, width, 120), fill=accent)
    draw.text((44, 28), title, font=font(34, True), fill="white")
    draw.text((44, 76), subtitle, font=font(18), fill="#d5e3ff")

    y = 160
    left = 54
    right = width - 54
    body_font = font(17)
    line_height = 24
    for heading, body in sections:
        if y > height - 180:
            break
        body_lines = wrap_lines(body, 128)
        available = max(130, height - 130 - y)
        section_h = min(available, 76 + max(1, len(body_lines)) * line_height + 24)
        max_body_lines = max(3, int((section_h - 100) / line_height))
        visible = body_lines[:max_body_lines]
        if len(body_lines) > max_body_lines:
            visible[-1] = "..."

        draw.rounded_rectangle((left, y, right, y + section_h), radius=12, fill="#ffffff", outline="#d0d5dd", width=2)
        draw.text((left + 24, y + 22), heading, font=font(22, True), fill="#172033")
        y_line = y + 62
        for line in visible:
            draw.text((left + 24, y_line), line, font=body_font, fill="#172033")
            y_line += line_height
        y += section_h + 12

    draw.text((54, height - 70), f"Source : {source}", font=font(16), fill="#667085")
    draw.text((54, height - 44), "Preuve documentaire generee depuis les livrables du dossier ; elle ne pretend pas etre une capture live d'un outil.", font=font(14), fill="#667085")
    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / filename
    image.save(out, "PNG")
    return out


def csv_rows(path: str, predicate=lambda row: True, max_rows: int = 6) -> str:
    rows = list(csv.DictReader((ROOT / path).read_text(encoding="utf-8").splitlines()))
    selected = [row for row in rows if predicate(row)][:max_rows]
    lines = []
    for row in selected:
        lines.append(" | ".join(f"{key}={value}" for key, value in row.items() if value))
    return "\n".join(lines)


def demo_log_summary() -> str:
    log_dir = ROOT / "Demo_Logs"
    lines = []
    total = 0
    for path in sorted(log_dir.glob("*.log")):
        events = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        total += len(events)
        lines.append(f"{path.name}: {len(events)} evenement(s)")
    lines.append(f"Total dry-run: {total} evenement(s) prets a rejouer")
    return "\n".join(lines)


def dry_run_excerpt() -> str:
    try:
        result = subprocess.run(
            ["python", str(ROOT / "tools" / "send_demo_logs_to_syslog.py"), "--dry-run"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        output = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
        (ROOT / "log-replay-dry-run-report.txt").write_text(output, encoding="utf-8")
        return "\n".join(output.splitlines()[:13])
    except Exception as exc:
        return f"Dry-run non execute : {exc}"


def main() -> int:
    outputs: list[Path] = []

    playbook = extract_between(read("03_PLAYBOOKS_PROCEDURES_REX.md"), "## Playbook PB-001 - Brute force SSH", "## Playbook PB-002")
    outputs.append(
        render_card(
            "CAP-10_playbook-brute-force.png",
            "CAP-10 - Playbook brute force SSH",
            "Procedure PB-001 directement exploitable par l'analyste SOC",
            "03_PLAYBOOKS_PROCEDURES_REX.md",
            [
                ("Playbook source", playbook),
                ("Decision SOC", "Severite haute. Qualification prioritaire, verification d'une connexion reussie apres echecs, blocage source si attaque confirmee."),
            ],
            "#7a3e00",
        )
    )

    rex_patient = extract_between(read("03_PLAYBOOKS_PROCEDURES_REX.md"), "## REX incident simule 2 - Acces dossier patient", "## REX incident simule 3")
    outputs.append(
        render_card(
            "CAP-11_rex-incident-acces-patient.png",
            "CAP-11 - REX acces dossier patient",
            "Retour d'experience incident critique donnees patients",
            "03_PLAYBOOKS_PROCEDURES_REX.md",
            [
                ("REX source", rex_patient),
                ("Lien RGPD", "Alerte critique 100120 : verifier utilisateur, role, site, patient_id et justification metier ; escalader au referent Daylight/DPO si suspicion confirmee."),
            ],
            "#8a1f11",
        )
    )

    syslog = extract_between(read("config/pfsense/pfsense_syslog_wazuh.md"), "## Cote pfSense", "## Preuve attendue")
    outputs.append(
        render_card(
            "CAP-14_pfsense-syslog-wazuh.png",
            "CAP-14 - pfSense vers Wazuh",
            "Configuration syslog concrete firewall vers Wazuh Manager",
            "config/pfsense/pfsense_syslog_wazuh.md",
            [
                ("Etapes pfSense/Wazuh", syslog),
                ("Recherche attendue", "pfsense OR filterlog OR rule.id:110010 OR rule.id:110020"),
            ],
            "#355c2f",
        )
    )

    setup = extract_between(read("Youssef GUERNIOU/setup-siem-lab.ps1"), "#  setup-siem-lab.ps1", "# ---------------------------------------------------------------------\n# 2. RBAC", 2200)
    outputs.append(
        render_card(
            "CAP-15_script-setup-siem-lab.png",
            "CAP-15 - Automatisation lab SIEM",
            "Script Youssef : serveur-01, agent Wazuh, SSH/rsyslog, brute force 5712",
            "Youssef GUERNIOU/setup-siem-lab.ps1",
            [
                ("Pipeline script", setup),
                ("Preuve attendue", "Commande reproductible : powershell -ExecutionPolicy Bypass -File .\\Youssef GUERNIOU\\setup-siem-lab.ps1"),
            ],
            "#234a7c",
        )
    )

    rbac = extract_between(read("Youssef GUERNIOU/setup-siem-lab.ps1"), "# 2. RBAC", "# ---------------------------------------------------------------------\n# 3.", 2200)
    outputs.append(
        render_card(
            "CAP-17_compte-supervision-dashboard.png",
            "CAP-17 - Compte supervision RBAC",
            "Profil supervision configure en lecture seule via soc_readonly",
            "Youssef GUERNIOU/setup-siem-lab.ps1",
            [
                ("Configuration RBAC", rbac),
                ("Compte attendu", "supervision / CTView2026!Blue ; role soc_readonly ; acces lecture dashboards et alertes, sans administration."),
            ],
            "#155eef",
        )
    )

    outputs.append(
        render_card(
            "CAP-18_export-dashboard-report.png",
            "CAP-18 - Export dashboard / rapport",
            "Rapports de statut generes depuis la checklist et les validations",
            "evidence-status-report.txt + validation-rendu-final.txt",
            [
                ("Statut preuves", read("evidence-status-report.txt")),
                ("Validation courte", "\n".join(read("validation-rendu-final.txt").splitlines()[:10])),
            ],
            "#53389e",
        )
    )

    pf_alerts = "\n".join(read("Demo_Logs/pfsense.log").splitlines()[:5])
    outputs.append(
        render_card(
            "CAP-19_wazuh-pfsense-alertes.png",
            "CAP-19 - Alerting pfSense",
            "Evenements firewall concrets et regles Wazuh 110010/110020/110050",
            "Demo_Logs/pfsense.log + config/wazuh/local_rules_daylight_pfsense.xml",
            [
                ("Logs pfSense demo", pf_alerts),
                ("Qualification", csv_rows("config/wazuh/daylight_alert_qualification_matrix.csv", lambda row: row["rule_id"].startswith("110"), 4)),
            ],
            "#0f766e",
        )
    )

    dry_run = dry_run_excerpt()
    outputs.append(
        render_card(
            "CAP-20_wazuh-rejeu-logs-demo.png",
            "CAP-20 - Rejeu logs vers Wazuh",
            "Mode dry-run : les evenements sont prets a etre envoyes en syslog",
            "tools/send_demo_logs_to_syslog.py --dry-run",
            [
                ("Synthese fichiers logs", demo_log_summary()),
                ("Extrait dry-run", dry_run),
            ],
            "#175cd3",
        )
    )

    outputs.append(
        render_card(
            "CAP-24_qualification-alerte-110020.png",
            "CAP-24 - Qualification alerte 110020",
            "Tentative inter-VLAN vers MGMT/SERVERS bloquee par pfSense",
            "config/wazuh/daylight_alert_qualification_matrix.csv",
            [
                ("Matrice SOC", csv_rows("config/wazuh/daylight_alert_qualification_matrix.csv", lambda row: row["rule_id"] == "110020", 1)),
                ("Action", "Confirmer le blocage pfSense, identifier la source, isoler le poste si comportement anormal, escalader SOC + exploitation reseau."),
            ],
            "#b42318",
        )
    )

    outputs.append(
        render_card(
            "CAP-27_rejeu-logs-dry-run.png",
            "CAP-27 - Dry-run replay logs",
            "Preuve de rejouabilite sans envoi reseau",
            "log-replay-dry-run-report.txt",
            [
                ("Commande", "python .\\tools\\send_demo_logs_to_syslog.py --dry-run"),
                ("Sortie", dry_run),
            ],
            "#6941c6",
        )
    )

    rex_rows = csv_rows("config/lab/daylight_rex_scenarios.csv", lambda row: row["incident_id"] in {"INC-DAYLIGHT-002", "INC-DAYLIGHT-004"}, 2)
    outputs.append(
        render_card(
            "CAP-28_rex-incident-rempli.png",
            "CAP-28 - REX incident pre-rempli",
            "Fiches REX exploitables pour donnees patients et mouvement lateral",
            "config/lab/daylight_rex_scenarios.csv",
            [
                ("Scenarios REX", rex_rows),
                ("Utilisation orale", "Mahamadou peut montrer cause, action immediate, corrective action, preventive action et owner pour prouver la boucle post-incident."),
            ],
            "#7a271a",
        )
    )

    lines = ["=== Generation captures documentaires Daylight / Cyber Trust ==="]
    lines.extend(f"[OK] {path.name} ({path.stat().st_size} octets)" for path in outputs)
    lines.append("")
    lines.append("Ces images sont documentaires : elles rendent visibles des preuves deja presentes dans les fichiers du projet.")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


