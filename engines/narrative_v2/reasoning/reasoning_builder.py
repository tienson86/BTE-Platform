"""Reasoning Builder — NarrativeEvidenceContext → NarrativeReasoningContext.

Connects published evidence. Does not recompute evidence or write prose.
"""

from __future__ import annotations

import logging

from engines.narrative_v2.evidence.evidence_context import NarrativeEvidenceContext
from engines.narrative_v2.evidence.evidence_item import STATUS_AVAILABLE
from engines.narrative_v2.reasoning.reasoning_context import (
    NarrativeReasoningContext,
    ReasoningContractGap,
    partition_nodes,
)
from engines.narrative_v2.reasoning.reasoning_edge import (
    DEFAULT_EDGE_WEIGHT,
    STATUS_ACTIVE as EDGE_ACTIVE,
    STATUS_CONFLICT as EDGE_CONFLICT,
    ReasoningEdge,
)
from engines.narrative_v2.reasoning.reasoning_errors import ReasoningError
from engines.narrative_v2.reasoning.reasoning_node import (
    KIND_BOUNDARY,
    KIND_OBSERVATION,
    KIND_RELATION,
    STATUS_ACTIVE,
    STATUS_CONFLICT,
    STATUS_GAP,
    STATUS_INSUFFICIENT,
    ReasoningNode,
)
from engines.narrative_v2.reasoning.reasoning_reference import ReasoningReference
from engines.narrative_v2.reasoning.reasoning_registry import ReasoningRegistry
from engines.narrative_v2.reasoning.reasoning_rules import ReasoningRule
from engines.narrative_v2.reasoning.reasoning_validator import ReasoningValidator

logger = logging.getLogger(__name__)

SHENSHA_NAMES_ID = "evidence.shensha.names"

_CONTEXT_METADATA: tuple[tuple[str, str], ...] = (
    ("shadow_mode", "true"),
    ("replaces_pack05", "false"),
    ("portal_connected", "false"),
    ("layer", "reasoning"),
)


