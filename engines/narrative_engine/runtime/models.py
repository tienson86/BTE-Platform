"""
Narrative Runtime models — Sprint D1.

Output is NarrativeTree (structural). No prose fields.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ComponentType(str, Enum):
    """Official Sprint B narrative component types."""

    EXECUTIVE_SUMMARY = "executive_summary"
    OBSERVATION = "observation"
    REASONING = "reasoning"
    IMPACT = "impact"
    RECOMMENDATION = "recommendation"
    WARNING = "warning"
    CONCLUSION = "conclusion"


class NodeStatus(str, Enum):
    """Per-node composition status (no customer wording)."""

    READY = "ready"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    BLOCKED = "blocked"
    INVALID = "invalid"


class EvidenceKind(str, Enum):
    """Evidence classification for component selection."""

    IDENTITY = "identity"
    STRENGTH = "strength"
    WEAKNESS = "weakness"
    EXPLANATION = "explanation"
    IMPLICATION = "implication"
    ACTION = "action"
    RISK = "risk"
    GRADE = "grade"
    OTHER = "other"


class TreeStatus(str, Enum):
    """Aggregate NarrativeTree status."""

    COMPLETE = "complete"
    PARTIAL_INSUFFICIENT = "partial_insufficient"
    INVALID = "invalid"


# Official published order (Sprint B).
OFFICIAL_COMPONENT_ORDER: tuple[ComponentType, ...] = (
    ComponentType.EXECUTIVE_SUMMARY,
    ComponentType.OBSERVATION,
    ComponentType.REASONING,
    ComponentType.IMPACT,
    ComponentType.RECOMMENDATION,
    ComponentType.WARNING,
    ComponentType.CONCLUSION,
)

# Flow dependencies (component → required upstream components).
COMPONENT_DEPENDENCIES: dict[ComponentType, tuple[ComponentType, ...]] = {
    ComponentType.EXECUTIVE_SUMMARY: (),
    ComponentType.OBSERVATION: (),
    ComponentType.REASONING: (ComponentType.OBSERVATION,),
    ComponentType.IMPACT: (ComponentType.OBSERVATION,),
    ComponentType.RECOMMENDATION: (),
    ComponentType.WARNING: (),
    ComponentType.CONCLUSION: (),
}

# Evidence kinds that can fill a component (non-exclusive).
COMPONENT_EVIDENCE_KINDS: dict[ComponentType, frozenset[EvidenceKind]] = {
    ComponentType.EXECUTIVE_SUMMARY: frozenset(
        {
            EvidenceKind.IDENTITY,
            EvidenceKind.STRENGTH,
            EvidenceKind.WEAKNESS,
            EvidenceKind.ACTION,
            EvidenceKind.RISK,
            EvidenceKind.GRADE,
        }
    ),
    ComponentType.OBSERVATION: frozenset(
        {
            EvidenceKind.IDENTITY,
            EvidenceKind.STRENGTH,
            EvidenceKind.GRADE,
            EvidenceKind.OTHER,
        }
    ),
    ComponentType.REASONING: frozenset({EvidenceKind.EXPLANATION}),
    ComponentType.IMPACT: frozenset({EvidenceKind.IMPLICATION}),
    ComponentType.RECOMMENDATION: frozenset({EvidenceKind.ACTION}),
    ComponentType.WARNING: frozenset({EvidenceKind.RISK, EvidenceKind.WEAKNESS}),
    ComponentType.CONCLUSION: frozenset(
        {
            EvidenceKind.IDENTITY,
            EvidenceKind.STRENGTH,
            EvidenceKind.WEAKNESS,
            EvidenceKind.ACTION,
            EvidenceKind.RISK,
            EvidenceKind.IMPLICATION,
            EvidenceKind.GRADE,
        }
    ),
}


@dataclass(slots=True)
class RuntimeEvidenceUnit:
    """One evidence unit available to the runtime (no narrative text)."""

    id: str
    kind: EvidenceKind
    confidence: float = 0.0
    source_path: str = ""
    commercial_ok: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Serialize evidence unit."""
        return {
            "id": self.id,
            "kind": self.kind.value,
            "confidence": self.confidence,
            "source_path": self.source_path,
            "commercial_ok": self.commercial_ok,
        }


@dataclass(slots=True)
class RuntimeInterpretationRef:
    """Reference to an Interpretation unit (ids only — no prose payload)."""

    id: str
    section_id: str = ""
    title: str = ""
    commercial_ok: bool = True
    intent_hints: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize interpretation reference."""
        return {
            "id": self.id,
            "section_id": self.section_id,
            "title": self.title,
            "commercial_ok": self.commercial_ok,
            "intent_hints": list(self.intent_hints),
        }


@dataclass(slots=True)
class RuntimeInput:
    """Validated structural input for Narrative Runtime."""

    evidence: tuple[RuntimeEvidenceUnit, ...] = ()
    interpretation_refs: tuple[RuntimeInterpretationRef, ...] = ()
    analysis_valid: bool = True
    interpretation_valid: bool = True
    run_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize runtime input."""
        return {
            "evidence": [item.to_dict() for item in self.evidence],
            "interpretation_refs": [item.to_dict() for item in self.interpretation_refs],
            "analysis_valid": self.analysis_valid,
            "interpretation_valid": self.interpretation_valid,
            "run_id": self.run_id,
        }


@dataclass(slots=True)
class NarrativeNode:
    """
    One NarrativeTree node.

    Contains structure and references only — never customer prose.
    """

    component_type: ComponentType
    evidence_refs: tuple[str, ...] = ()
    interpretation_refs: tuple[str, ...] = ()
    confidence: float = 0.0
    priority: int = 0
    dependencies: tuple[ComponentType, ...] = ()
    status: NodeStatus = NodeStatus.INSUFFICIENT_EVIDENCE

    def to_dict(self) -> dict[str, Any]:
        """Serialize node."""
        return {
            "component_type": self.component_type.value,
            "evidence_refs": list(self.evidence_refs),
            "interpretation_refs": list(self.interpretation_refs),
            "confidence": self.confidence,
            "priority": self.priority,
            "dependencies": [item.value for item in self.dependencies],
            "status": self.status.value,
        }


@dataclass(slots=True)
class NarrativeTree:
    """
    Sprint D1 output aggregate.

    Ordered narrative structure without NarrativeResult / prose.
    """

    nodes: tuple[NarrativeNode, ...] = ()
    run_id: str = ""
    status: TreeStatus = TreeStatus.INVALID
    validation_issues: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def node_map(self) -> dict[ComponentType, NarrativeNode]:
        """Index nodes by component type."""
        return {node.component_type: node for node in self.nodes}

    def to_dict(self) -> dict[str, Any]:
        """Serialize tree."""
        return {
            "nodes": [node.to_dict() for node in self.nodes],
            "run_id": self.run_id,
            "status": self.status.value,
            "validation_issues": list(self.validation_issues),
            "metadata": dict(self.metadata),
        }
