"""Action language and determinism tests (N-IMP-08)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.action import ActionBuilder
from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.interpretation import InterpretationBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.language import SentenceLibrary, SentenceRegistry
from engines.narrative_v2.language.language_asset_status import STATUS_APPROVED, STATUS_DRAFT
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine

SHORTHAND: tuple[str, ...] = (
    "Dựng khung vừa đủ để việc chạy",
    "Giữ một nền học/dưỡng",
    "Mở một kênh thoát có phép",
    "chỗ dưỡng",
    "kênh thoát",
)


def _plan(case_0001_canonical: dict[str, Any]) -> object:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    interpretation = InterpretationBuilder().build(rewrite)
    return ActionBuilder().build(rewrite, interpretation)


def test_a16_sentence_assets_approved_only() -> None:
    assets = [
        item
        for item in SentenceRegistry().assets()
        if item.category in {"decision", "action", "warning"}
    ]
    assert assets
    selected = SentenceLibrary().select(
        "core.pattern_context",
        category="decision",
        domain="pattern",
        meaning_key="knowledge.pattern.chinh_an",
    )
    assert selected is not None
    assert selected.status == STATUS_APPROVED
    drafts = [item for item in assets if item.status == STATUS_DRAFT]
    assert not drafts


def test_a17_natural_customer_language(case_0001_canonical: dict[str, Any]) -> None:
    plan = _plan(case_0001_canonical)
    blob = " ".join(
        part
        for part in (
            plan.top_priority.description if plan.top_priority else "",
            *(item.description for item in plan.actions),
            *(item.description for item in plan.warnings),
        )
        if part
    )
    for token in SHORTHAND:
        assert token not in blob
    if plan.actions:
        for action in plan.actions:
            assert action.description.startswith("Bạn")


def test_a18_same_input_same_output(case_0001_canonical: dict[str, Any]) -> None:
    first = _plan(case_0001_canonical)
    second = _plan(case_0001_canonical)
    assert first == second
