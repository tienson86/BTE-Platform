"""Public service API router.

Mounts:
- GET /health /live /ready
- GET /version
- GET /metrics (reserved)
- /api/v1/* resource APIs

Does not expose /api/v2/.
"""

from __future__ import annotations

from fastapi import APIRouter, FastAPI

from applications.api.v1 import analysis, health, knowledge, report, system
from applications.errors.exception_mapper import register_public_exception_handlers
from applications.middleware import register_public_middleware
from applications.services.service_registry import ServiceRegistry
from applications.versioning.api_versions import V1_MOUNT_PATH


def build_public_router() -> APIRouter:
    """Build the public service router tree."""
    router = APIRouter()
    router.include_router(health.router)
    router.include_router(system.router)
    router.include_router(analysis.router, prefix=V1_MOUNT_PATH)
    router.include_router(report.router, prefix=V1_MOUNT_PATH)
    router.include_router(knowledge.router, prefix=V1_MOUNT_PATH)
    return router


public_router = build_public_router()


def register_public_service_layer(
    app: FastAPI,
    *,
    registry: ServiceRegistry | None = None,
) -> None:
    """Attach public middleware, errors, services, and routers.

    Does not modify engines, pipelines, knowledge, or the existing host app
    unless the host explicitly calls this function.
    """
    register_public_middleware(app)
    register_public_exception_handlers(app)
    app.state.service_registry = registry or ServiceRegistry.create_default()
    app.include_router(build_public_router())
