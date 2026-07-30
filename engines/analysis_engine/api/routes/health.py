"""Health routes."""

from __future__ import annotations

from fastapi import APIRouter

from engines.analysis_engine.api.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
@router.get("/api/v1/health")
def health() -> dict[str, str]:
    """Liveness probe."""
    return {
        "status": "ok",
        "service": "bte-analysis-engine-api",
        "version": settings.app_version,
    }
