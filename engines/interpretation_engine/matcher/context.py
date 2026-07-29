from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class MatchContext:
    """
    Toàn bộ dữ liệu dùng để Match Rule.
    """

    chart: dict[str, Any]

    variables: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default=None):

        if key in self.variables:
            return self.variables[key]

        return self.chart.get(key, default)

    def exists(self, key: str):

        return key in self.variables or key in self.chart
