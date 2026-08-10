"""Public HealthService.

Standardizes /health, /live, /ready, and /version.
/metrics is reserved and not implemented.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from applications.contracts.response_models import PublicSuccessResponse, build_success_response
from applications.errors.error_codes import NOT_IMPLEMENTED
from applications.errors.error_response import PublicServiceError
from applications.versioning.version_manager import VersionManager, default_version_manager

if TYPE_CHECKING:
    from applications.services.service_registry import CanonicalPipelinePort

HEALTH_PIPELINE = "canonical_health_probe"


class HealthService:
    """Return public operational probes without monitoring implementation."""

    name = "HealthService"

    def __init__(
        self,
        pipeline: CanonicalPipelinePort,
        version_manager: VersionManager | None = None,
    ) -> None:
        self._pipeline = pipeline
        self._versions = version_manager or default_version_manager

    def health(
        self,
        *,
        request_id: str,
        correlation_id: str | None = None,
        api_version: str,
    ) -> PublicSuccessResponse:
        """Aggregate liveness probe."""
        probe = self._pipeline.probe_health()
        data: dict[str, Any] = {
            "probe": "health",
            "alive": True,
            "ready": bool(probe.get("ready", False)),
            "pipeline_bound": bool(probe.get("bound", False)),
        }
        return self._envelope("health", data, request_id, correlation_id, api_version)

    def live(
        self,
        *,
        request_id: str,
        correlation_id: str | None = None,
        api_version: str,
    ) -> PublicSuccessResponse:
        """Process liveness probe."""
        return self._envelope(
            "live",
            {"probe": "live", "alive": True},
            request_id,
            correlation_id,
            api_version,
        )

    def ready(
        self,
        *,
        request_id: str,
        correlation_id: str | None = None,
        api_version: str,
    ) -> PublicSuccessResponse:
        """Traffic readiness probe."""
        probe = self._pipeline.probe_health()
        data = {
            "probe": "ready",
            "ready": bool(probe.get("ready", False)),
            "pipeline_bound": bool(probe.get("bound", False)),
        }
        return self._envelope("ready", data, request_id, correlation_id, api_version)

    def version(
        self,
        *,
        request_id: str,
        correlation_id: str | None = None,
        api_version: str,
    ) -> PublicSuccessResponse:
        """Public version identity."""
        data = self._versions.describe()
        return self._envelope("version", data, request_id, correlation_id, api_version)

    def metrics(self) -> None:
        """Reserved metrics probe. No monitoring implementation."""
        raise PublicServiceError(
            NOT_IMPLEMENTED,
            details={"field": "metrics", "reason": "/metrics is reserved."},
        )

    def _envelope(
        self,
        operation: str,
        data: dict[str, Any],
        request_id: str,
        correlation_id: str | None,
        api_version: str,
    ) -> PublicSuccessResponse:
        return build_success_response(
            data=data,
            service=self.name,
            operation=operation,
            request_id=request_id,
            correlation_id=correlation_id,
            pipeline=HEALTH_PIPELINE,
            api_version=api_version,
        )
