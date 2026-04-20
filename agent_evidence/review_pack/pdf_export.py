from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas

_FONT_NAME = "STSong-Light"
_FONT_REGISTERED = False


def _ensure_font_registered() -> str:
    global _FONT_REGISTERED
    if not _FONT_REGISTERED:
        pdfmetrics.registerFont(UnicodeCIDFont(_FONT_NAME))
        _FONT_REGISTERED = True
    return _FONT_NAME


def _wrap_text(text: str, *, font_name: str, font_size: int, max_width: float) -> list[str]:
    if not text:
        return [""]

    wrapped: list[str] = []
    current = ""
    for char in text:
        candidate = f"{current}{char}"
        if current and pdfmetrics.stringWidth(candidate, font_name, font_size) > max_width:
            wrapped.append(current)
            current = char
        else:
            current = candidate
    if current:
        wrapped.append(current)
    return wrapped or [""]


def write_review_report_pdf(markdown: str, destination: str | Path) -> Path:
    font_name = _ensure_font_registered()
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)

    page_width, page_height = A4
    margin = 52
    usable_width = page_width - (margin * 2)
    bottom_margin = 48

    pdf = canvas.Canvas(str(target), pagesize=A4)
    pdf.setTitle("审阅报告")

    y = page_height - margin

    def ensure_space(required_height: float) -> None:
        nonlocal y
        if y - required_height < bottom_margin:
            pdf.showPage()
            y = page_height - margin

    def draw_line(text: str, *, font_size: int, leading: float) -> None:
        nonlocal y
        wrapped = _wrap_text(
            text,
            font_name=font_name,
            font_size=font_size,
            max_width=usable_width,
        )
        ensure_space(leading * len(wrapped))
        pdf.setFont(font_name, font_size)
        for line in wrapped:
            pdf.drawString(margin, y, line)
            y -= leading

    for raw_line in markdown.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            y -= 8
            ensure_space(0)
            continue

        if stripped.startswith("# "):
            draw_line(stripped[2:], font_size=20, leading=28)
            y -= 4
            continue

        if stripped.startswith("## "):
            draw_line(stripped[3:], font_size=14, leading=20)
            y -= 2
            continue

        draw_line(stripped, font_size=11, leading=16)

    pdf.save()
    return target
