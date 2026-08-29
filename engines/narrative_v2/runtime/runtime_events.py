"""Narrative V2 runtime events.

Internal tracing only. No customer-facing payload.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import time


@dataclass(frozen=True, slots=True)
class RuntimeEvent:
    """Base runtime event."""

    timestamp: float
    stage: str | None = None

    @property
    def name(self) -> str:
        """Event type name."""
        return type(self).__name__


@dataclass(frozen=True, slots=True)
class NarrativeStarted(RuntimeEvent):
    """Runtime pipeline started."""

    stage: str | None = "initialize"


@dataclass(frozen=True, slots=True)
class EvidenceStarted(RuntimeEvent):
    """Evidence stage started."""


@dataclass(frozen=True, slots=True)
class EvidenceFinished(RuntimeEvent):
    """Evidence stage finished."""


@dataclass(frozen=True, slots=True)
class ReasoningStarted(RuntimeEvent):
    """Reasoning stage started."""


@dataclass(frozen=True, slots=True)
class ReasoningFinished(RuntimeEvent):
    """Reasoning stage finished."""


@dataclass(frozen=True, slots=True)
class KnowledgeStarted(RuntimeEvent):
    """Knowledge stage started."""


@dataclass(frozen=True, slots=True)
class KnowledgeFinished(RuntimeEvent):
    """Knowledge stage finished."""


@dataclass(frozen=True, slots=True)
class RewriteStarted(RuntimeEvent):
    """Commercial rewrite stage started."""


@dataclass(frozen=True, slots=True)
class RewriteFinished(RuntimeEvent):
    """Commercial rewrite stage finished."""


@dataclass(frozen=True, slots=True)
class SummaryStarted(RuntimeEvent):
    """Summary stage started."""


@dataclass(frozen=True, slots=True)
class SummaryFinished(RuntimeEvent):
    """Summary stage finished."""


@dataclass(frozen=True, slots=True)
class InterpretationStarted(RuntimeEvent):
    """Interpretation stage started."""


@dataclass(frozen=True, slots=True)
class InterpretationFinished(RuntimeEvent):
    """Interpretation stage finished."""


@dataclass(frozen=True, slots=True)
class ActionStarted(RuntimeEvent):
    """Action stage started."""


@dataclass(frozen=True, slots=True)
class ActionFinished(RuntimeEvent):
    """Action stage finished."""


@dataclass(frozen=True, slots=True)
class CommercialStarted(RuntimeEvent):
    """Commercial stage started."""


@dataclass(frozen=True, slots=True)
class CommercialFinished(RuntimeEvent):
    """Commercial stage finished."""


@dataclass(frozen=True, slots=True)
class ValidationStarted(RuntimeEvent):
    """Validation stage started."""


@dataclass(frozen=True, slots=True)
class ValidationFinished(RuntimeEvent):
    """Validation stage finished."""


@dataclass(frozen=True, slots=True)
class PublishStarted(RuntimeEvent):
    """Publish stage started."""


@dataclass(frozen=True, slots=True)
class PublishFinished(RuntimeEvent):
    """Publish stage finished."""


@dataclass(frozen=True, slots=True)
class RuntimeFailed(RuntimeEvent):
    """Runtime entered FAILED."""


STAGE_EVENTS: dict[str, tuple[type[RuntimeEvent], type[RuntimeEvent]]] = {
    "build_evidence": (EvidenceStarted, EvidenceFinished),
    "build_reasoning": (ReasoningStarted, ReasoningFinished),
    "resolve_knowledge": (KnowledgeStarted, KnowledgeFinished),
    "commercial_rewrite": (RewriteStarted, RewriteFinished),
    "build_summary": (SummaryStarted, SummaryFinished),
    "build_interpretation": (InterpretationStarted, InterpretationFinished),
    "build_action": (ActionStarted, ActionFinished),
    "build_commercial": (CommercialStarted, CommercialFinished),
    "validate": (ValidationStarted, ValidationFinished),
    "publish": (PublishStarted, PublishFinished),
}


def now() -> float:
    """Monotonic timestamp for event and trace recording."""
    return time.perf_counter()


@dataclass(slots=True)
class EventLog:
    """In-memory runtime event log."""

    _events: list[RuntimeEvent] = field(default_factory=list)

    def emit(self, event: RuntimeEvent) -> RuntimeEvent:
        """Append an event and return it."""
        self._events.append(event)
        return event

    @property
    def events(self) -> tuple[RuntimeEvent, ...]:
        """Emitted events in order."""
        return tuple(self._events)

    @property
    def names(self) -> tuple[str, ...]:
        """Event type names in order."""
        return tuple(event.name for event in self._events)
