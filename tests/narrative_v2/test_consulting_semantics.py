"""Consulting Style semantic and negative tests (N-IMP-07B)."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from engines.narrative_v2.communication import CommunicationEngine, semantic_fingerprint
from engines.narrative_v2.conversation import ConversationComposer, ConversationNarrative
from engines.narrative_v2.conversation.conversation_context import ConversationReference
from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.interpretation import InterpretationBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine

COMMUNICATION_DIR = (
    Path(__file__).resolve().parents[2] / "engines" / "narrative_v2" / "communication"
)


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def _pair(case_0001_canonical: dict[str, Any]) -> tuple[ConversationNarrative, object]:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    interpretation = InterpretationBuilder().build(rewrite)
    conversation = ConversationComposer().compose(rewrite, interpretation)
    return conversation, CommunicationEngine().style(conversation)


def _synthetic(observation: str) -> ConversationNarrative:
    return ConversationNarrative(
        observation=observation,
        reasoning=None,
        meaning=None,
        impact=None,
        recommendation=None,
        closing=None,
        flow=observation,
        references=(
            ConversationReference(
                field="observation",
                rewrite_ids=("rewrite.demo.001",),
                knowledge_ids=("knowledge.demo",),
                reasoning_ids=("reasoning.demo",),
                evidence_ids=("evidence.demo",),
            ),
        ),
        metadata=(),
        status="partial",
    )


def test_cs5_cs6_cs7_cs8_no_escalation_prediction_action_or_new_meaning(
    case_0001_canonical: dict[str, Any],
) -> None:
    conversation, consulting = _pair(case_0001_canonical)
    blob = consulting.flow
    assert "chắc chắn" not in blob
    assert "Bạn nên" not in blob
    assert "thành công" not in blob
    assert "may mắn" not in blob
    assert semantic_fingerprint(consulting.flow) == semantic_fingerprint(conversation.flow)


def test_negative_shensha_not_escalated() -> None:
    consulting = CommunicationEngine().style(_synthetic("có lớp giảm xung."))
    assert "quý nhân bảo vệ" not in consulting.flow
    assert "Bạn sẽ luôn được quý nhân bảo vệ." not in consulting.flow


def test_negative_strength_not_escalated() -> None:
    consulting = CommunicationEngine().style(_synthetic("chịu tải tốt."))
    assert "chắc chắn thành công" not in consulting.flow
    assert "Bạn chắc chắn thành công trong sự nghiệp." not in consulting.flow


def test_negative_hong_loan_not_predicted() -> None:
    consulting = CommunicationEngine().style(_synthetic("Hồng Loan."))
    assert "đường tình duyên rất tốt" not in consulting.flow
    assert "Bạn có đường tình duyên rất tốt." not in consulting.flow


def test_negative_useful_god_not_action() -> None:
    consulting = CommunicationEngine().style(_synthetic("Dụng thần Hỏa."))
    assert "màu đỏ" not in consulting.flow
    assert "hướng Nam" not in consulting.flow
    assert "Bạn nên dùng màu đỏ và đi hướng Nam." not in consulting.flow


def test_cs14_cs15_cs16_no_pack05_portal_dashboard() -> None:
    forbidden = (
        "engines.narrative_engine",
        "applications.customer_portal",
        "applications.api",
        "OverviewCard",
        "Dashboard",
    )
    for path in COMMUNICATION_DIR.glob("*.py"):
        imported = _imported_modules(path)
        source = path.read_text(encoding="utf-8")
        for name in forbidden:
            assert not any(item == name or item.startswith(name + ".") for item in imported)
            if name in {"OverviewCard", "Dashboard"}:
                assert name not in source


def test_cs17_sentence_library_gaps_preserved(case_0001_canonical: dict[str, Any]) -> None:
    _, consulting = _pair(case_0001_canonical)
    meta = dict(consulting.metadata)
    assert meta["sentence_library"] in {"approved", "partial"}
    assert meta["consulting_language_asset_gap"] in {"true", "false"}
    assert consulting.status in {"styled", "partial"}
