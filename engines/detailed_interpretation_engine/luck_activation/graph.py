"""Luck force → domain activation graph. Not DI-10 domain interaction."""

from __future__ import annotations

from engines.detailed_interpretation_engine.enums import ActivationState
from engines.detailed_interpretation_engine.luck_activation.constants import KNOWN_ACTIVATION_IDS
from engines.detailed_interpretation_engine.luck_activation.models import (
    ACTIVATION_GRAPH_RELATIONS,
    ActivationGraph,
    ActivationGraphEdge,
    DomainActivationResult,
)

_TYPE_TO_RELATION: tuple[tuple[str, str], ...] = (
    ("suppression", "suppress"),
    ("recovery", "recover"),
    ("acceleration", "accelerate"),
    ("delay", "delay"),
    ("stress", "stress"),
    ("activation", "activate"),
    ("support", "activate"),
    ("opportunity", "activate"),
    ("restriction", "suppress"),
)


def build_activation_graph(
    items: dict[str, DomainActivationResult],
    order: tuple[str, ...],
    *,
    cycle_id: str,
) -> ActivationGraph:
    """Connect the luck cycle to each engaged domain. No domain-to-domain edges."""
    nodes = tuple(domain_id for domain_id in order if domain_id in items)
    source = cycle_id or "luck_cycle"
    edges: list[ActivationGraphEdge] = []
    seen: set[tuple[str, str, str]] = set()
    for domain_id in nodes:
        item = items[domain_id]
        if item.activation_state in {ActivationState.DORMANT, ActivationState.BLOCKED}:
            continue
        if domain_id not in KNOWN_ACTIVATION_IDS:
            continue
        relation = _relation(item)
        if relation not in ACTIVATION_GRAPH_RELATIONS:
            continue
        key = (source, domain_id, relation)
        if key in seen:
            continue
        seen.add(key)
        evidence = item.evidence_ids or (source,)
        edges.append(
            ActivationGraphEdge(
                source=source,
                target=domain_id,
                relation=relation,
                evidence_ids=evidence,
            )
        )
    return ActivationGraph(nodes=nodes, edges=tuple(edges))


def _relation(item: DomainActivationResult) -> str:
    types = set(item.activation_types)
    for code, relation in _TYPE_TO_RELATION:
        if code in types:
            return relation
    if item.activation_state is ActivationState.SUPPRESSED:
        return "suppress"
    if item.activation_state is ActivationState.OVERLOADED:
        return "stress"
    return "activate"
