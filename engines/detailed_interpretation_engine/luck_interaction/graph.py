"""Luck Interaction graph: activated domain ↔ activated domain. Not luck-force → domain."""

from __future__ import annotations

from engines.detailed_interpretation_engine.luck_activation.models import DomainActivationResult
from engines.detailed_interpretation_engine.luck_interaction.constants import (
    GRAPH_RELATIONS,
    TYPE_TO_RELATION,
)
from engines.detailed_interpretation_engine.luck_interaction.models import (
    DomainInteractionFinding,
    LuckInteractionGraph,
    LuckInteractionGraphEdge,
)


def build_interaction_graph(
    items: dict[str, DomainActivationResult],
    findings: tuple[DomainInteractionFinding, ...],
    order: tuple[str, ...],
) -> LuckInteractionGraph:
    """Project evidenced findings onto the DI-10 graph. No luck-cycle sources."""
    nodes = tuple(domain_id for domain_id in order if domain_id in items) or tuple(items)
    edges: list[LuckInteractionGraphEdge] = []
    seen: set[tuple[str, str, str]] = set()
    for finding in findings:
        relation = TYPE_TO_RELATION.get(finding.interaction_type, "")
        if relation not in GRAPH_RELATIONS or not finding.evidence_ids:
            continue
        key = (finding.source_domain, finding.target_domain, relation)
        if key in seen:
            continue
        seen.add(key)
        edges.append(
            LuckInteractionGraphEdge(
                source=finding.source_domain,
                target=finding.target_domain,
                relation=relation,
                evidence_ids=finding.evidence_ids,
                finding_id=finding.finding_id,
            )
        )
    return LuckInteractionGraph(nodes=nodes, edges=tuple(edges))
