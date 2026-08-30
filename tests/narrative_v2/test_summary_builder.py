"""Summary Builder tests (N-IMP-06)."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

import pytest

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import CommercialRewriteContext, RewriteEngine
from engines.narrative_v2.summary import OverviewSummary, SummaryBuilder, SummaryError

SUMMARY_DIR = Path(__file__).resolve().parents[2] / "engines" / "narrative_v2" / "summary"

FORBIDDEN_SENTENCES: tuple[str, ...] = (
    "Bạn chắc chắn thành công.",
    "Bạn rất may mắn.",
    "Đây là giai đoạn tốt.",
    "Bạn nên bổ Hỏa.",
    "Bạn nên mở rộng kinh doanh.",
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


def _rewrite(case_0001_canonical: dict[str, Any]) -> CommercialRewriteContext:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    return RewriteEngine().rewrite(knowledge, reasoning, evidence)


def test_s1_accepts_rewrite_context_only(case_0001_canonical: dict[str, Any]) -> None:
    rewrite = _rewrite(case_0001_canonical)
    overview = SummaryBuilder().build(rewrite)
    assert isinstance(overview, OverviewSummary)
    with pytest.raises(SummaryError, match="CommercialRewriteContext only"):
        SummaryBuilder().build(case_0001_canonical)


def test_s2_returns_overview_summary(case_0001_canonical: dict[str, Any]) -> None:
    overview = SummaryBuilder().build(_rewrite(case_0001_canonical))
    assert isinstance(overview, OverviewSummary)
    assert overview.status in {"complete", "partial", "insufficient", "invalid"}


def test_s3_exactly_one_primary_insight(case_0001_canonical: dict[str, Any]) -> None:
    overview = SummaryBuilder().build(_rewrite(case_0001_canonical))
    meta = dict(overview.metadata)
    assert meta["primary_insight_count"] == "1"
    assert meta["primary_rewrite_id"]
    assert meta["primary_rewrite_id"].count(",") == 0


def test_s5_no_direct_canonical_analysis_read() -> None:
    for path in SUMMARY_DIR.glob("*.py"):
        imported = _imported_modules(path)
        assert "CanonicalAnalysis" not in imported
        for name in imported:
            assert "canonical_analysis" not in name.lower()


def test_s6_no_direct_evidence_composition() -> None:
    for path in SUMMARY_DIR.glob("*.py"):
        imported = _imported_modules(path)
        for name in imported:
            assert "evidence" not in name.lower()
            assert "reasoning" not in name.lower()
            assert "knowledge" not in name.lower() or name.startswith(
                "engines.narrative_v2.rewrite"
            )


def test_s7_no_raw_domain_concatenation(case_0001_canonical: dict[str, Any]) -> None:
    rewrite = _rewrite(case_0001_canonical)
    overview = SummaryBuilder().build(rewrite)
    blob = " ".join(
        part
        for part in (
            overview.headline,
            overview.summary,
            overview.identity,
            overview.balance,
            overview.conclusion,
        )
        if part
    )
    ten_gods = [item for item in rewrite.items if item.domain == "ten_gods"]
    shensha = [item for item in rewrite.items if item.domain == "shensha"]
    for group in (ten_gods, shensha):
        if len(group) < 2:
            continue
        matched = sum(1 for item in group if item.customer_language in blob)
        assert matched < len(group)


def test_s11_output_traceable_to_rewrite(case_0001_canonical: dict[str, Any]) -> None:
    rewrite = _rewrite(case_0001_canonical)
    overview = SummaryBuilder().build(rewrite)
    rewrite_ids = {item.rewrite_id for item in rewrite.items}
    for ref in overview.references:
        assert ref.rewrite_ids
        assert set(ref.rewrite_ids) <= rewrite_ids
        assert ref.knowledge_ids
        assert ref.reasoning_ids
        assert ref.evidence_ids


def test_s17_deterministic(case_0001_canonical: dict[str, Any]) -> None:
    rewrite = _rewrite(case_0001_canonical)
    first = SummaryBuilder().build(rewrite)
    second = SummaryBuilder().build(rewrite)
    assert first == second


def test_insufficient_when_no_core_insight() -> None:
    empty = CommercialRewriteContext(
        items=(),
        unresolved=(),
        references=(),
        metadata=(),
        status="insufficient",
    )
    overview = SummaryBuilder().build(empty)
    assert overview.status == "insufficient"
    assert overview.headline is None
    assert overview.summary is None


def test_forbidden_sentences_not_generated(case_0001_canonical: dict[str, Any]) -> None:
    overview = SummaryBuilder().build(_rewrite(case_0001_canonical))
    blob = " ".join(
        part
        for part in (
            overview.headline,
            overview.summary,
            overview.identity,
            overview.balance,
            overview.conclusion,
        )
        if part
    )
    for sentence in FORBIDDEN_SENTENCES:
        assert sentence not in blob
