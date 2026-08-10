"""Public API v1 routers.

All resource APIs are mounted under ``/api/v1/``.
Health and system probes are mounted at the application root.
``/api/v2/`` is not exported.
"""

from __future__ import annotations

from dataclasses import dataclass

from fastapi import Request

from applications.services.service_registry import ServiceRegistry, get_service_registry
from applications.versioning.api_versions import CURRENT_API_VERSION


@dataclass(slots=True)
class PublicRequestContext:
    """Identifiers resolved from public middleware."""

    request_id: str
    correlation_id: str | None
    idempotency_key: str | None
    api_version: str


def get_request_context(request: Request) -> PublicRequestContext:
    """Read pass-through identifiers from request state."""
    return PublicRequestContext(
        request_id=str(getattr(request.state, "request_id", "") or "unknown"),
        correlation_id=getattr(request.state, "correlation_id", None),
        idempotency_key=getattr(request.state, "idempotency_key", None),
        api_version=str(getattr(request.state, "api_version", CURRENT_API_VERSION)),
    )


def get_registry(request: Request) -> ServiceRegistry:
    """Resolve the service registry from app state or the default graph."""
    registry = getattr(request.app.state, "service_registry", None)
    if isinstance(registry, ServiceRegistry):
        return registry
    return get_service_registry()
