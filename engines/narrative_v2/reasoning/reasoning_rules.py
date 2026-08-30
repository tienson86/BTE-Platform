"""Approved structural reasoning rules for N-IMP-03.

Rules encode published semantic relationships only.
They do not map evidence values to customer meaning.
"""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.reasoning.reasoning_context import ReasoningContractGap
from engines.narrative_v2.reasoning.reasoning_edge import (
    RELATION_CONTEXTUALIZES,
    RELATION_QUALIFIES,
    RELATION_SUPPORTS,
)
from engines.narrative_v2.reasoning.reasoning_node import KIND_OBSERVATION

RULE_STATUS_APPROVED = "approved"


@dataclass(frozen=True, slots=True)
class ReasoningRule:
    """Internal reasoning rule contract. rule_id never reaches Presentation."""

    rule_id: str
    status: str
    required_evidence: tuple[str, ...]
    optional_evidence: tuple[str, ...]
    relation_type: str
    output_semantic_key: str
    priority: int
    references: tuple[str, ...]
    domain: str
    kind: str
    support_relation_type: str | None = None


APPROVED_RULES: tuple[ReasoningRule, ...] = (
    ReasoningRule(
        rule_id="NR-REL-001",
        status=RULE_STATUS_APPROVED,
        required_evidence=(
            "evidence.strength.level",
            "evidence.pattern.primary",
        ),
        optional_evidence=("evidence.pattern.cach_cuc",),
        relation_type=RELATION_CONTEXTUALIZES,
        output_semantic_key="core.pattern_context",
        priority=10,
        references=(
            "knowledge/narrative_v2/00_ARCHITECTURE.md",
            "knowledge/narrative_v2/03_PIPELINE.md",
        ),
        domain="pattern",
        kind=KIND_OBSERVATION,
    ),
    ReasoningRule(
        rule_id="NR-REL-002",
        status=RULE_STATUS_APPROVED,
        required_evidence=(
            "evidence.strength.level",
            "evidence.useful_god.primary",
        ),
        optional_evidence=("evidence.useful_god.element",),
        relation_type=RELATION_CONTEXTUALIZES,
        output_semantic_key="core.useful_god_context",
        priority=20,
        references=(
            "knowledge/narrative_v2/00_ARCHITECTURE.md",
            "knowledge/reasoning_engine/CROSS_DOMAIN_V1_1/PRECEDENCE_POLICY.md",
        ),
        domain="useful_god",
        kind=KIND_OBSERVATION,
    ),
    ReasoningRule(
        rule_id="NR-REL-003",
        status=RULE_STATUS_APPROVED,
        required_evidence=(
            "evidence.temperature.climate_state",
            "evidence.temperature.balancing_need",
        ),
        optional_evidence=(),
        relation_type=RELATION_CONTEXTUALIZES,
        output_semantic_key="core.temperature_balancing_context",
        priority=30,
        references=(
            "knowledge/narrative_v2/00_ARCHITECTURE.md",
            "knowledge/interpretation/interaction/INTERACTION_BOUNDARIES.md",
        ),
        domain="temperature",
        kind=KIND_OBSERVATION,
    ),
    ReasoningRule(
        rule_id="NR-REL-004",
        status=RULE_STATUS_APPROVED,
        required_evidence=(
            "evidence.pattern.primary",
            "evidence.ten_gods.visible_labels",
        ),
        optional_evidence=(),
        relation_type=RELATION_QUALIFIES,
        output_semantic_key="core.pattern_ten_gods_relation",
        priority=40,
        references=(
            "knowledge/reasoning_engine/CROSS_DOMAIN_V1_1/PRECEDENCE_POLICY.md",
        ),
        domain="pattern",
        kind=KIND_OBSERVATION,
        support_relation_type=RELATION_SUPPORTS,
    ),
    ReasoningRule(
        rule_id="NR-REL-005",
        status=RULE_STATUS_APPROVED,
        required_evidence=("evidence.luck.current_cycle",),
        optional_evidence=(
            "evidence.luck.available",
            "evidence.luck.direction",
        ),
        relation_type=RELATION_CONTEXTUALIZES,
        output_semantic_key="core.luck_temporal_context",
        priority=50,
        references=(
            "knowledge/interpretation/interaction/INTERACTION_FACTS.md",
            "knowledge/interpretation/interaction/INTERACTION_BOUNDARIES.md",
        ),
        domain="luck",
        kind=KIND_OBSERVATION,
    ),
)

CATALOG_CONTRACT_GAPS: tuple[ReasoningContractGap, ...] = (
    ReasoningContractGap(
        field="reasoning.shensha.meaning",
        reason="REASONING CONTRACT GAP: no approved ShenSha meaning relationship",
    ),
    ReasoningContractGap(
        field="reasoning.career",
        reason="REASONING CONTRACT GAP: career reasoning is out of N-IMP-03 scope",
    ),
    ReasoningContractGap(
        field="reasoning.finance",
        reason="REASONING CONTRACT GAP: finance reasoning is out of N-IMP-03 scope",
    ),
    ReasoningContractGap(
        field="reasoning.relationship",
        reason="REASONING CONTRACT GAP: relationship reasoning is out of N-IMP-03 scope",
    ),
    ReasoningContractGap(
        field="reasoning.luck.quality",
        reason="REASONING CONTRACT GAP: luck quality interpretation is not approved",
    ),
    ReasoningContractGap(
        field="reasoning.impact.structure_preference",
        reason="REASONING CONTRACT GAP: no approved impact relationship catalog",
    ),
    ReasoningContractGap(
        field="reasoning.strength.customer_meaning",
        reason="REASONING CONTRACT GAP: strength customer meaning belongs to Rewrite",
    ),
    ReasoningContractGap(
        field="reasoning.pattern.customer_meaning",
        reason="REASONING CONTRACT GAP: pattern customer meaning belongs to Rewrite",
    ),
    ReasoningContractGap(
        field="reasoning.useful_god.action",
        reason="REASONING CONTRACT GAP: useful-god action belongs to Action Builder",
    ),
    ReasoningContractGap(
        field="reasoning.identity.structured_self_direction",
        reason="REASONING CONTRACT GAP: identity meaning key is not an approved rule",
    ),
)
