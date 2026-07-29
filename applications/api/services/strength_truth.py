"""Strength view adapters for API contract."""

from __future__ import annotations

from applications.api.models.analysis_result import StrengthView


def strength_source_fingerprint() -> dict[str, str]:
    return {
        "layer": "applications.api.services.strength_truth",
        "contract": "analysis_result.StrengthView@1.0",
        "owner": "api_ssot",
    }


def build_strength_view(result) -> StrengthView:
    data = result.to_portal_dict() if hasattr(result, "to_portal_dict") else {}
    return StrengthView(
        strength_level=str(data.get("strength_level") or "balanced"),
        strength_score=float(data.get("strength_score") or 0.0),
        season_score=float(data.get("season_score") or 0.0),
        root_score=float(data.get("root_score") or 0.0),
        support_score=float(data.get("support_score") or 0.0),
        drain_score=float(data.get("drain_score") or 0.0),
        control_score=float(data.get("control_score") or 0.0),
        reasoning=str(data.get("reasoning") or ""),
        confidence=float(data.get("confidence") or 0.0),
        matched_rules=[str(x) for x in (data.get("matched_rules") or [])],
    )
