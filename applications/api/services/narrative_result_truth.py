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

    Commercial V1 polish attaches structured Exec / primary Career Rec /
    secondary Promotion milestone without new routes or layout.
    """
    analysis_in = analysis or {}
    interpretation_in = interpretation or {}
    commercial_bundle_payload: dict[str, Any] | None = None
    career_selection_payload: dict[str, Any] | None = None
    promotion_readiness_payload: dict[str, Any] | None = None
    executive_payload: dict[str, Any] | None = None
    primary_rec_payload: dict[str, Any] | None = None
    secondary_milestone_payload: dict[str, Any] | None = None

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
        executive_payload = interpretation_in.get("commercial_executive_summary")
        primary_rec_payload = interpretation_in.get("primary_recommendation")
        secondary_milestone_payload = interpretation_in.get(
            "secondary_career_milestone"
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
        payload["career_selection_label"] = "Career Selection Assessment"
    if promotion_readiness_payload is not None:
        payload["promotion_readiness_assessment"] = promotion_readiness_payload
        payload["promotion_readiness_label"] = "Promotion Readiness Assessment"
    if isinstance(executive_payload, dict):
        payload["commercial_executive_summary"] = executive_payload
        # Prefer structured Exec identity for Portal without Engine redesign.
        summary = payload.get("summary")
        if isinstance(summary, dict) and executive_payload.get("composed_text"):
            summary = dict(summary)
            summary["identity"] = executive_payload["composed_text"]
            if executive_payload.get("supporting_points"):
                summary["strengths"] = list(executive_payload["supporting_points"])
            payload["summary"] = summary
    if isinstance(primary_rec_payload, dict):
        payload["primary_recommendation"] = primary_rec_payload
        summary = payload.get("summary")
        if isinstance(summary, dict) and primary_rec_payload.get("composed_text"):
            summary = dict(summary)
            summary["priority_recommendation"] = primary_rec_payload["composed_text"]
            summary["next_action"] = primary_rec_payload["composed_text"]
            payload["summary"] = summary
    if isinstance(secondary_milestone_payload, dict):
        payload["secondary_career_milestone"] = secondary_milestone_payload
    return payload


def narrative_result_source_fingerprint() -> dict[str, str]:
    """Provenance block for API meta."""
    return {
        "engine": "engines.narrative_engine.engine.NarrativeEngine",
        "method": "compose_narrative_result",
        "contract": "pack05_narrative_result_v1",
        "commercial_knowledge": "engines.commercial_knowledge.CommercialKnowledgeAdapter",
        "capabilities": "CAP-D1-CA-SEL;CAP-D1-CA-PRO",
        "polish": "commercial_v1_p0",
        "view": (
            "applications.api.services.narrative_result_truth.build_narrative_result_dict"
        ),
    }
