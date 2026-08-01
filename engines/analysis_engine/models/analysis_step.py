"""Analysis step model skeleton."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AnalysisStep:
    """Single pipeline step contract."""

    step_id: str
    name: str
    status: str
    order: int = 0
