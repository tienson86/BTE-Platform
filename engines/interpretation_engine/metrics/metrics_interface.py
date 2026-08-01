"""Metrics interface for Pack 03."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping


class InterpretationMetricsInterface(ABC):
    """Metrics collection contract. Architecture only."""

    @abstractmethod
    def record(self, name: str, value: float, tags: Mapping[str, str] | None = None) -> None:
        """Record a metric sample."""

    @abstractmethod
    def snapshot(self) -> Mapping[str, Any]:
        """Return a metrics snapshot."""
