"""ReasoningValidator tests (N-IMP-03)."""

from __future__ import annotations

from typing import Any

import pytest

from engines.narrative_v2.evidence import (
    EvidenceBuilder,
    EvidenceItem,
    EvidenceReference,
    NarrativeEvidenceContext,
)
from engines.narrative_v2.evidence.evidence_item import STATUS_AVAILABLE
from engines.narrative_v2.evidence.evidence_registry import ALLOWED_DOMAINS
from engines.narrative_v2.reasoning import (
    NarrativeReasoningContext,
    ReasoningBuilder,
    ReasoningEdge,
    ReasoningNode,
    ReasoningReference,
    ReasoningValidationError,
    ReasoningValidator,
)
from engines.narrative_v2.reasoning.reasoning_edge import (
    DEFAULT_EDGE_WEIGHT,
    RELATION_CONTEXTUALIZES,
)
from engines.narrative_v2.reasoning.reasoning_node import (
    KIND_OBSERVATION,
    STATUS_ACTIVE,
)


def _item() -> EvidenceItem:
    return EvidenceItem(
        evidence_id="evidence.strength.level",
        domain="strength",
        key="strength_level",
        label="strength class",
        value="strong",
        source_path="strength.strength_level",
        status=STATUS_AVAILABLE,
        references=(
            EvidenceReference(
                source_path="strength.strength_level",
                domain="strength",
            ),
        ),
    )


def _evidence(item: EvidenceItem) -> NarrativeEvidenceContext:
    empty: dict[str, tuple[EvidenceItem, ...]] = {domain: () for domain in ALLOWED_DOMAINS}
    empty["strength"] = (item,)
    return NarrativeEvidenceContext(
        identity=empty["identity"],
        calendar=empty["calendar"],
        bazi=empty["bazi"],
        strength=empty["strength"],
        temperature=empty["temperature"],
        pattern=empty["pattern"],
        useful_god=empty["useful_god"],
        five_elements=empty["five_elements"],
        ten_gods=empty["ten_gods"],
        shensha=empty["shensha"],
        luck=empty["luck"],
        references=item.references,
        metadata=(),
        items=(item,),
        contract_gaps=(),
    )


def _node(**overrides: object) -> ReasoningNode:
    base: dict[str, object] = dict(
        reasoning_id="reasoning.observation.core.pattern_context",
        domain="pattern",
        kind=KIND_OBSERVATION,
        semantic_key="core.pattern_context",
        evidence_ids=("evidence.strength.level",),
        relation=RELATION_CONTEXTUALIZES,
        priority=10,
        status=STATUS_ACTIVE,
        references=(ReasoningReference(source="evidence.strength.level", kind="evidence"),),
        metadata=(("rule_id", "NR-REL-001"),),
    )
    base.update(overrides)
    return ReasoningNode(**base)  # type: ignore[arg-type]


def _context(nodes: tuple[ReasoningNode, ...], edges: tuple[ReasoningEdge, ...] = ()) -> NarrativeReasoningContext:
    ordered = tuple(sorted(nodes, key=lambda node: (node.priority, node.reasoning_id)))
    return NarrativeReasoningContext(
        nodes=ordered,
        edges=edges,
        observations=tuple(node for node in ordered if node.kind == KIND_OBSERVATION),
        impacts=(),
        boundaries=(),
        references=(),
        metadata=(),
        status="active",
        contract_gaps=(),
    )


def test_duplicate_reasoning_ids_fail() -> None:
    node = _node()
    context = _context((node, node))
    with pytest.raises(ReasoningValidationError, match="Duplicate"):
        ReasoningValidator().assert_valid(context, _evidence(_item()))


def test_unknown_evidence_id_fails() -> None:
    node = _node(evidence_ids=("evidence.missing.field",))
    context = _context((node,))
    with pytest.raises(ReasoningValidationError, match="Unknown evidence_id"):
        ReasoningValidator().assert_valid(context, _evidence(_item()))


def test_unknown_rule_fails() -> None:
    node = _node(metadata=(("rule_id", "NR-REL-999"),))
    context = _context((node,))
    with pytest.raises(ReasoningValidationError, match="Unknown reasoning rule"):
        ReasoningValidator().assert_valid(context, _evidence(_item()))


def test_unsupported_relation_type_fails() -> None:
    node = _node(relation="predicts")
    context = _context((node,))
    with pytest.raises(ReasoningValidationError, match="Unsupported relation type"):
        ReasoningValidator().assert_valid(context, _evidence(_item()))


def test_customer_prose_fails() -> None:
    node = _node(semantic_key="Bạn có nội lực tốt")
    context = _context((node,))
    with pytest.raises(ReasoningValidationError, match="Customer prose"):
        ReasoningValidator().assert_valid(context, _evidence(_item()))


def test_circular_dependency_fails() -> None:
    a = _node(reasoning_id="reasoning.observation.a", semantic_key="core.a", priority=1)
    b = _node(reasoning_id="reasoning.observation.b", semantic_key="core.b", priority=2)
    edges = (
        ReasoningEdge(
            edge_id="reasoning.edge.a.contextualizes",
            source_ids=("reasoning.observation.a",),
            target_id="reasoning.observation.b",
            relation_type=RELATION_CONTEXTUALIZES,
            weight=DEFAULT_EDGE_WEIGHT,
            status="active",
            references=(),
        ),
        ReasoningEdge(
            edge_id="reasoning.edge.b.contextualizes",
            source_ids=("reasoning.observation.b",),
            target_id="reasoning.observation.a",
            relation_type=RELATION_CONTEXTUALIZES,
            weight=DEFAULT_EDGE_WEIGHT,
            status="active",
            references=(),
        ),
    )
    context = _context((a, b), edges)
    with pytest.raises(ReasoningValidationError, match="Circular"):
        ReasoningValidator().assert_valid(context, _evidence(_item()))


def test_unordered_nodes_fail() -> None:
    first = _node(reasoning_id="reasoning.observation.z", semantic_key="core.z", priority=1)
    second = _node(reasoning_id="reasoning.observation.a", semantic_key="core.a", priority=1)
    context = NarrativeReasoningContext(
        nodes=(first, second),
        edges=(),
        observations=(first, second),
        impacts=(),
        boundaries=(),
        references=(),
        metadata=(),
        status="active",
        contract_gaps=(),
    )
    with pytest.raises(ReasoningValidationError, match="deterministically ordered"):
        ReasoningValidator().assert_valid(context, _evidence(_item()))


def test_case_0001_context_passes_validator(case_0001_canonical: dict[str, Any]) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    outcome = ReasoningValidator().validate(reasoning, evidence)
    assert outcome.passed is True
    assert outcome.status == "PASS"
