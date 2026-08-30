"""Semantic and negative tests for Interpretation Builder (N-IMP-07)."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine
from engines.narrative_v2.interpretation import InterpretationBuilder

INTERPRETATION_DIR = (
    Path(__file__).resolve().parents[2] / "engines" / "narrative_v2" / "interpretation"
)

ACTION_MARKERS: tuple[str, ...] = (
    "You should",
    "Start ",
    "Priority",
    "Action",
    "Bạn nên",
)

PREDICTION_MARKERS: tuple[str, ...] = (
    "You will",
    "Definitely",
    "Surely",
    "Guaranteed",
    "chắc chắn",
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


def _blob(case_0001_canonical: dict[str, Any]) -> str:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    narrative = InterpretationBuilder().build(rewrite)
    return " ".join(
        part
        for part in (
            narrative.overview,
            narrative.observation,
            narrative.reasoning,
            narrative.meaning,
            narrative.impact,
            narrative.recommendation,
            narrative.closing,
        )
        if part
    )


def test_i4_no_action(case_0001_canonical: dict[str, Any]) -> None:
    blob = _blob(case_0001_canonical)
    for token in ACTION_MARKERS:
        assert token not in blob


def test_i5_no_prediction(case_0001_canonical: dict[str, Any]) -> None:
    blob = _blob(case_0001_canonical)
    for token in PREDICTION_MARKERS:
        assert token not in blob


def test_i6_no_json(case_0001_canonical: dict[str, Any]) -> None:
    blob = _blob(case_0001_canonical)
    assert "{" not in blob
    assert "}" not in blob
    assert "JSON" not in blob


def test_i7_no_engine_ids(case_0001_canonical: dict[str, Any]) -> None:
    blob = _blob(case_0001_canonical)
    assert "Engine" not in blob
    assert "NR-REL" not in blob
    assert "CanonicalAnalysis" not in blob


def test_i8_no_pack05() -> None:
    for path in INTERPRETATION_DIR.glob("*.py"):
        imported = _imported_modules(path)
        assert not any(
            item == "engines.narrative_engine" or item.startswith("engines.narrative_engine.")
            for item in imported
        )


def test_i9_no_portal() -> None:
    forbidden = (
        "applications.customer_portal",
        "applications.api",
        "OverviewCard",
        "InterpretationCard",
    )
    for path in INTERPRETATION_DIR.glob("*.py"):
        imported = _imported_modules(path)
        source = path.read_text(encoding="utf-8")
        for name in forbidden:
            assert not any(
                item == name or item.startswith(name + ".") for item in imported
            )
            if name in {"OverviewCard", "InterpretationCard"}:
                assert name not in source


def test_no_ten_gods_shensha_dump(case_0001_canonical: dict[str, Any]) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    narrative = InterpretationBuilder().build(rewrite)
    blob = " ".join(
        part
        for part in (
            narrative.overview,
            narrative.observation,
            narrative.reasoning,
            narrative.meaning,
            narrative.impact,
            narrative.recommendation,
            narrative.closing,
        )
        if part
    )
    extra = [item for item in rewrite.items if item.domain in {"ten_gods", "shensha"}]
    matched = sum(1 for item in extra if item.customer_language in blob)
    assert matched == 0
