"""Lookup registry for catalogued metrics. No exporters."""

from __future__ import annotations

from applications.metrics.metric_catalog import METRIC_CATALOG
from applications.metrics.metric_contract import MetricDefinition, MetricDomain


class MetricRegistry:
    """In-memory metric catalog index."""

    def __init__(self) -> None:
        self._items = {item.name: item for item in METRIC_CATALOG}

    def get(self, name: str) -> MetricDefinition | None:
        """Return a metric definition by name."""
        return self._items.get(name)

    def by_domain(self, domain: MetricDomain) -> tuple[MetricDefinition, ...]:
        """Return metrics for one domain."""
        return tuple(item for item in METRIC_CATALOG if item.domain == domain)

    def names(self) -> tuple[str, ...]:
        """Return all metric names."""
        return tuple(self._items.keys())

    def instrumented_count(self) -> int:
        """Return how many metrics are actually instrumented (Beta-3: 0)."""
        return sum(1 for item in self._items.values() if item.instrumented)

    def describe(self) -> dict[str, object]:
        """Return a JSON-safe catalog summary."""
        return {
            "count": len(self._items),
            "instrumented": self.instrumented_count(),
            "names": list(self.names()),
        }
