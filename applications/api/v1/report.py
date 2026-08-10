"""Public report endpoints under /api/v1."""

from __future__ import annotations

from fastapi import APIRouter, Request

from applications.api.v1 import get_registry, get_request_context
from applications.contracts.response_models import PublicSuccessResponse

router = APIRouter(tags=["report"])


@router.get("/report/{id}", response_model=PublicSuccessResponse)
def get_report(request: Request, id: str) -> PublicSuccessResponse:
    """Retrieve a report by public identifier."""
    ctx = get_request_context(request)
    return get_registry(request).report.get_report(
        id,
        request_id=ctx.request_id,
        correlation_id=ctx.correlation_id,
        api_version=ctx.api_version,
    )
