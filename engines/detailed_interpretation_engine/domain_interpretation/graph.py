"""Build an evidence-backed DomainGraph. Edges do not copy state."""

from __future__ import annotations

from engines.detailed_interpretation_engine.domain_interpretation.constants import (
    GRAPH_RELATIONS,
    MAIN_DOMAIN_IDS,
    OUTPUT_WEALTH_COMBINATIONS,
    SUPPORT_DOMAIN_IDS,
)
from engines.detailed_interpretation_engine.domain_interpretation.facts import DomainFacts
from engines.detailed_interpretation_engine.domain_interpretation.roles import (
    evidence_ids_of,
    scoped_findings,
)
from engines.detailed_interpretation_engine.domains import (
    DomainGraph,
    DomainGraphEdge,
    DomainInterpretationResult,
)
from engines.detailed_interpretation_engine.enums import DomainState


def build_domain_graph(
    facts: DomainFacts,
    mains: dict[str, DomainInterpretationResult],
    supporting: dict[str, DomainInterpretationResult],
) -> DomainGraph:
    """Draw only evidenced natal relations. Never copy one domain's state onto another."""
    nodes = tuple(
        domain_id
        for domain_id in MAIN_DOMAIN_IDS + SUPPORT_DOMAIN_IDS
        if _evaluated(mains.get(domain_id) or supporting.get(domain_id))
    )
    edges: list[DomainGraphEdge] = []
    edges.extend(_edge(facts, "authority", "career", "supports"))
    edges.extend(_edge(facts, "academic", "career", "supports"))
    edges.extend(_edge(facts, "leadership", "career", "supports"))
    edges.extend(_edge(facts, "management", "career", "supports"))
    edges.extend(_edge(facts, "academic", "learning", "reinforces"))
    edges.extend(_edge(facts, "academic", "legacy", "supports"))
    edges.extend(_edge(facts, "vitality", "career", "supports"))
    if any(item in OUTPUT_WEALTH_COMBINATIONS for item in facts.combination_ids):
        edges.extend(_edge(facts, "creative", "wealth", "supports"))
    if mains.get("career") and mains.get("wealth"):
        career_state = mains["career"].state
        wealth_state = mains["wealth"].state
        if career_state is not wealth_state:
            evidence = evidence_ids_of(scoped_findings(facts.ep, "career")) + evidence_ids_of(
                scoped_findings(facts.ep, "wealth")
            )
            if evidence:
                edges.append(
                    DomainGraphEdge(
                        source="career",
                        target="wealth",
                        relation="conflicts",
                        evidence_ids=evidence,
                    )
                )
    seen: set[tuple[str, str, str]] = set()
    unique: list[DomainGraphEdge] = []
    for edge in edges:
        key = (edge.source, edge.target, edge.relation)
        if key in seen or edge.relation not in GRAPH_RELATIONS or not edge.evidence_ids:
            continue
        if edge.source not in nodes or edge.target not in nodes:
            continue
        seen.add(key)
        unique.append(edge)
    return DomainGraph(nodes=nodes, edges=tuple(unique))


def _evaluated(result: DomainInterpretationResult | None) -> bool:
    return result is not None and result.state is not DomainState.NOT_EVALUATED


def _edge(facts: DomainFacts, source: str, target: str, relation: str) -> tuple[DomainGraphEdge, ...]:
    evidence = evidence_ids_of(scoped_findings(facts.ep, source)) + evidence_ids_of(
        scoped_findings(facts.ep, target)
    )
    if not evidence:
        return ()
    return (
        DomainGraphEdge(
            source=source,
            target=target,
            relation=relation,
            evidence_ids=tuple(dict.fromkeys(evidence)),
        ),
    )
