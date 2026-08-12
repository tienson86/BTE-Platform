"""Tests for DocxExporterV1."""

from __future__ import annotations

from pathlib import Path

import pytest
from docx import Document

from engines.report_engine.contracts.report_export_result_v1 import MEDIA_TYPE_DOCX
from engines.report_engine.contracts.report_input_v1 import (
    ReportInputV1,
    ReportInterpretationSectionV1,
    ReportInterpretationV1,
    ReportMetadataV1,
    ReportProfileV1,
)
from engines.report_engine.exporting.docx_exporter_v1 import (
    DocxExporterV1,
    validate_docx_file,
)


def _sample_input() -> ReportInputV1:
    return ReportInputV1(
        metadata=ReportMetadataV1(case_id="CASE-TEST", report_version="1.0"),
        profile=ReportProfileV1(
            full_name="Nguyễn Tiến Sơn",
            gender="male",
            birth_date="1987-01-21",
            birth_time="04:30",
            birth_place="Hà Tây, Việt Nam",
        ),
        interpretation=ReportInterpretationV1(
            executive_summary="Tổng quan luận giải.",
            sections=[
                ReportInterpretationSectionV1(
                    id="career",
                    title="Sự nghiệp",
                    content="Phù hợp quản lý.",
                )
            ],
        ),
    )


def _document_text(path: Path) -> str:
    document = Document(str(path))
    return "\n".join(paragraph.text for paragraph in document.paragraphs)


def test_docx_exporter_creates_valid_file(tmp_path: Path) -> None:
    """DOCX exporter creates reopenable OpenXML file."""
    output = tmp_path / "sample.docx"
    result = DocxExporterV1().export(_sample_input(), output)
    validate_docx_file(output)
    assert result.media_type == MEDIA_TYPE_DOCX
    assert result.format == "docx"


def test_docx_vietnamese_text_preserved(tmp_path: Path) -> None:
    """Vietnamese diacritics survive DOCX round-trip."""
    output = tmp_path / "vietnamese.docx"
    DocxExporterV1().export(_sample_input(), output)
    text = _document_text(output)
    assert "Nguyễn Tiến Sơn" in text
    assert "BÁO CÁO LUẬN GIẢI BÁT TỰ" in text
    assert "04. Thân vượng nhược" in text
    assert "07. Dụng thần – Hỷ thần – Kỵ thần" in text


def test_docx_required_headings_present(tmp_path: Path) -> None:
    """Required section headings exist in DOCX."""
    output = tmp_path / "headings.docx"
    DocxExporterV1().export(_sample_input(), output)
    text = _document_text(output)
    for heading in (
        "01. Thông tin lá số",
        "02. Tứ Trụ",
        "10. Luận giải tổng thể",
        "11. Nghề nghiệp",
        "17. Tổng kết",
    ):
        assert heading in text


def test_docx_missing_data_does_not_crash(tmp_path: Path) -> None:
    """Sparse ReportInputV1 still exports."""
    sparse = ReportInputV1(
        metadata=ReportMetadataV1(case_id="CASE-SPARSE"),
        profile=ReportProfileV1(),
    )
    output = tmp_path / "sparse.docx"
    DocxExporterV1().export(sparse, output)
    validate_docx_file(output)


def test_validate_docx_rejects_invalid(tmp_path: Path) -> None:
    """Invalid DOCX zip raises."""
    bad = tmp_path / "bad.docx"
    bad.write_bytes(b"not-a-zip")
    with pytest.raises(ValueError, match="Invalid DOCX zip"):
        validate_docx_file(bad)
