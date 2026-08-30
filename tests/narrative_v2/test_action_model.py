"""ActionPlanNarrative model contract tests (N-IMP-08)."""

from __future__ import annotations

from dataclasses import fields
from typing import Any

from engines.narrative_v2.action import ActionBuilder, ActionPlanNarrative
from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.interpretation import InterpretationBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine

CANONICAL_FIELDS = (
    "top_priority",
    "actions",
    "warnings",
    "current_period",
    "references",
    "metadata",
    "status",
)


def test_canonical_public_fields_only() -> None:
    names = tuple(item.name for item in fields(ActionPlanNarrative))
    assert names == CANONICAL_FIELDS


def test_case_0001_status_and_optional_current_period(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    interpretation = InterpretationBuilder().build(rewrite)
    plan = ActionBuilder().build(rewrite, interpretation)
    assert plan.status in {"complete", "partial", "insufficient", "invalid"}
    assert plan.current_period is None
    if plan.status != "insufficient":
        assert plan.top_priority is not None
        assert 1 <= len(plan.actions) <= 6
