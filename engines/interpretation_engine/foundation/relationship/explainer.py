"""Generic RelationshipExplainer — copies upstream truth, does not invent rules."""

from __future__ import annotations

from typing import Any, Sequence

from engines.interpretation_engine.foundation.relationship.metrics import (
    compute_relationship_metrics,
)
from engines.interpretation_engine.foundation.relationship.models import (
    RelationshipAssessment,
    RelationshipEdge,
    RelationshipGraph,
    RelationshipInput,
    RelationshipNode,
    RelationshipRecord,
)
from engines.interpretation_engine.foundation.relationship.validation import (
    validate_relationship_assessment,
)
from engines.interpretation_engine.foundation.status import DataAvailability


class GenericRelationshipExplainer:
    """Assemble a relationship graph from upstream records.

    Does not select a winner, classify a state, or author meaning.
    """

    def explain(self, facts: Any) -> RelationshipAssessment:
        """Copy upstream relationship records into RelationshipAssessment."""
        payload = _normalize_input(facts)
        graph = _build_graph(payload.records)
        confidence = _assessment_confidence(payload, graph.edges)
        summary_type, summary_direction, summary_strength, summary_conditions, summary_rules = (
            _single_edge_summary(graph.edges)
        )
        assessment = RelationshipAssessment(
            domain=payload.domain,
            graph=graph,
            evidence=payload.evidence,
            meaning=payload.meaning,
            applications=payload.applications,
            warnings=payload.warnings,
            confidence=confidence,
            diagnostics=(),
            status=(
                DataAvailability.MISSING if not payload.records else DataAvailability.AVAILABLE
            ),
            relationship_type=summary_type,
            direction=summary_direction,
            strength=summary_strength,
            conditions=summary_conditions,
            rule_ids=summary_rules,
        )
        metrics = compute_relationship_metrics(assessment)
        validation = validate_relationship_assessment(assessment)
        diagnostics = tuple(dict.fromkeys(issue.code for issue in validation.issues))
        return RelationshipAssessment(
            domain=assessment.domain,
            graph=assessment.graph,
            evidence=assessment.evidence,
            meaning=assessment.meaning,
            applications=assessment.applications,
            warnings=assessment.warnings,
            confidence=assessment.confidence,
            diagnostics=diagnostics,
            status=validation.status,
            relationship_type=assessment.relationship_type,
            direction=assessment.direction,
            strength=assessment.strength,
            conditions=assessment.conditions,
            rule_ids=assessment.rule_ids,
            metrics=metrics,
        )


def _normalize_input(facts: Any) -> RelationshipInput:
    """Accept RelationshipInput or a sequence of records. Do not infer new links."""
    if isinstance(facts, RelationshipInput):
        return facts
    if isinstance(facts, Sequence) and not isinstance(facts, (str, bytes)):
        records = tuple(item for item in facts if isinstance(item, RelationshipRecord))
        return RelationshipInput(domain="", records=records)
    raise TypeError("explain() requires RelationshipInput or RelationshipRecord sequence")


def _build_graph(records: tuple[RelationshipRecord, ...]) -> RelationshipGraph:
    """Materialize nodes and edges from records. No hidden links."""
    nodes: dict[str, RelationshipNode] = {}
    edges: list[RelationshipEdge] = []
    for index, record in enumerate(records, start=1):
        _add_node(
            nodes,
            node_id=record.source,
            kind=record.source_kind,
            label=record.source_label,
            origin=record.source_origin,
        )
        _add_node(
            nodes,
            node_id=record.target,
            kind=record.target_kind,
            label=record.target_label,
            origin=record.target_origin,
        )
        edge_id = record.record_id or f"rel_{index}"
        fact_refs = record.fact_refs or (f"record:{index}",)
        edges.append(
            RelationshipEdge(
                edge_id=edge_id,
                source=record.source,
                target=record.target,
                relationship_type=record.relationship_type,
                direction=record.direction,
                strength=record.strength,
                weight=record.weight,
                confidence=record.confidence,
                rule_ids=record.rule_ids,
                evidence_ids=record.evidence_ids,
                conditions=record.conditions,
                fact_refs=fact_refs,
                knowledge_key=record.knowledge_key,
            )
        )
    return RelationshipGraph(nodes=tuple(nodes.values()), edges=tuple(edges))


def _add_node(
    nodes: dict[str, RelationshipNode],
    *,
    node_id: str,
    kind: str,
    label: str,
    origin: str,
) -> None:
    """Index a participant once; later records do not overwrite identity."""
    if not node_id or node_id in nodes:
        return
    nodes[node_id] = RelationshipNode(
        node_id=node_id,
        kind=kind,
        label=label or node_id,
        source=origin,
    )


def _assessment_confidence(
    payload: RelationshipInput,
    edges: tuple[RelationshipEdge, ...],
) -> float:
    """Use explicit input confidence, else min of upstream edge confidences."""
    if payload.confidence is not None:
        return float(payload.confidence)
    if not edges:
        return 0.0
    return min(float(edge.confidence) for edge in edges)


def _single_edge_summary(
    edges: tuple[RelationshipEdge, ...],
) -> tuple[str, str, float, tuple[str, ...], tuple[str, ...]]:
    """Expose type/direction/strength only when exactly one upstream edge exists."""
    if len(edges) != 1:
        return "", "", 0.0, (), ()
    edge = edges[0]
    return (
        edge.relationship_type,
        edge.direction,
        edge.strength,
        edge.conditions,
        edge.rule_ids,
    )
