"""Semantic version helpers for the public service layer."""

from __future__ import annotations

from dataclasses import dataclass

from applications.versioning.api_versions import (
    CURRENT_API_VERSION,
    CURRENT_SEMVER,
    RESERVED_API_VERSIONS,
    SCHEMA_VERSION,
    SUPPORTED_API_VERSIONS,
    V1_MOUNT_PATH,
    V2_MOUNT_PATH,
    is_reserved_version,
    is_supported_version,
)


@dataclass(slots=True)
class ApiVersionInfo:
    """Resolved public API version identity."""

    api_version: str
    semver: str
    schema_version: str
    mount_path: str
    supported: tuple[str, ...]
    reserved: tuple[str, ...]
    v2_exposed: bool


class VersionManager:
    """Resolve and validate public API versions.

    Breaking changes require a new major mount (for example ``/api/v2``).
    This manager never exposes reserved mounts.
    """

    def __init__(
        self,
        *,
        current: str = CURRENT_API_VERSION,
        semver: str = CURRENT_SEMVER,
        schema_version: str = SCHEMA_VERSION,
    ) -> None:
        self._current = current
        self._semver = semver
        self._schema_version = schema_version

    def current(self) -> ApiVersionInfo:
        """Return the active public API version descriptor."""
        return ApiVersionInfo(
            api_version=self._current,
            semver=self._semver,
            schema_version=self._schema_version,
            mount_path=V1_MOUNT_PATH,
            supported=SUPPORTED_API_VERSIONS,
            reserved=RESERVED_API_VERSIONS,
            v2_exposed=False,
        )

    def negotiate(self, requested: str | None) -> str:
        """Return the API version to serve for a client request.

        Unknown or reserved versions raise ``ValueError``.
        """
        if requested is None or requested.strip() == "":
            return self._current
        value = requested.strip().lower()
        if value.isdigit():
            value = f"v{value}"
        if not value.startswith("v"):
            value = f"v{value}"
        if is_reserved_version(value):
            raise ValueError(f"API version {value} is reserved and not exposed.")
        if not is_supported_version(value):
            raise ValueError(f"API version {value} is not supported.")
        return value

    def describe(self) -> dict[str, object]:
        """Return a JSON-safe version payload for ``GET /version``."""
        info = self.current()
        return {
            "api_version": info.api_version,
            "semver": info.semver,
            "schema_version": info.schema_version,
            "mount_path": info.mount_path,
            "supported_versions": list(info.supported),
            "reserved_versions": list(info.reserved),
            "v2_exposed": info.v2_exposed,
            "v2_mount_path": V2_MOUNT_PATH,
        }


default_version_manager = VersionManager()
