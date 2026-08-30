"""Consulting style fluency tests (N-IMP-07B)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.communication import CommunicationEngine
from engines.narrative_v2.conversation import ConversationComposer
from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.interpretation import InterpretationBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine


def _styled(case_0001_canonical: dict[str, Any]) -> tuple[object, object]:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    interpretation = InterpretationBuilder().build(rewrite)
    conversation = ConversationComposer().compose(rewrite, interpretation)
    return conversation, CommunicationEngine().style(conversation)


def test_cs11_transitions_improve_without_semantic_change(
    case_0001_canonical: dict[str, Any],
) -> None:
    conversation, consulting = _styled(case_0001_canonical)
    assert ", Bạn" not in consulting.flow
    assert "Điểm nổi bật ở đây là" in consulting.flow
    assert "Điều này cho thấy" in consulting.flow
    assert conversation.meaning
    assert "chỗ dưỡng" not in consulting.flow
    assert "chỗ dưỡng" not in (conversation.observation or "")


def test_cs12_repetition_handled_safely(case_0001_canonical: dict[str, Any]) -> None:
    conversation, consulting = _styled(case_0001_canonical)
    assert conversation.recommendation
    assert "kênh thoát" not in consulting.flow
    assert consulting.flow.casefold().count("hữu ích khi cần ủ") <= 1


def test_cs13_vietnamese_capitalization(case_0001_canonical: dict[str, Any]) -> None:
    _, consulting = _styled(case_0001_canonical)
    assert ", Bạn" not in consulting.flow
    assert "Vì vậy, Bạn" not in consulting.flow
