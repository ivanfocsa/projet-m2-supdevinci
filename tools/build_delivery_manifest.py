import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover - defensive when dependencies are missing
    PdfReader = None


ROOT = Path(__file__).resolve().parents[1]
ZIP_NAME = "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip"
PROJECT_NAME = "PE-2526 M2CS - Daylight / Cyber Trust"

MANIFEST_JSON = ROOT / "MANIFEST_DEPOT.json"
MANIFEST_MD = ROOT / "MANIFEST_DEPOT.md"
DOSSIER_MD = ROOT / "27_MANIFESTE_DEPOT_ET_INTEGRITE.md"
ZIP_HASH = ROOT / f"{ZIP_NAME}.sha256"

PDF_DIR = ROOT / "Rendus_PDF"
CAPTURE_DIR = ROOT / "Annexes_Captures"
CHECKLIST = ROOT / "config" / "captures" / "daylight_capture_checklist.csv"
VIDEO_LINK = ROOT / "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt"
COMBINED_PDF = PDF_DIR / "PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_DossierGroupeComplet.pdf"

MP4_CANDIDATES = [
    ROOT / "PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4",
    ROOT / "PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4",
]

TARGET_GLOBS = [
    "*.md",
    "Yvan FOCSA/*.md",
    "Youssef GUERNIOU/*.md",
    "Kilyan FELIX/*.md",
    "Mahamadou DIACOUMBA/*.md",
    "Rendus_PDF/*.pdf",
    "Annexes_Captures/*.png",
    "config/**/*.csv",
    "config/**/*.xml",
    "config/**/*.md",
    "config/**/*.txt",
    "Demo_Logs/*.log",
    "Dashboards_Offline/*.html",
    "Video_Overlays/*.png",
    "Video_Overlays/*.md",
    "tools/*.py",
    "tools/*.ps1",
    "*.pptx",
]

