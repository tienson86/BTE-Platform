"""End-to-end Wave 1.1 commercial knowledge integration tests."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from engines.commercial_knowledge import CommercialKnowledgeAdapter
from engines.commercial_knowledge.narrative_merge import enrich_narrative_inputs

from .conftest import strong_chart_with_useful_god


def _baseline_interpretation() -> dict[str, Any]:
    return {
        "sections": [
            {
                "section_id": "exec-base",
                "title": "Tóm tắt điều hành",
                "content": "Kết luận giải thích gốc từ Interpretation.",
            }
        ],
        "summary": "Baseline interpretation summary.",
    }


def test_enrich_appends_without_replacing_interpretation() -> None:
    """Commercial merge enriches; does not wipe Interpretation conclusions."""
    analysis = strong_chart_with_useful_god()
    interpretation = _baseline_interpretation()
    before_sections = deepcopy(interpretation["sections"])
    before_strength = analysis["strength"]["reasoning"]
    before_rec = analysis["score"]["recommendation"]

    adapter = CommercialKnowledgeAdapter()
    bundle, payload = adapter.adapt(
        analysis=analysis,
        interpretation=interpretation,
        run_id="int-1",
    )
    enriched_analysis, enriched_interp = enrich_narrative_inputs(
        analysis=analysis,
        interpretation=interpretation,
        bundle=bundle,
        payload=payload,
    )

    assert enriched_interp["sections"][: len(before_sections)] == before_sections
    assert any(
        str(section.get("id", "")).startswith("ck-")
        for section in enriched_interp["sections"]
    )
    assert before_strength in enriched_analysis["strength"]["reasoning"]
    assert len(enriched_analysis["strength"]["reasoning"]) > len(before_strength)
    assert enriched_analysis["score"].get("analytical_recommendation") == before_rec
    assert enriched_analysis["useful_god"].get("commercial_recommendation")
    assert bundle.recommendations


def test_wave_1_1_enriches_executive_and_recommendation_paths() -> None:
    """Identity/strength/UG and RC cores are present for Narrative enrichment."""
    adapter = CommercialKnowledgeAdapter()
    bundle, payload = adapter.adapt(analysis=strong_chart_with_useful_god())
    assert any(item.evidence_kind == "identity" for item in bundle.identity)
    assert any(item.evidence_kind == "strength" for item in bundle.strengths)
    assert any(item.evidence_kind == "explanation" for item in bundle.useful_god)
    assert any(item.evidence_kind == "action" for item in bundle.recommendations)
    kinds = {unit.evidence_kind for unit in payload.evidence_units}
    assert "identity" in kinds
    assert "action" in kinds
    assert any("executive_summary" in unit.component_targets for unit in payload.evidence_units)
    assert any("recommendation" in unit.component_targets for unit in payload.evidence_units)


def test_no_duplicate_advice_in_bundle() -> None:
    """Bundle does not emit duplicate advice texts for same evidence kind."""
    adapter = CommercialKnowledgeAdapter()
    bundle, _payload = adapter.adapt(analysis=strong_chart_with_useful_god())
    texts = [item.text.strip() for item in bundle.recommendations]
    assert len(texts) == len(set(texts))
    kinds = [item.evidence_kind for item in bundle.selected_units]
    assert len(kinds) == len(set(kinds))


def test_build_narrative_result_attaches_bundle() -> None:
    """API truth helper attaches commercial_knowledge_bundle without crashing."""
    from applications.api.services.narrative_result_truth import build_narrative_result_dict

    result = build_narrative_result_dict(
        analysis=strong_chart_with_useful_god(),
        interpretation=_baseline_interpretation(),
        run_id="api-ck-1",
        include_commercial_knowledge=True,
    )
    assert result.get("contract") == "pack05_narrative_result_v1"
    bundle = result.get("commercial_knowledge_bundle")
    assert isinstance(bundle, dict)
    assert bundle.get("contract_id") == "bte.commercial_knowledge.retrieval.v1"
    assert bundle.get("selected_units")
