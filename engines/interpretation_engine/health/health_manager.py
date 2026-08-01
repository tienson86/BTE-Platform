"""Aggregate health management for Pack 03 runtimes.

Tracks READY / RUNNING / FAILED / DISABLED / UNKNOWN.
Infrastructure only.
"""

from __future__ import annotations

import logging
from typing import Mapping

from engines.interpretation_engine.runtime.contracts import HealthStatus, RuntimeContract

logger = logging.getLogger(__name__)


class HealthManager:
    """Collect and evaluate health of injected runtimes."""

    def __init__(self) -> None:
        """Initialize empty health manager."""
        self._runtimes: dict[str, RuntimeContract] = {}

    def register(self, runtime_id: str, runtime: RuntimeContract) -> None:
        """Register a runtime for health observation."""
        if not runtime_id:
            raise ValueError("health_runtime_id_required")
        self._runtimes[runtime_id] = runtime

    def unregister(self, runtime_id: str) -> None:
        """Unregister a runtime."""
        self._runtimes.pop(runtime_id, None)

    def status_map(self) -> dict[str, HealthStatus]:
        """Return health status for each registered runtime."""
        return {
            runtime_id: runtime.health()
            for runtime_id, runtime in sorted(self._runtimes.items())
        }

    def overall(self) -> HealthStatus:
        """Compute aggregate health from registered runtimes."""
        if not self._runtimes:
            return HealthStatus.UNKNOWN
        statuses = list(self.status_map().values())
        if any(status is HealthStatus.FAILED for status in statuses):
            return HealthStatus.FAILED
        if any(status is HealthStatus.RUNNING for status in statuses):
            return HealthStatus.RUNNING
        if all(status is HealthStatus.DISABLED for status in statuses):
            return HealthStatus.DISABLED
        if all(status is HealthStatus.READY for status in statuses):
            return HealthStatus.READY
        if any(status is HealthStatus.UNKNOWN for status in statuses):
            return HealthStatus.UNKNOWN
        return HealthStatus.READY

    def validate(self) -> bool:
        """Validate that all registered runtimes report READY or RUNNING."""
        if not self._runtimes:
            return False
        return all(
            status in {HealthStatus.READY, HealthStatus.RUNNING}
            for status in self.status_map().values()
        )

    def snapshot(self) -> Mapping[str, str]:
        """Return string health snapshot for logging/metrics."""
        data = {key: value.value for key, value in self.status_map().items()}
        data["overall"] = self.overall().value
        logger.info("health_snapshot", extra={"health": dict(data)})
        return data
