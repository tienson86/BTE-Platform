"""IE-2 evidence selector tests."""

from __future__ import annotations

from engines.interpretation_engine.context.canonical_interpretation_context import (
    build_interpretation_context,
)
from engines.interpretation_engine.knowledge.composition_context import build_composition_context
from engines.interpretation_engine.knowledge.evidence_selector import EvidenceSelector
from engines.interpretation_engine.knowledge.knowledge_selector import (
    KnowledgeSelector,
    ReleasedKnowledgeSpec,
    default_released_catalog,
)
from tests.interpretation_engine.ie1_snapshots import ax2_snapshot, ax3_snapshot, ax4_snapshot


def test_evidence_bundles_resolve_without_synthesis() -> None:
    """Evidence ids, confidence, and references are copied from released specs."""
    analysis = ax2_snapshot()
    decision = ax3_snapshot()
    luck = ax4_snapshot()
    interpretation = build_interpretation_context(
        analysis_result=analysis,
        decision_result=decision,
        luck_result=luck,
    )
    context = build_composition_context(
        analysis_result=analysis,
        decision_result=decision,
        luck_result=luck,
        interpretation_context=interpretation,
    )
    knowledge = KnowledgeSelector().select(context)
    bundles = EvidenceSelector().select(context, knowledge)
    assert [item.evidence_id for item in bundles] == [
        "EV-IE2-AN-SEASONAL",
        "EV-IE2-AN-USEFUL_GOD",
        "EV-IE2-DC-FINAL_UG",
        "EV-IE2-LK-PRIORITY",
    ]
    seasonal = next(item for item in bundles if item.evidence_id == "EV-IE2-AN-SEASONAL")
    assert seasonal.boundary is False
    assert seasonal.confidence == "high"
    assert seasonal.references == ("analysis.seasonal.season",)


def test_boundary_case_when_confidence_path_missing() -> None:
    """Missing declared confidence path is a boundary case, not synthesis."""
    spec = ReleasedKnowledgeSpec(
        knowledge_id="KN-IE2-AN-SEASONAL",
        source="analysis",
        field_path="seasonal.season",
        evidence_id="EV-IE2-AN-SEASONAL",
        reasoning_id="RC-IE2-AN-SEASONAL",
        reasoning_chain_id="RC-IE2-AN-SEASONAL",
        reasoning_graph_id="RG-IE2-AN-SEASONAL",
        reasoning_trace_id="RT-IE2-AN-SEASONAL",
        template_id="TPL-IE2-OVERVIEW-SEASONAL",
        placeholders=("analysis.seasonal.season",),
        default_confidence="high",
        confidence_path="seasonal.missing_confidence",
    )
    analysis = ax2_snapshot()
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
    knowledge = KnowledgeSelector((spec,)).select(context)
    bundles = EvidenceSelector().select(context, knowledge)
    assert len(bundles) == 1
    assert bundles[0].boundary is True
    assert bundles[0].status == "boundary"
    assert bundles[0].confidence == "none"
    assert default_released_catalog()
