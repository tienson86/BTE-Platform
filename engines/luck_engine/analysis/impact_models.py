"""Canonical analytical impact models. Not fortune scores."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.luck_engine.analysis_constants import ANALYSIS_VERSION


@dataclass(frozen=True, slots=True)
class ImpactDirection:
    """Structural influence direction. Not auspiciousness."""

    value: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize direction."""
        return {"value": self.value}


@dataclass(frozen=True, slots=True)
class ImpactScore:
    """Overlap intensity 0–100. Not a luck or fortune score."""

    value: float
    unit: str = "overlap_intensity"

    def to_dict(self) -> dict[str, Any]:
        """Serialize overlap intensity."""
        return {"value": self.value, "unit": self.unit}


@dataclass(frozen=True, slots=True)
class ImpactDelta:
    """Signed structural shift in [-1.0, 1.0]."""

    value: float

    def to_dict(self) -> dict[str, Any]:
        """Serialize delta."""
        return {"value": self.value}


@dataclass(frozen=True, slots=True)
class ImpactConfidence:
    """Completeness of upstream analytical evidence."""

    value: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize confidence."""
        return {"value": self.value}


@dataclass(frozen=True, slots=True)
class ImpactEvidence:
    """Traceable periods and consumed published fields."""

    period_ids: tuple[str, ...]
    consumed_fields: tuple[str, ...]
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize evidence."""
        return {
            "period_ids": list(self.period_ids),
            "consumed_fields": list(self.consumed_fields),
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class ImpactSummary:
    """Human-readable structural summary. No fortune wording."""

    text: str
    amplifying_count: int
    dampening_count: int
    unresolved_count: int
    period_count: int

    def to_dict(self) -> dict[str, Any]:
        """Serialize summary."""
        return {
            "text": self.text,
            "amplifying_count": self.amplifying_count,
            "dampening_count": self.dampening_count,
            "unresolved_count": self.unresolved_count,
            "period_count": self.period_count,
        }


@dataclass(frozen=True, slots=True)
class StageImpact:
    """One published impact stage payload."""

    stage_id: str
    direction: ImpactDirection
    score: ImpactScore
    delta: ImpactDelta
    confidence: ImpactConfidence
    evidence: ImpactEvidence
    summary: ImpactSummary
    analysis_version: str = ANALYSIS_VERSION

    def to_dict(self) -> dict[str, Any]:
        """Serialize one stage impact."""
        return {
            "stage_id": self.stage_id,
            "direction": self.direction.to_dict(),
            "score": self.score.to_dict(),
            "delta": self.delta.to_dict(),
            "confidence": self.confidence.to_dict(),
            "evidence": self.evidence.to_dict(),
            "summary": self.summary.to_dict(),
            "analysis_version": self.analysis_version,
        }
