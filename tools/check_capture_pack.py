from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = ROOT / "config" / "captures" / "daylight_capture_checklist.csv"
CAPTURE_DIR = ROOT / "Annexes_Captures"
REPORT = ROOT / "capture-pack-report.txt"


def main() -> int:
    rows = list(csv.DictReader(CHECKLIST.read_text(encoding="utf-8").splitlines()))
    present_files = {path.name for path in CAPTURE_DIR.glob("CAP-*.png")} if CAPTURE_DIR.exists() else set()

    required = [row for row in rows if row["required_for_deposit"].lower() == "yes"]
    required_present = [row for row in required if row["filename"] in present_files]
    missing_required = [row for row in required if row["filename"] not in present_files]
    optional_missing = [row for row in rows if row["required_for_deposit"].lower() != "yes" and row["filename"] not in present_files]

    lines: list[str] = []
    lines.append("=== Controle captures Daylight / Cyber Trust ===")
    lines.append(f"Dossier captures : {CAPTURE_DIR}")
    lines.append(f"Checklist        : {CHECKLIST}")
    lines.append(f"Captures detectees CAP-*.png : {len(present_files)}")
    lines.append(f"Captures prioritaires presentes : {len(required_present)}/{len(required)}")
    lines.append("")

    if missing_required:
        lines.append("## Captures prioritaires manquantes")
        for row in missing_required:
            lines.append(f"- {row['filename']} | {row['responsible']} | {row['evidence']} | {row['screen']}")
    else:
        lines.append("## Captures prioritaires")
        lines.append("[OK] Toutes les captures prioritaires sont presentes.")
    lines.append("")

    if optional_missing:
        lines.append("## Captures optionnelles encore absentes")
        for row in optional_missing:
            lines.append(f"- {row['filename']} | {row['responsible']} | {row['evidence']}")
        lines.append("")

    unexpected = sorted(name for name in present_files if name not in {row["filename"] for row in rows})
    if unexpected:
        lines.append("## Captures non referencees")
        for name in unexpected:
            lines.append(f"- {name}")
        lines.append("")

    if len(required_present) >= 8 and not missing_required:
        lines.append("[OK] Pack captures prioritaire pret.")
        exit_code = 0
    else:
        lines.append("[WARN] Pack captures incomplet : reprendre les captures prioritaires avant depot officiel.")
        exit_code = 1

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nRapport ecrit : {REPORT}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
