"""PACK 06 Date Selection report contracts.

Reuses PACK 05 foundation identity. Does not duplicate Report Engine.
"""

from __future__ import annotations

from typing import Any, Protocol

from engines.date_selection_report.constants import (
    GENERATOR,
    LOCALE,
    PACK05_REPORT_VERSION,
    REPORT_CONTRACT_ID,
    REPORT_SCHEMA_VERSION,
    REPORT_TYPE,
    TITLE,
)


class CanonicalSearchResult(Protocol):
    """Minimal SearchResult surface consumed by the report adapter."""

    target_year: int
    target_month: int

    def to_dict(self) -> dict[str, Any]:
        """Serialize canonical Date Selection output."""


REPORT_FOUNDATION_CONTRACT: dict[str, str] = {
    "pack": "06",
    "report_type": REPORT_TYPE,
    "schema_version": REPORT_SCHEMA_VERSION,
    "locale": LOCALE,
    "title": TITLE,
    "generator": GENERATOR,
    "pack_05_contract_id": REPORT_CONTRACT_ID,
    "pack_05_report_version": PACK05_REPORT_VERSION,
}

RENDER_CONTRACT: dict[str, str] = {
    "input": "DateSelectionReportModel",
    "output": "DateSelectionRenderTree",
    "template_id": "date_selection_report",
    "pack_05_theme_id": "bte.report.theme.v1",
    "pack_05_placeholder_model": "PlaceholderModel",
}

EXPORT_CONTRACT: dict[str, str] = {
    "input": "DateSelectionRenderTree",
    "pdf_exporter": "DateSelectionPdfExporter",
    "docx_exporter": "DateSelectionDocxExporter",
    "pack_05_backend": "PlaywrightPdfBackend",
    "pack_05_docx_exporter": "DocxExporterV1",
    "pack_05_template": "templates/v1/report_v1.html",
    "pack_05_css": "templates/v1/report_v1.css",
}
