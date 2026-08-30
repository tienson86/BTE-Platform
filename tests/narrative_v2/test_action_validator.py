"""ActionValidator tests (N-IMP-08)."""

from __future__ import annotations

from typing import Any

import pytest

from engines.narrative_v2.action import (
    ActionBuilder,
    ActionItem,
    ActionPlanNarrative,
    ActionReference,
    ActionValidationError,
    ActionValidator,
    DecisionBuilder,
)
from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.interpretation import InterpretationBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine


def _built(case_0001_canonical: dict[str, Any]) -> tuple[object, object, object, object]:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    interpretation = InterpretationBuilder().build(rewrite)
    plan = ActionBuilder().build(rewrite, interpretation)
    decisions = DecisionBuilder().build(rewrite, interpretation).items
    return plan, rewrite, decisions, interpretation


def test_case_0001_passes_validator(case_0001_canonical: dict[str, Any]) -> None:
    plan, rewrite, decisions, _ = _built(case_0001_canonical)
    outcome = ActionValidator().validate(plan, rewrite, decisions)
    assert outcome.passed is True
    assert outcome.status == "PASS"


def test_action_without_decision_is_rejected(case_0001_canonical: dict[str, Any]) -> None:
    plan, rewrite, decisions, _ = _built(case_0001_canonical)
    if not plan.actions:
        pytest.skip("no actions")
    item = plan.actions[0]
    broken = ActionItem(
        action_id=item.action_id,
        decision_id="",
        title=item.title,
        description=item.description,
        category=item.category,
        priority=item.priority,
        source_knowledge_ids=item.source_knowledge_ids,
        references=item.references,
        status=item.status,
    )
    context = ActionPlanNarrative(
        top_priority=plan.top_priority,
        actions=(broken,),
        warnings=plan.warnings,
        current_period=None,
        references=plan.references,
        metadata=plan.metadata,
        status=plan.status,
    )
    with pytest.raises(ActionValidationError):
        ActionValidator().assert_valid(context, rewrite, decisions)


def test_a15_contradictory_actions_rejected(case_0001_canonical: dict[str, Any]) -> None:
    plan, rewrite, decisions, _ = _built(case_0001_canonical)
    if not plan.actions:
        pytest.skip("no actions")
    item = plan.actions[0]
    expand = ActionItem(
        action_id="action.conflict.expand.001",
        decision_id=item.decision_id,
        title="Mở rộng",
        description="Bạn hãy mở rộng ngay.",
        category=item.category,
        priority=1,
        source_knowledge_ids=item.source_knowledge_ids,
        references=(
            ActionReference(
                field="actions",
                rewrite_ids=item.references[0].rewrite_ids,
                knowledge_ids=item.source_knowledge_ids,
                reasoning_ids=item.references[0].reasoning_ids,
                evidence_ids=item.references[0].evidence_ids,
                decision_ids=(item.decision_id,),
            ),
        ),
        status=item.status,
    )
    context = ActionPlanNarrative(
        top_priority=plan.top_priority,
        actions=tuple(sorted((item, expand), key=lambda row: (-row.priority, row.action_id))),
        warnings=(),
        current_period=None,
        references=plan.references,
        metadata=plan.metadata,
        status=plan.status,
    )
    with pytest.raises(ActionValidationError):
        ActionValidator().assert_valid(context, rewrite, decisions)
