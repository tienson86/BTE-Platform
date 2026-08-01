"""Liuyue analyzer model skeletons."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class LiuyueAnalyzerInput:
    """Input contract for the Liuyue analyzer."""

    context_id: str
    chart_id: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class LiuyueAnalyzerResult:
    """Result contract for the Liuyue analyzer."""

    analyzer_id: str
    success: bool
    payload: dict[str, Any] = field(default_factory=dict)
    messages: tuple[str, ...] = ()
