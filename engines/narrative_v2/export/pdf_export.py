"""Shadow PDF export. Presentation blocks only. No Report Builder."""

from __future__ import annotations

import html
from dataclasses import dataclass
from pathlib import Path

from engines.narrative_v2.export.export_context import ExportBlock, ExportContext

PDF_SIGNATURE = b"%PDF"
MIN_PDF_BYTES = 512


@dataclass(frozen=True, slots=True)
class PdfExport:
    """Shadow PDF bytes plus the HTML used to print them."""

    version: str
    status: str
    blocks: tuple[ExportBlock, ...]
    html: str
    pdf_bytes: bytes
    path: str | None


def export_pdf(context: ExportContext, output_path: Path | None = None) -> PdfExport:
    """Render Presentation blocks to a shadow PDF. No new sentences."""
    markup = render_export_html(context)
    target = output_path
    if target is None:
        raise TypeError("output_path is required for PDF export")
    _print_pdf(markup, target)
    data = target.read_bytes()
    if data[:4] != PDF_SIGNATURE or len(data) < MIN_PDF_BYTES:
        raise ValueError("invalid shadow PDF")
    return PdfExport(
        version=context.version,
        status=context.status,
        blocks=context.blocks,
        html=markup,
        pdf_bytes=data,
        path=str(target.resolve()),
    )


def render_export_html(context: ExportContext) -> str:
    """HTML whose visible text is exactly the Presentation blocks."""
    paragraphs = "\n".join(
        f'<p data-field="{html.escape(block.field)}">{html.escape(block.text)}</p>'
        for block in context.blocks
    )
    return (
        "<!DOCTYPE html><html lang=\""
        + html.escape(context.language)
        + "\"><head><meta charset=\"utf-8\"/>"
        "<title>"
        + html.escape(context.version)
        + "</title>"
        "<style>body{font-family:Arial,sans-serif;font-size:12pt;line-height:1.5;"
        "margin:24px;color:#1c1c1c}p{margin:0 0 12px}</style></head>"
        f'<body data-export="narrative-v2-shadow" data-version="{html.escape(context.version)}" '
        f'data-status="{html.escape(context.status)}" data-replaces-pack05="false">'
        f"{paragraphs}</body></html>"
    )


def extract_html_texts(markup: str) -> tuple[str, ...]:
    """Visible paragraph texts from export HTML. Formatting ignored."""
    texts: list[str] = []
    start = 0
    token = "<p "
    while True:
        index = markup.find(token, start)
        if index < 0:
            break
        open_end = markup.find(">", index)
        close = markup.find("</p>", open_end)
        if open_end < 0 or close < 0:
            break
        raw = markup[open_end + 1 : close]
        texts.append(html.unescape(raw))
        start = close + 4
    return tuple(texts)


def _print_pdf(markup: str, output_path: Path) -> None:
    from playwright.sync_api import sync_playwright

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page()
            page.set_content(markup, wait_until="networkidle")
            page.emulate_media(media="print")
            page.pdf(
                path=str(output_path),
                format="A4",
                print_background=True,
                margin={"top": "16mm", "right": "16mm", "bottom": "16mm", "left": "16mm"},
            )
        finally:
            browser.close()
