"""Action Builder tests (N-IMP-08)."""

from __future__ import annotations

from typing import Any

import pytest

from engines.narrative_v2.action import ActionBuilder, ActionError, ActionPlanNarrative
from engines.narrative_v2.conversation import ConversationComposer
from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.interpretation import InterpretationBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine


def _plan(case_0001_canonical: dict[str, Any]) -> tuple[object, object, ActionPlanNarrative]:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    interpretation = InterpretationBuilder().build(rewrite)
    return rewrite, interpretation, ActionBuilder().build(rewrite, interpretation)


def test_a1_accepts_downstream_context_only(case_0001_canonical: dict[str, Any]) -> None:
    rewrite, interpretation, plan = _plan(case_0001_canonical)
    assert isinstance(plan, ActionPlanNarrative)
    with pytest.raises(ActionError, match="CommercialRewriteContext only"):
        ActionBuilder().build(case_0001_canonical, interpretation)
    with pytest.raises(ActionError, match="InterpretationNarrative only"):
        ActionBuilder().build(rewrite, case_0001_canonical)


def test_a2_returns_action_plan_narrative(case_0001_canonical: dict[str, Any]) -> None:
    _, _, plan = _plan(case_0001_canonical)
    assert isinstance(plan, ActionPlanNarrative)
    assert plan.status in {"complete", "partial", "insufficient", "invalid"}


def test_a3_decision_required_before_action(case_0001_canonical: dict[str, Any]) -> None:
    _, _, plan = _plan(case_0001_canonical)
    if plan.actions:
        assert plan.top_priority is not None
        for action in plan.actions:
            assert action.decision_id == plan.top_priority.decision_id or action.decision_id


def test_a4_exactly_one_top_priority_when_eligible(
    case_0001_canonical: dict[str, Any],
) -> None:
    _, _, plan = _plan(case_0001_canonical)
    if plan.status != "insufficient":
        assert plan.top_priority is not None
        assert plan.top_priority.decision_id


def test_a5_action_traces_to_decision(case_0001_canonical: dict[str, Any]) -> None:
    _, _, plan = _plan(case_0001_canonical)
    for action in plan.actions:
        assert action.decision_id
        assert action.references
        assert action.references[0].decision_ids == (action.decision_id,)


def test_consulting_is_optional(case_0001_canonical: dict[str, Any]) -> None:
    rewrite, interpretation, _ = _plan(case_0001_canonical)
    conversation = ConversationComposer().compose(rewrite, interpretation)
    first = ActionBuilder().build(rewrite, interpretation)
    second = ActionBuilder().build(rewrite, interpretation, conversation)
    assert first == second
