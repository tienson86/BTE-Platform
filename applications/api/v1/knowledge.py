"""Public knowledge endpoints under /api/v1."""

from __future__ import annotations

from fastapi import APIRouter, Request

from applications.api.v1 import get_registry, get_request_context
from applications.contracts.response_models import PublicSuccessResponse

router = APIRouter(tags=["knowledge"])


@router.get("/knowledge/{id}", response_model=PublicSuccessResponse)
def get_knowledge(request: Request, id: str) -> PublicSuccessResponse:
    """Retrieve a published knowledge resource by public identifier."""
    ctx = get_request_context(request)
    return get_registry(request).knowledge.get_knowledge(
        id,
        request_id=ctx.request_id,
        correlation_id=ctx.correlation_id,
        api_version=ctx.api_version,
    )
