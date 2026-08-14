"""Useful God interpretation result contract (Sprint B1)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class UsefulGodCandidateScoreEvidence:
    """One candidate score line for explainability."""

    useful_god: str
    rule_id: str
    confidence: float
    rule_group: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize candidate evidence."""
        return {
            "useful_god": self.useful_god,
            "rule_id": self.rule_id,
            "confidence": self.confidence,
            "rule_group": self.rule_group,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class UsefulGodInterpretationEvidence:
    """Structured evidence — rule IDs for traceability, not customer raw JSON."""

    rule_ids: tuple[str, ...]
    selected_rule_id: str
    candidate_scores: tuple[UsefulGodCandidateScoreEvidence, ...]
    confidence: float
    engine_source: str
    matched_rules: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize evidence block."""
        return {
            "rule_ids": list(self.rule_ids),
            "selected_rule_id": self.selected_rule_id,
            "candidate_scores": [item.to_dict() for item in self.candidate_scores],
            "confidence": self.confidence,
            "engine_source": self.engine_source,
            "matched_rules": list(self.matched_rules),
        }


@dataclass(frozen=True, slots=True)
class UsefulGodDomainImpact:
    """Impact on one life domain."""

    domain: str
    text: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize one impact."""
        return {"domain": self.domain, "text": self.text}


@dataclass(frozen=True, slots=True)
class UsefulGodRecommendationGroup:
    """Structured recommendation category."""

    category: str
    items: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize recommendation group."""
        return {"category": self.category, "items": list(self.items)}


@dataclass(frozen=True, slots=True)
class UsefulGodInterpretationResult:
    """Complete structured Useful God interpretation — no HTML/markdown."""

    observations: tuple[str, ...]
    reasoning: tuple[str, ...]
    evidence: UsefulGodInterpretationEvidence
    conclusions: tuple[str, ...]
    impacts: tuple[UsefulGodDomainImpact, ...]
    recommendations: tuple[UsefulGodRecommendationGroup, ...]
    warnings: tuple[str, ...]
    confidence: float
    diagnostics: tuple[str, ...]
    status: DataAvailability = DataAvailability.AVAILABLE
    domain: str = "useful_god"

    def to_dict(self) -> dict[str, Any]:
        """Serialize interpretation result."""
        return {
            "domain": self.domain,
            "status": self.status.value,
            "observations": list(self.observations),
            "reasoning": list(self.reasoning),
            "evidence": self.evidence.to_dict(),
            "conclusions": list(self.conclusions),
            "impacts": [item.to_dict() for item in self.impacts],
            "recommendations": [item.to_dict() for item in self.recommendations],
            "warnings": list(self.warnings),
            "confidence": self.confidence,
            "diagnostics": list(self.diagnostics),
        }
