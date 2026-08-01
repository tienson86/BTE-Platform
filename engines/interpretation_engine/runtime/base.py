"""Base runtime implementation for Pack 03.

Provides shared lifecycle, metrics, and health handling.
Infrastructure only — no business logic.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from typing import Any

from engines.interpretation_engine.runtime.contracts import (
    HealthStatus,
    RuntimeContract,
    RuntimeExecuteResult,
    RuntimeMetricsSnapshot,
)

logger = logging.getLogger(__name__)


def _utc_now() -> str:
    """Return UTC ISO-8601 timestamp."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class BaseRuntime(RuntimeContract):
    """Shared runtime base with required public contract methods."""

    def __init__(self, *, runtime_id: str) -> None:
        """Initialize runtime identity and counters."""
        self.runtime_id = runtime_id
        self._initialized = False
        self._health = HealthStatus.UNKNOWN
        self._execution_count = 0
        self._success_count = 0
        self._failure_count = 0
        self._execution_time = 0.0
        self._last_execution: str | None = None

    def initialize(self) -> None:
        """Initialize runtime resources."""
        self._initialized = True
        self._health = HealthStatus.READY
        logger.info(
            "runtime_initialized",
            extra={"runtime_id": self.runtime_id, "health": self._health.value},
        )

    def shutdown(self) -> None:
        """Release runtime resources."""
        self._initialized = False
        self._health = HealthStatus.DISABLED
        logger.info(
            "runtime_shutdown",
            extra={"runtime_id": self.runtime_id, "health": self._health.value},
        )

    def validate(self) -> bool:
        """Validate runtime readiness."""
        if not self.runtime_id:
            return False
        return self._initialized and self._health in {
            HealthStatus.READY,
            HealthStatus.RUNNING,
        }

    def execute(self, context: Any) -> RuntimeExecuteResult:
        """Execute runtime stage; subclasses override ``_execute_body``."""
        if not self._initialized:
            self._health = HealthStatus.FAILED
            return RuntimeExecuteResult(
                runtime_id=self.runtime_id,
                success=False,
                messages=("runtime_not_initialized",),
                metrics=self.metrics(),
            )

        self._health = HealthStatus.RUNNING
        started = time.perf_counter()
        self._execution_count += 1
        self._last_execution = _utc_now()
        try:
            result = self._execute_body(context)
            elapsed = time.perf_counter() - started
            self._execution_time += elapsed
            if result.success:
                self._success_count += 1
                self._health = HealthStatus.READY
            else:
                self._failure_count += 1
                self._health = HealthStatus.FAILED
            return RuntimeExecuteResult(
                runtime_id=self.runtime_id,
                success=result.success,
                payload=dict(result.payload),
                messages=result.messages,
                metrics=self.metrics(),
            )
        except Exception as exc:  # noqa: BLE001 - runtime boundary
            elapsed = time.perf_counter() - started
            self._execution_time += elapsed
            self._failure_count += 1
            self._health = HealthStatus.FAILED
            logger.exception(
                "runtime_execute_failed",
                extra={"runtime_id": self.runtime_id, "error": type(exc).__name__},
            )
            return RuntimeExecuteResult(
                runtime_id=self.runtime_id,
                success=False,
                messages=(f"runtime_execute_error:{type(exc).__name__}:{exc}",),
                metrics=self.metrics(),
            )

    def metrics(self) -> RuntimeMetricsSnapshot:
        """Return current metrics snapshot."""
        average = (
            self._execution_time / self._execution_count
            if self._execution_count
            else 0.0
        )
        return RuntimeMetricsSnapshot(
            execution_count=self._execution_count,
            success_count=self._success_count,
            failure_count=self._failure_count,
            execution_time=self._execution_time,
            average_time=average,
            last_execution=self._last_execution,
            health=self._health,
        )

    def health(self) -> HealthStatus:
        """Return current health status."""
        return self._health

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Subclass execution body. Default is a successful no-op shell."""
        context_id = getattr(context, "id", None) or "unknown"
        return RuntimeExecuteResult(
            runtime_id=self.runtime_id,
            success=True,
            payload={"context_id": context_id, "stage": self.runtime_id},
            messages=("runtime_noop_success",),
        )