EXCLUDED_NAMES = {
    MANIFEST_JSON.name,
    MANIFEST_MD.name,
    ZIP_HASH.name,
    ZIP_NAME,
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_targets() -> list[Path]:
    files: set[Path] = set()
    for pattern in TARGET_GLOBS:
        for path in ROOT.glob(pattern):
            if path.is_file() and path.name not in EXCLUDED_NAMES:
                files.add(path)
    return sorted(files, key=lambda item: rel(item).lower())


def read_capture_status() -> dict:
    present = {path.name for path in CAPTURE_DIR.glob("CAP-*.png")} if CAPTURE_DIR.exists() else set()
    rows = []
    if CHECKLIST.exists():
        rows = list(csv.DictReader(CHECKLIST.read_text(encoding="utf-8").splitlines()))

    required = [row for row in rows if row.get("required_for_deposit", "").lower() == "yes"]
    missing_required = [row["filename"] for row in required if row["filename"] not in present]

    return {
        "cap_png_count": len(present),
        "required_total": len(required),
        "required_present": len(required) - len(missing_required),
        "missing_required": missing_required,
        "required_rows": required,
        "present_files": sorted(present),
    }


def read_video_status() -> dict:
    link_text = VIDEO_LINK.read_text(encoding="utf-8", errors="ignore") if VIDEO_LINK.exists() else ""
    has_link = ("http://" in link_text or "https://" in link_text) and "Coller ici" not in link_text
    mp4 = [path for path in MP4_CANDIDATES if path.exists() and path.stat().st_size > 10_000_000]
    return {
        "link_file": rel(VIDEO_LINK) if VIDEO_LINK.exists() else None,
        "has_youtube_link": has_link,
        "mp4_files": [rel(path) for path in mp4],
        "ready": has_link or bool(mp4),
    }


def pdf_page_count(path: Path) -> int | None:
    if not path.exists() or PdfReader is None:
        return None
    try:
        return len(PdfReader(str(path)).pages)
    except Exception:
        return None


def build_manifest() -> dict:
    captures = read_capture_status()
    video = read_video_status()
    files = []
    for path in collect_targets():
        files.append(
            {
                "path": rel(path),
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    pdfs = sorted(PDF_DIR.glob("*.pdf")) if PDF_DIR.exists() else []
    blockers = []
    if captures["missing_required"]:
        blockers.append(
            {
                "type": "captures_wazuh_preflight",
                "detail": "Captures prioritaires reelles manquantes",
                "items": captures["missing_required"],
            }
        )
    if not video["ready"]:
        blockers.append(
            {
                "type": "video",
                "detail": "Lien YouTube non repertorie ou MP4 final absent",
                "items": [rel(VIDEO_LINK)],
            }
        )

    return {
        "project": PROJECT_NAME,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": "pret_pour_depot_officiel" if not blockers else "pret_structurellement_avec_preuves_reelles_restantes",
        "summary": {
            "pdf_count": len(pdfs),
            "combined_pdf_pages": pdf_page_count(COMBINED_PDF),
            "cap_png_count": captures["cap_png_count"],
            "required_capture_present": captures["required_present"],
            "required_capture_total": captures["required_total"],
            "video_ready": video["ready"],
            "hashed_files": len(files),
        },
        "capture_status": {
            "required_total": captures["required_total"],
            "required_present": captures["required_present"],
            "missing_required": captures["missing_required"],
            "present_files": captures["present_files"],
        },
        "video_status": video,
        "blocking_before_official_deposit": blockers,
        "files": files,
        "zip_hash_note": "Le hash final du ZIP est produit dans le fichier .sha256 adjacent apres compression, car l'archive contient ce manifeste et ne peut pas contenir sa propre empreinte finale.",
    }


def short_hash(value: str) -> str:
    return value[:16]


def find_file(files: list[dict], name: str) -> dict | None:
    for item in files:
        if item["path"].endswith(name):
            return item
    return None


def render_markdown(manifest: dict) -> str:
    summary = manifest["summary"]
    blockers = manifest["blocking_before_official_deposit"]
    files = manifest["files"]
    critical_names = [
        "PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_DossierGroupeComplet.pdf",
        "PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_RapportGroupe.pdf",
        "Presentation_Daylight_CyberTrust.pptx",
        "16_ANNEXE_CAPTURES_WAZUH.pdf",
        "18_SOLUTIONS_CONCRETES_DEMO.pdf",
        "20_MODE_OPERATOIRE_PFSENSE_WAZUH_LAB.pdf",
        "21_DASHBOARDS_ALERTES_QUALIFICATION.pdf",
        "24_DASHBOARD_SOC_OFFLINE.pdf",
        "25_MODE_OPERATOIRE_CAPTURE_WAZUH_PREUVES.pdf",
        "26_MODE_OPERATOIRE_VIDEO_DEPOT.pdf",
        "27_MANIFESTE_DEPOT_ET_INTEGRITE.pdf",
        "28_RUNBOOK_EXPRESS_PREUVES_RESTANTES.pdf",
        "29_IMPORT_PREUVES_FINALES.pdf",
        "30_TABLEAU_BORD_STATUT_FINAL.pdf",
        "README_LIVRABLES.md",
        "post_capture_finalize.ps1",
        "import_final_evidence.ps1",
        "build_final_evidence_dashboard.py",
        "build_demo_control_center.py",
        "open_demo_control_center.ps1",
        "repair_lab_and_capture_cap25.ps1",
        "lab-cap25-recovery-report.txt",
        "daylight_demo_control_center.html",
        "daylight_video_overlays.html",
        "README_VIDEO_OVERLAYS.md",
        "overlay_yvan_focsa.png",
        "overlay_youssef_guerniou.png",
        "overlay_kilyan_felix.png",
        "overlay_mahamadou_diacoumba.png",
    ]

    lines = [
        "# Manifeste depot et integrite - Daylight / Cyber Trust",
        "",
        "Ce manifeste sert de controle final lisible par le groupe avant depot. Il liste l'etat reel du dossier, les pieces critiques et les empreintes SHA-256 utiles pour verifier qu'un fichier n'a pas ete modifie.",
        "",
        "## Etat synthetique",
        "",
        f"- Statut : `{manifest['status']}`",
        f"- Generation : `{manifest['generated_at']}`",
        f"- PDF detectes : `{summary['pdf_count']}`",
        f"- Pages du dossier groupe complet : `{summary['combined_pdf_pages']}`",
        f"- Captures CAP-*.png : `{summary['cap_png_count']}`",
        f"- Captures prioritaires presentes : `{summary['required_capture_present']}/{summary['required_capture_total']}`",
        f"- Video prete : `{'oui' if summary['video_ready'] else 'non'}`",
        f"- Fichiers hashes dans `MANIFEST_DEPOT.json` : `{summary['hashed_files']}`",
        "",
        "## Points restants avant depot officiel",
        "",
    ]

    if blockers:
        for blocker in blockers:
            lines.append(f"- {blocker['detail']} : {', '.join(blocker['items'])}")
    else:
        lines.append("- Aucun point bloquant detecte par le manifeste.")

    lines.extend(
        [
            "",
            "## Captures prioritaires",
            "",
            "| Capture | Responsable | Preuve attendue | Etat |",
            "|---|---|---|---|",
        ]
    )
    present = set(manifest["capture_status"]["present_files"])
    for row in read_capture_status()["required_rows"]:
        state = "presente" if row["filename"] in present else "manquante"
        lines.append(f"| `{row['filename']}` | {row['responsible']} | {row['evidence']} | {state} |")

    lines.extend(
        [
            "",
            "## Pieces critiques et empreintes",
            "",
            "| Piece | Taille | SHA-256 court |",
            "|---|---:|---|",
        ]
    )
    for name in critical_names:
        item = find_file(files, name)
        if item:
            lines.append(f"| `{item['path']}` | {item['size_bytes']} | `{short_hash(item['sha256'])}` |")

    lines.extend(
        [
            "",
            "## Verification recommandee",
            "",
            "```powershell",
            "python .\\tools\\build_delivery_manifest.py",
            "Get-FileHash -Algorithm SHA256 .\\PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip",
            "```",
            "",
            "Le fichier `MANIFEST_DEPOT.json` contient la liste complete des fichiers hashes. Le hash final du ZIP est conserve dans le fichier `.sha256` adjacent apres reconstruction de l'archive.",
            "",
        ]
    )
    return "\n".join(lines)


def write_zip_hash() -> None:
    zip_path = ROOT / ZIP_NAME
    if not zip_path.exists():
        return
    ZIP_HASH.write_text(f"{sha256(zip_path)}  {ZIP_NAME}\n", encoding="utf-8")


def main() -> int:
    manifest = build_manifest()
    MANIFEST_JSON.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown = render_markdown(manifest)
    MANIFEST_MD.write_text(markdown, encoding="utf-8")
    write_zip_hash()

    print(f"Manifeste JSON : {MANIFEST_JSON}")
    print(f"Manifeste Markdown : {MANIFEST_MD}")
    if DOSSIER_MD.exists():
        print(f"Document dossier statique : {DOSSIER_MD}")
    if ZIP_HASH.exists():
        print(f"Hash ZIP adjacent : {ZIP_HASH}")
    print(f"Statut : {manifest['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())





