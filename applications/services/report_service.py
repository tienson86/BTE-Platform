"""Public ReportService.

Calls the canonical report pipeline port only. No report rendering.
No engine internals. No knowledge package imports.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from applications.contracts.response_models import PublicSuccessResponse, build_success_response
from applications.errors.error_codes import NOT_FOUND
from applications.errors.error_response import PublicServiceError

if TYPE_CHECKING:
    from applications.services.service_registry import CanonicalPipelinePort

CANONICAL_REPORT_PIPELINE = "canonical_report_pipeline"


class ReportService:
    """Retrieve reports through the canonical report pipeline port."""

    name = "ReportService"

    def __init__(self, pipeline: CanonicalPipelinePort) -> None:
        self._pipeline = pipeline

    def get_report(
        self,
        report_id: str,
        *,
        request_id: str,
        correlation_id: str | None = None,
        api_version: str,
    ) -> PublicSuccessResponse:
        """Return a public report envelope for the given identifier."""
        record = self._pipeline.get_report(report_id)
        if record is None:
            raise PublicServiceError(
                NOT_FOUND,
                details={"field": "id", "reason": "Report resource was not found."},
            )
        data: dict[str, Any] = {
            "report_id": report_id,
            "resource": "report",
            "record": dict(record),
        }
        return build_success_response(
            data=data,
            service=self.name,
            operation="get_report",
            request_id=request_id,
            correlation_id=correlation_id,
            pipeline=CANONICAL_REPORT_PIPELINE,
            api_version=api_version,
        )
