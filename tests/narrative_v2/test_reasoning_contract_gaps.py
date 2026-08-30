"""Reasoning contract-gap tests (N-IMP-03)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.reasoning import ReasoningBuilder, ReasoningRegistry


EXPECTED_GAPS: tuple[str, ...] = (
    "reasoning.shensha.meaning",
    "reasoning.career",
    "reasoning.finance",
    "reasoning.relationship",
    "reasoning.luck.quality",
    "reasoning.impact.structure_preference",
    "reasoning.strength.customer_meaning",
    "reasoning.pattern.customer_meaning",
    "reasoning.useful_god.action",
    "reasoning.identity.structured_self_direction",
)


def test_catalog_gaps_are_recorded_not_invented(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    context = ReasoningBuilder().build(evidence)
    fields = {gap.field for gap in context.contract_gaps}
    for field in EXPECTED_GAPS:
        assert field in fields
    for gap in context.contract_gaps:
        if gap.field in EXPECTED_GAPS:
            assert gap.reason.startswith("REASONING CONTRACT GAP")


def test_shensha_presence_does_not_invent_a_rule(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    context = ReasoningBuilder().build(evidence)
    boundary = context.node("reasoning.boundary.shensha.approved_rule_unavailable")
    assert boundary is not None
    assert boundary.kind == "boundary"
    assert boundary.status == "gap"
    assert "evidence.shensha.names" in boundary.evidence_ids
    keys = {node.semantic_key for node in context.nodes}
    assert "hong_luan.relationship" not in keys
    assert ReasoningRegistry().get("NR-REL-SHENSHA") is None


def test_no_impact_candidates_without_approved_catalog(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    context = ReasoningBuilder().build(evidence)
    assert context.impacts == ()
    for node in context.nodes:
        assert node.kind != "impact_candidate"
