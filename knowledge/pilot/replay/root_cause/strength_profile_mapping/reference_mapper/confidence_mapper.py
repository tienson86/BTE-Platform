"""Confidence mapping — no fabricated numeric confidence."""

from __future__ import annotations

from typing import Any

from .ascii_utils import SCHEMA_VERSION
from .source_reader import RuntimeBundle


def map_confidence(
    bundle: RuntimeBundle,
    *,
    completeness_overall: str,
    conflict_count: int,
) -> dict[str, Any]:
    """Map confidence factors qualitatively from available metadata only."""
    factors = {
        "evidence_completeness": _map_completeness(completeness_overall),
        "evidence_conflict": "low" if conflict_count > 0 else "unknown",
        "calendar_certainty": _calendar(bundle),
        "structural_certainty": "unknown",
        "expert_agreement": _expert(bundle),
        "boundary_proximity": "unknown",
        "runtime_stability": "unknown",
    }
    # Overall: unknown unless we have enough positive signals; never invent high.
    known = [v for v in factors.values() if v != "unknown"]
    if not known:
        overall = "unknown"
    elif "low" in known:
        overall = "low"
    elif all(v == "high" for v in known) and len(known) >= 2:
        overall = "medium"  # still conservative; runtime confidence often non-discriminative
    else:
        overall = "medium" if "medium" in known or "high" in known else "low"

    return {
        "schema_version": SCHEMA_VERSION,
        "overall": overall,
        "factors": factors,
        "numeric_runtime_confidence": bundle.runtime_confidence,
        "notes": (
            "numeric_runtime_confidence is observed V1 value if present; "
            "overall confidence is qualitative and not a new score"
        ),
    }


def _map_completeness(overall: str) -> str:
    return {
        "complete": "high",
        "partial": "medium",
        "limited": "low",
        "unknown": "unknown",
    }.get(overall, "unknown")


def _calendar(bundle: RuntimeBundle) -> str:
    if bundle.calendar_status in {"VERIFIED", "VERIFIED_CORRECTED_PROJECTION"}:
        return "high"
    if bundle.population == "synthetic_stress":
        return "low"
    return "unknown"


def _expert(bundle: RuntimeBundle) -> str:
    if not bundle.expert_external:
        return "unknown"
    agreement = (bundle.expert_external.get("agreement") or {}).get("expert_agreement")
    if agreement == "EXACT_MATCH":
        return "high"
    if agreement:
        return "medium"
    return "unknown"
