"""Shared confidence type aliases, literals, and typed dicts."""

from __future__ import annotations

from typing import Literal, TypedDict, TypeAlias

ConfidenceValue: TypeAlias = float
ConfidencePercent: TypeAlias = float

ConfidenceBand = Literal["very_low", "low", "medium", "high", "very_high"]


class ConfidencePayload(TypedDict):
    """Confidence payload contract."""

    value: ConfidenceValue
    band: ConfidenceBand
    unit: Literal["ratio", "percent"]
