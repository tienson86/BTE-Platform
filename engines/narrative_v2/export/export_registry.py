"""Presentation Export Layer facade and consumer registry. Shadow only."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from engines.narrative_v2.presentation.presentation_model import NarrativeV2Presentation

from engines.narrative_v2.export.docx_export import DocxExport, export_docx
from engines.narrative_v2.export.export_builder import build_export_context
from engines.narrative_v2.export.export_context import ExportContext
from engines.narrative_v2.export.export_validator import ExportValidator
from engines.narrative_v2.export.json_export import JsonExport, export_json
from engines.narrative_v2.export.pdf_export import PdfExport, export_pdf, extract_html_texts
from engines.narrative_v2.export.portal_export import PortalExport, export_portal

CONSUMERS: tuple[str, ...] = ("portal", "pdf", "docx", "json")


@dataclass(frozen=True, slots=True)
class ExportBundle:
    """All shadow consumers from one Presentation."""

    context: ExportContext
    portal: PortalExport
    json: JsonExport
    pdf: PdfExport
    docx: DocxExport


class PresentationExportLayer:
    """Only component allowed to expose Presentation to external consumers."""

    def __init__(self, *, validator: ExportValidator | None = None) -> None:
        self._validator = validator or ExportValidator()

    def prepare(self, presentation: NarrativeV2Presentation) -> ExportContext:
        """Validate and freeze the shared export context."""
        context = build_export_context(presentation)
        self._validator.validate_context(context)
        return context

    def export_portal(self, presentation: NarrativeV2Presentation) -> PortalExport:
        """Shadow Portal payload."""
        return export_portal(self.prepare(presentation))

    def export_json(self, presentation: NarrativeV2Presentation) -> JsonExport:
        """Canonical JSON. Equals Presentation."""
        return export_json(self.prepare(presentation))

    def export_pdf(self, presentation: NarrativeV2Presentation, output_path: Path) -> PdfExport:
        """Shadow PDF file."""
        return export_pdf(self.prepare(presentation), output_path)

    def export_docx(self, presentation: NarrativeV2Presentation, output_path: Path) -> DocxExport:
        """Shadow DOCX file."""
        return export_docx(self.prepare(presentation), output_path)

    def export_all(
        self,
        presentation: NarrativeV2Presentation,
        *,
        pdf_path: Path,
        docx_path: Path,
    ) -> ExportBundle:
        """Build Portal, JSON, PDF, and DOCX from the same blocks."""
        context = self.prepare(presentation)
        portal = export_portal(context)
        json_export = export_json(context)
        pdf = export_pdf(context, pdf_path)
        docx = export_docx(context, docx_path)
        texts = tuple(block.text for block in context.blocks)
        self._validator.assert_same_narrative(
            texts, tuple(block.text for block in portal.blocks), label="portal"
        )
        self._validator.assert_same_narrative(
            texts, tuple(block.text for block in json_export.blocks), label="json"
        )
        self._validator.assert_same_narrative(texts, extract_html_texts(pdf.html), label="pdf")
        self._validator.assert_same_narrative(texts, docx.paragraphs, label="docx")
        return ExportBundle(
            context=context,
            portal=portal,
            json=json_export,
            pdf=pdf,
            docx=docx,
        )
