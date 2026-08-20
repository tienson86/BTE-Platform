"""Strength Engine context."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class StrengthContext:
    """Normalized context for strength rule matching."""

    day_master: str | None = None
    day_master_element: str | None = None
    day_master_yin_yang: str | None = None

    month_stem: str | None = None
    month_branch: str | None = None
    month_branch_element: str | None = None
    month_branch_ten_god: str | None = None
    month_status: str | None = None

    root_level: str | None = None
    root_count: int = 0

    support_type: str | None = None
    control_type: str | None = None
    drain_type: str | None = None

    season: str | None = None
    season_phase: str | None = None
    temperature_type: str | None = None

    element_distribution: dict[str, int] = field(default_factory=dict)
    ten_gods_list: list[str] = field(default_factory=list)

    resource_elements: list[str] = field(default_factory=list)
    companion_elements: list[str] = field(default_factory=list)
    wealth_elements: list[str] = field(default_factory=list)
    officer_elements: list[str] = field(default_factory=list)
    output_elements: list[str] = field(default_factory=list)

    resource_count: int = 0
    companion_count: int = 0
    wealth_count: int = 0
    officer_count: int = 0
    output_count: int = 0
    drain_count: int = 0
    output_branch_count: int = 0

    # Populated during scoring pass
    season_score: float = 0.0
    root_score: float = 0.0
    support_score: float = 0.0
    drain_score: float = 0.0
    control_score: float = 0.0
    strength_score: float = 0.0

    metadata: dict[str, Any] = field(default_factory=dict)
    source_bazi: Any = None
