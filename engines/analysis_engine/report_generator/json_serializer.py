"""JSON serializer for StructuredReport."""

from __future__ import annotations

from engines.analysis_engine.report_generator.exceptions import ReportSerializationError
from engines.analysis_engine.report_generator.models import (
    JsonReportArtifact,
    StructuredReport,
    dumps_json,
)


class JsonSerializer:
    """Serialize StructuredReport to a lossless JSON envelope."""

    def serialize(self, report: StructuredReport) -> JsonReportArtifact:
        """Render deterministic JSON artifact."""
        try:
            payload = {
                "report": report.to_dict(),
                "format": "json",
                "schema_version": "1.0.0",
            }
            content = dumps_json(payload)
        except (TypeError, ValueError) as exc:
            raise ReportSerializationError(
                "JSON serialization failed",
                details={"error": str(exc)},
            ) from exc
        return JsonReportArtifact(content=content, payload=payload)
