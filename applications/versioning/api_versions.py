"""Public API version catalog.

v2 is reserved and must never be mounted in this release.
"""

from __future__ import annotations

from typing import Final

API_PREFIX: Final[str] = "/api"
CURRENT_API_VERSION: Final[str] = "v1"
CURRENT_SEMVER: Final[str] = "1.0.0"
SCHEMA_VERSION: Final[str] = "1.0.0"
PLATFORM_VERSION: Final[str] = "1.0.0"

SUPPORTED_API_VERSIONS: Final[tuple[str, ...]] = ("v1",)
RESERVED_API_VERSIONS: Final[tuple[str, ...]] = ("v2",)

V1_MOUNT_PATH: Final[str] = f"{API_PREFIX}/{CURRENT_API_VERSION}"
V2_MOUNT_PATH: Final[str] = f"{API_PREFIX}/v2"


def is_supported_version(version: str) -> bool:
    """Return True when *version* is an exposed public API version."""
    normalized = version.strip().lower().lstrip("v")
    return f"v{normalized}" in SUPPORTED_API_VERSIONS if normalized.isdigit() else (
        version.strip().lower() in SUPPORTED_API_VERSIONS
    )


def is_reserved_version(version: str) -> bool:
    """Return True when *version* is defined but not exposed."""
    normalized = version.strip().lower()
    if normalized.isdigit():
        normalized = f"v{normalized}"
    elif not normalized.startswith("v"):
        normalized = f"v{normalized}"
    return normalized in RESERVED_API_VERSIONS
