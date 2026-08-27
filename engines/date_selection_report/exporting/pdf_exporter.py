"""Date Selection PDF exporter. Reuses PACK 05 Playwright print backend."""

from __future__ import annotations

import logging
from pathlib import Path

from engines.date_selection_report.exceptions import DateSelectionReportExportError
from engines.date_selection_report.exporting.filename import build_pdf_filename
from engines.date_selection_report.exporting.html_projection import (
    PDF_AUTHOR,
    PDF_DOCUMENT_TITLE,
    PDF_SUBJECT,
    project_render_tree_to_html,
)
from engines.date_selection_report.rendering.nodes import DateSelectionRenderTree
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


class DateSelectionPdfExporter:
    """Export one RenderTree through PACK 05 PlaywrightPdfBackend."""

    def __init__(self, *, backend: PdfBackend | None = None) -> None:
        self._backend = backend or PlaywrightPdfBackend()

    def export(
        self,
        tree: DateSelectionRenderTree,
        output_path: Path,
    ) -> ReportExportResultV1:
        """Write a PDF beside output_path, using the canonical filename when needed."""
        _require_tree(tree)
        html = project_render_tree_to_html(tree)
        target = _resolve_pdf_path(tree, output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        page_count = self._backend.html_to_pdf(html, target, title=PDF_DOCUMENT_TITLE)
        validate_pdf_file(target)
        page_count = _ensure_page_count(target, page_count)
        logger.info(
            "date_selection_pdf report_id=%s path=%s size=%s",
            tree.header.report_id,
            target,
            target.stat().st_size,
        )
        return ReportExportResultV1(
            format=EXPORT_FORMAT_PDF,
            file_path=str(target.resolve()),
            file_name=target.name,
            media_type=MEDIA_TYPE_PDF,
            size_bytes=target.stat().st_size,
            report_version=tree.footer.report_version,
            case_id=tree.header.report_id,
            generated_at=tree.header.generated_at,
            page_count=page_count,
        )


def export_pdf(tree: DateSelectionRenderTree, output_path: Path) -> ReportExportResultV1:
    """Module-level PDF export helper."""
    return DateSelectionPdfExporter().export(tree, output_path)


def _require_tree(tree: DateSelectionRenderTree) -> None:
    if tree is None:
        raise DateSelectionReportExportError("RenderTree is required")
    if not tree.header.title:
        raise DateSelectionReportExportError("missing header")
    if not tree.person.rows:
        raise DateSelectionReportExportError("missing person")
    if not tree.recommendations and tree.empty_state is None:
        raise DateSelectionReportExportError("missing recommendations")


def _resolve_pdf_path(tree: DateSelectionRenderTree, output_path: Path) -> Path:
    if output_path.suffix.lower() == ".pdf":
        return output_path
    return output_path / build_pdf_filename(tree)


def _ensure_page_count(path: Path, reported: int | None) -> int:
    if reported is not None and reported > 0:
        return reported
    data = path.read_bytes()
    pages = data.count(b"/Type /Page") - data.count(b"/Type /Pages")
    return max(pages, 1)


def pdf_document_identity() -> dict[str, str]:
    """Canonical PDF Info values for Title / Author / Subject."""
    return {
        "title": PDF_DOCUMENT_TITLE,
        "author": PDF_AUTHOR,
        "subject": PDF_SUBJECT,
    }
