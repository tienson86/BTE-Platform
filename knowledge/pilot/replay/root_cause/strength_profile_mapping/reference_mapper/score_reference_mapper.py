"""Score reference mapping — preserve observed scores only."""

from __future__ import annotations

from typing import Any

from .source_reader import RuntimeBundle


def map_score_reference(bundle: RuntimeBundle) -> dict[str, Any]:
    """Map existing score fields without reconstruction."""
    return {
        "raw_score": bundle.raw_score,
        "normalized_score": bundle.normalized_score,
        "published_score": bundle.published_score,
        "current_v1_band": bundle.current_v1_band or "unknown",
        "score_source": "strength_engine_v1_runtime_observation",
        "score_status": "observed"
        if bundle.normalized_score is not None or bundle.raw_score is not None
        else "unknown",
        "saturation_detected": None,  # filled by saturation_mapper
        "saturation_type": None,
    }
