"""Tests for knowledge catalog loader."""

from __future__ import annotations

from engines.interpretation_engine_v2.strength.knowledge_loader.loader import KnowledgeCatalogLoader


def test_load_pack_01_catalog() -> None:
    loader = KnowledgeCatalogLoader()
    units = loader.load_all()
    assert len(units) == 339
    ids = {unit.knowledge_id for unit in units}
    assert "IK-STR-MEAN-0006" in ids
    assert "IK-STR-CAUS-0002" in ids


def test_parse_single_unit_fields() -> None:
    loader = KnowledgeCatalogLoader()
    units = loader.load_all()
    mean = next(unit for unit in units if unit.knowledge_id == "IK-STR-MEAN-0006")
    assert mean.purpose == "MEANING"
    assert mean.strength_class == "strong"
    assert "classification" in mean.required_facts
    assert mean.claim
