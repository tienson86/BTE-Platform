"""Runtime stage trace. No customer payloads."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class StageTrace:
    """One stage execution record."""

    stage: str
    start_time: str
    end_time: str
    duration_ms: float
    status: str
