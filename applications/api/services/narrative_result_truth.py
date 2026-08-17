"""
Canonical NarrativeResult truth — Narrative Composer V2 with Pack 05 fallback.

Consumer contract stays pack05_narrative_result_v1 so Portal, report, and PDF
do not need a redesign. Pack 05 NarrativeEngine is legacy compatibility only.
"""

from __future__ import annotations

import logging
from typing import Any

from engines.commercial_knowledge import (
    PRODUCTION_ALLOW_LIST,
    CommercialKnowledgeAdapter,
    bundle_to_dict,
    enrich_narrative_inputs,
)
from engines.interpretation_engine.foundation.narrative.constants import (
    NARRATIVE_RESULT_V2_GENERATOR,
    PACK05_CONTRACT,
)
from engines.interpretation_engine.foundation.narrative.composer import (
    compose_narrative_v2_from_production,
)
from engines.interpretation_engine.foundation.narrative.publish import (
    EDITION_EXECUTIVE,
    apply_published_narrative,
    apply_report_edition,
)
from engines.interpretation_engine.foundation.narrative.publish.current_dayun import (
    stamp_dayun_frame,
    stamp_interaction_truth,
    stamp_luck_analysis,
)
from engines.interpretation_engine.foundation.narrative.result_v2 import (
    narrative_result_v2_to_dict,
)
from engines.narrative_engine import NarrativeEngine

logger = logging.getLogger(__name__)


def build_narrative_result_dict(
    *,
    analysis: dict[str, Any] | None,
    interpretation: dict[str, Any] | None,
    run_id: str = "",
    scenario_id: str = "default",
    include_commercial_knowledge: bool = True,
    engine_output: Any | None = None,
    publication_edition: str = EDITION_EXECUTIVE,
) -> dict[str, Any]:
    """Compose the production NarrativeResult.

    Prefers Narrative Composer V2 when Decision/State/Relationship/Knowledge
    bundles can be built. Pack 05 remains the compatibility fallback.
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

    payload = _compose_v2_or_legacy(
        engine_output=engine_output,
        analysis_in=analysis_in,
        interpretation_in=interpretation_in,
        run_id=run_id,
    )
    payload["contract"] = PACK05_CONTRACT
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
    published = apply_published_narrative(payload)
    published = stamp_dayun_frame(published, engine_output)
    published = stamp_luck_analysis(published, engine_output)
    published = stamp_interaction_truth(published, engine_output)
    return apply_report_edition(published, publication_edition)


def narrative_result_source_fingerprint() -> dict[str, str]:
    """Provenance block for API meta."""
    return {
        "engine": (
            "engines.interpretation_engine.foundation.narrative.NarrativeComposerV2"
        ),
        "method": "compose",
        "contract": PACK05_CONTRACT,
        "generator": NARRATIVE_RESULT_V2_GENERATOR,
        "fallback": "engines.narrative_engine.engine.NarrativeEngine",
        "commercial_knowledge": "engines.commercial_knowledge.CommercialKnowledgeAdapter",
        "capabilities": "CAP-D1-CA-SEL;CAP-D1-CA-PRO",
        "polish": "commercial_v1_p0",
        "view": (
            "applications.api.services.narrative_result_truth.build_narrative_result_dict"
        ),
    }


def _compose_v2_or_legacy(
    *,
    engine_output: Any | None,
    analysis_in: dict[str, Any],
    interpretation_in: dict[str, Any],
    run_id: str,
) -> dict[str, Any]:
    """Prefer V2 composition. Fall back to Pack 05 only when bundles are unavailable."""
    if engine_output is not None and getattr(
        engine_output, "interpretation_foundation", None
    ) is not None:
        try:
            composed = compose_narrative_v2_from_production(engine_output)
            payload = narrative_result_v2_to_dict(composed, run_id=run_id)
            if _has_canonical_sections(payload):
                return payload
            logger.warning("Narrative Composer V2 missing canonical sections; using Pack 05 fallback")
        except Exception:
            logger.exception("Narrative Composer V2 failed; using Pack 05 fallback")
    engine = NarrativeEngine()
    result = engine.compose_narrative_result(
        analysis=analysis_in,
        interpretation=interpretation_in,
        run_id=run_id,
    )
    payload = result.to_dict()
    payload["generator"] = "pack05_narrative_engine"
    return payload


def _has_canonical_sections(payload: dict[str, Any]) -> bool:
    """True when the seven live report sections all have body text."""
    sections = payload.get("sections") or []
    if len(sections) != 7:
        return False
    return all(
        isinstance(item, dict) and (item.get("paragraphs") or item.get("recommendations"))
        for item in sections
    )
