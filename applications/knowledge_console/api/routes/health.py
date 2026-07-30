"""Health routes."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def health() -> dict[str, str]:
    """Liveness probe."""
    return {
        "status": "ok",
        "service": "bte-knowledge-console-api",
        "version": "1.0.0",
    }


@router.get("/api/v1/health")
def health_v1() -> dict[str, str]:
    """Versioned health probe."""
    return health()
