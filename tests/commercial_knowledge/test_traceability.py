"""Traceability provenance tests for CommercialKnowledgeBundle."""

from __future__ import annotations

from engines.commercial_knowledge import CommercialKnowledgeAdapter, bundle_to_dict

from .conftest import strong_chart_with_useful_god


def test_traceability_chain_and_selected_ids() -> None:
    """Bundle preserves KU → evidence → interpretation → narrative → portal chain."""
    adapter = CommercialKnowledgeAdapter()
    bundle, payload = adapter.adapt(
        analysis=strong_chart_with_useful_god(),
        run_id="trace-1",
    )
    assert bundle.traceability
    assert bundle.traceability["chain"] == [
        "knowledge_unit",
        "evidence",
        "interpretation_enrichment",
        "narrative",
        "portal",
    ]
    selected_ids = {item.knowledge_unit_id for item in bundle.selected_units}
    assert set(bundle.traceability["selected_knowledge_unit_ids"]) == selected_ids
    assert selected_ids
    for item in (
        *bundle.identity,
        *bundle.strengths,
        *bundle.useful_god,
        *bundle.recommendations,
    ):
        assert item.knowledge_unit_id in selected_ids
        assert item.signal_refs
        assert item.confidence > 0
    for unit in payload.evidence_units:
        assert unit.knowledge_unit_id in selected_ids
        assert unit.signal_refs
        assert unit.text


def test_serialized_bundle_keeps_provenance() -> None:
    """API dict keeps knowledge_unit_id + signal_refs on every commercial item."""
    adapter = CommercialKnowledgeAdapter()
    bundle, _payload = adapter.adapt(analysis=strong_chart_with_useful_god())
    data = bundle_to_dict(bundle)
    for bucket in ("identity", "strengths", "useful_god", "recommendations"):
        for item in data[bucket]:
            assert item["knowledge_unit_id"].startswith("KU-")
            assert item["signal_refs"]
            assert item["version"]
    assert data["traceability"]["chain"][-1] == "portal"
