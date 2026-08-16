"""Reason Composer — structured chains grouped later by customer topic."""

from __future__ import annotations

from collections import defaultdict

from engines.interpretation_engine.foundation.narrative.constants import (
    CUSTOMER_DOMAINS,
    KIND_APPLICATION,
    KIND_CONCLUSION,
    KIND_EVIDENCE,
    KIND_FACT,
    KIND_REASON,
)
from engines.interpretation_engine.foundation.narrative.mapping import (
    default_topic,
    narrative_topic,
)
from engines.interpretation_engine.foundation.narrative.models import (
    EvidenceGraph,
    EvidenceNode,
    ReasoningChain,
)


def compose_reasons(graph: EvidenceGraph) -> tuple[ReasoningChain, ...]:
    """Build Fact → Evidence → Reason → Conclusion chains per bundle.

    Chains copy existing statements. Missing reasons are not invented.
    Topic is copied from mapped applications in the same bundle.
    """
    grouped: dict[str, list[EvidenceNode]] = defaultdict(list)
    for node in graph.nodes:
        grouped[node.bundle_id].append(node)
    chains: list[ReasoningChain] = []
    index = 0
    seen_evidence: set[str] = set()
    for bundle_id, nodes in grouped.items():
        facts = [item for item in nodes if item.kind == KIND_FACT]
        evidence = [item for item in nodes if item.kind == KIND_EVIDENCE]
        reasons = [item for item in nodes if item.kind == KIND_REASON]
        conclusions = [item for item in nodes if item.kind == KIND_CONCLUSION]
        topic = _bundle_topic(nodes)
        if not reasons:
            continue
        for position, reason in enumerate(reasons):
            if reason.evidence_id in seen_evidence:
                continue
            fact = facts[position] if position < len(facts) else (facts[0] if facts else None)
            conclusion = (
                conclusions[position]
                if position < len(conclusions)
                else (conclusions[0] if conclusions else None)
            )
            if fact is None or conclusion is None:
                continue
            index += 1
            evidence_ids = tuple(item.evidence_id for item in evidence) or (reason.evidence_id,)
            seen_evidence.add(reason.evidence_id)
            chains.append(
                ReasoningChain(
                    chain_id=f"reason:{bundle_id}:{index}",
                    bundle_id=bundle_id,
                    domain=reason.domain,
                    fact_ids=(fact.evidence_id,),
                    evidence_ids=evidence_ids,
                    reason_id=reason.evidence_id,
                    conclusion_id=conclusion.evidence_id,
                    fact=fact.statement,
                    reason=reason.statement,
                    conclusion=conclusion.statement,
                    topic=narrative_topic(
                        reason.customer_domain,
                        reason.domain,
                        reason.engine_truth_ref,
                    )
                    or topic,
                )
            )
    return tuple(chains)


def _bundle_topic(nodes: list[EvidenceNode]) -> str:
    """Pick the first supported application topic, else the domain default."""
    for node in nodes:
        if node.kind == KIND_APPLICATION and node.customer_domain in CUSTOMER_DOMAINS:
            return node.customer_domain
    domain = nodes[0].domain if nodes else ""
    return default_topic(domain)
