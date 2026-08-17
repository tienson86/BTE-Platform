"""Frozen composer inputs — Decision, State, Relationship, Knowledge only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.narrative.constants import (
    CANONICAL_BUNDLE_KINDS,
)


@dataclass(frozen=True, slots=True)
class ChartFocus:
    """Current-chart facts used to drop unused knowledge from customer text."""

    selected: str = ""
    favorable: tuple[str, ...] = ()
    unfavorable: tuple[str, ...] = ()
    pattern_label: str = ""
    strength_label: str = ""
    strength_state: str = ""
    day_master: str = ""
    present_ten_gods: tuple[str, ...] = ()
    canonical_shensha: tuple[str, ...] = ()
    current_dayun: str = ""
    next_dayun: str = ""
    useful_god_role: str = ""
    five_elements: tuple[tuple[str, int], ...] = ()
    dominant_element: str = ""
    stem_roles: tuple[tuple[str, str], ...] = ()
    selected_entity_type: str = ""
    favorable_entity_types: tuple[str, ...] = ()
    unfavorable_entity_types: tuple[str, ...] = ()

    def active_names(self) -> frozenset[str]:
        """Names that belong to this chart's governing reading."""
        names = [
            self.selected,
            self.pattern_label,
            self.strength_label,
            self.strength_state,
            self.day_master,
            *self.favorable,
            *self.unfavorable,
            *self.present_ten_gods,
            *self.canonical_shensha,
        ]
        return frozenset(item for item in names if item)

    def role_for(self, key: str) -> str:
        """Map an entity key to its current-chart role."""
        if key and key == self.selected:
            return "useful_god"
        if key in self.favorable:
            return "hy"
        if key in self.unfavorable:
            return "ky"
        if key and key == self.pattern_label:
            return "pattern"
        if key in {self.strength_label, self.strength_state, "strong", "weak", "balanced"}:
            return "strength"
        if key in self.present_ten_gods:
            return "ten_god"
        if key in self.canonical_shensha:
            return "shensha"
        return ""


@dataclass(frozen=True, slots=True)
class CopiedStatement:
    """One already-validated statement copied from an upstream bundle."""

    text: str
    kind: str
    slot: str
    engine_truth_ref: str
    customer_domain: str = ""
    category: str = ""
    rationale: str = ""
    condition: str = ""
    mitigation: str = ""
    confidence: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Serialize a copied statement."""
        return {
            "text": self.text,
            "kind": self.kind,
            "slot": self.slot,
            "engine_truth_ref": self.engine_truth_ref,
            "customer_domain": self.customer_domain,
            "category": self.category,
            "rationale": self.rationale,
            "condition": self.condition,
            "mitigation": self.mitigation,
            "confidence": self.confidence,
        }


@dataclass(frozen=True, slots=True)
class DecisionBundle:
    """Decision-class input. Composer does not re-select a winner."""

    bundle_id: str
    domain: str
    selected: str
    reason: str
    confidence: float
    importance: float
    statements: tuple[CopiedStatement, ...]
    engine_truth_refs: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize a decision bundle."""
        return {
            "bundle_id": self.bundle_id,
            "kind": "decision",
            "domain": self.domain,
            "selected": self.selected,
            "reason": self.reason,
            "confidence": self.confidence,
            "importance": self.importance,
            "statements": [item.to_dict() for item in self.statements],
            "engine_truth_refs": list(self.engine_truth_refs),
        }


@dataclass(frozen=True, slots=True)
class StateBundle:
    """State-class input. Composer does not reclassify the state."""

    bundle_id: str
    domain: str
    state: str
    label: str
    confidence: float
    importance: float
    statements: tuple[CopiedStatement, ...]
    engine_truth_refs: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize a state bundle."""
        return {
            "bundle_id": self.bundle_id,
            "kind": "state",
            "domain": self.domain,
            "state": self.state,
            "label": self.label,
            "confidence": self.confidence,
            "importance": self.importance,
            "statements": [item.to_dict() for item in self.statements],
            "engine_truth_refs": list(self.engine_truth_refs),
        }


@dataclass(frozen=True, slots=True)
class RelationshipBundle:
    """Relationship-class input. Composer does not invent edges."""

    bundle_id: str
    domain: str
    confidence: float
    importance: float
    statements: tuple[CopiedStatement, ...]
    engine_truth_refs: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize a relationship bundle."""
        return {
            "bundle_id": self.bundle_id,
            "kind": "relationship",
            "domain": self.domain,
            "confidence": self.confidence,
            "importance": self.importance,
            "statements": [item.to_dict() for item in self.statements],
            "engine_truth_refs": list(self.engine_truth_refs),
        }


@dataclass(frozen=True, slots=True)
class KnowledgeBundle:
    """Knowledge-class input. Composer does not own or rewrite knowledge."""

    bundle_id: str
    domain: str
    entity_keys: tuple[str, ...]
    confidence: float
    importance: float
    statements: tuple[CopiedStatement, ...]
    engine_truth_refs: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize a knowledge bundle."""
        return {
            "bundle_id": self.bundle_id,
            "kind": "knowledge",
            "domain": self.domain,
            "entity_keys": list(self.entity_keys),
            "confidence": self.confidence,
            "importance": self.importance,
            "statements": [item.to_dict() for item in self.statements],
            "engine_truth_refs": list(self.engine_truth_refs),
        }


@dataclass(frozen=True, slots=True)
class NarrativeComposerInput:
    """Canonical composer input. No other bundle kinds are accepted."""

    decision_bundles: tuple[DecisionBundle, ...] = ()
    state_bundles: tuple[StateBundle, ...] = ()
    relationship_bundles: tuple[RelationshipBundle, ...] = ()
    knowledge_bundles: tuple[KnowledgeBundle, ...] = ()
    chart_focus: ChartFocus | None = None

    def all_bundles(
        self,
    ) -> tuple[DecisionBundle | StateBundle | RelationshipBundle | KnowledgeBundle, ...]:
        """Return bundles in frozen kind order."""
        return (
            *self.decision_bundles,
            *self.state_bundles,
            *self.relationship_bundles,
            *self.knowledge_bundles,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize composer input."""
        return {
            "accepted_kinds": list(CANONICAL_BUNDLE_KINDS),
            "decision_bundles": [item.to_dict() for item in self.decision_bundles],
            "state_bundles": [item.to_dict() for item in self.state_bundles],
            "relationship_bundles": [item.to_dict() for item in self.relationship_bundles],
            "knowledge_bundles": [item.to_dict() for item in self.knowledge_bundles],
        }
