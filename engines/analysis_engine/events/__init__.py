"""Internal Analysis Engine event framework."""

from __future__ import annotations

from engines.analysis_engine.events.dispatcher import (
    DispatchErrorPolicy,
    DispatchResult,
    EventDispatcher,
    ListenerDispatchError,
)
from engines.analysis_engine.events.event_bus import EventBus
from engines.analysis_engine.events.event_types import EventType
from engines.analysis_engine.events.events import Event, create_event, utc_now
from engines.analysis_engine.events.listeners import (
    EventHandler,
    EventListener,
    RecordingEventListener,
    TypedEventListener,
    WildcardEventListener,
)

__all__ = [
    "DispatchErrorPolicy",
    "DispatchResult",
    "Event",
    "EventBus",
    "EventDispatcher",
    "EventHandler",
    "EventListener",
    "EventType",
    "ListenerDispatchError",
    "RecordingEventListener",
    "TypedEventListener",
    "WildcardEventListener",
    "create_event",
    "utc_now",
]
