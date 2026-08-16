"""Narrative Composer V2 result models — composition, not calculation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class EvidenceNode:
    """One collected evidence item. Copied, never inferred."""

    evidence_id: str
    bundle_id: str
    bundle_kind: str
    domain: str
    kind: str
    slot: str
    statement: str
    engine_truth_ref: str
    customer_domain: str = ""
    category: str = ""
    rationale: str = ""
    condition: str = ""
    mitigation: str = ""
    confidence: float = 0.0
    importance: float = 0.0
    alias_ids: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize an evidence node."""
        return {
            "evidence_id": self.evidence_id,
            "bundle_id": self.bundle_id,
            "bundle_kind": self.bundle_kind,
            "domain": self.domain,
            "kind": self.kind,
            "slot": self.slot,
            "statement": self.statement,
            "engine_truth_ref": self.engine_truth_ref,
            "customer_domain": self.customer_domain,
            "category": self.category,
            "rationale": self.rationale,
            "condition": self.condition,
            "mitigation": self.mitigation,
            "confidence": self.confidence,
            "importance": self.importance,
            "alias_ids": list(self.alias_ids),
        }


@dataclass(frozen=True, slots=True)
class EvidenceGraph:
    """Collected evidence for one composition. No new facts."""

    nodes: tuple[EvidenceNode, ...]
    raw_count: int
    merged_count: int

    def get(self, evidence_id: str) -> EvidenceNode | None:
        """Return one node by id or alias."""
        for node in self.nodes:
            if node.evidence_id == evidence_id or evidence_id in node.alias_ids:
                return node
        return None

    def to_dict(self) -> dict[str, Any]:
        """Serialize the evidence graph."""
        return {
            "nodes": [item.to_dict() for item in self.nodes],
            "raw_count": self.raw_count,
            "merged_count": self.merged_count,
        }


@dataclass(frozen=True, slots=True)
class ReasoningChain:
    """Structured chain Fact → Evidence → Reason → Conclusion. No prose."""

    chain_id: str
    bundle_id: str
    domain: str
    fact_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    reason_id: str
    conclusion_id: str
    fact: str
    reason: str
    conclusion: str
    topic: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize a reasoning chain."""
        return {
            "chain_id": self.chain_id,
            "bundle_id": self.bundle_id,
            "domain": self.domain,
            "topic": self.topic,
            "fact_ids": list(self.fact_ids),
            "evidence_ids": list(self.evidence_ids),
            "reason_id": self.reason_id,
            "conclusion_id": self.conclusion_id,
            "fact": self.fact,
            "reason": self.reason,
            "conclusion": self.conclusion,
        }


@dataclass(frozen=True, slots=True)
class ApplicationItem:
    """Customer-domain implication. Not an outcome prediction."""

    application_id: str
    customer_domain: str
    statement: str
    evidence_ids: tuple[str, ...]
    bundle_id: str
    domain: str
    confidence: float
    importance: float

    def to_dict(self) -> dict[str, Any]:
        """Serialize an application item."""
        return {
            "application_id": self.application_id,
            "customer_domain": self.customer_domain,
            "statement": self.statement,
            "evidence_ids": list(self.evidence_ids),
            "bundle_id": self.bundle_id,
            "domain": self.domain,
            "confidence": self.confidence,
            "importance": self.importance,
        }


@dataclass(frozen=True, slots=True)
class RecommendationItem:
    """Structured recommendation copied from knowledge/decision/state/relationship."""

    recommendation_id: str
    action: str
    rationale: str
    category: str
    evidence_ids: tuple[str, ...]
    bundle_id: str
    domain: str
    customer_domain: str = ""
    confidence: float = 0.0
    importance: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Serialize a recommendation item."""
        return {
            "recommendation_id": self.recommendation_id,
            "action": self.action,
            "rationale": self.rationale,
            "category": self.category,
            "evidence_ids": list(self.evidence_ids),
            "bundle_id": self.bundle_id,
            "domain": self.domain,
            "customer_domain": self.customer_domain,
            "confidence": self.confidence,
            "importance": self.importance,
        }


@dataclass(frozen=True, slots=True)
class WarningItem:
    """Structured warning copied from knowledge/decision/state/relationship."""

    warning_id: str
    risk: str
    condition: str
    mitigation: str
    evidence_ids: tuple[str, ...]
    bundle_id: str
    domain: str
    confidence: float = 0.0
    importance: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Serialize a warning item."""
        return {
            "warning_id": self.warning_id,
            "risk": self.risk,
            "condition": self.condition,
            "mitigation": self.mitigation,
            "evidence_ids": list(self.evidence_ids),
            "bundle_id": self.bundle_id,
            "domain": self.domain,
            "confidence": self.confidence,
            "importance": self.importance,
        }


@dataclass(frozen=True, slots=True)
class NarrativeSentence:
    """One rendered sentence with full traceability. No orphans."""

    sentence_id: str
    section: str
    text: str
    evidence_ids: tuple[str, ...]
    bundle_ids: tuple[str, ...]
    engine_truth_refs: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize a narrative sentence."""
        return {
            "sentence_id": self.sentence_id,
            "section": self.section,
            "text": self.text,
            "evidence_ids": list(self.evidence_ids),
            "bundle_ids": list(self.bundle_ids),
            "engine_truth_refs": list(self.engine_truth_refs),
        }


