"""Local in-process Event Bus for Pack 03 runtime.

No external broker. Dependency Injection only. No singleton globals.
Handler failures are isolated and do not abort publish fan-out.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any

from engines.interpretation_engine.events.event_bus_interface import (
    EventHandler,
    InterpretationEventBusInterface,
)
from engines.interpretation_engine.events.event_model import RuntimeEvent, make_event
from engines.interpretation_engine.events.event_types import (
    REQUIRED_RUNTIME_EVENTS,
    InterpretationEventType,
)
logger = logging.getLogger(__name__)


class LocalEventBus(InterpretationEventBusInterface):
    """Local runtime event bus (in-process pub/sub)."""

    def __init__(self, *, bus_id: str = "local_event_bus", history_limit: int = 256) -> None:
        """Initialize an empty local event bus.

        Args:
            bus_id: Identifier for diagnostics.
            history_limit: Max retained published events for inspection/tests.
        """
        self.bus_id = bus_id
        self._history_limit = max(0, history_limit)
        self._subscribers: dict[InterpretationEventType, list[EventHandler]] = defaultdict(
            list
        )
        self._history: list[RuntimeEvent] = []

    def subscribe(
        self,
        event_type: InterpretationEventType,
        handler: EventHandler,
    ) -> None:
        """Subscribe a handler to an event type."""
        if handler is None:
            raise ValueError("event_handler_required")
        handlers = self._subscribers[event_type]
        if handler not in handlers:
            handlers.append(handler)
            logger.info(
                "event_subscribed",
                extra={"bus_id": self.bus_id, "event_type": event_type.value},
            )

    def unsubscribe(
        self,
        event_type: InterpretationEventType,
        handler: EventHandler,
    ) -> None:
        """Unsubscribe a handler from an event type."""
        handlers = self._subscribers.get(event_type)
        if not handlers:
            return
        try:
            handlers.remove(handler)
        except ValueError:
            return
        if not handlers:
            self._subscribers.pop(event_type, None)

    def publish(self, event_type: InterpretationEventType, payload: Any) -> None:
        """Publish an event to all subscribers of ``event_type``."""
        event = self._coerce_event(event_type, payload)
        self._record(event)
        for handler in list(self._subscribers.get(event_type, ())):
            try:
                handler(event_type, payload)
            except Exception as exc:  # noqa: BLE001 - handler isolation
                logger.exception(
                    "event_handler_failed",
                    extra={
                        "bus_id": self.bus_id,
                        "event_type": event_type.value,
                        "error": type(exc).__name__,
                    },
                )

    def publish_event(self, event: RuntimeEvent) -> None:
        """Publish a structured RuntimeEvent envelope."""
        if not event.validate():
            raise ValueError("runtime_event_invalid")
        self._record(event)
        for handler in list(self._subscribers.get(event.event_type, ())):
            try:
                handler(event.event_type, event)
            except Exception as exc:  # noqa: BLE001 - handler isolation
                logger.exception(
                    "event_handler_failed",
                    extra={
                        "bus_id": self.bus_id,
                        "event_type": event.event_type.value,
                        "error": type(exc).__name__,
                    },
                )

    def emit(
        self,
        event_type: InterpretationEventType,
        *,
        source: str,
        payload: dict[str, Any] | None = None,
        correlation_id: str | None = None,
    ) -> RuntimeEvent:
        """Build and publish a RuntimeEvent; return the envelope."""
        event = make_event(
            event_type,
            source=source,
            payload=payload,
            correlation_id=correlation_id,
        )
        self.publish_event(event)
        return event

    def clear(self) -> None:
        """Remove all subscribers and history."""
        self._subscribers.clear()
        self._history.clear()

    def subscriber_count(self, event_type: InterpretationEventType | None = None) -> int:
        """Return subscriber count for one type or all types."""
        if event_type is not None:
            return len(self._subscribers.get(event_type, ()))
        return sum(len(handlers) for handlers in self._subscribers.values())

    def subscribed_types(self) -> tuple[InterpretationEventType, ...]:
        """Return event types that currently have subscribers."""
        return tuple(sorted(self._subscribers.keys(), key=lambda item: item.value))

    def history(self) -> tuple[RuntimeEvent, ...]:
        """Return retained publish history (oldest → newest)."""
        return tuple(self._history)

    def history_of(
        self, event_type: InterpretationEventType
    ) -> tuple[RuntimeEvent, ...]:
        """Return retained history filtered by event type."""
        return tuple(item for item in self._history if item.event_type is event_type)

    def validate(self) -> bool:
        """Validate bus structural readiness."""
        return bool(self.bus_id) and self._history_limit >= 0

    def supports_required_events(self) -> bool:
        """Return True when required runtime event types are defined."""
        return all(
            isinstance(event_type, InterpretationEventType)
            for event_type in REQUIRED_RUNTIME_EVENTS
        )

    def _coerce_event(
        self,
        event_type: InterpretationEventType,
        payload: Any,
    ) -> RuntimeEvent:
        """Normalize publish input into a RuntimeEvent."""
        if isinstance(payload, RuntimeEvent):
            return payload
        if isinstance(payload, dict):
            return make_event(event_type, source=self.bus_id, payload=payload)
        return make_event(
            event_type,
            source=self.bus_id,
            payload={"value": payload},
        )

    def _record(self, event: RuntimeEvent) -> None:
        """Retain event in bounded history."""
        if self._history_limit <= 0:
            return
        self._history.append(event)
        overflow = len(self._history) - self._history_limit
        if overflow > 0:
            del self._history[:overflow]


# Backward-compatible alias.
EventBus = LocalEventBus
