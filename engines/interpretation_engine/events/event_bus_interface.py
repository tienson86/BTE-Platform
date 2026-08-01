"""Event bus interface for Pack 03."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable

from engines.interpretation_engine.events.event_types import InterpretationEventType

EventHandler = Callable[[InterpretationEventType, Any], None]


class InterpretationEventBusInterface(ABC):
    """In-process event bus contract."""

    @abstractmethod
    def publish(self, event_type: InterpretationEventType, payload: Any) -> None:
        """Publish an event."""

    @abstractmethod
    def subscribe(self, event_type: InterpretationEventType, handler: EventHandler) -> None:
        """Subscribe a handler to an event type."""
