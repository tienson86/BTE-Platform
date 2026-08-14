"""Luck / Da Yun analytical truth facts for interpretation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.ownership import DOMAIN_OWNERS
from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class LuckCycleFact:
    """One Da Yun cycle from LuckEngine — no career prose."""

    gan_zhi: str
    year_start: int | None
    year_end: int | None
    age_start: int | None
    age_end: int | None
    is_current: bool
    index: int

    def to_dict(self) -> dict[str, Any]:
        """Serialize one luck cycle."""
        return {
            "gan_zhi": self.gan_zhi,
            "year_start": self.year_start,
            "year_end": self.year_end,
            "age_start": self.age_start,
            "age_end": self.age_end,
            "is_current": self.is_current,
            "index": self.index,
        }


@dataclass(frozen=True, slots=True)
class LuckInterpretationFacts:
    """Structured luck truth — owned by LuckEngine."""

    available: bool
    direction: str
    start_age: int | None
    current_cycle: LuckCycleFact | None
    cycles: tuple[LuckCycleFact, ...]
    status: DataAvailability
    owner: str = DOMAIN_OWNERS["luck"]
    diagnostics: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize luck facts."""
        return {
            "available": self.available,
            "direction": self.direction,
            "start_age": self.start_age,
            "current_cycle": self.current_cycle.to_dict() if self.current_cycle else None,
            "cycles": [item.to_dict() for item in self.cycles],
            "status": self.status.value,
            "owner": self.owner,
            "diagnostics": list(self.diagnostics),
        }
