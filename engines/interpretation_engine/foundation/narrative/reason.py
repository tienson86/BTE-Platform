"""Reason Composer — structured chains only. No customer prose."""

from __future__ import annotations

from collections import defaultdict

from engines.interpretation_engine.foundation.narrative.constants import (
    KIND_CONCLUSION,
    KIND_EVIDENCE,
    KIND_FACT,
    KIND_REASON,
)
from engines.interpretation_engine.foundation.narrative.models import (
    EvidenceGraph,
    EvidenceNode,
    ReasoningChain,
)


def compose_reasons(graph: EvidenceGraph) -> tuple[ReasoningChain, ...]:
    """Build Fact → Evidence → Reason → Conclusion chains per bundle.

    Chains copy existing statements. Missing reasons are not invented.
    """
    grouped: dict[str, list[EvidenceNode]] = defaultdict(list)
    for node in graph.nodes:
        grouped[node.bundle_id].append(node)
    chains: list[ReasoningChain] = []
    index = 0
    for bundle_id, nodes in grouped.items():
        facts = [item for item in nodes if item.kind == KIND_FACT]
        evidence = [item for item in nodes if item.kind == KIND_EVIDENCE]
        reasons = [item for item in nodes if item.kind == KIND_REASON]
        conclusions = [item for item in nodes if item.kind == KIND_CONCLUSION]
        if not reasons:
            continue
        for position, reason in enumerate(reasons):
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
                )
            )
    return tuple(chains)
