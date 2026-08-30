"""Conversation flow and duplicate-merge tests (N-IMP-07A)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.conversation import ConversationComposer, FLOW_STAGES
from engines.narrative_v2.conversation.conversation_bridge import is_duplicate
from engines.narrative_v2.conversation.conversation_flow import split_sentences
from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.interpretation import InterpretationBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine


def _conversation(case_0001_canonical: dict[str, Any]) -> tuple[object, object]:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    interpretation = InterpretationBuilder().build(rewrite)
    return interpretation, ConversationComposer().compose(rewrite, interpretation)


def test_flow_is_one_conversation(case_0001_canonical: dict[str, Any]) -> None:
    interpretation, conversation = _conversation(case_0001_canonical)
    assert conversation.flow
    assert conversation.flow != " ".join(
        getattr(interpretation, stage)
        for stage in FLOW_STAGES
        if getattr(interpretation, stage)
    )
    assert len(split_sentences(conversation.flow)) >= 2


def test_duplicate_closing_merged(case_0001_canonical: dict[str, Any]) -> None:
    interpretation, conversation = _conversation(case_0001_canonical)
    assert is_duplicate(interpretation.closing, interpretation.observation)
    assert conversation.closing is None
    assert conversation.observation == interpretation.observation
    assert conversation.flow.count(interpretation.observation) == 1


def test_duplicate_impact_not_repeated_in_flow(case_0001_canonical: dict[str, Any]) -> None:
    interpretation, conversation = _conversation(case_0001_canonical)
    assert interpretation.impact
    assert interpretation.impact in (interpretation.meaning or "")
    assert conversation.flow.count(interpretation.impact) == 1