class ReasoningBuilder:
    """Structural reasoning graph. Shadow mode. No narrative."""

    def __init__(
        self,
        *,
        registry: ReasoningRegistry | None = None,
        validator: ReasoningValidator | None = None,
    ) -> None:
        self._registry = registry or ReasoningRegistry()
        self._validator = validator or ReasoningValidator(registry=self._registry)

    def build(self, evidence_context: object) -> NarrativeReasoningContext:
        """Build ReasoningContext from EvidenceContext only."""
        evidence = _require_evidence(evidence_context)
        nodes: dict[str, ReasoningNode] = {}
        edges: list[ReasoningEdge] = []
        gaps = list(self._registry.catalog_gaps())
        for rule in self._registry.rules():
            fired = self._apply_rule(evidence, rule, nodes, edges)
            if not fired:
                self._record_insufficient(evidence, rule, nodes, gaps)
        self._record_shensha_gap(evidence, nodes)
        ordered_nodes = _ordered_nodes(nodes)
        ordered_edges = _mark_conflicts(tuple(edges), ordered_nodes)
        ordered_nodes = _apply_conflict_status(ordered_nodes, ordered_edges)
        observations, impacts, boundaries = partition_nodes(ordered_nodes)
        status = "active" if any(node.kind == KIND_RELATION for node in ordered_nodes) else "insufficient"
        context = NarrativeReasoningContext(
            nodes=ordered_nodes,
            edges=ordered_edges,
            observations=observations,
            impacts=impacts,
            boundaries=boundaries,
            references=_collect_references(ordered_nodes),
            metadata=_CONTEXT_METADATA,
            status=status,
            contract_gaps=tuple(gaps),
        )
        self._validator.assert_valid(context, evidence)
        return context

    def _apply_rule(
        self,
        evidence: NarrativeEvidenceContext,
        rule: ReasoningRule,
        nodes: dict[str, ReasoningNode],
        edges: list[ReasoningEdge],
    ) -> bool:
        evidence_ids = _available_ids(evidence, rule.required_evidence)
        if evidence_ids is None:
            return False
        optional_ids = _optional_available_ids(evidence, rule.optional_evidence)
        all_ids = evidence_ids + optional_ids
        for evidence_id in all_ids:
            self._ensure_evidence_observation(evidence, evidence_id, nodes)
        observation = _observation_candidate(rule, all_ids)
        relation = _relation_node(rule, all_ids)
        nodes[observation.reasoning_id] = observation
        nodes[relation.reasoning_id] = relation
        source_id = _evidence_observation_id(rule.required_evidence[0])
        edges.append(_edge(rule, source_id, observation.reasoning_id, rule.relation_type))
        if rule.support_relation_type is not None and len(rule.required_evidence) > 1:
            support_source = _evidence_observation_id(rule.required_evidence[1])
            edges.append(
                _edge(
                    rule,
                    support_source,
                    observation.reasoning_id,
                    rule.support_relation_type,
                    suffix="support",
                )
            )
        logger.debug("Fired reasoning rule %s", rule.rule_id)
        return True

    def _ensure_evidence_observation(
        self,
        evidence: NarrativeEvidenceContext,
        evidence_id: str,
        nodes: dict[str, ReasoningNode],
    ) -> None:
        reasoning_id = _evidence_observation_id(evidence_id)
        if reasoning_id in nodes:
            return
        item = evidence.item(evidence_id)
        domain = item.domain if item is not None else evidence_id.split(".")[1]
        nodes[reasoning_id] = ReasoningNode(
            reasoning_id=reasoning_id,
            domain=domain,
            kind=KIND_OBSERVATION,
            semantic_key=_evidence_semantic_key(evidence_id),
            evidence_ids=(evidence_id,),
            relation="",
            priority=0,
            status=STATUS_ACTIVE,
            references=(_evidence_ref(evidence_id),),
        )

    def _record_insufficient(
        self,
        evidence: NarrativeEvidenceContext,
        rule: ReasoningRule,
        nodes: dict[str, ReasoningNode],
        gaps: list[ReasoningContractGap],
    ) -> None:
        missing = _missing_required(evidence, rule.required_evidence)
        reason = (
            "temporal_context_unavailable"
            if rule.output_semantic_key == "core.luck_temporal_context"
            else "evidence_insufficient"
        )
        semantic = f"boundary.{rule.output_semantic_key}.insufficient"
        reasoning_id = f"reasoning.boundary.{rule.output_semantic_key}.insufficient"
        present = tuple(
            eid for eid in rule.required_evidence if _is_available(evidence, eid)
        )
        nodes[reasoning_id] = ReasoningNode(
            reasoning_id=reasoning_id,
            domain=rule.domain,
            kind=KIND_BOUNDARY,
            semantic_key=semantic,
            evidence_ids=present,
            relation=rule.relation_type,
            priority=rule.priority,
            status=STATUS_INSUFFICIENT,
            references=tuple(ReasoningReference(source=path, kind="spec") for path in rule.references),
            metadata=(
                ("rule_id", rule.rule_id),
                ("reason", reason),
            ),
        )
        gaps.append(
            ReasoningContractGap(
                field=rule.output_semantic_key,
                reason="REASONING CONTRACT GAP: required evidence is not available",
                rule_id=rule.rule_id,
            )
        )
        logger.debug("Boundary for %s missing %s", rule.rule_id, ",".join(missing))

    def _record_shensha_gap(
        self,
        evidence: NarrativeEvidenceContext,
        nodes: dict[str, ReasoningNode],
    ) -> None:
        if not _is_available(evidence, SHENSHA_NAMES_ID):
            return
        reasoning_id = "reasoning.boundary.shensha.approved_rule_unavailable"
        nodes[reasoning_id] = ReasoningNode(
            reasoning_id=reasoning_id,
            domain="shensha",
            kind=KIND_BOUNDARY,
            semantic_key="boundary.approved_rule_unavailable",
            evidence_ids=(SHENSHA_NAMES_ID,),
            relation="",
            priority=90,
            status=STATUS_GAP,
            references=(
                ReasoningReference(source=SHENSHA_NAMES_ID, kind="evidence"),
            ),
            metadata=(("reason", "approved_rule_unavailable"),),
        )


def _require_evidence(value: object) -> NarrativeEvidenceContext:
    if isinstance(value, NarrativeEvidenceContext):
        return value
    raise ReasoningError("Reasoning Builder accepts NarrativeEvidenceContext only")


def _is_available(evidence: NarrativeEvidenceContext, evidence_id: str) -> bool:
    item = evidence.item(evidence_id)
    return item is not None and item.status == STATUS_AVAILABLE


def _available_ids(
    evidence: NarrativeEvidenceContext,
    required: tuple[str, ...],
) -> tuple[str, ...] | None:
    ids: list[str] = []
    for evidence_id in required:
        if not _is_available(evidence, evidence_id):
            return None
        ids.append(evidence_id)
    return tuple(ids)


def _optional_available_ids(
    evidence: NarrativeEvidenceContext,
    optional: tuple[str, ...],
) -> tuple[str, ...]:
    return tuple(eid for eid in optional if _is_available(evidence, eid))


def _missing_required(
    evidence: NarrativeEvidenceContext,
    required: tuple[str, ...],
) -> tuple[str, ...]:
    return tuple(eid for eid in required if not _is_available(evidence, eid))


def _evidence_observation_id(evidence_id: str) -> str:
    suffix = evidence_id.removeprefix("evidence.")
    return f"reasoning.observation.{suffix}"


def _evidence_semantic_key(evidence_id: str) -> str:
    return f"core.{evidence_id.removeprefix('evidence.')}"


def _evidence_ref(evidence_id: str) -> ReasoningReference:
    return ReasoningReference(source=evidence_id, kind="evidence")


