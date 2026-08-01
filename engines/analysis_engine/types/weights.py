"""Shared weight type aliases, literals, and typed dicts."""

from __future__ import annotations

from typing import Literal, TypedDict, TypeAlias

WeightValue: TypeAlias = float
NormalizedWeight: TypeAlias = float

WeightUnit = Literal["absolute", "normalized", "percent"]


class WeightPayload(TypedDict):
    """Weight payload contract."""

    value: WeightValue
    unit: WeightUnit
    dimension: str
