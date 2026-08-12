"""Tests for ReportExportServiceV1."""

from __future__ import annotations

from pathlib import Path

from engines.report_engine.contracts.report_export_result_v1 import (
    MEDIA_TYPE_DOCX,
    MEDIA_TYPE_PDF,
)
from engines.report_engine.contracts.report_input_v1 import (
    ReportInputV1,
    ReportMetadataV1,
    ReportProfileV1,
)
from engines.report_engine.exporting.filename import build_export_filename
from engines.report_engine.services.report_export_service_v1 import ReportExportServiceV1


class _FakePdfExporter:
    def export(self, report_input: ReportInputV1, output_path: Path):
        from engines.report_engine.contracts.report_export_result_v1 import (
            EXPORT_FORMAT_PDF,
            ReportExportResultV1,
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(b"%PDF-1.4\n" + b"x" * 1200)
        return ReportExportResultV1(
            format=EXPORT_FORMAT_PDF,
            file_path=str(output_path),
            file_name=output_path.name,
            media_type=MEDIA_TYPE_PDF,
            size_bytes=output_path.stat().st_size,
            report_version=report_input.metadata.report_version,
            case_id=report_input.metadata.case_id,
            generated_at=report_input.metadata.generated_at,
            page_count=1,
        )


class _FakeDocxExporter:
    def export(self, report_input: ReportInputV1, output_path: Path):
        from engines.report_engine.contracts.report_export_result_v1 import (
            EXPORT_FORMAT_DOCX,
            ReportExportResultV1,
        )
        from engines.report_engine.exporting.docx_exporter_v1 import DocxExporterV1

        return DocxExporterV1().export(report_input, output_path)


def _sample_input() -> ReportInputV1:
    return ReportInputV1(
        metadata=ReportMetadataV1(case_id="CASE-0001", report_version="1.0"),
        profile=ReportProfileV1(full_name="Nguyễn Tiến Sơn"),
    )


def test_service_routes_pdf(tmp_path: Path) -> None:
    """Service routes PDF export and returns metadata."""
    service = ReportExportServiceV1(
        export_root=tmp_path,
        pdf_exporter=_FakePdfExporter(),
        docx_exporter=_FakeDocxExporter(),
    )
    result = service.export_pdf(_sample_input())
    assert result.media_type == MEDIA_TYPE_PDF
    assert Path(result.file_path).is_file()


def test_service_routes_docx(tmp_path: Path) -> None:
    """Service routes DOCX export and returns metadata."""
    service = ReportExportServiceV1(
        export_root=tmp_path,
        pdf_exporter=_FakePdfExporter(),
        docx_exporter=_FakeDocxExporter(),
    )
    result = service.export_docx(_sample_input())
    assert result.media_type == MEDIA_TYPE_DOCX
    assert result.case_id == "CASE-0001"


def test_service_builds_default_filename(tmp_path: Path) -> None:
    """Default output path uses deterministic filename."""
    service = ReportExportServiceV1(
        export_root=tmp_path,
        pdf_exporter=_FakePdfExporter(),
        docx_exporter=_FakeDocxExporter(),
    )
    report_input = _sample_input()
    expected = tmp_path / build_export_filename(report_input, "pdf")
    result = service.export_pdf(report_input)
    assert Path(result.file_path) == expected.resolve()
