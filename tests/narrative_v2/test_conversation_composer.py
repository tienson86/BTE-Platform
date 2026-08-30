"""Conversation Composer tests (N-IMP-07A)."""

from __future__ import annotations

from typing import Any

import pytest

from engines.narrative_v2.conversation import (
    ConversationComposer,
    ConversationError,
    ConversationNarrative,
    meaning_hash,
)
from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.interpretation import InterpretationBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import CommercialRewriteContext, RewriteEngine


def _pipeline(
    case_0001_canonical: dict[str, Any],
) -> tuple[CommercialRewriteContext, object, ConversationNarrative]:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    interpretation = InterpretationBuilder().build(rewrite)
    conversation = ConversationComposer().compose(rewrite, interpretation)
    return rewrite, interpretation, conversation


def test_accepts_rewrite_and_interpretation_only(
    case_0001_canonical: dict[str, Any],
) -> None:
    rewrite, interpretation, conversation = _pipeline(case_0001_canonical)
    assert isinstance(conversation, ConversationNarrative)
    with pytest.raises(ConversationError, match="CommercialRewriteContext only"):
        ConversationComposer().compose(case_0001_canonical, interpretation)
    with pytest.raises(ConversationError, match="InterpretationNarrative only"):
        ConversationComposer().compose(rewrite, case_0001_canonical)


def test_meaning_hash_unchanged(case_0001_canonical: dict[str, Any]) -> None:
    _, interpretation, conversation = _pipeline(case_0001_canonical)
    assert conversation.meaning == interpretation.meaning
    assert meaning_hash(conversation.meaning) == meaning_hash(interpretation.meaning)


def test_recommendation_unchanged(case_0001_canonical: dict[str, Any]) -> None:
    _, interpretation, conversation = _pipeline(case_0001_canonical)
    assert conversation.recommendation == interpretation.recommendation


def test_deterministic(case_0001_canonical: dict[str, Any]) -> None:
    rewrite, interpretation, _ = _pipeline(case_0001_canonical)
    first = ConversationComposer().compose(rewrite, interpretation)
    second = ConversationComposer().compose(rewrite, interpretation)
    assert first == second
