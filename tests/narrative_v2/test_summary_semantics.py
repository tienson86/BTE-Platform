"""Semantic and negative tests for Summary Builder (N-IMP-06)."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine
from engines.narrative_v2.summary import SummaryBuilder

SUMMARY_DIR = Path(__file__).resolve().parents[2] / "engines" / "narrative_v2" / "summary"

RAW_BYPASS_TERMS: tuple[str, ...] = (
    "strong",
    "chinh_an",
    "Hỏa",
    "Hồng Loan",
    "Ất Tỵ",
)

FORBIDDEN_CLAIMS: tuple[str, ...] = (
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


def _overview_blob(case_0001_canonical: dict[str, Any]) -> tuple[object, str, object]:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
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
    return overview, blob, rewrite


def test_s8_no_action_generated(case_0001_canonical: dict[str, Any]) -> None:
    _, blob, _ = _overview_blob(case_0001_canonical)
    assert "Bạn nên" not in blob
    assert "Action" not in blob


def test_s9_no_prediction_generated(case_0001_canonical: dict[str, Any]) -> None:
    _, blob, _ = _overview_blob(case_0001_canonical)
    assert "chắc chắn" not in blob
    assert "Đây là giai đoạn tốt." not in blob


def test_s10_no_raw_technical_ids(case_0001_canonical: dict[str, Any]) -> None:
    _, blob, _ = _overview_blob(case_0001_canonical)
    assert "Engine" not in blob
    assert "NR-REL" not in blob
    assert "CanonicalAnalysis" not in blob
    assert "{" not in blob


def test_s12_missing_useful_god_not_invented(case_0001_canonical: dict[str, Any]) -> None:
    overview, blob, rewrite = _overview_blob(case_0001_canonical)
    unresolved = {entry.semantic_key for entry in rewrite.unresolved}
    assert "core.useful_god_context" in unresolved
    assert overview.balance is None
    assert "Dụng thần" not in blob
    assert "Bạn nên bổ Hỏa" not in blob


def test_s13_missing_temperature_not_invented(case_0001_canonical: dict[str, Any]) -> None:
    overview, blob, rewrite = _overview_blob(case_0001_canonical)
    unresolved = {entry.semantic_key for entry in rewrite.unresolved}
    assert "core.temperature_balancing_context" in unresolved
    assert overview.balance is None
    assert "Điều Hậu" not in blob


def test_s14_missing_luck_not_invented(case_0001_canonical: dict[str, Any]) -> None:
    _, blob, rewrite = _overview_blob(case_0001_canonical)
    unresolved = {entry.semantic_key for entry in rewrite.unresolved}
    assert "core.luck_temporal_context" in unresolved
    assert "Ất Tỵ" not in blob
    assert "Đây là giai đoạn tốt." not in blob


def test_s15_no_ui04_or_portal_prose() -> None:
    forbidden = (
        "applications.customer_portal",
        "applications.api",
        "ui_04",
        "OverviewCard",
    )
    for path in SUMMARY_DIR.glob("*.py"):
        imported = _imported_modules(path)
        source = path.read_text(encoding="utf-8")
        for name in forbidden:
            assert not any(
                item == name or item.startswith(name + ".")
                for item in imported
            )
            if name in {"OverviewCard", "ui_04"}:
                assert name not in source


def test_s16_no_pack05_read() -> None:
    for path in SUMMARY_DIR.glob("*.py"):
        imported = _imported_modules(path)
        assert not any(
            item == "engines.narrative_engine" or item.startswith("engines.narrative_engine.")
            for item in imported
        )


def test_raw_terms_do_not_bypass_rewrite(case_0001_canonical: dict[str, Any]) -> None:
    overview, blob, rewrite = _overview_blob(case_0001_canonical)
    del overview
    approved = " ".join(item.customer_language for item in rewrite.items)
    for term in RAW_BYPASS_TERMS:
        if term not in approved:
            assert term not in blob


def test_forbidden_generated_claims(case_0001_canonical: dict[str, Any]) -> None:
    _, blob, _ = _overview_blob(case_0001_canonical)
    for claim in FORBIDDEN_CLAIMS:
        assert claim not in blob
