"""Traceability: Knowledge Unit → Bundle → Narrative → Portal."""

from __future__ import annotations

from applications.api.services.narrative_result_truth import build_narrative_result_dict
from engines.commercial_knowledge import (
    CAREER_SELECTION_ALLOW_LIST,
    PRODUCTION_ALLOW_LIST,
    CommercialKnowledgeAdapter,
    enrich_narrative_inputs,
)

from .conftest import baseline_interpretation, strong_employee_chart


def test_trace_chain_knowledge_to_portal() -> None:
    """Every Career Selection statement retains KU id through Portal JSON."""
    adapter = CommercialKnowledgeAdapter()
    bundle, payload = adapter.adapt(
        analysis=strong_employee_chart(),
        allow_list_ids=PRODUCTION_ALLOW_LIST,
        run_id="trace-1",
    )
    assert bundle.career_selection is not None
    assert bundle.traceability["capability_chain"] == [
        "knowledge_unit",
        "commercial_bundle",
        "narrative",
        "portal",
    ]
    assert bundle.traceability["chain"] == [
        "knowledge_unit",
        "evidence",
        "interpretation_enrichment",
        "narrative",
        "portal",
    ]
    assert bundle.traceability["capability_id"] == "CAP-D1-CA-SEL"
    assert set(bundle.traceability["career_selection_unit_ids"]).issubset(
        CAREER_SELECTION_ALLOW_LIST
    )

    _analysis, interpretation = enrich_narrative_inputs(
        analysis=strong_employee_chart(),
        interpretation=baseline_interpretation(),
        bundle=bundle,
        payload=payload,
    )
    assessment = interpretation["career_selection_assessment"]
    for unit_id in bundle.career_selection.knowledge_unit_ids:
        assert any(
            (assessment[field] or {}).get("knowledge_unit_id") == unit_id
            for field in assessment
            if isinstance(assessment.get(field), dict)
        )

    portal = build_narrative_result_dict(
        analysis=strong_employee_chart(),
        interpretation=baseline_interpretation(),
        run_id="trace-2",
    )
    portal_assessment = portal["career_selection_assessment"]
    portal_ids = set(portal_assessment["knowledge_unit_ids"])
    assert portal_ids == set(bundle.career_selection.knowledge_unit_ids)
    assert portal_ids.issubset(CAREER_SELECTION_ALLOW_LIST)


def test_no_raw_knowledge_unit_leak_in_portal_payload() -> None:
    """Portal payload never exposes full CSV Knowledge Unit rows."""
    portal = build_narrative_result_dict(
        analysis=strong_employee_chart(),
        interpretation=baseline_interpretation(),
        run_id="trace-3",
    )
    blob = str(portal)
    assert "classical_text" not in blob
    assert "author_notes" not in blob
    assert "ethics_flags" not in blob
    assessment = portal["career_selection_assessment"]
    direction = assessment["career_direction"]
    assert set(direction.keys()) >= {
        "text",
        "knowledge_unit_id",
        "evidence_kind",
        "version",
        "confidence",
    }
