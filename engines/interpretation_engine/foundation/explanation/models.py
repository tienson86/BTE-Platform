"""Core models for Decision Explanation Framework."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class AnalysisFact:
    """One analytical condition considered in the explanation."""

    fact: str
    value: str
    source: str
    role: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize analysis fact."""
        return {
            "fact": self.fact,
            "value": self.value,
            "source": self.source,
            "role": self.role,
        }


@dataclass(frozen=True, slots=True)
class DecisionPathStep:
    """One deterministic step in the expert reasoning path."""

    step_id: str
    order: int
    title: str
    input_facts: tuple[str, ...]
    rule_refs: tuple[str, ...]
    condition: str
    outcome: str
    effect: str
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize decision path step."""
        return {
            "step_id": self.step_id,
            "order": self.order,
            "title": self.title,
            "input_facts": list(self.input_facts),
            "rule_refs": list(self.rule_refs),
            "condition": self.condition,
            "outcome": self.outcome,
            "effect": self.effect,
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class EvidenceItem:
    """Traceable evidence supporting a decision step."""

    evidence_id: str
    source_engine: str
    source_field: str
    rule_id: str
    fact: str
    value: str
    confidence: float
    relevance: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize evidence item."""
        return {
            "evidence_id": self.evidence_id,
            "source_engine": self.source_engine,
            "source_field": self.source_field,
            "rule_id": self.rule_id,
            "fact": self.fact,
            "value": self.value,
            "confidence": self.confidence,
            "relevance": self.relevance,
        }


@dataclass(frozen=True, slots=True)
class Decision:
    """Selected decision — never inferred from prose."""

    selected: str
    selected_type: str
    reason: str
    confidence: float
    supporting_evidence_ids: tuple[str, ...]
    rejected_alternatives: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize decision."""
        return {
            "selected": self.selected,
            "selected_type": self.selected_type,
            "reason": self.reason,
            "confidence": self.confidence,
            "supporting_evidence_ids": list(self.supporting_evidence_ids),
            "rejected_alternatives": list(self.rejected_alternatives),
        }


@dataclass(frozen=True, slots=True)
class DecisionAlternative:
    """Competing option with acceptance/rejection state."""

    alternative_id: str
    candidate: str
    candidate_type: str
    score: float
    priority: int
    supporting_evidence: tuple[str, ...]
    opposing_evidence: tuple[str, ...]
    rejection_reason: str
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize alternative."""
        return {
            "alternative_id": self.alternative_id,
            "candidate": self.candidate,
            "candidate_type": self.candidate_type,
            "score": self.score,
            "priority": self.priority,
            "supporting_evidence": list(self.supporting_evidence),
            "opposing_evidence": list(self.opposing_evidence),
            "rejection_reason": self.rejection_reason,
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class DomainMeaningItem:
    """Expert meaning of the selected decision within the domain."""

    statement: str
    evidence_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize domain meaning."""
        return {
            "statement": self.statement,
            "evidence_ids": list(self.evidence_ids),
        }


@dataclass(frozen=True, slots=True)
class DomainApplication:
    """Application of domain decision to a life area."""

    domain: str
    statement: str
    basis_evidence_ids: tuple[str, ...]
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        """Serialize application."""
        return {
            "domain": self.domain,
            "statement": self.statement,
            "basis_evidence_ids": list(self.basis_evidence_ids),
            "confidence": self.confidence,
        }


@dataclass(frozen=True, slots=True)
class AdviceItem:
    """Structured advice separate from analytical facts."""

    category: str
    action: str
    priority: str
    rationale: str
    evidence_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize advice item."""
        return {
            "category": self.category,
            "action": self.action,
            "priority": self.priority,
            "rationale": self.rationale,
            "evidence_ids": list(self.evidence_ids),
        }


@dataclass(frozen=True, slots=True)
class WarningItem:
    """Evidence-backed warning."""

    condition: str
    risk: str
    severity: str
    evidence_ids: tuple[str, ...]
    mitigation: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize warning item."""
        return {
            "condition": self.condition,
            "risk": self.risk,
            "severity": self.severity,
            "evidence_ids": list(self.evidence_ids),
            "mitigation": self.mitigation,
        }


@dataclass(frozen=True, slots=True)
class ExplainabilityMetrics:
    """Machine-readable explainability quality metrics."""

    fact_count: int
    decision_step_count: int
    evidence_count: int
    alternative_count: int
    evidence_coverage_ratio: float
    unsupported_decision_count: int

    def to_dict(self) -> dict[str, Any]:
        """Serialize explainability metrics."""
        return {
            "fact_count": self.fact_count,
            "decision_step_count": self.decision_step_count,
            "evidence_count": self.evidence_count,
            "alternative_count": self.alternative_count,
            "evidence_coverage_ratio": self.evidence_coverage_ratio,
            "unsupported_decision_count": self.unsupported_decision_count,
        }


@dataclass(frozen=True, slots=True)
class DecisionExplanationResult:
    """Canonical structured explanation for any domain interpreter."""

    domain: str
    status: DataAvailability
    analysis: tuple[AnalysisFact, ...]
    decision_path: tuple[DecisionPathStep, ...]
    evidence: tuple[EvidenceItem, ...]
    decision: Decision | None
    alternatives: tuple[DecisionAlternative, ...]
    domain_meaning: tuple[DomainMeaningItem, ...]
    applications: tuple[DomainApplication, ...]
    advice: tuple[AdviceItem, ...]
    warnings: tuple[WarningItem, ...]
    confidence: float
    diagnostics: tuple[str, ...]
    metrics: ExplainabilityMetrics | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize decision explanation result."""
        return {
            "domain": self.domain,
            "status": self.status.value,
            "analysis": [item.to_dict() for item in self.analysis],
            "decision_path": [item.to_dict() for item in self.decision_path],
            "evidence": [item.to_dict() for item in self.evidence],
            "decision": self.decision.to_dict() if self.decision else None,
            "alternatives": [item.to_dict() for item in self.alternatives],
            "domain_meaning": [item.to_dict() for item in self.domain_meaning],
            "applications": [item.to_dict() for item in self.applications],
            "advice": [item.to_dict() for item in self.advice],
            "warnings": [item.to_dict() for item in self.warnings],
            "confidence": self.confidence,
            "diagnostics": list(self.diagnostics),
            "metrics": self.metrics.to_dict() if self.metrics else None,
        }
