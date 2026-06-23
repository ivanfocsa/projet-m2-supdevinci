from __future__ import annotations

import re
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont

from export_markdown_to_pdf import DOCUMENTS, ROOT, convert_mermaid_fences


PDF_DIR = ROOT / "Rendus_PDF"
REPORT_OUT = ROOT / "pdf-pillow-export-report.txt"


def load_font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates: list[str] = []
    if mono:
        candidates.extend(
            [
                "C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
                "C:/Windows/Fonts/courbd.ttf" if bold else "C:/Windows/Fonts/cour.ttf",
            ]
        )
    else:
        candidates.extend(
            [
                "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
                "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
            ]
        )
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def clean_inline(text: str) -> str:
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"[image: \1]", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("`", "")
    text = text.replace("**", "").replace("__", "")
    text = text.replace("\\", "")
    return text


def wrap_by_pixels(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, width: int) -> list[str]:
    if not text:
        return [""]
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if draw.textlength(candidate, font=font) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def render_pdf(source: Path, output: Path, title: str) -> int:
    page_width, page_height = 1240, 1754
    margin_x, margin_y = 82, 88
    footer_y = page_height - 64
    max_width = page_width - 2 * margin_x
    pages: list[Image.Image] = []

    fonts = {
        "title": load_font(42, True),
        "h1": load_font(38, True),
        "h2": load_font(31, True),
        "h3": load_font(26, True),
        "body": load_font(22),
        "small": load_font(18),
        "code": load_font(18, mono=True),
        "footer": load_font(15),
    }

    def new_page() -> tuple[Image.Image, ImageDraw.ImageDraw, int]:
        image = Image.new("RGB", (page_width, page_height), "white")
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, page_width, 54), fill="#172033")
        draw.text((margin_x, 14), "Projet Daylight / Cyber Trust", font=fonts["footer"], fill="white")
        pages.append(image)
        return image, draw, margin_y

    image, draw, y = new_page()

    def finish_page() -> None:
        draw.text((margin_x, footer_y + 14), f"{title} - page {len(pages)}", font=fonts["footer"], fill="#667085")

    def ensure_space(height: int) -> None:
        nonlocal image, draw, y
        if y + height > footer_y:
            finish_page()
            image, draw, y = new_page()

    def write_wrapped(text: str, font: ImageFont.ImageFont, fill: str, indent: int = 0, gap: int = 7) -> None:
        nonlocal y
        lines = wrap_by_pixels(draw, text, font, max_width - indent)
        line_height = max(27, int(getattr(font, "size", 16) * 1.45))
        ensure_space(line_height * len(lines) + gap)
        for line in lines:
            draw.text((margin_x + indent, y), line, font=font, fill=fill)
            y += line_height
        y += gap

    raw = convert_mermaid_fences(source.read_text(encoding="utf-8", errors="ignore"))
    write_wrapped(title, fonts["title"], "#0f172a", gap=20)

    in_code = False
    for original in raw.splitlines():
        line = original.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code = not in_code
            write_wrapped("```", fonts["code"], "#475467", gap=2)
            continue

        if not stripped:
            y += 10
            continue

        if in_code:
            for chunk in wrap(stripped, width=112) or [""]:
                write_wrapped(chunk, fonts["code"], "#1f2937", gap=1)
            continue

        if stripped.startswith("# "):
            y += 10
            write_wrapped(clean_inline(stripped[2:]), fonts["h1"], "#0f172a", gap=12)
        elif stripped.startswith("## "):
            y += 8
            write_wrapped(clean_inline(stripped[3:]), fonts["h2"], "#1f2937", gap=10)
        elif stripped.startswith("### "):
            write_wrapped(clean_inline(stripped[4:]), fonts["h3"], "#374151", gap=8)
        elif stripped.startswith("|"):
            for chunk in wrap(stripped, width=116) or [""]:
                write_wrapped(chunk, fonts["code"], "#1f2937", gap=1)
        elif stripped.startswith(("- ", "* ")):
            write_wrapped("- " + clean_inline(stripped[2:]), fonts["body"], "#111827", indent=24)
        elif re.match(r"^\d+\.\s+", stripped):
            write_wrapped(clean_inline(stripped), fonts["body"], "#111827", indent=24)
        else:
            write_wrapped(clean_inline(stripped), fonts["body"], "#111827")

    finish_page()
    output.parent.mkdir(exist_ok=True)
    first, *rest = pages
    first.save(output, "PDF", resolution=150.0, save_all=True, append_images=rest)
    return len(pages)


def main() -> int:
    PDF_DIR.mkdir(exist_ok=True)
    lines = ["=== Export PDF Pillow Daylight / Cyber Trust ==="]
    count = 0
    total_pages = 0
    for source_name, output_name in DOCUMENTS.items():
        source = ROOT / source_name
        if not source.exists():
            lines.append(f"[SKIP] {source_name}")
            continue
        output = PDF_DIR / f"{output_name}.pdf"
        pages = render_pdf(source, output, output_name)
        total_pages += pages
        count += 1
        lines.append(f"[OK] {output.name} - {pages} page(s)")

    lines.append(f"PDF regeneres : {count}")
    lines.append(f"Pages totales exportees : {total_pages}")
    REPORT_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(REPORT_OUT.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

