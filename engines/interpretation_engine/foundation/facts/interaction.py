"""Interaction Truth facts — relations between natal truth and current Da Yun."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class InteractionPeriodIdentity:
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

    def to_dict(self) -> dict[str, Any]:
        """Serialize period identity."""
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
        }


@dataclass(frozen=True, slots=True)
class InteractionFactor:
    """One evidenced identity overlap. Not a prediction."""

    fact_id: str
    kind: str
    natal_identity: str
    natal_owner: str
    natal_field: str
    period_identity: str
    period_field: str
    polarity: str
    evidence_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize one overlap factor."""
        return {
            "fact_id": self.fact_id,
            "kind": self.kind,
            "natal_identity": self.natal_identity,
            "natal_owner": self.natal_owner,
            "natal_field": self.natal_field,
            "period_identity": self.period_identity,
            "period_field": self.period_field,
            "polarity": self.polarity,
            "evidence_ids": list(self.evidence_ids),
        }


@dataclass(frozen=True, slots=True)
class InteractionDirection:
    """Natal operating direction still in force, with overlap qualifier."""

    identities: tuple[str, ...]
    overlap_status: str
    evidence_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize a direction fact."""
        return {
            "identities": list(self.identities),
            "overlap_status": self.overlap_status,
            "evidence_ids": list(self.evidence_ids),
        }


@dataclass(frozen=True, slots=True)
class InteractionSummary:
    """Structured relation record. Not a customer paragraph."""

    period_label: str
    pattern: str
    strength: str
    useful_god: str
    overlap_count: int
    empty_overlap: bool
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize the structured summary."""
        return {
            "period_label": self.period_label,
            "pattern": self.pattern,
            "strength": self.strength,
            "useful_god": self.useful_god,
            "overlap_count": self.overlap_count,
            "empty_overlap": self.empty_overlap,
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class InteractionTruthFacts:
    """Canonical Interaction Truth — facts only, no prose."""

    current_period_identity: InteractionPeriodIdentity | None
    interaction_summary: InteractionSummary
    helpful_factors: tuple[InteractionFactor, ...]
    pressure_factors: tuple[InteractionFactor, ...]
    supported_direction: InteractionDirection
    restricted_direction: InteractionDirection
    confidence: str
    evidence: tuple[str, ...]
    diagnostics: tuple[str, ...]
    status: DataAvailability

    def to_dict(self) -> dict[str, Any]:
        """Serialize interaction truth."""
        return {
            "current_period_identity": (
                self.current_period_identity.to_dict()
                if self.current_period_identity is not None
                else None
            ),
            "interaction_summary": self.interaction_summary.to_dict(),
            "helpful_factors": [item.to_dict() for item in self.helpful_factors],
            "pressure_factors": [item.to_dict() for item in self.pressure_factors],
            "supported_direction": self.supported_direction.to_dict(),
            "restricted_direction": self.restricted_direction.to_dict(),
            "confidence": self.confidence,
            "evidence": list(self.evidence),
            "diagnostics": list(self.diagnostics),
            "status": self.status.value,
        }
