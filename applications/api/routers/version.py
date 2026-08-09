"""Public version router."""

from __future__ import annotations

from fastapi import APIRouter

from applications.api.contracts.version import (
    API_VERSION,
    MIN_ENGINE_VERSION,
    SCHEMA_VERSION,
)

router = APIRouter(tags=["version"])


@router.get("/version")
def get_version_info() -> dict[str, str]:
    """Return frozen public API version information."""
    return {
        "api_version": API_VERSION,
        "schema_version": SCHEMA_VERSION,
        "minimum_engine_version": MIN_ENGINE_VERSION,
    }
