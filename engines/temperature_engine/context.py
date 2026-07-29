"""Temperature Engine context."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class TemperatureContext:
    """Normalized context for temperature rule matching."""

    day_master: str | None = None
    day_master_element: str | None = None
    day_master_yin_yang: str | None = None

    month_stem: str | None = None
    month_branch: str | None = None
    month_branch_element: str | None = None
    month_branch_ten_god: str | None = None

    season: str | None = None
    season_phase: str | None = None
    climate_type: str | None = None

    dryness_level: str | None = None
    humidity_level: str | None = None

    fire_count: int = 0
    water_count: int = 0
    earth_count: int = 0
    wood_count: int = 0
    metal_count: int = 0

    element_distribution: dict[str, int] = field(default_factory=dict)
    ten_gods_list: list[str] = field(default_factory=list)

    strength_level: str | None = None
    strength_score: float = 0.0

    warm_score: float = 0.0
    cold_score: float = 0.0
    dry_score: float = 0.0
    humid_score: float = 0.0
    temperature_score: float = 0.0

    metadata: dict[str, Any] = field(default_factory=dict)
    source_bazi: Any = None
