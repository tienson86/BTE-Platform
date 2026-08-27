"""PACK 06 Date Selection PDF export (P6-03). Reuses PACK 05 Playwright PDF."""

from engines.date_selection_report.exporting.filename import build_pdf_filename
from engines.date_selection_report.exporting.html_projection import (
    PDF_AUTHOR,
    PDF_DOCUMENT_TITLE,
    PDF_SUBJECT,
    project_render_tree_to_html,
)
from engines.date_selection_report.exporting.pdf_exporter import (
    DateSelectionPdfExporter,
    export_pdf,
    pdf_document_identity,
)

__all__ = [
    "DateSelectionPdfExporter",
    "PDF_AUTHOR",
    "PDF_DOCUMENT_TITLE",
    "PDF_SUBJECT",
    "build_pdf_filename",
    "export_pdf",
    "pdf_document_identity",
    "project_render_tree_to_html",
]
