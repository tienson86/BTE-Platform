"""Interpreter priority helpers for execution ordering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from engines.interpretation_engine.interpreter_framework.interpreter_exception import (
    ConfigurationError,
)


@dataclass(frozen=True, slots=True)
class InterpreterPriority:
    """Priority value for an interpreter (lower runs first)."""

    interpreter_id: str
    priority: int

    def validate(self) -> bool:
        """Validate priority record."""
        return bool(self.interpreter_id) and isinstance(self.priority, int)


def sort_by_priority(
    priorities: Sequence[InterpreterPriority],
) -> tuple[InterpreterPriority, ...]:
    """Return priorities sorted by priority then interpreter_id."""
    return tuple(
        sorted(priorities, key=lambda item: (item.priority, item.interpreter_id))
    )


def order_ids_by_priority(
    priority_map: Mapping[str, int],
    *,
    ids: Iterable[str] | None = None,
) -> tuple[str, ...]:
    """Order interpreter ids by priority map (lower first)."""
    selected = list(ids) if ids is not None else list(priority_map.keys())
    missing = [item for item in selected if item not in priority_map]
    if missing:
        raise ConfigurationError(
            f"missing priority for interpreters: {', '.join(sorted(missing))}"
        )
    return tuple(sorted(selected, key=lambda item: (priority_map[item], item)))
