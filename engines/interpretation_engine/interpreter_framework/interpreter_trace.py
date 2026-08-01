"""Interpreter execution trace model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class InterpreterTraceEvent:
    """One trace event recorded during interpreter execution."""

    name: str
    detail: str = ""
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize event."""
        return {
            "name": self.name,
            "detail": self.detail,
            "attributes": dict(self.attributes),
        }


@dataclass(frozen=True, slots=True)
class InterpreterTrace:
    """Ordered execution trace for an interpreter run."""

    events: tuple[InterpreterTraceEvent, ...] = ()

    def validate(self) -> bool:
        """Validate trace events."""
        return all(bool(event.name) for event in self.events)

    def with_event(
        self,
        name: str,
        *,
        detail: str = "",
        attributes: Mapping[str, Any] | None = None,
    ) -> InterpreterTrace:
        """Return a new trace with an appended event."""
        event = InterpreterTraceEvent(
            name=name,
            detail=detail,
            attributes=dict(attributes or {}),
        )
        return InterpreterTrace(events=(*self.events, event))

    def names(self) -> tuple[str, ...]:
        """Return ordered event names."""
        return tuple(event.name for event in self.events)

    def to_dict(self) -> dict[str, Any]:
        """Serialize trace."""
        return {"events": [event.to_dict() for event in self.events]}
