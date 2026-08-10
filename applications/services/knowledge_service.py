"""Public KnowledgeService.

Calls the canonical knowledge pipeline port only.
Never imports knowledge packages.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from applications.contracts.response_models import PublicSuccessResponse, build_success_response
from applications.errors.error_codes import NOT_FOUND
from applications.errors.error_response import PublicServiceError

if TYPE_CHECKING:
    from applications.services.service_registry import CanonicalPipelinePort

CANONICAL_KNOWLEDGE_PIPELINE = "canonical_knowledge_pipeline"


class KnowledgeService:
    """Retrieve published knowledge resources through the pipeline port."""

    name = "KnowledgeService"

    def __init__(self, pipeline: CanonicalPipelinePort) -> None:
        self._pipeline = pipeline

    def get_knowledge(
        self,
        knowledge_id: str,
        *,
        request_id: str,
        correlation_id: str | None = None,
        api_version: str,
    ) -> PublicSuccessResponse:
        """Return a public knowledge envelope for the given identifier."""
        record = self._pipeline.get_knowledge(knowledge_id)
        if record is None:
            raise PublicServiceError(
                NOT_FOUND,
                details={"field": "id", "reason": "Knowledge resource was not found."},
            )
        data: dict[str, Any] = {
            "knowledge_id": knowledge_id,
            "resource": "knowledge",
            "record": dict(record),
        }
        return build_success_response(
            data=data,
            service=self.name,
            operation="get_knowledge",
            request_id=request_id,
            correlation_id=correlation_id,
            pipeline=CANONICAL_KNOWLEDGE_PIPELINE,
            api_version=api_version,
        )
