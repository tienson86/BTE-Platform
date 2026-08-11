"""Saturation metadata from explicitly observable score relationships."""

from __future__ import annotations

from typing import Any

from .source_reader import RuntimeBundle


def map_saturation(bundle: RuntimeBundle) -> dict[str, Any]:
    """Record observed clamp relationship when raw and published are both present.

    Rule is observational only (PILOT-1H): when raw_score >= 50 and
    published/normalized == 1.0, mark upper_clamp. No new scoring logic.
    """
    raw = bundle.raw_score
    published = bundle.published_score
    if raw is None or published is None:
        return {
            "saturation_detected": "unknown",
            "saturation_type": "unknown",
            "saturation_source": "insufficient_score_fields",
        }
    if raw >= 50.0 and abs(published - 1.0) < 1e-9:
        return {
            "saturation_detected": True,
            "saturation_type": "upper_clamp",
            "saturation_source": "observed_raw_ge_50_and_published_1_0",
        }
    if raw <= -50.0 and abs(published - 0.0) < 1e-9:
        return {
            "saturation_detected": True,
            "saturation_type": "lower_clamp",
            "saturation_source": "observed_raw_le_minus_50_and_published_0_0",
        }
    return {
        "saturation_detected": False,
        "saturation_type": "none",
        "saturation_source": "observed_no_clamp_relationship",
    }
