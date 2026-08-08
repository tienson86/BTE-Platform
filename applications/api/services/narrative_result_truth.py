"""
Pack 05 NarrativeResult truth — API serialization only.

Does not modify engines.narrative_engine.
"""

from __future__ import annotations

from typing import Any

from engines.narrative_engine import NarrativeEngine


def build_narrative_result_dict(
    *,
    analysis: dict[str, Any] | None,
    interpretation: dict[str, Any] | None,
    run_id: str = "",
) -> dict[str, Any]:
    """
    Compose Pack 05 NarrativeResult and return portal JSON.

    Uses public NarrativeEngine.compose_narrative_result only.
    """
    engine = NarrativeEngine()
    result = engine.compose_narrative_result(
        analysis=analysis or {},
        interpretation=interpretation or {},
        run_id=run_id,
    )
    payload = result.to_dict()
    payload["contract"] = "pack05_narrative_result_v1"
    return payload


def narrative_result_source_fingerprint() -> dict[str, str]:
    """Provenance block for API meta."""
    return {
        "engine": "engines.narrative_engine.engine.NarrativeEngine",
        "method": "compose_narrative_result",
        "contract": "pack05_narrative_result_v1",
        "view": (
            "applications.api.services.narrative_result_truth.build_narrative_result_dict"
        ),
    }
