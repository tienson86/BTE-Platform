"""Generate Pack 03 Interpretation Runtime Foundation (infrastructure only)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path("engines/interpretation_engine")


def write(rel: str, content: str) -> None:
    """Write UTF-8 file under interpretation_engine."""
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip("\n"), encoding="utf-8")


# ---------------------------------------------------------------------------
# Core runtime contracts
# ---------------------------------------------------------------------------

write(
    "runtime/__init__.py",
    '''
"""Pack 03 shared runtime contracts and base types."""

from __future__ import annotations

from engines.interpretation_engine.runtime.base import BaseRuntime
from engines.interpretation_engine.runtime.contracts import (
    HealthStatus,
    RuntimeContract,
    RuntimeExecuteResult,
    RuntimeMetricsSnapshot,
)
from engines.interpretation_engine.runtime.registry_base import BaseRegistry

__all__ = [
    "BaseRegistry",
    "BaseRuntime",
    "HealthStatus",
    "RuntimeContract",
    "RuntimeExecuteResult",
    "RuntimeMetricsSnapshot",
]
''',
)

write(
    "runtime/contracts.py",
    '''
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
''',
)

write(
    "runtime/registry_base.py",
    '''
"""Base registry contract for Pack 03 runtimes.

Dependency injection only. No singleton globals.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from engines.interpretation_engine.exceptions.interpretation_error import (
    InterpretationArchitectureError,
)

T = TypeVar("T")


class RegistryError(InterpretationArchitectureError):
    """Raised for runtime registry contract failures."""


class BaseRegistry(Generic[T]):
    """In-memory DI registry with register/unregister/lookup/list/validate."""

    def __init__(self, *, registry_id: str) -> None:
        """Initialize an empty registry."""
        self.registry_id = registry_id
        self._entries: dict[str, T] = {}

    def register(self, entry_id: str, entry: T) -> None:
        """Register an entry by identifier."""
        if not entry_id:
            raise RegistryError("registry_entry_id_required")
        if entry is None:
            raise RegistryError("registry_entry_required")
        self._entries[entry_id] = entry

    def unregister(self, entry_id: str) -> None:
        """Remove an entry by identifier."""
        self._entries.pop(entry_id, None)

    def lookup(self, entry_id: str) -> T | None:
        """Lookup an entry by identifier."""
        return self._entries.get(entry_id)

    def list(self) -> tuple[str, ...]:
        """List registered entry identifiers in deterministic order."""
        return tuple(sorted(self._entries.keys()))

    def validate(self) -> bool:
        """Validate registry structural readiness."""
        return bool(self.registry_id) and all(bool(key) for key in self._entries)
''',
)

write(
    "runtime/base.py",
    '''
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
''',
)

print("core_runtime_written")
