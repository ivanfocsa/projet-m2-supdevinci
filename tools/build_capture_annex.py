from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPTURE_DIR = ROOT / "Annexes_Captures"
CHECKLIST = ROOT / "config" / "captures" / "daylight_capture_checklist.csv"
OUT = ROOT / "16_ANNEXE_CAPTURES_WAZUH.md"


def load_captures() -> list[dict[str, str]]:
    return list(csv.DictReader(CHECKLIST.read_text(encoding="utf-8").splitlines()))


def status_for(path: Path) -> str:
    return "OK" if path.exists() else "MANQUANT"


def figure_for(path: Path, caption: str) -> str:
    if not path.exists():
        return f"> Capture/preuve manquante : `{path.name}`\n"
    uri = path.resolve().as_uri()
    return (
        f'<figure class="capture">\n'
        f'  <img src="{uri}" alt="{caption}">\n'
        f'  <figcaption>{caption}</figcaption>\n'
        f'</figure>\n'
    )


def build() -> None:
    CAPTURE_DIR.mkdir(exist_ok=True)
    captures = load_captures()

    present = 0
    required = [row for row in captures if row["required_for_deposit"].lower() == "yes"]
    required_present = 0
    lines = [
        "# Annexe captures et preuves - Daylight / Cyber Trust",
        "",
        "## Objectif",
        "",
        "Cette annexe assemble les captures et preuves visuelles du demonstrateur SOC. Elle est generee automatiquement depuis `config/captures/daylight_capture_checklist.csv` et le dossier `Annexes_Captures/`.",
        "",
        "Regeneration :",
        "",
        "```powershell",
        "python .\\tools\\render_static_proof_images.py",
        "python .\\tools\\build_capture_annex.py",
        "python .\\tools\\export_markdown_to_pdf.py",
        "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -ExecutionPolicy Bypass -File .\\tools\\rebuild_rendu_final.ps1",
        "```",
        "",
        "## Synthese des preuves",
        "",
        "| ID | Statut | Priorite | Obligatoire depot | Fichier | Preuve | Responsable |",
        "|---|---|---:|---|---|---|---|",
    ]

    for row in captures:
        path = CAPTURE_DIR / row["filename"]
        status = status_for(path)
        required_flag = row["required_for_deposit"].lower() == "yes"
        if status == "OK":
            present += 1
            if required_flag:
                required_present += 1
        lines.append(
            f"| {row['id']} | {status} | {row['priority']} | {row['required_for_deposit']} | `{row['filename']}` | {row['evidence']} | {row['responsible']} |"
        )

    lines.extend(
        [
            "",
            f"Captures/preuves presentes : **{present} / {len(captures)}**.",
            f"Captures prioritaires presentes : **{required_present} / {len(required)}**.",
            "",
            "## Captures integrees",
            "",
        ]
    )

    for row in captures:
        path = CAPTURE_DIR / row["filename"]
        lines.extend(
            [
                f"### {row['id']} - {row['evidence']}",
                "",
                f"Responsable : {row['responsible']}  ",
                f"Priorite : {row['priority']}  ",
                f"Obligatoire depot : {row['required_for_deposit']}",
                "",
                figure_for(path, row["screen"]),
                "",
            ]
        )

    lines.extend(
        [
            "## Lecture du statut",
            "",
            "- `OK` signifie que l'image existe dans `Annexes_Captures/` et sera integree au PDF.",
            "- `MANQUANT` signifie que la preuve doit encore etre capturee ou produite depuis le lab/document correspondant.",
            "- Les images statiques generees depuis les fichiers de configuration sont admises uniquement quand la checklist les decrit comme preuve documentaire, par exemple la matrice pfSense.",
            "- Aucune capture Wazuh n'est simulee : l'annexe reflete l'etat reel du dossier.",
        ]
    )

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Annexe generee : {OUT}")
    print(f"Captures/preuves presentes : {present}/{len(captures)}")
    print(f"Captures prioritaires presentes : {required_present}/{len(required)}")


if __name__ == "__main__":
    build()
