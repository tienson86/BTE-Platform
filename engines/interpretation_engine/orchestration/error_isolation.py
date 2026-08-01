"""Error isolation helpers for Pack 03 execution pipeline.

Isolates per-interpreter failures so one failure does not abort the pipeline.
Infrastructure only. No BaZi logic.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class IsolatedExecutionResult:
    """Immutable result of an error-isolated callable execution."""

    entry_id: str
    success: bool
    value: Any = None
    error_type: str | None = None
    error_message: str | None = None
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate structural integrity."""
        return bool(self.entry_id)


class ErrorIsolator:
    """Execute callables with per-entry exception isolation."""

    def run(
        self,
        entry_id: str,
        callback: Callable[[], Any],
    ) -> IsolatedExecutionResult:
        """Run callback; capture exceptions without propagating."""
        try:
            value = callback()
            return IsolatedExecutionResult(
                entry_id=entry_id,
                success=True,
                value=value,
            )
        except Exception as exc:  # noqa: BLE001 - isolation boundary
            logger.exception(
                "execution_isolated_error",
                extra={"entry_id": entry_id, "error": type(exc).__name__},
            )
            return IsolatedExecutionResult(
                entry_id=entry_id,
                success=False,
                error_type=type(exc).__name__,
                error_message=str(exc),
            )

    def run_many(
        self,
        entries: tuple[tuple[str, Callable[[], Any]], ...],
    ) -> tuple[IsolatedExecutionResult, ...]:
        """Run many callbacks with isolation; preserve input order."""
        return tuple(self.run(entry_id, callback) for entry_id, callback in entries)
