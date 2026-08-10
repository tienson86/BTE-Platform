"""Metric definition contract. No instrumentation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

MetricKind = Literal["counter", "histogram", "gauge", "ratio"]
MetricDomain = Literal["api", "pipeline", "system"]


@dataclass(slots=True, frozen=True)
class MetricDefinition:
    """One catalogued metric. `instrumented` is always False in Beta-3."""

    name: str
    domain: MetricDomain
    kind: MetricKind
    unit: str
    description: str
    instrumented: bool = False
    owner: str = "platform-ops"
