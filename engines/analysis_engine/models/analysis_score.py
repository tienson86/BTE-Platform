"""Analysis score model skeleton."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AnalysisScore:
    """Score value contract for analysis outputs."""

    score_id: str
    dimension: str
    value: float
    unit: str | None = None
