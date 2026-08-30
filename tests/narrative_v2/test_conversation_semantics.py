"""Meaning preservation and negative tests for Conversation Composer (N-IMP-07A)."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from engines.narrative_v2.conversation import ConversationComposer, meaning_hash
from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.interpretation import InterpretationBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine

CONVERSATION_DIR = (
    Path(__file__).resolve().parents[2] / "engines" / "narrative_v2" / "conversation"
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


def _pair(case_0001_canonical: dict[str, Any]) -> tuple[object, object]:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    interpretation = InterpretationBuilder().build(rewrite)
    return interpretation, ConversationComposer().compose(rewrite, interpretation)


def test_meaning_preservation(case_0001_canonical: dict[str, Any]) -> None:
    interpretation, conversation = _pair(case_0001_canonical)
    assert conversation.meaning == interpretation.meaning
    assert meaning_hash(conversation.meaning) == meaning_hash(interpretation.meaning)
    assert conversation.recommendation == interpretation.recommendation
    assert conversation.observation == interpretation.observation
    assert conversation.reasoning == interpretation.reasoning
    assert conversation.impact == interpretation.impact


def test_no_action_or_prediction(case_0001_canonical: dict[str, Any]) -> None:
    _, conversation = _pair(case_0001_canonical)
    blob = conversation.flow
    assert "Bạn nên" not in blob
    assert "You should" not in blob
    assert "chắc chắn" not in blob
    assert "You will" not in blob


def test_no_pack05_or_portal() -> None:
    forbidden = (
        "engines.narrative_engine",
        "applications.customer_portal",
        "applications.api",
        "CanonicalAnalysis",
    )
    for path in CONVERSATION_DIR.glob("*.py"):
        imported = _imported_modules(path)
        for name in forbidden:
            assert not any(item == name or item.startswith(name + ".") for item in imported)
