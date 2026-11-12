"""PDF Export V1 — HTML Report V1 via Playwright Chromium print-to-PDF."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Protocol

from engines.report_engine.contracts.report_export_result_v1 import (
    EXPORT_FORMAT_PDF,
    MEDIA_TYPE_PDF,
    ReportExportResultV1,
)
from engines.report_engine.contracts.report_input_v1 import ReportInputV1
from engines.report_engine.exporting.filename import build_export_filename, build_pdf_title
from engines.report_engine.rendering.html_report_v1 import HtmlReportV1Renderer

logger = logging.getLogger(__name__)

PDF_SIGNATURE = b"%PDF"
MIN_PDF_BYTES = 1024


class PdfBackend(Protocol):
    """Protocol for HTML → PDF backends (Playwright default)."""

    def html_to_pdf(self, html: str, output_path: Path, *, title: str) -> int | None:
        """Write PDF bytes to output_path; return page count if known."""


class PlaywrightPdfBackend:
    """Chromium headless print-to-PDF backend."""

    def html_to_pdf(self, html: str, output_path: Path, *, title: str) -> int | None:
        """Render HTML to PDF using Playwright Chromium."""
        from playwright.sync_api import sync_playwright

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            try:
                page = browser.new_page()
                page.set_content(html, wait_until="networkidle")
                page.emulate_media(media="print")
                page.pdf(
                    path=str(output_path),
                    format="A4",
                    print_background=True,
                    display_header_footer=True,
                    header_template="<div></div>",
                    footer_template=(
                        '<div style="font-size:9px;width:100%;padding:0 16mm;color:#555;'
                        "font-family:Arial,'Segoe UI',sans-serif;display:flex;"
                        'justify-content:space-between;">'
                        "<span>BTE V1.0</span>"
                        '<span><span class="pageNumber"></span> / '
                        '<span class="totalPages"></span></span>'
                        "</div>"
                    ),
                    margin={
                        "top": "16mm",
                        "right": "16mm",
                        "bottom": "20mm",
                        "left": "16mm",
                    },
                    tagged=True,
                )
            finally:
                browser.close()
        return _estimate_page_count(output_path)


def _estimate_page_count(output_path: Path) -> int | None:
    """Estimate page count from PDF /Count if present."""
    try:
        data = output_path.read_bytes()
        text = data.decode("latin-1", errors="ignore")
        for token in ("/Count ", "/N "):
            index = text.rfind(token)
            if index == -1:
                continue
            fragment = text[index + len(token) : index + len(token) + 6]
            digits = "".join(ch for ch in fragment if ch.isdigit())
            if digits:
                return int(digits)
    except OSError:
        return None
    return None


def validate_pdf_file(output_path: Path) -> None:
    """Validate exported PDF file basics."""
    if not output_path.is_file():
        raise FileNotFoundError(f"PDF not created: {output_path}")
    signature = output_path.read_bytes()[:4]
    if signature != PDF_SIGNATURE:
        raise ValueError(f"Invalid PDF signature: {signature!r}")
    size = output_path.stat().st_size
    if size < MIN_PDF_BYTES:
        raise ValueError(f"PDF too small ({size} bytes): {output_path}")


class PdfExporterV1:
    """Export ReportInputV1 to PDF via HTML Report V1."""

    def __init__(
        self,
        *,
        html_renderer: HtmlReportV1Renderer | None = None,
        backend: PdfBackend | None = None,
    ) -> None:
        self._html_renderer = html_renderer or HtmlReportV1Renderer()
        self._backend = backend or PlaywrightPdfBackend()

    def export(
        self,
        report_input: ReportInputV1,
        output_path: Path,
    ) -> ReportExportResultV1:
        """Render HTML and export PDF to output_path."""
        html = self._html_renderer.render(report_input)
        title = build_pdf_title(report_input)
        page_count = self._backend.html_to_pdf(html, output_path, title=title)
        validate_pdf_file(output_path)
        logger.info(
            "report_export_pdf case_id=%s path=%s size=%s",
            report_input.metadata.case_id,
            output_path,
            output_path.stat().st_size,
        )
        return ReportExportResultV1(
            format=EXPORT_FORMAT_PDF,
            file_path=str(output_path.resolve()),
            file_name=output_path.name,
            media_type=MEDIA_TYPE_PDF,
            size_bytes=output_path.stat().st_size,
            report_version=report_input.metadata.report_version,
            case_id=report_input.metadata.case_id,
            generated_at=report_input.metadata.generated_at,
            page_count=page_count,
        )


def export_pdf(report_input: ReportInputV1, output_path: Path) -> ReportExportResultV1:
    """Module-level PDF export helper."""
    return PdfExporterV1().export(report_input, output_path)
