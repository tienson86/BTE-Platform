"""Ten Gods analyzer model skeletons."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class TenGodsAnalyzerInput:
    """Input contract for the Ten Gods analyzer."""

    context_id: str
    chart_id: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TenGodsAnalyzerResult:
    """Result contract for the Ten Gods analyzer."""

    analyzer_id: str
    success: bool
    payload: dict[str, Any] = field(default_factory=dict)
    messages: tuple[str, ...] = ()
