"""Luck Analysis facts — production-owned luck analysis copied for Narrative."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class LuckPeriodIdentity:
    """Current Da Yun identity copied from LuckEngine. Not a luck reading."""

    gan_zhi: str
    year_start: int | None
    year_end: int | None
    is_current: bool
    label: str = ""
    stem: str = ""
    branch: str = ""
    element: str = ""
    yin_yang: str = ""
    ten_god: str = ""
    hidden_stems: tuple[str, ...] = ()
    age_start: int | None = None
    age_end: int | None = None
    index: int | None = None
    direction: str = ""
    next_gan_zhi: str = ""
    next_label: str = ""
    support_level: str = ""
    attack_level: str = ""
    luck_stage: str = ""
    luck_strength: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize period identity plus already-published evaluation slots."""
        return {
            "gan_zhi": self.gan_zhi,
            "year_start": self.year_start,
            "year_end": self.year_end,
            "is_current": self.is_current,
            "label": self.label,
            "stem": self.stem,
            "branch": self.branch,
            "element": self.element,
            "yin_yang": self.yin_yang,
            "ten_god": self.ten_god,
            "hidden_stems": list(self.hidden_stems),
            "age_start": self.age_start,
            "age_end": self.age_end,
            "index": self.index,
            "direction": self.direction,
            "next_gan_zhi": self.next_gan_zhi,
            "next_label": self.next_label,
            "support_level": self.support_level,
            "attack_level": self.attack_level,
            "luck_stage": self.luck_stage,
            "luck_strength": self.luck_strength,
        }


@dataclass(frozen=True, slots=True)
class LuckGoverningRole:
    """One already-published governor. Natal or period-owned. Not inferred."""

    name: str
    owner: str
    field: str
    scope: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize one governing role."""
        return {
            "name": self.name,
            "owner": self.owner,
            "field": self.field,
            "scope": self.scope,
        }


@dataclass(frozen=True, slots=True)
class LuckAnalysisRelation:
    """Helpful or pressure relation copied from LuckEngine evaluation."""

    identities: tuple[str, ...]
    level: str
    polarity: str
    source: str
    evidence_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize one production relation."""
        return {
            "identities": list(self.identities),
            "level": self.level,
            "polarity": self.polarity,
            "source": self.source,
            "evidence_ids": list(self.evidence_ids),
        }


@dataclass(frozen=True, slots=True)
class LuckAnalysisDirection:
    """Natal operating direction still in force. Not a new Useful God."""

    identities: tuple[str, ...]
    source: str
    evidence_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize a copied natal direction."""
        return {
            "identities": list(self.identities),
            "source": self.source,
            "evidence_ids": list(self.evidence_ids),
        }


@dataclass(frozen=True, slots=True)
class LuckAnalysisFacts:
    """Canonical Luck Analysis — facts only, no prose, no token-overlap meaning."""

    current_period_identity: LuckPeriodIdentity | None
    governing_roles: tuple[LuckGoverningRole, ...]
    helpful_relations: tuple[LuckAnalysisRelation, ...]
    pressure_relations: tuple[LuckAnalysisRelation, ...]
    supported_direction: LuckAnalysisDirection
    restricted_direction: LuckAnalysisDirection
    confidence: str
    evidence: tuple[str, ...]
    diagnostics: tuple[str, ...]
    status: DataAvailability

    def to_dict(self) -> dict[str, Any]:
        """Serialize luck analysis facts."""
        return {
            "current_period_identity": (
                self.current_period_identity.to_dict()
                if self.current_period_identity is not None
                else None
            ),
            "governing_roles": [item.to_dict() for item in self.governing_roles],
            "helpful_relations": [item.to_dict() for item in self.helpful_relations],
            "pressure_relations": [item.to_dict() for item in self.pressure_relations],
            "supported_direction": self.supported_direction.to_dict(),
            "restricted_direction": self.restricted_direction.to_dict(),
            "confidence": self.confidence,
            "evidence": list(self.evidence),
            "diagnostics": list(self.diagnostics),
            "status": self.status.value,
        }
