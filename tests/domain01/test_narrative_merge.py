"""Narrative merge enrichment for Career Selection Assessment."""

from __future__ import annotations

from copy import deepcopy

from engines.commercial_knowledge import (
    CAREER_SELECTION_ALLOW_LIST,
    PRODUCTION_ALLOW_LIST,
    WAVE_1_1_ALLOW_LIST,
    CommercialKnowledgeAdapter,
    enrich_narrative_inputs,
)

from .conftest import baseline_interpretation, strong_employee_chart

_SEL_ALLOW = WAVE_1_1_ALLOW_LIST | CAREER_SELECTION_ALLOW_LIST


def test_narrative_merge_enriches_without_replacing_interpretation() -> None:
    """Merge appends commercial sections; baseline Interpretation survives."""
    analysis = strong_employee_chart()
    interpretation = baseline_interpretation()
    before_sections = deepcopy(interpretation["sections"])
    before_summary = interpretation["summary"]

    adapter = CommercialKnowledgeAdapter()
    bundle, payload = adapter.adapt(
        analysis=analysis,
        allow_list_ids=_SEL_ALLOW,
        run_id="merge-1",
    )
    enriched_analysis, enriched_interp = enrich_narrative_inputs(
        analysis=analysis,
        interpretation=interpretation,
        bundle=bundle,
        payload=payload,
    )

    assert enriched_interp["sections"][: len(before_sections)] == before_sections
    assert enriched_interp["summary"] == before_summary
    assert enriched_interp.get("career_selection_capability_id") == "CAP-D1-CA-SEL"
    assert enriched_interp["career_selection_assessment"]["career_direction"]["text"]
    assert "Họ nghề hợp bạn" in enriched_analysis["strength"]["reasoning"]
    assert "Kế hoạch 90 ngày" in enriched_analysis["score"]["recommendation"]
    assert enriched_analysis["score"].get("analytical_recommendation") == "Thủy"


def test_narrative_prefers_career_action_over_generic_rec() -> None:
    """Career 90-day plan specializes Recommendation path (SEL allow-list)."""
    adapter = CommercialKnowledgeAdapter()
    bundle, payload = adapter.adapt(
        analysis=strong_employee_chart(),
        allow_list_ids=_SEL_ALLOW,
    )
    enriched_analysis, _interp = enrich_narrative_inputs(
        analysis=strong_employee_chart(),
        interpretation=baseline_interpretation(),
        bundle=bundle,
        payload=payload,
    )
    assert bundle.career_selection is not None
    assert (
        enriched_analysis["score"]["commercial_knowledge_unit_id"]
        == "KU-AC-CA-000001"
    )
    assert "Tháng 1" in enriched_analysis["score"]["recommendation"]


def test_production_narrative_prefers_promotion_action_when_both_present() -> None:
    """Full production allow-list prefers Promotion 90-day plan for Rec."""
    adapter = CommercialKnowledgeAdapter()
    bundle, payload = adapter.adapt(
        analysis=strong_employee_chart(),
        allow_list_ids=PRODUCTION_ALLOW_LIST,
    )
    enriched_analysis, enriched_interp = enrich_narrative_inputs(
        analysis=strong_employee_chart(),
        interpretation=baseline_interpretation(),
        bundle=bundle,
        payload=payload,
    )
    assert enriched_interp.get("promotion_readiness_capability_id") == "CAP-D1-CA-PRO"
    assert (
        enriched_analysis["score"]["commercial_knowledge_unit_id"]
        == "KU-AC-CA-000020"
    )
    assert "thăng tiến" in enriched_analysis["score"]["recommendation"]
