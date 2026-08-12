"""Export filename helpers for Report V1."""

from __future__ import annotations

import re
import unicodedata

from engines.report_engine.contracts.report_input_v1 import REPORT_INPUT_VERSION, ReportInputV1

_UNSAFE_FILENAME = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def ascii_slug(text: str) -> str:
    """Strip diacritics and unsafe characters for cross-platform filenames."""
    normalized = unicodedata.normalize("NFKD", text)
    without_marks = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    cleaned = _UNSAFE_FILENAME.sub("", without_marks)
    cleaned = re.sub(r"\s+", "_", cleaned.strip())
    cleaned = re.sub(r"_+", "_", cleaned)
    return cleaned or "Report"


def build_export_filename(report_input: ReportInputV1, fmt: str) -> str:
    """Build deterministic export filename for PDF or DOCX."""
    case_id = (report_input.metadata.case_id or "CASE-UNKNOWN").strip()
    name_slug = ascii_slug(report_input.profile.full_name or "Report")
    version = (report_input.metadata.report_version or REPORT_INPUT_VERSION).replace(
        ".",
        "_",
    )
    extension = fmt.lower().lstrip(".")
    return f"BTE_{case_id}_{name_slug}_Report_V{version}.{extension}"


def build_pdf_title(report_input: ReportInputV1) -> str:
    """PDF document title from profile metadata."""
    name = report_input.profile.full_name.strip()
    if name:
        return f"Báo cáo luận giải Bát Tự — {name}"
    return "Báo cáo luận giải Bát Tự"
