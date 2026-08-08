"""CommercialKnowledgeAdapter behavior tests."""

from __future__ import annotations

from engines.commercial_knowledge import CommercialKnowledgeAdapter

from .conftest import chart_without_useful_god, strong_chart_with_useful_god


def test_adapter_returns_bundle_and_payload() -> None:
    """Adapter returns both bundle and narrative payload."""
    adapter = CommercialKnowledgeAdapter()
    bundle, payload = adapter.adapt(
        analysis=strong_chart_with_useful_god(),
        scenario_id="default",
        run_id="adapter-1",
    )
    assert bundle.bundle_id.startswith("ckb-")
    assert payload.bundle_id == bundle.bundle_id
    kinds = {unit.evidence_kind for unit in payload.evidence_units}
    assert "identity" in kinds
    assert "action" in kinds


def test_adapter_drops_ug_and_rc_without_useful_god() -> None:
    """Without useful god, UG/RC units are not selected."""
    adapter = CommercialKnowledgeAdapter()
    bundle, _payload = adapter.adapt(analysis=chart_without_useful_god())
    selected = {item.knowledge_unit_id for item in bundle.selected_units}
    assert "KU-UG-001" not in selected
    assert "KU-RC-001" not in selected
    assert "KU-ID-001" in selected
    assert not bundle.recommendations


def test_adapter_no_duplicate_evidence_kinds() -> None:
    """At most one selected unit per evidence kind."""
    adapter = CommercialKnowledgeAdapter()
    bundle, _payload = adapter.adapt(analysis=strong_chart_with_useful_god())
    kinds = [item.evidence_kind for item in bundle.selected_units]
    assert len(kinds) == len(set(kinds))


def test_adapter_rejects_technical_bound_text() -> None:
    """Technical marker detection exists on retrieval path (sanity)."""
    from engines.commercial_knowledge.retrieval_service import _looks_technical

    assert _looks_technical("kích hoạt khi thân suy")
    assert not _looks_technical("Ưu tiên các việc nuôi Dụng thần Thủy.")
