"""Evidence Composer — collect evidence from every bundle. Never infer facts."""

from __future__ import annotations

from engines.interpretation_engine.foundation.narrative.constants import (
    BUNDLE_KIND_DECISION,
    BUNDLE_KIND_KNOWLEDGE,
    BUNDLE_KIND_RELATIONSHIP,
    BUNDLE_KIND_STATE,
)
from engines.interpretation_engine.foundation.narrative.input import (
    CopiedStatement,
    DecisionBundle,
    KnowledgeBundle,
    NarrativeComposerInput,
    RelationshipBundle,
    StateBundle,
)
from engines.interpretation_engine.foundation.narrative.models import (
    EvidenceGraph,
    EvidenceNode,
)


def compose_evidence(source: NarrativeComposerInput) -> EvidenceGraph:
    """Collect copied statements into an evidence graph.

    Missing facts stay missing. No new astrology is generated.
    """
    nodes: list[EvidenceNode] = []
    index = 0
    for bundle, kind in _iter_bundles(source):
        for statement in bundle.statements:
            index += 1
            nodes.append(_node_from_statement(index, bundle, kind, statement))
    collected = tuple(nodes)
    return EvidenceGraph(
        nodes=collected,
        raw_count=len(collected),
        merged_count=len(collected),
    )


def _iter_bundles(
    source: NarrativeComposerInput,
) -> tuple[tuple[DecisionBundle | StateBundle | RelationshipBundle | KnowledgeBundle, str], ...]:
    """Walk frozen bundle kinds only."""
    items: list[
        tuple[DecisionBundle | StateBundle | RelationshipBundle | KnowledgeBundle, str]
    ] = []
    for bundle in source.decision_bundles:
        items.append((bundle, BUNDLE_KIND_DECISION))
    for bundle in source.state_bundles:
        items.append((bundle, BUNDLE_KIND_STATE))
    for bundle in source.relationship_bundles:
        items.append((bundle, BUNDLE_KIND_RELATIONSHIP))
    for bundle in source.knowledge_bundles:
        items.append((bundle, BUNDLE_KIND_KNOWLEDGE))
    return tuple(items)


def _node_from_statement(
    index: int,
    bundle: DecisionBundle | StateBundle | RelationshipBundle | KnowledgeBundle,
    kind: str,
    statement: CopiedStatement,
) -> EvidenceNode:
    """Promote one copied statement to an evidence node."""
    evidence_id = f"ev:{kind}:{bundle.domain}:{index}"
    return EvidenceNode(
        evidence_id=evidence_id,
        bundle_id=bundle.bundle_id,
        bundle_kind=kind,
        domain=bundle.domain,
        kind=statement.kind,
        slot=statement.slot,
        statement=statement.text,
        engine_truth_ref=statement.engine_truth_ref or next(iter(bundle.engine_truth_refs), ""),
        customer_domain=statement.customer_domain,
        category=statement.category,
        rationale=statement.rationale,
        condition=statement.condition,
        mitigation=statement.mitigation,
        confidence=statement.confidence or bundle.confidence,
        importance=bundle.importance,
    )
