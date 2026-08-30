"""Conversation transition tests (N-IMP-07A)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.conversation import ALLOWED_TRANSITIONS, ConversationComposer
from engines.narrative_v2.conversation.conversation_transition import (
    apply_transition,
    leading_connector,
    strip_transition,
)
from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.interpretation import InterpretationBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine


def test_apply_and_strip_roundtrip() -> None:
    body = "Bạn có nền lực để chịu tải."
    for connector in ALLOWED_TRANSITIONS:
        wrapped = apply_transition(connector, body)
        assert wrapped.startswith(connector)
        assert strip_transition(wrapped) == body
        assert leading_connector(wrapped) == connector


def test_case_0001_uses_registered_transitions_only(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    interpretation = InterpretationBuilder().build(rewrite)
    conversation = ConversationComposer().compose(rewrite, interpretation)
    assert "Vì vậy, " in conversation.flow
    assert "Từ đó, " in conversation.flow
    assert "Đồng thời, " in conversation.flow
    for token in ("randomly", "bỗng nhiên", "LLM"):
        assert token not in conversation.flow
