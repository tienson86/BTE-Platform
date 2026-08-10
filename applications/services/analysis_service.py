"""Public AnalysisService.

Calls the canonical analysis pipeline port only. No engine internals.
No knowledge package imports. No business logic.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from uuid import uuid4

from applications.contracts.request_models import AnalysisCreateRequest
from applications.contracts.response_models import PublicSuccessResponse, build_success_response
from applications.errors.error_codes import NOT_FOUND
from applications.errors.error_response import PublicServiceError

if TYPE_CHECKING:
    from applications.services.service_registry import CanonicalPipelinePort

CANONICAL_ANALYSIS_PIPELINE = "canonical_analysis_pipeline"


class AnalysisService:
    """Validate analysis requests and delegate to the canonical pipeline port."""

    name = "AnalysisService"

    def __init__(self, pipeline: CanonicalPipelinePort) -> None:
        self._pipeline = pipeline

    def create_analysis(
        self,
        request: AnalysisCreateRequest,
        *,
        request_id: str,
        correlation_id: str | None = None,
        idempotency_key: str | None = None,
        api_version: str,
    ) -> PublicSuccessResponse:
        """Submit a validated analysis request to the canonical pipeline port."""
        analysis_id = f"anl_{uuid4().hex}"
        payload = {
            "analysis_id": analysis_id,
            "birth_data": request.birth_data.model_dump(),
            "customer": request.customer.model_dump() if request.customer else None,
            "options": request.options.model_dump(),
            "request_id": request_id,
            "idempotency_key": idempotency_key,
        }
        pipeline_result = self._pipeline.submit_analysis(payload)
        data = {
            "analysis_id": analysis_id,
            "execution": pipeline_result.get("execution", "accepted"),
            "resource": "analysis",
        }
        return build_success_response(
            data=data,
            service=self.name,
            operation="create_analysis",
            request_id=request_id,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
            pipeline=CANONICAL_ANALYSIS_PIPELINE,
            api_version=api_version,
        )

    def get_analysis(
        self,
        analysis_id: str,
        *,
        request_id: str,
        correlation_id: str | None = None,
        api_version: str,
    ) -> PublicSuccessResponse:
        """Retrieve analysis by id through the canonical pipeline port."""
        record = self._pipeline.get_analysis(analysis_id)
        if record is None:
            raise PublicServiceError(
                NOT_FOUND,
                details={"field": "id", "reason": "Analysis resource was not found."},
            )
        data: dict[str, Any] = {
            "analysis_id": analysis_id,
            "resource": "analysis",
            "record": dict(record),
        }
        return build_success_response(
            data=data,
            service=self.name,
            operation="get_analysis",
            request_id=request_id,
            correlation_id=correlation_id,
            pipeline=CANONICAL_ANALYSIS_PIPELINE,
            api_version=api_version,
        )
