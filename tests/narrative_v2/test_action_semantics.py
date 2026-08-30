"""Semantic and negative tests for Action Builder (N-IMP-08)."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from engines.narrative_v2.action import ActionBuilder
from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.interpretation import InterpretationBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine

ACTION_DIR = Path(__file__).resolve().parents[2] / "engines" / "narrative_v2" / "action"


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
    interpretation = InterpretationBuilder().build(rewrite)
    plan = ActionBuilder().build(rewrite, interpretation)
    parts: list[str] = []
    if plan.top_priority is not None:
        parts.extend((plan.top_priority.title, plan.top_priority.description))
    for action in plan.actions:
        parts.extend((action.title, action.description))
    for warning in plan.warnings:
        parts.extend((warning.title, warning.description))
    return " ".join(parts)


def test_a8_no_raw_useful_god_inference(case_0001_canonical: dict[str, Any]) -> None:
    blob = _blob(case_0001_canonical)
    assert "màu đỏ" not in blob
    assert "hướng Nam" not in blob
    assert "Dụng thần" not in blob


def test_a9_no_raw_shensha_inference(case_0001_canonical: dict[str, Any]) -> None:
    blob = _blob(case_0001_canonical)
    assert "hãy kết hôn" not in blob
    assert "Hồng Loan" not in blob


def test_a10_no_raw_luck_inference(case_0001_canonical: dict[str, Any]) -> None:
    blob = _blob(case_0001_canonical)
    assert "Ất Tỵ" not in blob
    assert "hãy mở rộng kinh doanh" not in blob


def test_a11_no_prediction(case_0001_canonical: dict[str, Any]) -> None:
    blob = _blob(case_0001_canonical)
    assert "chắc chắn" not in blob
    assert "nhất định" not in blob


def test_a12_no_fear_language(case_0001_canonical: dict[str, Any]) -> None:
    blob = _blob(case_0001_canonical)
    assert "Nguy hiểm" not in blob
    assert "Đại hung" not in blob
    assert "Tai họa" not in blob


def test_a13_no_unsupported_action(case_0001_canonical: dict[str, Any]) -> None:
    blob = _blob(case_0001_canonical)
    assert "hãy mở rộng mạnh hơn" not in blob
    assert "hãy học thêm" not in blob


def test_a14_no_duplicate_actions(case_0001_canonical: dict[str, Any]) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    interpretation = InterpretationBuilder().build(rewrite)
    plan = ActionBuilder().build(rewrite, interpretation)
    texts = [item.description.casefold() for item in plan.actions]
    assert len(texts) == len(set(texts))


def test_a7_a22_a23_a24_no_raw_engine_portal_or_ui12() -> None:
    forbidden = (
        "engines.narrative_engine",
        "applications.customer_portal",
        "applications.api",
        "CanonicalAnalysis",
        "ui_12",
        "UI-12",
        "UI_12",
    )
    for path in ACTION_DIR.glob("*.py"):
        imported = _imported_modules(path)
        source = path.read_text(encoding="utf-8")
        for name in forbidden:
            assert not any(item == name or item.startswith(name + ".") for item in imported)
            if name in {"ui_12", "UI-12", "UI_12", "CanonicalAnalysis"}:
                assert name not in source
