"""Tests for export filename helpers."""

from __future__ import annotations

from engines.report_engine.contracts.report_input_v1 import (
    ReportInputV1,
    ReportMetadataV1,
    ReportProfileV1,
)
from engines.report_engine.exporting.filename import (
    ascii_slug,
    build_export_filename,
    build_pdf_title,
)


def test_ascii_slug_strips_diacritics() -> None:
    """Filename slug removes Vietnamese diacritics."""
    assert ascii_slug("Nguyễn Tiến Sơn") == "Nguyen_Tien_Son"


def test_build_export_filename_deterministic() -> None:
    """Export filename is deterministic and safe."""
    report_input = ReportInputV1(
        metadata=ReportMetadataV1(case_id="CASE-0001", report_version="1.0"),
        profile=ReportProfileV1(full_name="Nguyễn Tiến Sơn"),
    )
    assert (
        build_export_filename(report_input, "pdf")
        == "BTE_CASE-0001_Nguyen_Tien_Son_Report_V1_0.pdf"
    )


def test_build_pdf_title_from_profile() -> None:
    """PDF title uses profile full name."""
    report_input = ReportInputV1(
        profile=ReportProfileV1(full_name="Nguyễn Tiến Sơn"),
    )
    assert build_pdf_title(report_input) == "Báo cáo luận giải Bát Tự — Nguyễn Tiến Sơn"
