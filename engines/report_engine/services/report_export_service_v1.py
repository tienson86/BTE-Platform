"""Report Export Service V1 — unified PDF/DOCX export orchestration."""

from __future__ import annotations

import logging
from pathlib import Path

from engines.report_engine.contracts.report_export_result_v1 import (
    EXPORT_FORMAT_DOCX,
    EXPORT_FORMAT_PDF,
    ReportExportResultV1,
)
from engines.report_engine.contracts.report_input_v1 import ReportInputV1
from engines.report_engine.exporting.docx_exporter_v1 import DocxExporterV1
from engines.report_engine.exporting.filename import build_export_filename
from engines.report_engine.exporting.pdf_exporter_v1 import PdfExporterV1

logger = logging.getLogger(__name__)

DEFAULT_EXPORT_ROOT = Path("knowledge/report_v1_validation/exports")


class ReportExportServiceV1:
    """Validate ReportInputV1 and route to PDF/DOCX exporters."""

    def __init__(
        self,
        *,
        export_root: Path | None = None,
        pdf_exporter: PdfExporterV1 | None = None,
        docx_exporter: DocxExporterV1 | None = None,
    ) -> None:
        self._export_root = export_root or DEFAULT_EXPORT_ROOT
        self._pdf_exporter = pdf_exporter or PdfExporterV1()
        self._docx_exporter = docx_exporter or DocxExporterV1()

    def export_pdf(
        self,
        report_input: ReportInputV1,
        output_path: Path | None = None,
    ) -> ReportExportResultV1:
        """Export PDF; default path under export_root when output_path omitted."""
        self._validate_report_input(report_input)
        target = output_path or self._default_path(report_input, EXPORT_FORMAT_PDF)
        return self._pdf_exporter.export(report_input, target)

    def export_docx(
        self,
        report_input: ReportInputV1,
        output_path: Path | None = None,
    ) -> ReportExportResultV1:
        """Export DOCX; default path under export_root when output_path omitted."""
        self._validate_report_input(report_input)
        target = output_path or self._default_path(report_input, EXPORT_FORMAT_DOCX)
        return self._docx_exporter.export(report_input, target)

    def _default_path(self, report_input: ReportInputV1, fmt: str) -> Path:
        filename = build_export_filename(report_input, fmt)
        return self._export_root / filename

    def _validate_report_input(self, report_input: ReportInputV1) -> None:
        if report_input is None:
            raise ValueError("ReportInputV1 is required.")
        if not report_input.metadata.case_id:
            logger.warning("report_export_missing_case_id")
        if not report_input.profile.full_name:
            logger.warning("report_export_missing_profile_name")
