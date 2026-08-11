"""Match / mismatch classification for synthetic vs runtime v1 bands."""

from __future__ import annotations

from typing import Any

# Conceptual v2 -> v1 projection (design only; not production taxonomy v2).
SYNTHETIC_TO_V1: dict[str, str] = {
    "very_weak": "weak",
    "weak": "weak",
    "slightly_weak": "weak",
    "balanced": "balanced",
    "slightly_strong": "strong",
    "strong": "strong",
    "very_strong": "strong",
}

MISMATCH_CATEGORIES = (
    "EXACT_SYNTHETIC_MATCH",
    "TAXONOMY_RESOLUTION_GAP",
    "SCORE_PROFILE_MISMATCH",
    "SEASONAL_WEIGHTING_GAP",
    "ROOTING_GAP",
    "SUPPORT_PRESSURE_GAP",
    "STRUCTURAL_INTERACTION_GAP",
    "UNCLASSIFIED",
)


def expected_v1_band(synthetic_expected_taxonomy: str) -> str:
    """Project synthetic seven-level expectation onto v1 three-band enum."""
    key = str(synthetic_expected_taxonomy or "").strip().lower()
    if key not in SYNTHETIC_TO_V1:
        raise ValueError(f"unknown synthetic taxonomy: {synthetic_expected_taxonomy!r}")
    return SYNTHETIC_TO_V1[key]


def classify_match(
    *,
    synthetic_expected_taxonomy: str,
    runtime_v1_band: str,
    runtime_score: float,
    runtime_profile: dict[str, float],
) -> dict[str, Any]:
    """Compare synthetic expectation to runtime v1 output.

    Returns match flag, category, and brief rationale.
    Does not claim a production bug.
    """
    expected_band = expected_v1_band(synthetic_expected_taxonomy)
    runtime_band = str(runtime_v1_band or "").strip().lower()
    taxonomy = str(synthetic_expected_taxonomy or "").strip().lower()

    if runtime_band == expected_band:
        # Extremes still cannot be named by v1 even when coarse band matches.
        if taxonomy in {"very_weak", "very_strong", "slightly_weak", "slightly_strong"}:
            return {
                "match": True,
                "exact_synthetic_match": True,
                "mismatch_category": "EXACT_SYNTHETIC_MATCH",
                "expected_v1_band": expected_band,
                "note": (
                    "Coarse v1 band matches projected synthetic expectation; "
                    "seven-level intensity/tilt is not expressible in v1."
                ),
                "taxonomy_resolution_note": "TAXONOMY_RESOLUTION_GAP_LATENT",
            }
        return {
            "match": True,
            "exact_synthetic_match": True,
            "mismatch_category": "EXACT_SYNTHETIC_MATCH",
            "expected_v1_band": expected_band,
            "note": "Runtime v1 band matches projected synthetic expectation.",
            "taxonomy_resolution_note": None,
        }

    category = _infer_mismatch_category(
        taxonomy=taxonomy,
        expected_band=expected_band,
        runtime_band=runtime_band,
        runtime_score=runtime_score,
        runtime_profile=runtime_profile,
    )
    return {
        "match": False,
        "exact_synthetic_match": False,
        "mismatch_category": category,
        "expected_v1_band": expected_band,
        "note": (
            f"Projected expected v1={expected_band} vs runtime v1={runtime_band} "
            f"for synthetic_expected_taxonomy={taxonomy}."
        ),
        "taxonomy_resolution_note": None,
    }


def _infer_mismatch_category(
    *,
    taxonomy: str,
    expected_band: str,
    runtime_band: str,
    runtime_score: float,
    runtime_profile: dict[str, float],
) -> str:
    season = float(runtime_profile.get("season") or 0.0)
    root = float(runtime_profile.get("root") or 0.0)
    support = float(runtime_profile.get("support") or 0.0)
    control = float(runtime_profile.get("control") or 0.0)
    drain = float(runtime_profile.get("drain") or 0.0)

    # Adjacent tilt bands often expose v1 granularity limits.
    if taxonomy in {"slightly_weak", "slightly_strong"} and {
        expected_band,
        runtime_band,
    } <= {"weak", "balanced", "strong"}:
        if abs(runtime_score - 0.5) < 0.2 or (
            expected_band == "weak" and runtime_band == "balanced"
        ) or (expected_band == "strong" and runtime_band == "balanced"):
            return "TAXONOMY_RESOLUTION_GAP"

    if taxonomy in {"very_weak", "very_strong"}:
        # Extreme synthetic intent but score/band not extreme.
        if taxonomy == "very_weak" and runtime_score > 0.35:
            return "SCORE_PROFILE_MISMATCH"
        if taxonomy == "very_strong" and runtime_score < 0.65:
            return "SCORE_PROFILE_MISMATCH"
        return "TAXONOMY_RESOLUTION_GAP"

    if taxonomy in {"very_weak", "weak"} and season > 0:
        return "SEASONAL_WEIGHTING_GAP"
    if taxonomy in {"very_strong", "strong"} and season < 0:
        return "SEASONAL_WEIGHTING_GAP"

    if taxonomy in {"very_weak", "weak"} and root >= 12:
        return "ROOTING_GAP"
    if taxonomy in {"very_strong", "strong"} and root <= 0:
        return "ROOTING_GAP"

    pressure = abs(control) + abs(drain)
    support_mass = support + max(root, 0.0)
    if taxonomy.endswith("weak") and support_mass > pressure:
        return "SUPPORT_PRESSURE_GAP"
    if taxonomy.endswith("strong") and pressure > support_mass:
        return "SUPPORT_PRESSURE_GAP"

    if expected_band != runtime_band:
        # Opposite polarity is structural / profile disagreement.
        if {expected_band, runtime_band} == {"weak", "strong"}:
            return "STRUCTURAL_INTERACTION_GAP"
        return "SCORE_PROFILE_MISMATCH"

    return "UNCLASSIFIED"
