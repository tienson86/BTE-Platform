"""Runtime execution manager for Pack 03 orchestration.

Coordinates initialize / validate / execute / shutdown for a RuntimePipeline.
Infrastructure only. No BaZi logic.
"""

from __future__ import annotations

import logging
from typing import Any

from engines.interpretation_engine.orchestration.runtime_pipeline import RuntimePipeline
from engines.interpretation_engine.runtime.contracts import (
    HealthStatus,
    RuntimeExecuteResult,
    RuntimeMetricsSnapshot,
)

logger = logging.getLogger(__name__)


class ExecutionManager:
    """Manage lifecycle and execution of an injected RuntimePipeline."""

    def __init__(self, pipeline: RuntimePipeline | None = None) -> None:
        """Initialize with optional injected pipeline (DI only)."""
        self._pipeline = pipeline or RuntimePipeline()
        self._active = False

    @property
    def pipeline(self) -> RuntimePipeline:
        """Return managed pipeline."""
        return self._pipeline

    def initialize(self) -> None:
        """Initialize managed pipeline."""
        self._pipeline.initialize()
        self._active = True
        logger.info("execution_manager_initialized")

    def shutdown(self) -> None:
        """Shutdown managed pipeline."""
        self._pipeline.shutdown()
        self._active = False
        logger.info("execution_manager_shutdown")

    def validate(self) -> bool:
        """Validate managed pipeline readiness."""
        if not self._active:
            return False
        return self._pipeline.validate()

    def execute(self, context: Any) -> RuntimeExecuteResult:
        """Execute managed pipeline against PackInterpretationContext."""
        if not self._active:
            return RuntimeExecuteResult(
                runtime_id=self._pipeline.runtime_id,
                success=False,
                messages=("execution_manager_not_initialized",),
                metrics=self.metrics(),
            )
        return self._pipeline.execute(context)

    def metrics(self) -> RuntimeMetricsSnapshot:
        """Return pipeline metrics snapshot."""
        return self._pipeline.metrics()

    def health(self) -> HealthStatus:
        """Return pipeline health status."""
        if not self._active:
            return HealthStatus.DISABLED
        return self._pipeline.health()