def _rule_metadata(rule: ReasoningRule) -> tuple[tuple[str, str], ...]:
    return (("rule_id", rule.rule_id),)


def _observation_candidate(rule: ReasoningRule, evidence_ids: tuple[str, ...]) -> ReasoningNode:
    return ReasoningNode(
        reasoning_id=f"reasoning.observation.{rule.output_semantic_key}",
        domain=rule.domain,
        kind=KIND_OBSERVATION,
        semantic_key=rule.output_semantic_key,
        evidence_ids=evidence_ids,
        relation=rule.relation_type,
        priority=rule.priority,
        status=STATUS_ACTIVE,
        references=tuple(ReasoningReference(source=path, kind="spec") for path in rule.references)
        + tuple(_evidence_ref(eid) for eid in evidence_ids),
        metadata=_rule_metadata(rule),
    )


def _relation_node(rule: ReasoningRule, evidence_ids: tuple[str, ...]) -> ReasoningNode:
    return ReasoningNode(
        reasoning_id=f"reasoning.relation.{rule.output_semantic_key}",
        domain=rule.domain,
        kind=KIND_RELATION,
        semantic_key=rule.output_semantic_key,
        evidence_ids=evidence_ids,
        relation=rule.relation_type,
        priority=rule.priority,
        status=STATUS_ACTIVE,
        references=tuple(ReasoningReference(source=path, kind="spec") for path in rule.references)
        + tuple(_evidence_ref(eid) for eid in evidence_ids),
        metadata=_rule_metadata(rule),
    )


def _edge(
    rule: ReasoningRule,
    source_id: str,
    target_id: str,
    relation_type: str,
    *,
    suffix: str = "",
) -> ReasoningEdge:
    edge_id = f"reasoning.edge.{rule.output_semantic_key}.{relation_type}"
    if suffix:
        edge_id = f"{edge_id}.{suffix}"
    return ReasoningEdge(
        edge_id=edge_id,
        source_ids=(source_id,),
        target_id=target_id,
        relation_type=relation_type,
        weight=DEFAULT_EDGE_WEIGHT,
        status=EDGE_ACTIVE,
        references=tuple(ReasoningReference(source=path, kind="spec") for path in rule.references),
        metadata=_rule_metadata(rule),
    )


def _ordered_nodes(nodes: dict[str, ReasoningNode]) -> tuple[ReasoningNode, ...]:
    return tuple(sorted(nodes.values(), key=lambda node: (node.priority, node.reasoning_id)))


def _collect_references(nodes: tuple[ReasoningNode, ...]) -> tuple[ReasoningReference, ...]:
    seen: set[tuple[str, str]] = set()
    refs: list[ReasoningReference] = []
    for node in nodes:
        for ref in node.references:
            key = (ref.source, ref.kind)
            if key in seen:
                continue
            seen.add(key)
            refs.append(ref)
    return tuple(refs)


def _mark_conflicts(
    edges: tuple[ReasoningEdge, ...],
    nodes: tuple[ReasoningNode, ...],
) -> tuple[ReasoningEdge, ...]:
    """Preserve supports and constrains on the same target. Do not resolve."""
    incoming: dict[str, set[str]] = {}
    for edge in edges:
        incoming.setdefault(edge.target_id, set()).add(edge.relation_type)
    conflicted = {
        target
        for target, types in incoming.items()
        if "supports" in types and "constrains" in types
    }
    if not conflicted:
        return tuple(sorted(edges, key=lambda edge: edge.edge_id))
    marked: list[ReasoningEdge] = []
    for edge in edges:
        if edge.target_id not in conflicted:
            marked.append(edge)
            continue
        marked.append(
            ReasoningEdge(
                edge_id=edge.edge_id,
                source_ids=edge.source_ids,
                target_id=edge.target_id,
                relation_type=edge.relation_type,
                weight=edge.weight,
                status=EDGE_CONFLICT,
                references=edge.references,
                metadata=edge.metadata,
            )
        )
    return tuple(sorted(marked, key=lambda edge: edge.edge_id))


def _apply_conflict_status(
    nodes: tuple[ReasoningNode, ...],
    edges: tuple[ReasoningEdge, ...],
) -> tuple[ReasoningNode, ...]:
    conflicted = {edge.target_id for edge in edges if edge.status == EDGE_CONFLICT}
    if not conflicted:
        return nodes
    updated: list[ReasoningNode] = []
    for node in nodes:
        if node.reasoning_id not in conflicted:
            updated.append(node)
            continue
        updated.append(
            ReasoningNode(
                reasoning_id=node.reasoning_id,
                domain=node.domain,
                kind=node.kind,
                semantic_key=node.semantic_key,
                evidence_ids=node.evidence_ids,
                relation=node.relation,
                priority=node.priority,
                status=STATUS_CONFLICT,
                references=node.references,
                metadata=node.metadata,
            )
        )
    return tuple(sorted(updated, key=lambda node: (node.priority, node.reasoning_id)))
