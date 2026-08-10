"""Public health probes: /health, /live, /ready."""

from __future__ import annotations

from fastapi import APIRouter, Request

from applications.api.v1 import get_registry, get_request_context
from applications.contracts.response_models import PublicSuccessResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=PublicSuccessResponse)
def get_health(request: Request) -> PublicSuccessResponse:
    """Aggregate liveness probe."""
    ctx = get_request_context(request)
    return get_registry(request).health.health(
        request_id=ctx.request_id,
        correlation_id=ctx.correlation_id,
        api_version=ctx.api_version,
    )


@router.get("/live", response_model=PublicSuccessResponse)
def get_live(request: Request) -> PublicSuccessResponse:
    """Process liveness probe."""
    ctx = get_request_context(request)
    return get_registry(request).health.live(
        request_id=ctx.request_id,
        correlation_id=ctx.correlation_id,
        api_version=ctx.api_version,
    )


@router.get("/ready", response_model=PublicSuccessResponse)
def get_ready(request: Request) -> PublicSuccessResponse:
    """Traffic readiness probe."""
    ctx = get_request_context(request)
    return get_registry(request).health.ready(
        request_id=ctx.request_id,
        correlation_id=ctx.correlation_id,
        api_version=ctx.api_version,
    )
