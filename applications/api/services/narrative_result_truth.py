"""
Pack 05 NarrativeResult truth — API serialization + commercial enrichment.

Does not modify Interpretation Engine logic or Narrative architecture.
Commercial Knowledge Adapter enriches inputs before compose
(Wave 1.1 + Career Selection + Promotion Readiness).
"""

from __future__ import annotations

from typing import Any

from engines.commercial_knowledge import (
    PRODUCTION_ALLOW_LIST,
    CommercialKnowledgeAdapter,
    bundle_to_dict,
    enrich_narrative_inputs,
)
from engines.narrative_engine import NarrativeEngine


def build_narrative_result_dict(
    *,
    analysis: dict[str, Any] | None,
    interpretation: dict[str, Any] | None,
    run_id: str = "",
    scenario_id: str = "default",
    include_commercial_knowledge: bool = True,
) -> dict[str, Any]:
    """
    Compose Pack 05 NarrativeResult and return portal JSON.

    When commercial knowledge is enabled, production allow-listed units enrich
    Executive Summary / Recommendation / Career Selection / Promotion Readiness
    without replacing Interpretation analytical meaning.
    """
    analysis_in = analysis or {}
    interpretation_in = interpretation or {}
    commercial_bundle_payload: dict[str, Any] | None = None
    career_selection_payload: dict[str, Any] | None = None
    promotion_readiness_payload: dict[str, Any] | None = None

    if include_commercial_knowledge:
        adapter = CommercialKnowledgeAdapter(
            default_allow_list=PRODUCTION_ALLOW_LIST,
        )
        bundle, payload = adapter.adapt(
            analysis=analysis_in,
            interpretation=interpretation_in,
            scenario_id=scenario_id,
            run_id=run_id,
            allow_list_ids=PRODUCTION_ALLOW_LIST,
        )
        analysis_in, interpretation_in = enrich_narrative_inputs(
            analysis=analysis_in,
            interpretation=interpretation_in,
            bundle=bundle,
            payload=payload,
        )
        commercial_bundle_payload = bundle_to_dict(bundle)
        career_selection_payload = commercial_bundle_payload.get(
            "career_selection_assessment"
        )
        promotion_readiness_payload = commercial_bundle_payload.get(
            "promotion_readiness_assessment"
        )

    engine = NarrativeEngine()
    result = engine.compose_narrative_result(
        analysis=analysis_in,
        interpretation=interpretation_in,
        run_id=run_id,
    )
    payload = result.to_dict()
    payload["contract"] = "pack05_narrative_result_v1"
    if commercial_bundle_payload is not None:
        payload["commercial_knowledge_bundle"] = commercial_bundle_payload
    if career_selection_payload is not None:
        payload["career_selection_assessment"] = career_selection_payload
    if promotion_readiness_payload is not None:
        payload["promotion_readiness_assessment"] = promotion_readiness_payload
    return payload


def narrative_result_source_fingerprint() -> dict[str, str]:
    """Provenance block for API meta."""
    return {
        "engine": "engines.narrative_engine.engine.NarrativeEngine",
        "method": "compose_narrative_result",
        "contract": "pack05_narrative_result_v1",
        "commercial_knowledge": "engines.commercial_knowledge.CommercialKnowledgeAdapter",
        "capabilities": "CAP-D1-CA-SEL;CAP-D1-CA-PRO",
        "view": (
            "applications.api.services.narrative_result_truth.build_narrative_result_dict"
        ),
    }
