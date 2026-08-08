"""CommercialKnowledgeBundle construction tests."""

from __future__ import annotations

from engines.commercial_knowledge import CommercialKnowledgeAdapter, bundle_to_dict

from .conftest import strong_chart_with_useful_god, weak_chart_with_useful_god


def test_bundle_generated_for_strong_chart() -> None:
    """Strong chart yields identity/strength/useful_god/recommendations."""
    adapter = CommercialKnowledgeAdapter()
    bundle, payload = adapter.adapt(analysis=strong_chart_with_useful_god(), run_id="t1")
    assert bundle.bundle_status in {"complete", "partial"}
    assert bundle.identity
    assert bundle.strengths
    assert bundle.useful_god
    assert bundle.recommendations
    assert not bundle.weaknesses
    assert payload.evidence_units
    assert payload.bundle_id == bundle.bundle_id


def test_bundle_weak_chart_selects_weakness() -> None:
    """Weak chart selects weakness path instead of strength."""
    adapter = CommercialKnowledgeAdapter()
    bundle, _payload = adapter.adapt(analysis=weak_chart_with_useful_god(), run_id="t2")
    assert bundle.identity
    assert bundle.weaknesses
    assert not bundle.strengths
    assert bundle.recommendations


def test_bundle_dict_hides_raw_knowledge_units() -> None:
    """Serialized bundle must not expose raw KU CSV fields."""
    adapter = CommercialKnowledgeAdapter()
    bundle, _payload = adapter.adapt(analysis=strong_chart_with_useful_god())
    data = bundle_to_dict(bundle)
    assert "modern_interpretation" not in data
    assert "condition" not in data
    assert "identity" in data
    assert "recommendations" in data
    assert data["contract_id"] == "bte.commercial_knowledge.retrieval.v1"
    for item in data["identity"]:
        assert "text" in item
        assert "knowledge_unit_id" in item
        assert "author_notes" not in item
