"""
Pack 05 NarrativeResult models — Sprint D2.

Distinct from WP7 ``engines.narrative_engine.models.NarrativeParagraph``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ParagraphRole(str, Enum):
    """Sprint A / B paragraph roles."""

    OBSERVATION = "observation"
    EXPLANATION = "explanation"
    IMPACT = "impact"
    SUGGESTION = "suggestion"
    SUMMARY = "summary"
    OTHER = "other"


class RecommendationPriority(str, Enum):
    """Semantic recommendation priority."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ResultStatus(str, Enum):
    """NarrativeResult aggregate status."""

    COMPLETE = "complete"
    PARTIAL_INSUFFICIENT = "partial_insufficient"
    FAILED = "failed"


@dataclass(slots=True)
class NarrativeParagraph:
    """Smallest customer-facing narrative unit with full traceability."""

    id: str
    role: ParagraphRole
    text: str
    evidence_refs: tuple[str, ...] = ()
    interpretation_refs: tuple[str, ...] = ()
    rule_refs: tuple[str, ...] = ()
    knowledge_refs: tuple[str, ...] = ()
    confidence: float = 0.0
    insufficient_data: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Serialize paragraph."""
        return {
            "id": self.id,
            "role": self.role.value,
            "text": self.text,
            "evidence_refs": list(self.evidence_refs),
            "interpretation_refs": list(self.interpretation_refs),
            "rule_refs": list(self.rule_refs),
            "knowledge_refs": list(self.knowledge_refs),
            "confidence": self.confidence,
            "insufficient_data": self.insufficient_data,
        }


@dataclass(slots=True)
class NarrativeRecommendation:
    """Action-oriented narrative unit."""

    id: str
    priority: RecommendationPriority
    action: str
    reason: str = ""
    benefit: str = ""
    evidence_refs: tuple[str, ...] = ()
    interpretation_refs: tuple[str, ...] = ()
    rule_refs: tuple[str, ...] = ()
    knowledge_refs: tuple[str, ...] = ()
    insufficient_data: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Serialize recommendation."""
        return {
            "id": self.id,
            "priority": self.priority.value,
            "action": self.action,
            "reason": self.reason,
            "benefit": self.benefit,
            "evidence_refs": list(self.evidence_refs),
            "interpretation_refs": list(self.interpretation_refs),
            "rule_refs": list(self.rule_refs),
            "knowledge_refs": list(self.knowledge_refs),
            "insufficient_data": self.insufficient_data,
        }


@dataclass(slots=True)
class NarrativeSection:
    """One narrative section aligned to a Sprint B component."""

    id: str
    intent: str
    title: str
    paragraphs: tuple[NarrativeParagraph, ...] = ()
    recommendations: tuple[NarrativeRecommendation, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    interpretation_refs: tuple[str, ...] = ()
    confidence: float = 0.0
    insufficient_data: bool = False
    tone: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize section."""
        return {
            "id": self.id,
            "intent": self.intent,
            "title": self.title,
            "paragraphs": [item.to_dict() for item in self.paragraphs],
            "recommendations": [item.to_dict() for item in self.recommendations],
            "evidence_refs": list(self.evidence_refs),
            "interpretation_refs": list(self.interpretation_refs),
            "confidence": self.confidence,
            "insufficient_data": self.insufficient_data,
            "tone": self.tone,
        }


@dataclass(slots=True)
class NarrativeSummary:
    """Executive-level five commercial answers."""

    identity: str
    strengths: tuple[str, ...]
    weaknesses: tuple[str, ...]
    priority_recommendation: str
    next_action: str
    overall_confidence: float = 0.0
    insufficient_flags: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize summary."""
        return {
            "identity": self.identity,
            "strengths": list(self.strengths),
            "weaknesses": list(self.weaknesses),
            "priority_recommendation": self.priority_recommendation,
            "next_action": self.next_action,
            "overall_confidence": self.overall_confidence,
            "insufficient_flags": list(self.insufficient_flags),
        }


@dataclass(slots=True)
class NarrativeResult:
    """Aggregate root — commercial narrative output (Sprint A / D2)."""

    summary: NarrativeSummary
    sections: tuple[NarrativeSection, ...]
    recommendations: tuple[NarrativeRecommendation, ...] = ()
    confidence: float = 0.0
    status: ResultStatus = ResultStatus.PARTIAL_INSUFFICIENT
    run_id: str = ""
    source_fingerprint: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    validation_issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize NarrativeResult."""
        return {
            "summary": self.summary.to_dict(),
            "sections": [item.to_dict() for item in self.sections],
            "recommendations": [item.to_dict() for item in self.recommendations],
            "confidence": self.confidence,
            "status": self.status.value,
            "run_id": self.run_id,
            "source_fingerprint": dict(self.source_fingerprint),
            "metadata": dict(self.metadata),
            "validation_issues": list(self.validation_issues),
        }
