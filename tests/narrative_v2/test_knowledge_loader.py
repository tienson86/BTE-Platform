"""Knowledge loader tests (N-IMP-04)."""

from __future__ import annotations

from engines.narrative_v2.knowledge import KnowledgeLoader
from engines.narrative_v2.knowledge.knowledge_status import STATUS_APPROVED


def test_loader_indexes_only_approved_records() -> None:
    index = KnowledgeLoader().load_index()
    assert index.records()
    for record in index.records():
        assert record.status == STATUS_APPROVED
        assert record.knowledge_id
        assert record.key
        assert record.source_path
        assert record.technical_meaning is None or isinstance(record.technical_meaning, str)


def test_loader_cache_is_deterministic() -> None:
    loader = KnowledgeLoader()
    first = loader.load_index()
    second = loader.load_index()
    assert first.records() == second.records()
    assert first.versions() == second.versions()
