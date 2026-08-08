"""
Pack 05 NarrativeResult truth — API serialization + Wave 1.1 commercial enrichment.

Does not modify Interpretation Engine logic or Narrative architecture.
Commercial Knowledge Adapter enriches inputs before compose.
"""

from __future__ import annotations

from typing import Any

from engines.commercial_knowledge import (
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

    When commercial knowledge is enabled, Wave 1.1 allow-listed units enrich
    Executive Summary / Recommendation inputs without replacing Interpretation.
    """
    analysis_in = analysis or {}
    interpretation_in = interpretation or {}
    commercial_bundle_payload: dict[str, Any] | None = None

    if include_commercial_knowledge:
        adapter = CommercialKnowledgeAdapter()
        bundle, payload = adapter.adapt(
            analysis=analysis_in,
            interpretation=interpretation_in,
            scenario_id=scenario_id,
            run_id=run_id,
        )
        analysis_in, interpretation_in = enrich_narrative_inputs(
            analysis=analysis_in,
            interpretation=interpretation_in,
            bundle=bundle,
            payload=payload,
        )
        commercial_bundle_payload = bundle_to_dict(bundle)

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
    return payload


def narrative_result_source_fingerprint() -> dict[str, str]:
    """Provenance block for API meta."""
    return {
        "engine": "engines.narrative_engine.engine.NarrativeEngine",
        "method": "compose_narrative_result",
        "contract": "pack05_narrative_result_v1",
        "commercial_knowledge": "engines.commercial_knowledge.CommercialKnowledgeAdapter",
        "view": (
            "applications.api.services.narrative_result_truth.build_narrative_result_dict"
        ),
    }
