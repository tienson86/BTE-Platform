"""Public system probes: /version. /metrics is reserved."""

from __future__ import annotations

from fastapi import APIRouter, Request

from applications.api.v1 import get_registry, get_request_context
from applications.contracts.response_models import PublicSuccessResponse

router = APIRouter(tags=["system"])


@router.get("/version", response_model=PublicSuccessResponse)
def get_version(request: Request) -> PublicSuccessResponse:
    """Return public API and schema versions."""
    ctx = get_request_context(request)
    return get_registry(request).health.version(
        request_id=ctx.request_id,
        correlation_id=ctx.correlation_id,
        api_version=ctx.api_version,
    )


@router.get("/metrics")
def get_metrics(request: Request) -> None:
    """Reserved metrics endpoint. No monitoring implementation."""
    get_registry(request).health.metrics()
