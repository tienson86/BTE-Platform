"""Date Selection report export from a displayed SearchResult.

Does not rerun Date Selection or recompute recommendations.
"""

from __future__ import annotations

import logging
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from applications.api.exceptions import CustomerExportError
from engines.date_selection_report import (
    DateSelectionReportAdapter,
    build_render_tree,
    create_render_context,
    export_docx,
    export_pdf,
)
from engines.date_selection_report.exceptions import (
    DateSelectionReportError,
    DateSelectionReportValidationError,
)
from engines.report_engine.contracts.report_export_result_v1 import (
    MEDIA_TYPE_DOCX,
    MEDIA_TYPE_PDF,
    ReportExportResultV1,
)

logger = logging.getLogger(__name__)

ExportFormat = Literal["pdf", "docx"]

EXPORT_FAILED_MESSAGE = "Không tạo được báo cáo. Vui lòng thử lại."
MISSING_RESULT_MESSAGE = "Không có kết quả để xuất báo cáo."
NO_RECOMMENDATIONS_MESSAGE = "Không có ngày đề xuất để xuất báo cáo."

_EXPORT_ROOT = Path(tempfile.gettempdir()) / "bte_date_selection_report"
_MEDIA_TYPES: dict[str, str] = {
    "pdf": MEDIA_TYPE_PDF,
    "docx": MEDIA_TYPE_DOCX,
}


@dataclass(frozen=True, slots=True)
class DisplayedSearchResult:
    """Portal snapshot of the SearchResult currently on screen."""

    payload: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Return the displayed payload unchanged."""
        return self.payload


def export_displayed_search_result(
    search_result: dict[str, Any] | None,
    fmt: ExportFormat,
) -> tuple[Path, str, str, ReportExportResultV1]:
    """Adapt the displayed SearchResult and render PDF or DOCX."""
    payload = _require_payload(search_result)
    _require_recommendations(payload)
    try:
        model = DateSelectionReportAdapter().adapt(DisplayedSearchResult(payload))
        tree = build_render_tree(create_render_context(model))
    except DateSelectionReportValidationError:
        logger.info("date_selection_report_export_invalid format=%s", fmt)
        raise CustomerExportError(
            NO_RECOMMENDATIONS_MESSAGE,
            status_code=400,
            code="export_invalid_search_result",
        ) from None
    except DateSelectionReportError:
        logger.exception("date_selection_report_export_adapt_failed format=%s", fmt)
        raise CustomerExportError(
            EXPORT_FAILED_MESSAGE,
            status_code=500,
            code="export_adapt_failed",
        ) from None
    _EXPORT_ROOT.mkdir(parents=True, exist_ok=True)
    token = uuid.uuid4().hex[:12]
    output_dir = _EXPORT_ROOT / token
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        if fmt == "pdf":
            result = export_pdf(tree, output_dir)
        elif fmt == "docx":
            result = export_docx(tree, output_dir)
        else:
            raise CustomerExportError(EXPORT_FAILED_MESSAGE, code="export_unsupported_format")
    except CustomerExportError:
        _cleanup(output_dir)
        raise
    except DateSelectionReportError:
        logger.exception("date_selection_report_export_renderer_failed format=%s", fmt)
        _cleanup(output_dir)
        raise CustomerExportError(
            EXPORT_FAILED_MESSAGE,
            status_code=500,
            code="export_renderer_failed",
        ) from None
    except Exception:
        logger.exception("date_selection_report_export_unhandled format=%s", fmt)
        _cleanup(output_dir)
        raise CustomerExportError(
            EXPORT_FAILED_MESSAGE,
            status_code=500,
            code="export_renderer_failed",
        ) from None
    path = Path(result.file_path)
    if not path.is_file() or path.stat().st_size == 0:
        _cleanup(path)
        raise CustomerExportError(
            EXPORT_FAILED_MESSAGE,
            status_code=500,
            code="export_empty_file",
        )
    logger.info(
        "date_selection_report_export format=%s report_id=%s file=%s",
        fmt,
        result.case_id,
        result.file_name,
    )
    return path, result.file_name, _MEDIA_TYPES[fmt], result


def cleanup_date_selection_export(path: Path | str | None) -> None:
    """Delete a temporary Date Selection export file."""
    _cleanup(path)


def _require_payload(search_result: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(search_result, dict) or not search_result:
        raise CustomerExportError(
            MISSING_RESULT_MESSAGE,
            status_code=400,
            code="export_missing_search_result",
        )
    return search_result


def _require_recommendations(payload: dict[str, Any]) -> None:
    dates = payload.get("dates")
    if not isinstance(dates, list) or not dates:
        raise CustomerExportError(
            NO_RECOMMENDATIONS_MESSAGE,
            status_code=400,
            code="export_no_recommendations",
        )


def _cleanup(path: Path | str | None) -> None:
    if not path:
        return
    target = Path(path)
    try:
        if target.is_file():
            target.unlink()
        elif target.is_dir():
            for child in target.iterdir():
                if child.is_file():
                    child.unlink()
            target.rmdir()
    except OSError:
        logger.warning("date_selection_report_export_cleanup_failed")
