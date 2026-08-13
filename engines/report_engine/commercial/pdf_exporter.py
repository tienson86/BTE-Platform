"""PDF export for Commercial Report V2."""

from __future__ import annotations

import logging
from pathlib import Path

from engines.report_engine.commercial.html_renderer import CommercialHtmlRenderer
from engines.report_engine.commercial.models import CommercialReport
from engines.report_engine.contracts.report_export_result_v1 import (
    EXPORT_FORMAT_PDF,
    MEDIA_TYPE_PDF,
    ReportExportResultV1,
)
from engines.report_engine.exporting.pdf_exporter_v1 import (
    PdfBackend,
    PlaywrightPdfBackend,
    validate_pdf_file,
)

logger = logging.getLogger(__name__)


class CommercialPdfExporter:
    """Export CommercialReport to PDF via HTML print."""

    def __init__(
        self,
        *,
        html_renderer: CommercialHtmlRenderer | None = None,
        backend: PdfBackend | None = None,
    ) -> None:
        self._html_renderer = html_renderer or CommercialHtmlRenderer()
        self._backend = backend or PlaywrightPdfBackend()

    def export(
        self,
        report: CommercialReport,
        output_path: Path,
    ) -> ReportExportResultV1:
        """Render commercial HTML and write PDF."""
        html = self._html_renderer.render(report)
        html_path = output_path.with_suffix(".html")
        html_path.parent.mkdir(parents=True, exist_ok=True)
        html_path.write_text(html, encoding="utf-8")
        title = report.cover.heading
        if report.cover.client_name:
            title = f"{report.cover.heading} — {report.cover.client_name}"
        page_count = self._backend.html_to_pdf(html, output_path, title=title)
        validate_pdf_file(output_path)
        logger.info(
            "commercial_report_pdf case_id=%s path=%s size=%s",
            report.cover.case_id,
            output_path,
            output_path.stat().st_size,
        )
        return ReportExportResultV1(
            format=EXPORT_FORMAT_PDF,
            file_path=str(output_path.resolve()),
            file_name=output_path.name,
            media_type=MEDIA_TYPE_PDF,
            size_bytes=output_path.stat().st_size,
            report_version=report.version,
            case_id=report.cover.case_id,
            generated_at="",
            page_count=page_count,
        )
