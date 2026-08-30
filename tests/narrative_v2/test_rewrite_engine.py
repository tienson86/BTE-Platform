"""Commercial Rewrite Engine tests (N-IMP-05)."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

import pytest

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import (
    CommercialRewriteContext,
    RewriteEngine,
    RewriteError,
)

REWRITE_DIR = Path(__file__).resolve().parents[2] / "engines" / "narrative_v2" / "rewrite"

FORBIDDEN_SENTENCES: tuple[str, ...] = (
    "Bạn chắc chắn thành công.",
    "Bạn nhất định giàu.",
    "Bạn sẽ ly hôn.",
    "Đây là vận đại cát.",
    "Bạn nên dùng màu đỏ vì Hỏa là Dụng thần.",
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


def _pipeline(case_0001_canonical: dict[str, Any]) -> tuple[object, object]:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    return knowledge, RewriteEngine().rewrite(knowledge, reasoning, evidence)


def test_rw1_rw2_accepts_knowledge_returns_context(
    case_0001_canonical: dict[str, Any],
) -> None:
    knowledge, context = _pipeline(case_0001_canonical)
    assert isinstance(context, CommercialRewriteContext)
    del knowledge


def test_rw1_rejects_canonical_analysis(case_0001_canonical: dict[str, Any]) -> None:
    with pytest.raises(RewriteError, match="NarrativeKnowledgeContext only"):
        RewriteEngine().rewrite(case_0001_canonical)


def test_rw3_only_resolved_knowledge_rewrites(
    case_0001_canonical: dict[str, Any],
) -> None:
    knowledge, context = _pipeline(case_0001_canonical)
    known = {item.knowledge_id for item in knowledge.items}
    for item in context.items:
        assert set(item.source_knowledge_ids) <= known


def test_rw4_unresolved_knowledge_remains_unresolved(
    case_0001_canonical: dict[str, Any],
) -> None:
    _, context = _pipeline(case_0001_canonical)
    keys = {entry.semantic_key for entry in context.unresolved}
    assert "core.temperature_balancing_context" in keys
    assert "core.luck_temporal_context" in keys


def test_rw5_meaning_preserved(case_0001_canonical: dict[str, Any]) -> None:
    _, context = _pipeline(case_0001_canonical)
    assert context.items
    for item in context.items:
        assert item.source_meaning.strip()
        meta = dict(item.metadata)
        if meta.get("sentence_source") == "sentence_library":
            assert item.customer_language.startswith("Bạn")
            assert item.source_knowledge_ids
            continue
        source = item.source_meaning.rstrip(".").casefold()
        customer = item.customer_language.casefold()
        assert source in customer or source[1:] in customer


def test_rw10_stable_rewrite_ids(case_0001_canonical: dict[str, Any]) -> None:
    _, context = _pipeline(case_0001_canonical)
    ids = [item.rewrite_id for item in context.items]
    assert ids == sorted(ids)
    for rewrite_id in ids:
        assert rewrite_id.startswith("rewrite.")
    assert len(ids) == len(set(ids))


def test_rw11_stable_order(case_0001_canonical: dict[str, Any]) -> None:
    _, context = _pipeline(case_0001_canonical)
    ids = [item.rewrite_id for item in context.items]
    assert ids == sorted(ids)


def test_rw13_no_llm_or_network() -> None:
    for path in REWRITE_DIR.glob("*.py"):
        source = path.read_text(encoding="utf-8").lower()
        for token in ("openai", "httpx", "requests", "urllib", "embed"):
            assert token not in source


def test_rw19_rw20_no_pack05_or_portal_imports() -> None:
    forbidden = (
        "engines.narrative_engine",
        "applications.customer_portal",
        "applications.api.services.narrative_result_truth",
    )
    for path in REWRITE_DIR.glob("*.py"):
        imported = _imported_modules(path)
        for name in forbidden:
            assert not any(
                item == name or item.startswith(name + ".")
                for item in imported
            ), f"{path} imports {name}"


def test_forbidden_sentences_not_generated(case_0001_canonical: dict[str, Any]) -> None:
    _, context = _pipeline(case_0001_canonical)
    blob = " ".join(item.customer_language for item in context.items)
    for sentence in FORBIDDEN_SENTENCES:
        assert sentence not in blob
