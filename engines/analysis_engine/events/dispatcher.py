"""Internal Analysis Engine event dispatcher."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from engines.analysis_engine.events.events import Event
from engines.analysis_engine.events.listeners import EventListener
from engines.analysis_engine.exceptions.runtime_error import AnalysisRuntimeError


class DispatchErrorPolicy(str, Enum):
    """Error handling policy for internal event dispatch."""

    CONTINUE = "continue"
    FAIL_FAST = "fail_fast"


@dataclass(frozen=True, slots=True)
class ListenerDispatchError:
    """Record of a listener failure during dispatch."""

    listener_id: str
    event_id: str
    error_type: str
    message: str


@dataclass(frozen=True, slots=True)
class DispatchResult:
    """Immutable result of an internal event dispatch."""

    event_id: str
    event_type: str
    notified_listener_ids: tuple[str, ...] = ()
    skipped_listener_ids: tuple[str, ...] = ()
    errors: tuple[ListenerDispatchError, ...] = ()
    success: bool = True

    @property
    def notified_count(self) -> int:
        """Return the number of successfully notified listeners."""
        return len(self.notified_listener_ids)


class EventDispatcher:
    """Synchronous in-process dispatcher for internal runtime events.

    Invokes matching listeners in subscription order.
    Does not use external queues, brokers, or network messaging.
    """

    def __init__(
        self,
        *,
        error_policy: DispatchErrorPolicy = DispatchErrorPolicy.CONTINUE,
    ) -> None:
        """Initialize dispatcher with an error policy."""
        self._error_policy = error_policy

    @property
    def error_policy(self) -> DispatchErrorPolicy:
        """Return the active dispatch error policy."""
        return self._error_policy

    def dispatch(
        self,
        event: Event,
        listeners: tuple[EventListener, ...],
    ) -> DispatchResult:
        """Dispatch an event to matching listeners synchronously."""
        notified: list[str] = []
        skipped: list[str] = []
        errors: list[ListenerDispatchError] = []

        for listener in listeners:
            listener_id = listener.listener_id()
            if not listener.handles(event.event_type):
                skipped.append(listener_id)
                continue
            try:
                listener.on_event(event)
            except Exception as exc:  # noqa: BLE001 - dispatch boundary
                errors.append(
                    ListenerDispatchError(
                        listener_id=listener_id,
                        event_id=event.event_id,
                        error_type=type(exc).__name__,
                        message=str(exc),
                    )
                )
                if self._error_policy == DispatchErrorPolicy.FAIL_FAST:
                    result = DispatchResult(
                        event_id=event.event_id,
                        event_type=event.event_type.value,
                        notified_listener_ids=tuple(notified),
                        skipped_listener_ids=tuple(skipped),
                        errors=tuple(errors),
                        success=False,
                    )
                    raise AnalysisRuntimeError(
                        f"event_dispatch_failed:{listener_id}:{event.event_id}"
                    ) from exc
                continue
            notified.append(listener_id)

        return DispatchResult(
            event_id=event.event_id,
            event_type=event.event_type.value,
            notified_listener_ids=tuple(notified),
            skipped_listener_ids=tuple(skipped),
            errors=tuple(errors),
            success=not errors,
        )
