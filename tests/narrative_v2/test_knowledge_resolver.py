"""Knowledge Resolver tests (N-IMP-04)."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

import pytest

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.knowledge import (
    KnowledgeError,
    KnowledgeIndex,
    KnowledgeResolver,
    NarrativeKnowledgeContext,
)
from engines.narrative_v2.knowledge.knowledge_index import IndexedKnowledge
from engines.narrative_v2.knowledge.knowledge_status import STATUS_APPROVED, STATUS_DRAFT
from engines.narrative_v2.reasoning import ReasoningBuilder

KNOWLEDGE_DIR = Path(__file__).resolve().parents[2] / "engines" / "narrative_v2" / "knowledge"

REWRITE_MARKERS: tuple[str, ...] = (
    "Bạn có nội lực tốt",
    "Bạn làm việc có hệ thống",
    "Tình duyên thuận lợi",
    "Giai đoạn thuận lợi để mở rộng",
    "Nên dùng màu đỏ",
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


def _blob(context: NarrativeKnowledgeContext) -> str:
    parts: list[str] = [context.status]
    for item in context.items:
        parts.extend(
            [
                item.knowledge_id,
                item.semantic_key,
                item.technical_meaning or "",
                item.customer_meaning_candidate or "",
            ]
        )
        parts.extend(item.recommendations)
        parts.extend(item.boundaries)
    for gap in context.unresolved:
        parts.extend([gap.semantic_key, gap.reason])
    return " ".join(parts)


def _pair(case_0001_canonical: dict[str, Any]) -> tuple[object, object]:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    return reasoning, evidence


def test_k1_k2_resolver_accepts_reasoning_and_returns_context(
    case_0001_canonical: dict[str, Any],
) -> None:
    reasoning, evidence = _pair(case_0001_canonical)
    context = KnowledgeResolver().resolve(reasoning, evidence)
    assert isinstance(context, NarrativeKnowledgeContext)


def test_k1_rejects_canonical_analysis(case_0001_canonical: dict[str, Any]) -> None:
    with pytest.raises(KnowledgeError, match="NarrativeReasoningContext only"):
        KnowledgeResolver().resolve(case_0001_canonical)


def test_k3_only_approved_sources_resolve(case_0001_canonical: dict[str, Any]) -> None:
    reasoning, evidence = _pair(case_0001_canonical)
    context = KnowledgeResolver().resolve(reasoning, evidence)
    for item in context.items:
        assert item.status == STATUS_APPROVED


def test_k6_k17_exact_match_deterministic(case_0001_canonical: dict[str, Any]) -> None:
    reasoning, evidence = _pair(case_0001_canonical)
    first = KnowledgeResolver().resolve(reasoning, evidence)
    second = KnowledgeResolver().resolve(reasoning, evidence)
    assert first.items == second.items
    assert first.matches == second.matches
    assert first.unresolved == second.unresolved


def test_k8_missing_knowledge_is_unresolved(case_0001_canonical: dict[str, Any]) -> None:
    reasoning, evidence = _pair(case_0001_canonical)
    context = KnowledgeResolver().resolve(reasoning, evidence)
    keys = {entry.semantic_key for entry in context.unresolved}
    assert "core.temperature_balancing_context" in keys
    assert "core.luck_temporal_context" in keys


def test_k9_no_fuzzy_guessing() -> None:
    source = (KNOWLEDGE_DIR / "knowledge_resolver.py").read_text(encoding="utf-8")
    forbidden = ("difflib", "embed", "openai", "fuzzy", "nearest", "levenshtein")
    for token in forbidden:
        assert token not in source.lower()


def test_k10_knowledge_traces_to_reasoning_and_evidence(
    case_0001_canonical: dict[str, Any],
) -> None:
    reasoning, evidence = _pair(case_0001_canonical)
    context = KnowledgeResolver().resolve(reasoning, evidence)
    reasoning_ids = {node.reasoning_id for node in reasoning.nodes}
    evidence_ids = {item.evidence_id for item in evidence.items}
    for item in context.items:
        assert item.references
        ref = item.references[0]
        assert ref.reasoning_ids
        assert ref.evidence_ids
        assert set(ref.reasoning_ids) <= reasoning_ids
        assert set(ref.evidence_ids) <= evidence_ids


def test_k11_no_customer_rewrite(case_0001_canonical: dict[str, Any]) -> None:
    reasoning, evidence = _pair(case_0001_canonical)
    blob = _blob(KnowledgeResolver().resolve(reasoning, evidence))
    for marker in REWRITE_MARKERS:
        assert marker not in blob


def test_k12_no_action_plan(case_0001_canonical: dict[str, Any]) -> None:
    reasoning, evidence = _pair(case_0001_canonical)
    context = KnowledgeResolver().resolve(reasoning, evidence)
    assert not hasattr(context, "action_plan")
    assert not hasattr(context, "final_action_plan")


def test_k13_k14_no_pack05_or_portal_imports() -> None:
    forbidden = (
        "engines.narrative_engine",
        "applications.customer_portal",
        "applications.api.services.narrative_result_truth",
    )
    for path in KNOWLEDGE_DIR.glob("*.py"):
        imported = _imported_modules(path)
        for name in forbidden:
            assert not any(
                item == name or item.startswith(name + ".")
                for item in imported
            ), f"{path} imports {name}"


def test_k18_versions_preserved(case_0001_canonical: dict[str, Any]) -> None:
    reasoning, evidence = _pair(case_0001_canonical)
    context = KnowledgeResolver().resolve(reasoning, evidence)
    assert context.items
    for item in context.items:
        assert item.version == "1.0.0"
    meta = dict(context.metadata)
    assert meta["resolver_version"]
    assert "knowledge_version" in meta


def test_draft_record_does_not_resolve() -> None:
    draft = IndexedKnowledge(
        knowledge_id="knowledge.strength.strong",
        domain="strength",
        key="strong",
        knowledge_type="meaning",
        status=STATUS_DRAFT,
        technical_meaning="draft only",
        customer_meaning_candidate=None,
        boundaries=(),
        recommendations=(),
        source_path="draft.json",
        version="1.0.0",
        aliases=(),
    )
    approved = IndexedKnowledge(
        knowledge_id="knowledge.pattern.chinh_an",
        domain="pattern",
        key="chinh_an",
        knowledge_type="meaning",
        status=STATUS_APPROVED,
        technical_meaning="approved pattern",
        customer_meaning_candidate=None,
        boundaries=(),
        recommendations=(),
        source_path="pattern.json",
        version="1.0.0",
        aliases=(),
    )
    index = KnowledgeIndex((draft, approved))
    assert index.get("strength", "strong") is None
    assert index.get("pattern", "chinh_an") is not None


def test_semantic_negatives(case_0001_canonical: dict[str, Any]) -> None:
    reasoning, evidence = _pair(case_0001_canonical)
    context = KnowledgeResolver().resolve(reasoning, evidence)
    blob = _blob(context)
    assert "Bạn có nội lực tốt." not in blob
    assert "Bạn làm việc có hệ thống." not in blob
    assert "Tình duyên thuận lợi." not in blob
    assert "Giai đoạn thuận lợi để mở rộng." not in blob
    assert "Nên dùng màu đỏ." not in blob
    for item in context.items:
        assert item.customer_meaning_candidate is None
