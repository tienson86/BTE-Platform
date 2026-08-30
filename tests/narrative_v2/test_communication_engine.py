"""Commercial Communication / Consulting Style tests (N-IMP-07B)."""

from __future__ import annotations

from typing import Any

import pytest

from engines.narrative_v2.communication import (
    DEFAULT_PROFILE_ID,
    CommunicationEngine,
    CommunicationError,
    ConsultingNarrative,
    semantic_fingerprint,
)
from engines.narrative_v2.conversation import ConversationComposer, ConversationNarrative
from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.interpretation import InterpretationBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine


def _conversation(case_0001_canonical: dict[str, Any]) -> ConversationNarrative:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    interpretation = InterpretationBuilder().build(rewrite)
    return ConversationComposer().compose(rewrite, interpretation)


def test_cs1_cs2_accepts_conversation_returns_consulting(
    case_0001_canonical: dict[str, Any],
) -> None:
    conversation = _conversation(case_0001_canonical)
    consulting = CommunicationEngine().style(conversation)
    assert isinstance(consulting, ConsultingNarrative)
    assert consulting.flow
    assert consulting.segments


def test_cs3_rejects_canonical_analysis(case_0001_canonical: dict[str, Any]) -> None:
    with pytest.raises(CommunicationError, match="ConversationNarrative only"):
        CommunicationEngine().style(case_0001_canonical)


def test_cs4_meaning_fingerprint_preserved(case_0001_canonical: dict[str, Any]) -> None:
    conversation = _conversation(case_0001_canonical)
    consulting = CommunicationEngine().style(conversation)
    assert semantic_fingerprint(consulting.flow) == semantic_fingerprint(conversation.flow)


def test_cs9_cs10_deterministic_profile(case_0001_canonical: dict[str, Any]) -> None:
    conversation = _conversation(case_0001_canonical)
    engine = CommunicationEngine()
    first = engine.style(conversation)
    second = engine.style(conversation)
    assert first == second
    assert first.style_profile == DEFAULT_PROFILE_ID
    assert first.segments[0].frame_id == "frame.observation.highlight"


def test_cs18_same_conversation_same_output(case_0001_canonical: dict[str, Any]) -> None:
    conversation = _conversation(case_0001_canonical)
    first = CommunicationEngine().style(conversation)
    second = CommunicationEngine().style(conversation)
    assert first == second
