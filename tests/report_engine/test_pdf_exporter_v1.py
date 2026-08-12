"""Tests for PdfExporterV1."""

from __future__ import annotations

from pathlib import Path

import pytest

from engines.report_engine.contracts.report_export_result_v1 import MEDIA_TYPE_PDF
from engines.report_engine.contracts.report_input_v1 import (
    ReportInputV1,
    ReportMetadataV1,
    ReportProfileV1,
)
from engines.report_engine.exporting.pdf_exporter_v1 import (
    MIN_PDF_BYTES,
    PdfExporterV1,
    PlaywrightPdfBackend,
    validate_pdf_file,
)


class _FakePdfBackend:
    """Fast PDF backend for unit tests."""

    def html_to_pdf(self, html: str, output_path: Path, *, title: str) -> int | None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        payload = b"%PDF-1.4\n" + html.encode("utf-8") + b"\n%%EOF\n"
        if len(payload) < MIN_PDF_BYTES:
            payload += b"0" * (MIN_PDF_BYTES - len(payload))
        output_path.write_bytes(payload)
        return 1


def _sample_input() -> ReportInputV1:
    return ReportInputV1(
        metadata=ReportMetadataV1(case_id="CASE-TEST", report_version="1.0"),
        profile=ReportProfileV1(
            full_name="Nguyễn Tiến Sơn",
            gender="male",
            birth_date="1987-01-21",
        ),
    )


def test_pdf_exporter_creates_valid_file(tmp_path: Path) -> None:
    """PDF exporter writes a file with PDF signature."""
    output = tmp_path / "sample.pdf"
    result = PdfExporterV1(backend=_FakePdfBackend()).export(_sample_input(), output)
    validate_pdf_file(output)
    assert result.media_type == MEDIA_TYPE_PDF
    assert result.size_bytes == output.stat().st_size
    assert result.case_id == "CASE-TEST"


def test_pdf_exporter_unicode_html_path(tmp_path: Path) -> None:
    """Renderer HTML path preserves Vietnamese before PDF write."""
    captured: dict[str, str] = {}

    class _CaptureBackend(_FakePdfBackend):
        def html_to_pdf(self, html: str, output_path: Path, *, title: str) -> int | None:
            captured["html"] = html
            captured["title"] = title
            return super().html_to_pdf(html, output_path, title=title)

    output = tmp_path / "unicode.pdf"
    PdfExporterV1(backend=_CaptureBackend()).export(_sample_input(), output)
    assert "Nguyễn Tiến Sơn" in captured["html"]
    assert "Bát Tự" in captured["html"]
    assert "Nguyễn Tiến Sơn" in captured["title"]


def test_validate_pdf_file_rejects_invalid(tmp_path: Path) -> None:
    """Invalid PDF signature raises."""
    bad = tmp_path / "bad.pdf"
    bad.write_bytes(b"NOTPDF")
    with pytest.raises(ValueError, match="Invalid PDF signature"):
        validate_pdf_file(bad)


def test_playwright_backend_importable() -> None:
    """Playwright backend is available for integration tests."""
    from playwright.sync_api import sync_playwright

    assert sync_playwright is not None
    assert PlaywrightPdfBackend is not None
