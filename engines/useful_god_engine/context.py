"""Useful God Engine context."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class UsefulGodContext:
    """Normalized context used by Useful God rule matching."""

    # Core fields from PatternContext V2
    day_master: str | None = None
    day_master_element: str | None = None
    day_master_yin_yang: str | None = None

    month_branch: str | None = None
    month_branch_element: str | None = None
    month_branch_ten_god: str | None = None

    strength_level: str | None = None
    season: str | None = None
    season_phase: str | None = None
    temperature_type: str | None = None

    element_distribution: dict[str, int] = field(default_factory=dict)

    support_elements: list[str] = field(default_factory=list)
    resource_elements: list[str] = field(default_factory=list)
    wealth_elements: list[str] = field(default_factory=list)
    officer_elements: list[str] = field(default_factory=list)
    output_elements: list[str] = field(default_factory=list)
    companion_elements: list[str] = field(default_factory=list)

    follow_pattern: str | None = None
    special_pattern: str | None = None
    main_pattern: str | None = None
    ug_override_eligible: bool | None = None

    ten_gods_list: list[str] = field(default_factory=list)
    officer_provenance: list[dict[str, Any]] = field(default_factory=list)

    # Trace/debug slots
    metadata: dict[str, Any] = field(default_factory=dict)
    source_pattern_context: Any = None
