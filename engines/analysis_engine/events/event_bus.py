"""Internal Analysis Engine event bus."""

from __future__ import annotations

from typing import Any, Mapping

from engines.analysis_engine.events.dispatcher import (
    DispatchErrorPolicy,
    DispatchResult,
    EventDispatcher,
)
from engines.analysis_engine.events.event_types import EventType
from engines.analysis_engine.events.events import Event, create_event
from engines.analysis_engine.events.listeners import EventListener
from engines.analysis_engine.exceptions.runtime_error import AnalysisRuntimeError


class EventBus:
    """In-process publish/subscribe bus for Analysis Engine runtime events.

    Internal runtime only. No external messaging systems.
    """

    def __init__(
        self,
        *,
        dispatcher: EventDispatcher | None = None,
        error_policy: DispatchErrorPolicy = DispatchErrorPolicy.CONTINUE,
    ) -> None:
        """Initialize an empty event bus."""
        self._listeners: list[EventListener] = []
        self._dispatcher = dispatcher or EventDispatcher(error_policy=error_policy)
        self._history: list[Event] = []
        self._record_history = True

    @property
    def listener_count(self) -> int:
        """Return the number of subscribed listeners."""
        return len(self._listeners)

    def subscribe(self, listener: EventListener) -> None:
        """Subscribe a listener. Duplicate listener ids are rejected."""
        listener_id = listener.listener_id()
        if any(item.listener_id() == listener_id for item in self._listeners):
            raise AnalysisRuntimeError(f"event_listener_already_subscribed:{listener_id}")
        self._listeners.append(listener)

    def unsubscribe(self, listener_id: str) -> bool:
        """Unsubscribe a listener by identifier. Return True if removed."""
        before = len(self._listeners)
        self._listeners = [
            listener
            for listener in self._listeners
            if listener.listener_id() != listener_id
        ]
        return len(self._listeners) < before

    def clear_listeners(self) -> None:
        """Remove all subscribed listeners."""
        self._listeners.clear()

    def publish(self, event: Event) -> DispatchResult:
        """Publish an event to matching listeners synchronously."""
        if self._record_history:
            self._history.append(event)
        return self._dispatcher.dispatch(event, tuple(self._listeners))

    def emit(
        self,
        event_type: EventType,
        *,
        source: str,
        payload: Mapping[str, Any] | None = None,
        correlation_id: str | None = None,
        pipeline_id: str | None = None,
        context_id: str | None = None,
        result_id: str | None = None,
    ) -> DispatchResult:
        """Create and publish an internal event in one step."""
        event = create_event(
            event_type,
            source=source,
            payload=payload,
            correlation_id=correlation_id,
            pipeline_id=pipeline_id,
            context_id=context_id,
            result_id=result_id,
        )
        return self.publish(event)

    def history(self) -> tuple[Event, ...]:
        """Return published events in emission order."""
        return tuple(self._history)

    def clear_history(self) -> None:
        """Clear published event history."""
        self._history.clear()

    def set_record_history(self, enabled: bool) -> None:
        """Enable or disable in-memory event history recording."""
        self._record_history = enabled

    def listeners(self) -> tuple[EventListener, ...]:
        """Return subscribed listeners in subscription order."""
        return tuple(self._listeners)
