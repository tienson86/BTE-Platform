"""Internal Analysis Engine event listeners."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Iterable

from engines.analysis_engine.events.event_types import EventType
from engines.analysis_engine.events.events import Event

EventHandler = Callable[[Event], None]


class EventListener(ABC):
    """Public listener contract for internal runtime events."""

    @abstractmethod
    def listener_id(self) -> str:
        """Return a stable listener identifier."""

    @abstractmethod
    def handles(self, event_type: EventType) -> bool:
        """Return True when this listener accepts the event type."""

    @abstractmethod
    def on_event(self, event: Event) -> None:
        """Handle a single internal runtime event."""


class TypedEventListener(EventListener):
    """Listener that accepts an explicit set of event types."""

    def __init__(
        self,
        listener_id: str,
        event_types: Iterable[EventType],
        handler: EventHandler,
    ) -> None:
        """Initialize a typed listener with a callable handler."""
        self._listener_id = listener_id
        self._event_types = frozenset(event_types)
        self._handler = handler

    def listener_id(self) -> str:
        """Return the listener identifier."""
        return self._listener_id

    def handles(self, event_type: EventType) -> bool:
        """Return True when the event type is in the accepted set."""
        return event_type in self._event_types

    def on_event(self, event: Event) -> None:
        """Invoke the bound handler."""
        self._handler(event)


class WildcardEventListener(EventListener):
    """Listener that accepts every internal event type."""

    def __init__(self, listener_id: str, handler: EventHandler) -> None:
        """Initialize a wildcard listener."""
        self._listener_id = listener_id
        self._handler = handler

    def listener_id(self) -> str:
        """Return the listener identifier."""
        return self._listener_id

    def handles(self, event_type: EventType) -> bool:
        """Accept all event types."""
        return True

    def on_event(self, event: Event) -> None:
        """Invoke the bound handler."""
        self._handler(event)


class RecordingEventListener(EventListener):
    """Test/debug listener that records received events in memory."""

    def __init__(
        self,
        listener_id: str = "recording_listener",
        event_types: Iterable[EventType] | None = None,
    ) -> None:
        """Initialize an empty recording listener."""
        self._listener_id = listener_id
        self._event_types = frozenset(event_types) if event_types is not None else None
        self._events: list[Event] = []

    def listener_id(self) -> str:
        """Return the listener identifier."""
        return self._listener_id

    def handles(self, event_type: EventType) -> bool:
        """Accept all types, or only the configured subset."""
        if self._event_types is None:
            return True
        return event_type in self._event_types

    def on_event(self, event: Event) -> None:
        """Record the event."""
        self._events.append(event)

    def recorded_events(self) -> tuple[Event, ...]:
        """Return recorded events in reception order."""
        return tuple(self._events)

    def clear(self) -> None:
        """Clear recorded events."""
        self._events.clear()