@dataclass(frozen=True, slots=True)
class NarrativeSection:
    """One canonical narrative section."""

    name: str
    sentences: tuple[NarrativeSentence, ...]
    evidence_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize a narrative section."""
        return {
            "name": self.name,
            "sentences": [item.to_dict() for item in self.sentences],
            "evidence_ids": list(self.evidence_ids),
        }


@dataclass(frozen=True, slots=True)
class TraceabilityRecord:
    """Sentence → evidence → bundle → engine truth."""

    sentence_id: str
    text: str
    evidence_ids: tuple[str, ...]
    bundle_ids: tuple[str, ...]
    bundle_kinds: tuple[str, ...]
    engine_truth_refs: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize one traceability record."""
        return {
            "sentence_id": self.sentence_id,
            "text": self.text,
            "evidence_ids": list(self.evidence_ids),
            "bundle_ids": list(self.bundle_ids),
            "bundle_kinds": list(self.bundle_kinds),
            "engine_truth_refs": list(self.engine_truth_refs),
        }


@dataclass(frozen=True, slots=True)
class ComposerMetrics:
    """Machine-readable composition quality metrics."""

    evidence_coverage: float
    duplicate_ratio: float
    reason_coverage: float
    recommendation_coverage: float
    warning_coverage: float
    traceability_coverage: float
    evidence_count: int
    sentence_count: int
    orphan_sentence_count: int
    customer_relevance_ratio: float = 1.0
    active_chart_fact_ratio: float = 1.0
    hypothetical_knowledge_leak_count: int = 0
    duplicate_section_ratio: float = 0.0
    broken_fragment_count: int = 0
    implementation_language_count: int = 0
    recommendation_count: int = 0
    priority_recommendation_count: int = 0
    domain_paragraph_count: int = 0
    customer_narrative_word_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Serialize composer metrics."""
        return {
            "evidence_coverage": self.evidence_coverage,
            "duplicate_ratio": self.duplicate_ratio,
            "reason_coverage": self.reason_coverage,
            "recommendation_coverage": self.recommendation_coverage,
            "warning_coverage": self.warning_coverage,
            "traceability_coverage": self.traceability_coverage,
            "evidence_count": self.evidence_count,
            "sentence_count": self.sentence_count,
            "orphan_sentence_count": self.orphan_sentence_count,
            "customer_relevance_ratio": self.customer_relevance_ratio,
            "active_chart_fact_ratio": self.active_chart_fact_ratio,
            "hypothetical_knowledge_leak_count": self.hypothetical_knowledge_leak_count,
            "duplicate_section_ratio": self.duplicate_section_ratio,
            "broken_fragment_count": self.broken_fragment_count,
            "implementation_language_count": self.implementation_language_count,
            "recommendation_count": self.recommendation_count,
            "priority_recommendation_count": self.priority_recommendation_count,
            "domain_paragraph_count": self.domain_paragraph_count,
            "customer_narrative_word_count": self.customer_narrative_word_count,
        }


@dataclass(frozen=True, slots=True)
class NarrativeComposerResult:
    """Canonical V2 output: narrative sections plus composition artifacts."""

    sections: tuple[NarrativeSection, ...]
    evidence: EvidenceGraph
    reasoning_chains: tuple[ReasoningChain, ...]
    applications: tuple[ApplicationItem, ...]
    recommendations: tuple[RecommendationItem, ...]
    warnings: tuple[WarningItem, ...]
    traceability: tuple[TraceabilityRecord, ...]
    metrics: ComposerMetrics
    diagnostics: tuple[str, ...] = ()

    def section(self, name: str) -> NarrativeSection | None:
        """Return one section by canonical name."""
        for item in self.sections:
            if item.name == name:
                return item
        return None

    def to_dict(self) -> dict[str, Any]:
        """Serialize the composer result."""
        return {
            "sections": [item.to_dict() for item in self.sections],
            "evidence": self.evidence.to_dict(),
            "reasoning_chains": [item.to_dict() for item in self.reasoning_chains],
            "applications": [item.to_dict() for item in self.applications],
            "recommendations": [item.to_dict() for item in self.recommendations],
            "warnings": [item.to_dict() for item in self.warnings],
            "traceability": [item.to_dict() for item in self.traceability],
            "metrics": self.metrics.to_dict(),
            "diagnostics": list(self.diagnostics),
        }
