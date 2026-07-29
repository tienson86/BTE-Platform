"""Health endpoint."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/api/v1/health")
def health() -> dict[str, str]:
    """Liveness probe for Applications API V1."""
    return {"status": "ok", "service": "bte-applications-api", "version": "1.0.0"}
