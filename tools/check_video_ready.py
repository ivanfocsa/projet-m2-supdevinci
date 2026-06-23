from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINK_FILE = ROOT / "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt"
MP4_CANDIDATES = [
    ROOT / "PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4",
    ROOT / "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4",
]
SHOTLIST = ROOT / "config" / "video" / "daylight_video_shotlist.csv"
CHECKLIST = ROOT / "config" / "video" / "daylight_video_recording_checklist.csv"
DESCRIPTION = ROOT / "config" / "video" / "youtube_description_daylight.txt"
REPORT = ROOT / "video-readiness-report.txt"

URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def find_video_link() -> tuple[bool, str]:
    text = read_text(LINK_FILE)
    match = URL_RE.search(text)
    if not match:
        return False, "aucune URL http/https trouvee"
    url = match.group(0).strip().rstrip(".)]")
    if "Coller ici" in text:
        return False, "le fichier contient encore le texte placeholder 'Coller ici'"
    if "youtube.com" not in url and "youtu.be" not in url:
        return False, f"URL detectee mais pas YouTube : {url}"
    return True, url


def find_mp4() -> tuple[bool, str]:
    for path in MP4_CANDIDATES:
        if path.exists():
            size = path.stat().st_size
            if size < 10_000_000:
                return False, f"MP4 detecte mais taille faible ({size} octets) : {path.name}"
            return True, f"{path.name} ({size} octets)"
    return False, "aucun MP4 final detecte"


def main() -> int:
    link_ok, link_detail = find_video_link()
    mp4_ok, mp4_detail = find_mp4()
    shotlist_ok = SHOTLIST.exists()
    checklist_ok = CHECKLIST.exists()
    description_ok = DESCRIPTION.exists()
    ready = link_ok or mp4_ok

    lines = [
        "=== Controle video Daylight / Cyber Trust ===",
        f"Fichier lien : {LINK_FILE}",
        f"Lien YouTube : {'OK' if link_ok else 'WARN'} - {link_detail}",
        f"MP4 final    : {'OK' if mp4_ok else 'WARN'} - {mp4_detail}",
        f"Shotlist     : {'OK' if shotlist_ok else 'WARN'} - {SHOTLIST}",
        f"Checklist    : {'OK' if checklist_ok else 'WARN'} - {CHECKLIST}",
        f"Description  : {'OK' if description_ok else 'WARN'} - {DESCRIPTION}",
        "",
    ]

    if ready:
        lines.append("[OK] Video prete pour depot : lien YouTube non repertorie ou MP4 final detecte.")
    else:
        lines.extend(
            [
                "[WARN] Video non prete pour depot.",
                "Actions restantes :",
                "- enregistrer la video 15-20 minutes avec les 4 membres ;",
                "- publier en YouTube non repertorie puis coller l'URL dans le fichier lien ;",
                "- ou deposer un MP4 final avec la nomenclature attendue ;",
                "- relancer tools/post_capture_finalize.ps1.",
            ]
        )

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nRapport ecrit : {REPORT}")
    return 0 if ready and shotlist_ok and checklist_ok and description_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

