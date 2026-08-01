"""Interpreter dispatcher with priority / dependency ordering.

Parallel-ready / future-async capable design.
No asyncio implementation yet. No BaZi logic.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable

from engines.interpretation_engine.runtime.registry_base import RegistryError

logger = logging.getLogger(__name__)

InterpreterHandler = Callable[[Any], Any]


@dataclass(frozen=True, slots=True)
class DispatcherEntry:
    """Immutable dispatcher registration entry."""

    entry_id: str
    handler: InterpreterHandler
    priority: int = 100
    dependencies: tuple[str, ...] = ()
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


class InterpreterDispatcher:
    """Register and order interpreter handlers for execution."""

    def __init__(self) -> None:
        """Initialize an empty dispatcher."""
        self._entries: dict[str, DispatcherEntry] = {}

    def register(
        self,
        entry_id: str,
        handler: InterpreterHandler,
        *,
        priority: int = 100,
        dependencies: tuple[str, ...] = (),
        enabled: bool = True,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Register a handler with priority and dependencies."""
        if not entry_id:
            raise RegistryError("dispatcher_entry_id_required")
        if handler is None:
            raise RegistryError("dispatcher_handler_required")
        self._entries[entry_id] = DispatcherEntry(
            entry_id=entry_id,
            handler=handler,
            priority=priority,
            dependencies=tuple(dependencies),
            enabled=enabled,
            metadata=dict(metadata or {}),
        )

    def unregister(self, entry_id: str) -> None:
        """Remove a registered handler."""
        self._entries.pop(entry_id, None)

    def list(self) -> tuple[str, ...]:
        """List registered handler ids."""
        return tuple(sorted(self._entries.keys()))

    def execution_order(self) -> tuple[str, ...]:
        """Return deterministic execution order by dependencies then priority.

        Missing dependencies are treated as soft external refs and ignored for
        topological ordering among registered nodes.
        """
        enabled = {
            entry_id: entry
            for entry_id, entry in self._entries.items()
            if entry.enabled
        }
        indegree: dict[str, int] = {entry_id: 0 for entry_id in enabled}
        adjacency: dict[str, set[str]] = {entry_id: set() for entry_id in enabled}
        for entry_id, entry in enabled.items():
            for dep in entry.dependencies:
                if dep in enabled:
                    adjacency[dep].add(entry_id)
                    indegree[entry_id] += 1

        ready = sorted(
            [entry_id for entry_id, degree in indegree.items() if degree == 0],
            key=lambda item: (enabled[item].priority, item),
        )
        ordered: list[str] = []
        while ready:
            node = ready.pop(0)
            ordered.append(node)
            nxt: list[str] = []
            for dependent in sorted(
                adjacency[node],
                key=lambda item: (enabled[item].priority, item),
            ):
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    nxt.append(dependent)
            ready.extend(nxt)
            ready.sort(key=lambda item: (enabled[item].priority, item))

        if len(ordered) != len(enabled):
            raise RegistryError("dispatcher_circular_dependency")
        return tuple(ordered)

    def dispatch(self, context: Any) -> tuple[tuple[str, Any], ...]:
        """Execute handlers in order; returns (entry_id, result) tuples.

        Designed for future async/parallel adapters. Currently synchronous.
        """
        results: list[tuple[str, Any]] = []
        for entry_id in self.execution_order():
            entry = self._entries[entry_id]
            logger.info(
                "dispatcher_execute",
                extra={"entry_id": entry_id, "priority": entry.priority},
            )
            results.append((entry_id, entry.handler(context)))
        return tuple(results)
