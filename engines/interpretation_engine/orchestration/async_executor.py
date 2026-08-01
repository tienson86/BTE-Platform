"""Future-async execution adapter for Pack 03 pipeline.

Parallel-ready / async-capable design.
No asyncio implementation yet — synchronous fallback only.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Mapping, Sequence

from engines.interpretation_engine.orchestration.error_isolation import (
    ErrorIsolator,
    IsolatedExecutionResult,
)

logger = logging.getLogger(__name__)


class ExecutionMode(str, Enum):
    """Execution modes supported by the async-ready executor."""

    ORDERED = "ordered"
    DEPENDENCY = "dependency"
    FUTURE_ASYNC = "future_async"


@dataclass(frozen=True, slots=True)
class AsyncExecutionPlan:
    """Immutable plan describing how entries should execute.

    ``future_async`` mode is reserved; currently falls back to ordered sync.
    """

    mode: ExecutionMode = ExecutionMode.ORDERED
    entry_ids: tuple[str, ...] = ()
    allow_parallel: bool = False
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate plan structural integrity."""
        return self.mode in ExecutionMode


class FutureAsyncExecutor:
    """Async-ready executor facade.

    Currently executes synchronously in declared order.
    Designed so a future asyncio/parallel adapter can replace ``_execute_sync``.
    """

    def __init__(self, *, isolator: ErrorIsolator | None = None) -> None:
        """Initialize with optional error isolator."""
        self._isolator = isolator or ErrorIsolator()

    def execute(
        self,
        plan: AsyncExecutionPlan,
        callbacks: Mapping[str, Callable[[], Any]],
    ) -> tuple[IsolatedExecutionResult, ...]:
        """Execute callbacks according to plan (sync fallback for all modes)."""
        if not plan.validate():
            return ()
        ordered_ids = plan.entry_ids or tuple(callbacks.keys())
        if plan.mode is ExecutionMode.FUTURE_ASYNC:
            logger.info(
                "future_async_fallback_sync",
                extra={
                    "entry_count": len(ordered_ids),
                    "allow_parallel": plan.allow_parallel,
                },
            )
        return self._execute_sync(ordered_ids, callbacks)

    def _execute_sync(
        self,
        ordered_ids: Sequence[str],
        callbacks: Mapping[str, Callable[[], Any]],
    ) -> tuple[IsolatedExecutionResult, ...]:
        """Synchronous ordered execution with error isolation."""
        entries: list[tuple[str, Callable[[], Any]]] = []
        for entry_id in ordered_ids:
            callback = callbacks.get(entry_id)
            if callback is None:
                continue
            entries.append((entry_id, callback))
        return self._isolator.run_many(tuple(entries))
