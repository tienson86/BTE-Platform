"""Admin & operations API routes (WP13)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request

from applications.admin.configuration_service import ConfigurationService
from applications.admin.dashboard_service import DashboardService
from applications.admin.health_service import HealthService
from applications.admin.system_service import SystemService
from applications.api.auth.dependencies import require_role
from applications.api.auth.roles import Role
from applications.api.auth.store import UserRecord
from applications.api.schemas.common import APIResponse
from applications.audit.audit_log import get_audit_log
from applications.audit.security_events import list_security_events
from applications.statistics.api_statistics import api_statistics
from applications.statistics.case_statistics import case_statistics
from applications.statistics.customer_statistics import customer_statistics
from applications.statistics.engine_statistics import engine_statistics
from applications.storage.factory import StorageConfig

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_role(Role.ADMIN))],
)


def _envelope(request: Request, message: str, data: dict) -> APIResponse:
    return APIResponse(
        success=True,
        message=message,
        data=data,
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/dashboard", response_model=APIResponse)
def admin_dashboard(
    request: Request,
    _: UserRecord = Depends(require_role(Role.ADMIN)),
) -> APIResponse:
    """Admin dashboard aggregates."""
    data = DashboardService(storage_config=StorageConfig.from_env()).build()
    return _envelope(request, "Dashboard OK", data)


@router.get("/system", response_model=APIResponse)
def admin_system(request: Request) -> APIResponse:
    """System information."""
    return _envelope(request, "System OK", SystemService().build())


@router.get("/health", response_model=APIResponse)
def admin_health(request: Request) -> APIResponse:
    """Operational health checks."""
    return _envelope(
        request,
        "Health OK",
        HealthService(storage_config=StorageConfig.from_env()).check(),
    )


@router.get("/config", response_model=APIResponse)
def admin_config(request: Request) -> APIResponse:
    """Non-secret configuration."""
    return _envelope(request, "Config OK", ConfigurationService().build())


@router.get("/statistics", response_model=APIResponse)
def admin_statistics(request: Request) -> APIResponse:
    """Combined statistics snapshot."""
    data = {
        "customers": customer_statistics(),
        "cases": case_statistics(),
        "api": api_statistics(),
        "engines": engine_statistics(),
    }
    return _envelope(request, "Statistics OK", data)


@router.get("/audit", response_model=APIResponse)
def admin_audit(
    request: Request,
    limit: int = Query(100, ge=1, le=1000),
    event_type: str | None = Query(None),
    security_only: bool = Query(False),
) -> APIResponse:
    """Audit trail (newest first)."""
    if security_only:
        events = list_security_events(limit=limit)
    else:
        events = get_audit_log().list(limit=limit, event_type=event_type)
    return _envelope(
        request,
        "Audit OK",
        {"events": events, "count": len(events)},
    )
