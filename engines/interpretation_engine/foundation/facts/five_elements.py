"""Five Elements analytical distribution facts for interpretation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.ownership import DOMAIN_OWNERS
from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class FiveElementsInterpretationFacts:
    """Structured wuxing counts — not ScoreEngine wuxing_score."""

    wood: int | None
    fire: int | None
    earth: int | None
    metal: int | None
    water: int | None
    dominant: str | None
    missing: tuple[str, ...]
    status: DataAvailability
    owner: str = DOMAIN_OWNERS["five_elements"]
    diagnostics: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize five-elements facts."""
        return {
            "wood": self.wood,
            "fire": self.fire,
            "earth": self.earth,
            "metal": self.metal,
            "water": self.water,
            "dominant": self.dominant,
            "missing": list(self.missing),
            "status": self.status.value,
            "owner": self.owner,
            "diagnostics": list(self.diagnostics),
        }
