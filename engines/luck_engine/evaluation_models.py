"""
Immutable Luck evaluation result models (Sprint 4.2).

Evaluations describe analysis outcomes only — they never mutate
provider runtime pillars or RuleContext.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

# Canonical status when no knowledge/business rule is defined yet.
UNKNOWN = "UNKNOWN"
NO_BUSINESS_RULE = "no_business_rule_defined"


def _freeze_mapping(data: Mapping[str, Any] | None) -> Mapping[str, Any]:
    """Return a read-only mapping view."""
    if data is None:
        return MappingProxyType({})
    if isinstance(data, MappingProxyType):
        return data
    return MappingProxyType(dict(data))


@dataclass(frozen=True, slots=True)
class SupportEvaluation:
    """Result of SupportEvaluator (hành/thần hỗ trợ)."""

    elements: tuple[str, ...] = ()
    level: str | None = UNKNOWN
    reasons: tuple[str, ...] = ()
    confidence: float | None = None
    reason: str | None = NO_BUSINESS_RULE
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze nested collections."""
        object.__setattr__(self, "elements", tuple(self.elements or ()))
        object.__setattr__(self, "reasons", tuple(self.reasons or ()))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Serialize for metadata / diagnostics."""
        return {
            "elements": list(self.elements),
            "level": self.level,
            "reasons": list(self.reasons),
            "confidence": self.confidence,
            "reason": self.reason,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class AttackEvaluation:
    """Result of AttackEvaluator (khắc / xung / hại / hình / phá)."""

    elements: tuple[str, ...] = ()
    level: str | None = UNKNOWN
    reasons: tuple[str, ...] = ()
    confidence: float | None = None
    reason: str | None = NO_BUSINESS_RULE
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze nested collections."""
        object.__setattr__(self, "elements", tuple(self.elements or ()))
        object.__setattr__(self, "reasons", tuple(self.reasons or ()))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Serialize for metadata / diagnostics."""
        return {
            "elements": list(self.elements),
            "level": self.level,
            "reasons": list(self.reasons),
            "confidence": self.confidence,
            "reason": self.reason,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class StrengthEvaluation:
    """Result of LuckStrengthEvaluator."""

    value: float | None = None
    confidence: float | None = None
    reason: str | None = NO_BUSINESS_RULE
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze metadata mapping."""
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Serialize for metadata / diagnostics."""
        return {
            "value": self.value,
            "confidence": self.confidence,
            "reason": self.reason,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class StageEvaluation:
    """Result of LuckStageEvaluator."""

    stage: str | None = UNKNOWN
    confidence: float | None = None
    reason: str | None = NO_BUSINESS_RULE
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze metadata mapping."""
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Serialize for metadata / diagnostics."""
        return {
            "stage": self.stage,
            "confidence": self.confidence,
            "reason": self.reason,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class SummaryEvaluation:
    """Result of LuckSummaryBuilder (structured summary only, not narrative)."""

    summary: str | None = None
    confidence: float | None = None
    reason: str | None = NO_BUSINESS_RULE
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze metadata mapping."""
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Serialize for metadata / diagnostics."""
        return {
            "summary": self.summary,
            "confidence": self.confidence,
            "reason": self.reason,
            "metadata": dict(self.metadata),
        }
