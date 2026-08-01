"""Shared runtime contracts for Pack 03 Interpretation Layer.

Infrastructure only. No BaZi interpretation logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class HealthStatus(str, Enum):
    """Runtime health states for Pack 03 runtimes."""

    READY = "READY"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    DISABLED = "DISABLED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class RuntimeMetricsSnapshot:
    """Immutable metrics snapshot for a runtime."""

    execution_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    execution_time: float = 0.0
    average_time: float = 0.0
    last_execution: str | None = None
    health: HealthStatus = HealthStatus.UNKNOWN
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate metrics snapshot structural integrity."""
        if self.execution_count < 0 or self.success_count < 0 or self.failure_count < 0:
            return False
        if self.execution_time < 0 or self.average_time < 0:
            return False
        return True


@dataclass(frozen=True, slots=True)
class RuntimeExecuteResult:
    """Immutable execute result shell for runtime stages.

    Holds structural payloads only — never rendered narrative content.
    """

    runtime_id: str
    success: bool
    payload: Mapping[str, Any] = field(default_factory=dict)
    messages: tuple[str, ...] = ()
    metrics: RuntimeMetricsSnapshot | None = None

    def validate(self) -> bool:
        """Validate execute result structural integrity."""
        return bool(self.runtime_id)


class RuntimeContract(ABC):
    """Public runtime contract for Pack 03 runtimes.

    Every runtime exposes only:
    initialize / shutdown / validate / execute / metrics / health
    """

    @abstractmethod
    def initialize(self) -> None:
        """Initialize runtime resources."""

    @abstractmethod
    def shutdown(self) -> None:
        """Release runtime resources."""

    @abstractmethod
    def validate(self) -> bool:
        """Validate runtime readiness and configuration."""

    @abstractmethod
    def execute(self, context: Any) -> RuntimeExecuteResult:
        """Execute runtime stage against PackInterpretationContext (or compatible)."""

    @abstractmethod
    def metrics(self) -> RuntimeMetricsSnapshot:
        """Return current metrics snapshot."""

    @abstractmethod
    def health(self) -> HealthStatus:
        """Return current health status."""
