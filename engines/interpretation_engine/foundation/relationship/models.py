"""Core models for Relationship Reasoning Framework.

Relationship describes interaction. It does not select a winner and does
not evaluate a condition/state. Meaning is a knowledge seam, not reasoning.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.knowledge.domain_classes import (
    INTERPRETATION_CLASS_RELATIONSHIP,
)
from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class RelationshipNode:
    """One participant in a relationship graph."""

    node_id: str
    kind: str = ""
    label: str = ""
    source: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize node."""
        return {
            "node_id": self.node_id,
            "kind": self.kind,
            "label": self.label,
            "source": self.source,
        }


@dataclass(frozen=True, slots=True)
class RelationshipEdge:
    """Directed semantic link between two participants.

    Preserves graph fields for later traversal. No graph algorithm runs here.
    """

    edge_id: str
    source: str
    target: str
    relationship_type: str
    direction: str = "source_to_target"
    strength: float = 0.0
    weight: float | None = None
    confidence: float = 0.0
    rule_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    fact_refs: tuple[str, ...] = ()
    knowledge_key: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize edge."""
        return {
            "edge_id": self.edge_id,
            "source": self.source,
            "target": self.target,
            "relationship_type": self.relationship_type,
            "direction": self.direction,
            "strength": self.strength,
            "weight": self.weight,
            "confidence": self.confidence,
            "rule_ids": list(self.rule_ids),
            "evidence_ids": list(self.evidence_ids),
            "conditions": list(self.conditions),
            "fact_refs": list(self.fact_refs),
            "knowledge_key": self.knowledge_key,
        }


@dataclass(frozen=True, slots=True)
class RelationshipGraph:
    """Node/edge container. Adjacency is stored; traversal algorithms are not."""

    nodes: tuple[RelationshipNode, ...]
    edges: tuple[RelationshipEdge, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize graph."""
        return {
            "nodes": [item.to_dict() for item in self.nodes],
            "edges": [item.to_dict() for item in self.edges],
        }

    def get_node(self, node_id: str) -> RelationshipNode | None:
        """Return one node by id."""
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None

    def edges_from(self, node_id: str) -> tuple[RelationshipEdge, ...]:
        """Return outgoing edges. Not a search algorithm."""
        return tuple(edge for edge in self.edges if edge.source == node_id)

    def edges_to(self, node_id: str) -> tuple[RelationshipEdge, ...]:
        """Return incoming edges. Not a search algorithm."""
        return tuple(edge for edge in self.edges if edge.target == node_id)


@dataclass(frozen=True, slots=True)
class RelationshipEvidence:
    """Traceable upstream evidence for one relationship claim."""

    evidence_id: str
    source_engine: str
    source_field: str
    rule_id: str
    fact: str
    value: str
    confidence: float
    relevance: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize evidence."""
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
class RelationshipMeaning:
    """Knowledge-layer meaning of a relationship. Not computed by reasoning."""

    statement: str
    evidence_ids: tuple[str, ...]
    knowledge_key: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize meaning."""
        return {
            "statement": self.statement,
            "evidence_ids": list(self.evidence_ids),
            "knowledge_key": self.knowledge_key,
        }


@dataclass(frozen=True, slots=True)
class RelationshipApplication:
    """Knowledge-layer application of a relationship. Not computed by reasoning."""

    area: str
    statement: str
    evidence_ids: tuple[str, ...]
    confidence: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Serialize application."""
        return {
            "area": self.area,
            "statement": self.statement,
            "evidence_ids": list(self.evidence_ids),
            "confidence": self.confidence,
        }


@dataclass(frozen=True, slots=True)
class RelationshipWarning:
    """Knowledge-layer warning tied to a relationship. Not computed by reasoning."""

    condition: str
    risk: str
    mitigation: str
    evidence_ids: tuple[str, ...]
    severity: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize warning."""
        return {
            "condition": self.condition,
            "risk": self.risk,
            "mitigation": self.mitigation,
            "evidence_ids": list(self.evidence_ids),
            "severity": self.severity,
        }


@dataclass(frozen=True, slots=True)
class RelationshipMetrics:
    """Machine-readable relationship explainability metrics."""

    node_count: int
    edge_count: int
    supported_relationships: int
    unsupported_relationships: int
    evidence_coverage: float

    def to_dict(self) -> dict[str, Any]:
        """Serialize metrics."""
        return {
            "node_count": self.node_count,
            "edge_count": self.edge_count,
            "supported_relationships": self.supported_relationships,
            "unsupported_relationships": self.unsupported_relationships,
            "evidence_coverage": self.evidence_coverage,
        }


@dataclass(frozen=True, slots=True)
class RelationshipRecord:
    """One upstream analytical relationship — copied, not invented."""

    source: str
    target: str
    relationship_type: str
    direction: str = "source_to_target"
    strength: float = 0.0
    conditions: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    rule_ids: tuple[str, ...] = ()
    confidence: float = 0.0
    weight: float | None = None
    source_kind: str = ""
    target_kind: str = ""
    source_label: str = ""
    target_label: str = ""
    record_id: str = ""
    fact_refs: tuple[str, ...] = ()
    knowledge_key: str = ""
    source_origin: str = ""
    target_origin: str = ""


@dataclass(frozen=True, slots=True)
class RelationshipInput:
    """Structured upstream input for RelationshipExplainer.explain()."""

    domain: str
    records: tuple[RelationshipRecord, ...]
    evidence: tuple[RelationshipEvidence, ...] = ()
    meaning: tuple[RelationshipMeaning, ...] = ()
    applications: tuple[RelationshipApplication, ...] = ()
    warnings: tuple[RelationshipWarning, ...] = ()
    confidence: float | None = None


@dataclass(frozen=True, slots=True)
class RelationshipAssessment:
    """Canonical relationship reasoning result.

    No winner. No state classification. Graph plus evidence and a knowledge seam.
    """

    domain: str
    graph: RelationshipGraph
    evidence: tuple[RelationshipEvidence, ...]
    meaning: tuple[RelationshipMeaning, ...]
    applications: tuple[RelationshipApplication, ...]
    warnings: tuple[RelationshipWarning, ...]
    confidence: float
    diagnostics: tuple[str, ...]
    status: DataAvailability
    interpretation_class: str = INTERPRETATION_CLASS_RELATIONSHIP
    relationship_type: str = ""
    direction: str = ""
    strength: float = 0.0
    conditions: tuple[str, ...] = ()
    rule_ids: tuple[str, ...] = ()
    metrics: RelationshipMetrics | None = None

    @property
    def participants(self) -> tuple[RelationshipNode, ...]:
        """Participant nodes in the relationship graph."""
        return self.graph.nodes

    def to_dict(self) -> dict[str, Any]:
        """Serialize assessment without generating customer prose."""
        return {
            "domain": self.domain,
            "interpretation_class": self.interpretation_class,
            "participants": [item.to_dict() for item in self.participants],
            "relationship_type": self.relationship_type,
            "direction": self.direction,
            "strength": self.strength,
            "conditions": list(self.conditions),
            "rule_ids": list(self.rule_ids),
            "graph": self.graph.to_dict(),
            "evidence": [item.to_dict() for item in self.evidence],
            "meaning": [item.to_dict() for item in self.meaning],
            "applications": [item.to_dict() for item in self.applications],
            "warnings": [item.to_dict() for item in self.warnings],
            "confidence": self.confidence,
            "diagnostics": list(self.diagnostics),
            "status": self.status.value,
            "metrics": self.metrics.to_dict() if self.metrics else None,
        }
