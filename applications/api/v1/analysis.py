"""Public analysis endpoints under /api/v1."""

from __future__ import annotations

from fastapi import APIRouter, Request

from applications.api.v1 import get_registry, get_request_context
from applications.contracts.request_models import AnalysisCreateRequest
from applications.contracts.response_models import PublicSuccessResponse

router = APIRouter(tags=["analysis"])


@router.post("/analysis", response_model=PublicSuccessResponse)
def create_analysis(
    request: Request,
    body: AnalysisCreateRequest,
) -> PublicSuccessResponse:
    """Validate and submit an analysis request to the canonical pipeline port."""
    ctx = get_request_context(request)
    return get_registry(request).analysis.create_analysis(
        body,
        request_id=ctx.request_id,
        correlation_id=ctx.correlation_id,
        idempotency_key=ctx.idempotency_key,
        api_version=ctx.api_version,
    )


@router.get("/analysis/{id}", response_model=PublicSuccessResponse)
def get_analysis(request: Request, id: str) -> PublicSuccessResponse:
    """Retrieve a previously submitted analysis by public identifier."""
    ctx = get_request_context(request)
    return get_registry(request).analysis.get_analysis(
        id,
        request_id=ctx.request_id,
        correlation_id=ctx.correlation_id,
        api_version=ctx.api_version,
    )
