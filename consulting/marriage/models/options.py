"""Resolved consultation options. Flags only."""

from __future__ import annotations

from dataclasses import dataclass

from consulting.marriage.models.timing import MarriageLuckWindow


@dataclass(slots=True)
class ResolvedMarriageOptions:
    """Resolved options after validation. Values are not inferred here."""

    include_luck: bool | None = None
    luck_window: MarriageLuckWindow | None = None
    include_shen_sha: bool | None = None
    include_feng_shui_reference: bool | None = None
    narrative_level: str | None = None
    language: str | None = None
    audience: str | None = None
    reading_level: str | None = None
    expert_mode: bool | None = None
