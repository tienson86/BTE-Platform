"""API contract version constants."""

from __future__ import annotations

API_VERSION: str = "1.0.0"
SCHEMA_VERSION: str = "1.0.0"
MIN_ENGINE_VERSION: str = "1.0.0"


def get_version() -> dict[str, str]:
    """Return frozen API contract version information."""
    return {
        "api_version": API_VERSION,
        "schema_version": SCHEMA_VERSION,
        "min_engine_version": MIN_ENGINE_VERSION,
    }
