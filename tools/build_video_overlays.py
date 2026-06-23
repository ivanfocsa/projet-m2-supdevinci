from __future__ import annotations

import html
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "Video_Overlays"
DASHBOARD_DIR = ROOT / "Dashboards_Offline"
HTML_OUT = DASHBOARD_DIR / "daylight_video_overlays.html"
REPORT_OUT = ROOT / "video-overlays-report.txt"
README_OUT = OUT_DIR / "README_VIDEO_OVERLAYS.md"

CANVAS = (1920, 260)

SPEAKERS = [
    {
        "slug": "kilyan_felix",
        "name": "Kilyan FELIX",
        "role": "Chef de projet SOC / detection, alertes, dashboards",
        "accent": "#22a699",
        "initials": "KF",
    },
    {
        "slug": "yvan_focsa",
        "name": "Yvan FOCSA",
        "role": "Architecte solution / pfSense, segmentation, architecture",
        "accent": "#1d4e89",
        "initials": "YF",
    },
    {
        "slug": "youssef_guerniou",
        "name": "Youssef GUERNIOU",
        "role": "Ingenieur SIEM / Wazuh, agents, regles, RBAC",
        "accent": "#7a4dd8",
        "initials": "YG",
    },
    {
        "slug": "mahamadou_diacoumba",
        "name": "Mahamadou DIACOUMBA",
        "role": "Exploitation lab / VM, playbooks, procedures, REX",
        "accent": "#d97706",
        "initials": "MD",
    },
    {
        "slug": "equipe_cyber_trust",
        "name": "Equipe Cyber Trust",
        "role": "Conclusion, depot final et prochaines etapes Daylight",
        "accent": "#475467",
        "initials": "CT",
    },
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def hex_to_rgba(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def draw_overlay(speaker: dict[str, str]) -> Path:
    image = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    accent = hex_to_rgba(speaker["accent"], 255)
    dark = (18, 32, 48, 232)
    panel = (255, 255, 255, 238)
    muted = (102, 112, 133, 255)
    ink = (24, 34, 48, 255)

    draw.rounded_rectangle((70, 42, 1510, 218), radius=18, fill=panel)
    draw.rounded_rectangle((70, 42, 260, 218), radius=18, fill=dark)
    draw.rectangle((238, 42, 280, 218), fill=dark)
    draw.rectangle((280, 42, 294, 218), fill=accent)

    draw.ellipse((105, 73, 205, 173), fill=accent)
    initials_font = font(34, True)
    box = draw.textbbox((0, 0), speaker["initials"], font=initials_font)
    draw.text(
        (155 - (box[2] - box[0]) / 2, 123 - (box[3] - box[1]) / 2),
        speaker["initials"],
        font=initials_font,
        fill="white",
    )

    draw.text((330, 70), speaker["name"], font=font(52, True), fill=ink)
    draw.text((334, 134), speaker["role"], font=font(27), fill=muted)
    draw.text((1210, 78), "Cyber Trust", font=font(30, True), fill=ink)
    draw.text((1213, 126), "Projet Daylight SOC externalise", font=font(20), fill=muted)

    out = OUT_DIR / f"overlay_{speaker['slug']}.png"
    image.save(out)
    return out


def render_html(paths: list[Path]) -> str:
    generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cards = []
    for path, speaker in zip(paths, SPEAKERS):
        rel = Path("..") / path.relative_to(ROOT)
        cards.append(
            f"""
<article>
  <h2>{html.escape(speaker['name'])}</h2>
  <p>{html.escape(speaker['role'])}</p>
  <img src="{html.escape(rel.as_posix())}" alt="{html.escape(speaker['name'])}">
  <code>{html.escape(path.name)}</code>
</article>
"""
        )

    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Daylight / Cyber Trust - Overlays video</title>
<style>
body {{ margin:0; font-family:Arial, sans-serif; background:#f6f7fb; color:#182230; }}
header {{ background:#182230; color:white; padding:24px 34px; border-bottom:4px solid #22a699; }}
header h1 {{ margin:0; font-size:28px; }}
header p {{ margin:8px 0 0; color:#d7e3f4; }}
main {{ padding:22px 34px 40px; display:grid; gap:16px; }}
article {{ background:white; border:1px solid #d0d5dd; border-radius:8px; padding:18px; }}
h2 {{ margin:0 0 6px; }}
p {{ margin:0 0 12px; color:#667085; }}
img {{ display:block; max-width:100%; background:#98a2b3; border-radius:6px; }}
code {{ display:inline-block; margin-top:10px; background:#f2f4f7; border:1px solid #e4e7ec; border-radius:5px; padding:4px 7px; }}
pre {{ white-space:pre-wrap; background:#111827; color:#f9fafb; border-radius:8px; padding:14px; }}
</style>
</head>
<body>
<header>
  <h1>Daylight / Cyber Trust - Overlays video</h1>
  <p>Genere le {generated}. Utiliser ces PNG comme image superposee dans OBS, Teams, PowerPoint ou l'outil de montage.</p>
</header>
<main>
<section>
<pre>Dans OBS : Sources > + > Image > choisir le PNG de l'intervenant > positionner en bas de l'ecran.
Dans PowerPoint : Inserer > Images > PNG de l'intervenant > placer en bas de la diapositive.
Pendant la video : changer le PNG a chaque prise de parole.</pre>
</section>
{''.join(cards)}
</main>
</body>
</html>
"""


def render_readme(paths: list[Path]) -> str:
    rows = [
        "| Fichier | Intervenant | Role affiche |",
        "|---|---|---|",
    ]
    for path, speaker in zip(paths, SPEAKERS):
        rows.append(f"| `{path.name}` | {speaker['name']} | {speaker['role']} |")

    return "\n".join(
        [
            "# Overlays video - Daylight / Cyber Trust",
            "",
            "Ces PNG transparents servent a afficher le nom et le role de chaque intervenant pendant la video 15-20 minutes.",
            "",
            "## Utilisation rapide",
            "",
            "1. Ouvrir OBS, Teams, PowerPoint ou l'outil de montage.",
            "2. Ajouter le PNG correspondant a l'intervenant comme image superposee.",
            "3. Le placer en bas de l'ecran.",
            "4. Changer de PNG a chaque changement d'intervenant.",
            "",
            "## Fichiers",
            "",
            *rows,
            "",
        ]
    )


def main() -> int:
    OUT_DIR.mkdir(exist_ok=True)
    DASHBOARD_DIR.mkdir(exist_ok=True)
    paths = [draw_overlay(speaker) for speaker in SPEAKERS]
    HTML_OUT.write_text(render_html(paths), encoding="utf-8")
    README_OUT.write_text(render_readme(paths), encoding="utf-8")
    REPORT_OUT.write_text(
        "\n".join(
            [
                "=== Overlays video Daylight / Cyber Trust ===",
                f"Images : {len(paths)}",
                f"Dossier : {OUT_DIR}",
                f"Preview HTML : {HTML_OUT}",
                "Usage : afficher le PNG correspondant pendant chaque prise de parole.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(REPORT_OUT.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
