"""Ten Gods analytical truth facts for interpretation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.ownership import DOMAIN_OWNERS
from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class TenGodPositionFact:
    """One Ten God occurrence with position metadata."""

    name: str
    pillar: str
    stem: str
    branch: str
    visibility: str
    relation_to_day_master: str
    count: int | None = None
    weight: float | None = None
    evidence: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize one Ten God position."""
        return {
            "name": self.name,
            "pillar": self.pillar,
            "stem": self.stem,
            "branch": self.branch,
            "visibility": self.visibility,
            "relation_to_day_master": self.relation_to_day_master,
            "count": self.count,
            "weight": self.weight,
            "evidence": self.evidence,
        }


@dataclass(frozen=True, slots=True)
class TenGodInterpretationFacts:
    """Structured Ten Gods truth — owned by TenGodsEngine / BaZi."""

    visible: tuple[TenGodPositionFact, ...]
    hidden: tuple[TenGodPositionFact, ...]
    distribution: tuple[dict[str, Any], ...]
    day_master: str
    day_master_element: str
    status: DataAvailability
    owner: str = DOMAIN_OWNERS["ten_gods"]
    diagnostics: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize Ten Gods facts."""
        return {
            "visible": [item.to_dict() for item in self.visible],
            "hidden": [item.to_dict() for item in self.hidden],
            "distribution": list(self.distribution),
            "day_master": self.day_master,
            "day_master_element": self.day_master_element,
            "status": self.status.value,
            "owner": self.owner,
            "diagnostics": list(self.diagnostics),
        }
