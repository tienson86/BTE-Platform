"""Runtime metrics collector for Pack 03 infrastructure.

Collects execution_count, success_count, failure_count, execution_time,
average_time, last_execution, and health.
"""

from __future__ import annotations

import logging
from typing import Mapping

from engines.interpretation_engine.runtime.contracts import (
    HealthStatus,
    RuntimeContract,
    RuntimeMetricsSnapshot,
)

logger = logging.getLogger(__name__)


class RuntimeMetricsCollector:
    """Aggregate metrics snapshots from injected runtimes."""

    def __init__(self) -> None:
        """Initialize empty collector."""
        self._runtimes: dict[str, RuntimeContract] = {}

    def register(self, runtime_id: str, runtime: RuntimeContract) -> None:
        """Register a runtime for metrics collection."""
        if not runtime_id:
            raise ValueError("metrics_runtime_id_required")
        self._runtimes[runtime_id] = runtime

    def unregister(self, runtime_id: str) -> None:
        """Unregister a runtime."""
        self._runtimes.pop(runtime_id, None)

    def collect(self) -> dict[str, RuntimeMetricsSnapshot]:
        """Collect metrics snapshots for all registered runtimes."""
        collected = {
            runtime_id: runtime.metrics()
            for runtime_id, runtime in sorted(self._runtimes.items())
        }
        logger.info(
            "runtime_metrics_collected",
            extra={"runtime_ids": list(collected.keys())},
        )
        return collected

    def aggregate(self) -> RuntimeMetricsSnapshot:
        """Aggregate totals across registered runtimes."""
        snapshots = list(self.collect().values())
        if not snapshots:
            return RuntimeMetricsSnapshot(health=HealthStatus.UNKNOWN)
        execution_count = sum(item.execution_count for item in snapshots)
        success_count = sum(item.success_count for item in snapshots)
        failure_count = sum(item.failure_count for item in snapshots)
        execution_time = sum(item.execution_time for item in snapshots)
        average = execution_time / execution_count if execution_count else 0.0
        last_values = [item.last_execution for item in snapshots if item.last_execution]
        last_execution = max(last_values) if last_values else None
        if any(item.health is HealthStatus.FAILED for item in snapshots):
            health = HealthStatus.FAILED
        elif any(item.health is HealthStatus.RUNNING for item in snapshots):
            health = HealthStatus.RUNNING
        elif all(item.health is HealthStatus.DISABLED for item in snapshots):
            health = HealthStatus.DISABLED
        elif all(item.health is HealthStatus.READY for item in snapshots):
            health = HealthStatus.READY
        else:
            health = HealthStatus.UNKNOWN
        return RuntimeMetricsSnapshot(
            execution_count=execution_count,
            success_count=success_count,
            failure_count=failure_count,
            execution_time=execution_time,
            average_time=average,
            last_execution=last_execution,
            health=health,
        )

    def as_dict(self) -> Mapping[str, Mapping[str, object]]:
        """Return serializable metrics dictionary."""
        result: dict[str, Mapping[str, object]] = {}
        for runtime_id, snapshot in self.collect().items():
            result[runtime_id] = {
                "execution_count": snapshot.execution_count,
                "success_count": snapshot.success_count,
                "failure_count": snapshot.failure_count,
                "execution_time": snapshot.execution_time,
                "average_time": snapshot.average_time,
                "last_execution": snapshot.last_execution,
                "health": snapshot.health.value,
            }
        aggregate = self.aggregate()
        result["aggregate"] = {
            "execution_count": aggregate.execution_count,
            "success_count": aggregate.success_count,
            "failure_count": aggregate.failure_count,
            "execution_time": aggregate.execution_time,
            "average_time": aggregate.average_time,
            "last_execution": aggregate.last_execution,
            "health": aggregate.health.value,
        }
        return result
