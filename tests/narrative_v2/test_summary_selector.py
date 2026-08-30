"""Insight selection tests (N-IMP-06)."""

from __future__ import annotations

from engines.narrative_v2.rewrite.rewrite_item import RewriteItem, RewriteReference
from engines.narrative_v2.summary.summary_selector import SummarySelector


def _item(
    rewrite_id: str,
    semantic_key: str,
    domain: str,
    language: str = "Bạn có nền tảng ổn định.",
) -> RewriteItem:
    return RewriteItem(
        rewrite_id=rewrite_id,
        semantic_key=semantic_key,
        domain=domain,
        source_knowledge_ids=(f"knowledge.{domain}.x",),
        source_reasoning_ids=("NR-REL-001",),
        source_evidence_ids=("evidence.x",),
        source_meaning="Có nền tảng ổn định.",
        normalized_meaning="Có nền tảng ổn định.",
        customer_language=language,
        strategy="clarification",
        style="consultant",
        status="rewritten",
        references=(
            RewriteReference(
                knowledge_id=f"knowledge.{domain}.x",
                source_path="knowledge/demo.json",
                reasoning_ids=("NR-REL-001",),
                evidence_ids=("evidence.x",),
            ),
        ),
    )


def test_s4_pattern_context_beats_ten_gods() -> None:
    items = (
        _item("rewrite.ten_gods.a.001", "core.pattern_ten_gods_relation", "ten_gods"),
        _item("rewrite.pattern.a.001", "core.pattern_context", "pattern"),
        _item("rewrite.shensha.a.001", "boundary.approved_rule_unavailable", "shensha"),
    )
    selection = SummarySelector().select(items)
    assert selection is not None
    assert selection.primary.rewrite_id == "rewrite.pattern.a.001"


def test_s4_pattern_domain_beats_strength_on_same_key() -> None:
    items = (
        _item("rewrite.strength.strong.001", "core.pattern_context", "strength"),
        _item("rewrite.pattern.chinh_an.001", "core.pattern_context", "pattern"),
    )
    selection = SummarySelector().select(items)
    assert selection is not None
    assert selection.primary.rewrite_id == "rewrite.pattern.chinh_an.001"
    assert selection.supporting is not None
    assert selection.supporting.rewrite_id == "rewrite.strength.strong.001"


def test_s4_deterministic_order() -> None:
    items = (
        _item("rewrite.strength.strong.001", "core.pattern_context", "strength"),
        _item("rewrite.pattern.chinh_an.001", "core.pattern_context", "pattern"),
        _item("rewrite.ten_gods.a.001", "core.pattern_ten_gods_relation", "ten_gods"),
    )
    selector = SummarySelector()
    first = selector.select(items)
    second = selector.select(tuple(reversed(items)))
    assert first == second


def test_no_core_insight_returns_none() -> None:
    items = (
        _item("rewrite.shensha.a.001", "boundary.approved_rule_unavailable", "shensha"),
    )
    assert SummarySelector().select(items) is None
