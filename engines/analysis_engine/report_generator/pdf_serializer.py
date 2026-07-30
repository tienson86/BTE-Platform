"""PDF serializer for StructuredReport (no external dependencies)."""

from __future__ import annotations

from pathlib import Path

from engines.analysis_engine.report_generator.exceptions import ReportSerializationError
from engines.analysis_engine.report_generator.models import (
    PdfReportArtifact,
    StructuredReport,
)
from engines.analysis_engine.report_generator.simple_pdf import write_simple_pdf_bytes


class PdfSerializer:
    """Serialize StructuredReport to a minimal PDF document."""

    def serialize(
        self,
        report: StructuredReport,
        *,
        output_path: str | Path | None = None,
    ) -> PdfReportArtifact:
        """Render deterministic PDF artifact as bytes (optional file write)."""
        try:
            lines = self._lines(report)
            pdf_bytes = write_simple_pdf_bytes(
                lines,
                title=report.metadata.title,
            )
            path: str | None = None
            if output_path is not None:
                target = Path(output_path)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(pdf_bytes)
                path = str(target)
        except (OSError, ValueError, TypeError) as exc:
            raise ReportSerializationError(
                "PDF serialization failed",
                details={"error": str(exc)},
            ) from exc
        return PdfReportArtifact(content=pdf_bytes, path=path)

    @staticmethod
    def _lines(report: StructuredReport) -> list[str]:
        lines: list[str] = [
            report.metadata.title,
            "=" * 40,
            report.overview,
            "",
        ]
        for section in report.sections:
            lines.append(section.title)
            lines.append("-" * 20)
            lines.extend(section.body.splitlines() or [section.body])
            lines.append("")
        if report.data_blocks:
            lines.append("Analytical Data")
            lines.append("=" * 40)
            for block in report.data_blocks:
                lines.append(block.title)
                lines.append(f"[{block.stage_id}]")
                lines.append(str(dict(block.payload)))
                lines.append("")
        return lines
