"""Knowledge index tests (N-IMP-04)."""

from __future__ import annotations

from engines.narrative_v2.knowledge import KnowledgeIndex, KnowledgeLoader


def test_k6_exact_domain_key_match() -> None:
    index = KnowledgeLoader().load_index()
    record = index.get("pattern", "chinh_an")
    assert record is not None
    assert record.knowledge_id == "knowledge.pattern.chinh_an"
    assert index.get("pattern", "not_a_real_pattern") is None


def test_k7_approved_alias_is_deterministic() -> None:
    index = KnowledgeLoader().load_index()
    by_key = index.get("pattern", "chinh_an")
    by_id = index.get("pattern", "knowledge.pattern.chinh_an")
    assert by_key is not None
    assert by_id is not None
    assert by_key.knowledge_id == by_id.knowledge_id
    useful = index.get("useful_god", "Chính Quan")
    aliased = index.get("useful_god", "chinh_quan")
    assert useful is not None
    assert aliased is not None
    assert useful.knowledge_id == aliased.knowledge_id == "knowledge.useful_god.chinh_quan"


def test_index_does_not_cross_domains() -> None:
    index = KnowledgeLoader().load_index()
    pattern = index.get("pattern", "chinh_an")
    ten_gods = index.get("ten_gods", "Chính Ấn")
    assert pattern is not None
    assert ten_gods is not None
    assert pattern.knowledge_id != ten_gods.knowledge_id


def test_empty_index_is_valid() -> None:
    index = KnowledgeIndex(())
    assert index.records() == ()
    assert index.get("pattern", "chinh_an") is None
