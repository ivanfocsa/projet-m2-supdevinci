from __future__ import annotations

from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "preflight-demo-report.txt"
CAPTURE_DIR = ROOT / "Annexes_Captures"
OK_IMAGE = CAPTURE_DIR / "CAP-25_preflight-demo-ok.png"
RETRY_IMAGE = CAPTURE_DIR / "PRE-25_preflight-a-reprendre.png"
TEXT_REPORT = ROOT / "preflight-evidence-report.txt"


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


def draw_wrapped(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt: ImageFont.ImageFont, fill: str, width: int, gap: int = 5) -> int:
    x, y = xy
    for line in wrap(text, width=width) or [""]:
        draw.text((x, y), line, font=fnt, fill=fill)
        box = draw.textbbox((0, 0), line or "A", font=fnt)
        y += (box[3] - box[1]) + gap
    return y


def is_lab_ok(text: str) -> tuple[bool, list[str], list[str]]:
    lines = text.splitlines()
    ok_lines = [line for line in lines if line.startswith("[OK]")]
    warn_lines = [line for line in lines if line.startswith("[WARN]")]
    docker_ok = any("Docker daemon" in line and "repond" in line and line.startswith("[OK]") for line in lines)
    wazuh_ok = any("https://localhost" in line and line.startswith("[OK]") for line in lines)
    blockers = []
    if not docker_ok:
        blockers.append("Docker daemon ne repond pas dans le preflight courant")
    if not wazuh_ok:
        blockers.append("Wazuh Dashboard https://localhost inaccessible dans le preflight courant")
    return docker_ok and wazuh_ok, ok_lines, blockers or warn_lines[:6]


def render(status_ok: bool, ok_lines: list[str], notes: list[str]) -> Path:
    width, height = 1500, 980
    image = Image.new("RGB", (width, height), "#f7f9fc")
    draw = ImageDraw.Draw(image)
    color = "#1f7a4f" if status_ok else "#b42318"
    title = "CAP-25 - Preflight demo OK" if status_ok else "Preflight demo a reprendre"
    subtitle = "Docker/Wazuh repondent, preuve prioritaire exploitable" if status_ok else "Le lab doit etre relance avant de produire CAP-25"

    draw.rectangle((0, 0, width, 112), fill="#172033")
    draw.text((46, 26), title, font=font(34, True), fill="white")
    draw.text((46, 70), subtitle, font=font(18), fill="#d5e3ff")

    draw.rounded_rectangle((55, 155, 1445, 270), radius=14, fill="#ffffff", outline="#d0d5dd", width=2)
    draw.ellipse((85, 185, 137, 237), fill=color)
    draw.text((165, 187), "STATUT LAB", font=font(18, True), fill="#667085")
    draw.text((165, 214), "OK pour capture" if status_ok else "A reprendre", font=font(26, True), fill=color)

    draw.rounded_rectangle((55, 315, 720, 820), radius=14, fill="#ffffff", outline="#d0d5dd", width=2)
    draw.text((85, 345), "Checks OK detectes", font=font(24, True), fill="#172033")
    y = 395
    for line in ok_lines[:12]:
        y = draw_wrapped(draw, (90, y), line, font(16), "#172033", 76, 4)
        y += 5

    draw.rounded_rectangle((770, 315, 1445, 820), radius=14, fill="#ffffff", outline="#d0d5dd", width=2)
    draw.text((800, 345), "Notes / actions", font=font(24, True), fill="#172033")
    y = 395
    for note in notes[:10]:
        y = draw_wrapped(draw, (805, y), "- " + note, font(17), "#172033", 68, 5)
        y += 5

    draw.text((55, 910), f"Source : {REPORT.name}. Image generee automatiquement, sans modifier le rapport.", font=font(16), fill="#667085")
    out = OK_IMAGE if status_ok else RETRY_IMAGE
    CAPTURE_DIR.mkdir(exist_ok=True)
    image.save(out)
    return out


def main() -> int:
    if not REPORT.exists():
        TEXT_REPORT.write_text("[WARN] preflight-demo-report.txt introuvable. Lancer tools/preflight_demo.ps1 -WriteReport.\n", encoding="utf-8")
        print(TEXT_REPORT.read_text(encoding="utf-8"))
        return 1

    text = REPORT.read_text(encoding="utf-8", errors="ignore")
    status_ok, ok_lines, notes = is_lab_ok(text)
    out = render(status_ok, ok_lines, notes)
    lines = [
        "=== Preuve preflight Daylight / Cyber Trust ===",
        f"Rapport source : {REPORT}",
        f"Image generee : {out}",
        f"CAP-25 valide : {'oui' if status_ok else 'non'}",
    ]
    if not status_ok:
        lines.append("CAP-25_preflight-demo-ok.png n'est pas cree car le lab ne prouve pas encore Docker + Wazuh OK.")
        lines.extend("- " + note for note in notes)
    TEXT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0 if status_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
