"""Tests for knowledge selector."""

from __future__ import annotations

from engines.interpretation_engine_v2.strength.contracts.models import AudienceMode
from engines.interpretation_engine_v2.strength.knowledge_loader.loader import KnowledgeCatalogLoader
from engines.interpretation_engine_v2.strength.runtime.case_0001 import load_case_0001_facts
from engines.interpretation_engine_v2.strength.selector.selector import KnowledgeSelector


def test_selector_matches_strong_class() -> None:
    loader = KnowledgeCatalogLoader()
    units = loader.load_all()
    published = load_case_0001_facts()
    selector = KnowledgeSelector()
    candidates = selector.select_candidates(units, published, AudienceMode.CUSTOMER)
    ids = {unit.knowledge_id for unit in candidates}
    assert "IK-STR-MEAN-0006" in ids
    assert "IK-STR-MEAN-0010" not in ids
    assert all(unit.topic != "examples" for unit in candidates)
