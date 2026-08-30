"""Presentation Export Layer — shadow consumers only.

Portal / PDF / DOCX / JSON render NarrativeV2Presentation.
None of them compose or rewrite Narrative.
"""

from __future__ import annotations

from engines.narrative_v2.export.docx_export import DocxExport, export_docx, extract_docx_paragraphs
from engines.narrative_v2.export.export_builder import build_export_context
from engines.narrative_v2.export.export_context import ExportBlock, ExportContext
from engines.narrative_v2.export.export_errors import (
    ExportError,
    ExportValidationError,
    IncompatiblePresentationVersion,
)
from engines.narrative_v2.export.export_registry import (
    CONSUMERS,
    ExportBundle,
    PresentationExportLayer,
)
from engines.narrative_v2.export.export_serializer import (
    presentation_from_mapping,
    serialize_presentation,
)
from engines.narrative_v2.export.export_validator import ExportValidator
from engines.narrative_v2.export.json_export import JsonExport, export_json
from engines.narrative_v2.export.pdf_export import PdfExport, export_pdf, extract_html_texts, render_export_html
from engines.narrative_v2.export.portal_export import PortalExport, export_portal

__all__ = [
    "CONSUMERS",
    "DocxExport",
    "ExportBlock",
    "ExportBundle",
    "ExportContext",
    "ExportError",
    "ExportValidationError",
    "ExportValidator",
    "IncompatiblePresentationVersion",
    "JsonExport",
    "PdfExport",
    "PortalExport",
    "PresentationExportLayer",
    "build_export_context",
    "export_docx",
    "export_json",
    "export_pdf",
    "export_portal",
    "extract_docx_paragraphs",
    "extract_html_texts",
    "presentation_from_mapping",
    "render_export_html",
    "serialize_presentation",
]
