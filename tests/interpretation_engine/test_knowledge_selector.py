"""IE-2 knowledge selector tests."""

from __future__ import annotations

from engines.interpretation_engine.context.canonical_interpretation_context import (
    build_interpretation_context,
)
from engines.interpretation_engine.knowledge.composition_context import build_composition_context
from engines.interpretation_engine.knowledge.knowledge_selector import (
    KnowledgeSelector,
    ReleasedKnowledgeSpec,
    STATUS_DRAFT,
    default_released_catalog,
)
from tests.interpretation_engine.ie1_snapshots import ax2_snapshot, ax3_snapshot, ax4_snapshot


def _context():
    analysis = ax2_snapshot()
    decision = ax3_snapshot()
    luck = ax4_snapshot()
    interpretation = build_interpretation_context(
        analysis_result=analysis,
        decision_result=decision,
        luck_result=luck,
    )
    return build_composition_context(
        analysis_result=analysis,
        decision_result=decision,
        luck_result=luck,
        interpretation_context=interpretation,
    )


def test_selects_released_knowledge_when_fields_present() -> None:
    """Released catalog items whose published fields exist are selected."""
    selected = KnowledgeSelector().select(_context())
    ids = [item.knowledge_id for item in selected]
    assert ids == [
        "KN-IE2-AN-SEASONAL",
        "KN-IE2-AN-USEFUL_GOD",
        "KN-IE2-DC-FINAL_UG",
        "KN-IE2-LK-PRIORITY",
    ]
    assert all(item.spec.status == "released" for item in selected)


def test_skips_draft_and_missing_fields() -> None:
    """Draft entries and missing published fields are not selected."""
    draft = ReleasedKnowledgeSpec(
        knowledge_id="KN-IE2-DRAFT",
        source="analysis",
        field_path="seasonal.season",
        evidence_id="EV-DRAFT",
        reasoning_id="RC-DRAFT",
        reasoning_chain_id="RC-DRAFT",
        reasoning_graph_id="RG-DRAFT",
        reasoning_trace_id="RT-DRAFT",
        template_id="TPL-DRAFT",
        placeholders=("analysis.seasonal.season",),
        default_confidence="low",
        status=STATUS_DRAFT,
    )
    missing = ReleasedKnowledgeSpec(
        knowledge_id="KN-IE2-AN-TEMPERATURE",
        source="analysis",
        field_path="temperature.temperature_level",
        evidence_id="EV-TEMP",
        reasoning_id="RC-TEMP",
        reasoning_chain_id="RC-TEMP",
        reasoning_graph_id="RG-TEMP",
        reasoning_trace_id="RT-TEMP",
        template_id="TPL-TEMP",
        placeholders=("analysis.temperature.temperature_level",),
        default_confidence="low",
    )
    catalog = default_released_catalog() + (draft, missing)
    analysis = ax2_snapshot()
    del analysis["seasonal"]
    interpretation = build_interpretation_context(
        analysis_result=analysis,
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
    )
    context = build_composition_context(
        analysis_result=analysis,
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
        interpretation_context=interpretation,
    )
    ids = [item.knowledge_id for item in KnowledgeSelector(catalog).select(context)]
    assert "KN-IE2-DRAFT" not in ids
    assert "KN-IE2-AN-SEASONAL" not in ids
    assert "KN-IE2-AN-TEMPERATURE" not in ids
    assert "KN-IE2-DC-FINAL_UG" in ids
