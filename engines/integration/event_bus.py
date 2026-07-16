"""
Event Bus.

Hệ thống phát sự kiện trong Pipeline.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Callable


class EventBus:

    def __init__(self):

        self._listeners = defaultdict(list)

    def subscribe(
        self,
        event: str,
        listener: Callable,
    ) -> None:

        self._listeners[event].append(listener)

    def unsubscribe(
        self,
        event: str,
        listener: Callable,
    ) -> None:

        if listener in self._listeners[event]:

            self._listeners[event].remove(listener)

    def publish(
        self,
        event: str,
        *args,
        **kwargs,
    ) -> None:

        for listener in self._listeners.get(event, []):

            listener(
                *args,
                **kwargs,
            )

    def clear(self):

        self._listeners.clear()

    def listener_count(
        self,
        event: str,
    ) -> int:

        return len(
            self._listeners.get(event, [])
        )

    def events(self):

        return list(
            self._listeners.keys()
        )
