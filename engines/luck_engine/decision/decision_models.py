"""Canonical Luck Decision models. Structured data only — no interpretation prose."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.luck_engine.decision_constants import (
    CONFIDENCE_NONE,
    DECISION_VERSION,
    IMPACT_OUTPUT_KEYS,
)


@dataclass(frozen=True, slots=True)
class OpportunityScore:
    """Normalized opportunity index 0–100 from amplifying overlap."""

    value: float
    unit: str = "opportunity_index"

    def to_dict(self) -> dict[str, Any]:
        """Serialize opportunity score."""
        return {"value": self.value, "unit": self.unit}


@dataclass(frozen=True, slots=True)
class RiskScore:
    """Normalized risk index 0–100 from dampening overlap."""

    value: float
    unit: str = "risk_index"

    def to_dict(self) -> dict[str, Any]:
        """Serialize risk score."""
        return {"value": self.value, "unit": self.unit}


@dataclass(frozen=True, slots=True)
class DecisionPriority:
    """Priority class. Not a narrative recommendation."""

    value: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize priority."""
        return {"value": self.value}


@dataclass(frozen=True, slots=True)
class DecisionConfidence:
    """Decision confidence from upstream completeness."""

    value: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize confidence."""
        return {"value": self.value}


@dataclass(frozen=True, slots=True)
class DecisionEvidence:
    """Machine-readable evidence pointers."""

    impact_keys: tuple[str, ...]
    consumed_fields: tuple[str, ...]
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize evidence."""
        return {
            "impact_keys": list(self.impact_keys),
            "consumed_fields": list(self.consumed_fields),
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class DecisionSummary:
    """Numeric summary. No consultant wording."""

    opportunity_value: float
    risk_value: float
    priority_value: str
    confidence_value: str
    impact_count: int

    def to_dict(self) -> dict[str, Any]:
        """Serialize summary."""
        return {
            "opportunity_value": self.opportunity_value,
            "risk_value": self.risk_value,
            "priority_value": self.priority_value,
            "confidence_value": self.confidence_value,
            "impact_count": self.impact_count,
        }


@dataclass(frozen=True, slots=True)
class DecisionReason:
    """Structured reason token. Not interpretive text."""

    code: str
    consumed: tuple[str, ...]
    value: str | float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize one reason token."""
        return {
            "code": self.code,
            "consumed": list(self.consumed),
            "value": self.value,
        }


def iter_stage_impacts(luck_analysis: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Return LE-2 impact payloads in canonical key order."""
    impacts: list[dict[str, Any]] = []
    for key in IMPACT_OUTPUT_KEYS:
        payload = luck_analysis.get(key)
        if isinstance(payload, Mapping):
            impacts.append(dict(payload))
    return impacts


def mean_or_zero(values: list[float]) -> float:
    """Return rounded arithmetic mean or 0.0."""
    if not values:
        return 0.0
    return round(sum(values) / len(values), 4)


def min_confidence(values: list[str]) -> str:
    """Return the lowest confidence label."""
    rank = {"none": 0, "low": 1, "medium": 2, "high": 3}
    if not values:
        return CONFIDENCE_NONE
    return min(values, key=lambda item: rank.get(item, 0))


def extract_score_delta(impact: Mapping[str, Any]) -> tuple[float, float]:
    """Read overlap score and delta from an LE-2 impact payload."""
    score_block = impact.get("score") if isinstance(impact.get("score"), Mapping) else {}
    delta_block = impact.get("delta") if isinstance(impact.get("delta"), Mapping) else {}
    score = float(score_block.get("value") or 0.0)
    delta = float(delta_block.get("value") or 0.0)
    return score, delta


def decision_version() -> str:
    """Return this engine generation."""
    return DECISION_VERSION
