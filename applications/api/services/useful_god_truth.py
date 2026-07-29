"""Useful God view adapters for API contract."""

from __future__ import annotations

from applications.api.models.analysis_result import UsefulGodView


def useful_god_source_fingerprint() -> dict[str, str]:
    return {
        "layer": "applications.api.services.useful_god_truth",
        "contract": "analysis_result.UsefulGodView@1.0",
        "owner": "api_ssot",
    }


def build_useful_god_view(result) -> UsefulGodView:
    data = result.to_portal_dict() if hasattr(result, "to_portal_dict") else {}
    return UsefulGodView(
        useful_god=str(data.get("useful_god") or ""),
        favorable_gods=list(data.get("favorable_gods") or []),
        unfavorable_gods=list(data.get("unfavorable_gods") or []),
        reasoning=str(data.get("reasoning") or ""),
        confidence=float(data.get("confidence") or 0.0),
        matched_rules=[str(x) for x in (data.get("matched_rules") or [])],
    )
