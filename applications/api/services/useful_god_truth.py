"""Useful God view adapters for API contract."""

from __future__ import annotations

from applications.api.models.analysis_result import UsefulGodView


def useful_god_source_fingerprint() -> dict[str, str]:
    return {
        "layer": "applications.api.services.useful_god_truth",
        "contract": "analysis_result.UsefulGodView@1.1",
        "owner": "api_ssot",
    }


def build_useful_god_view(result) -> UsefulGodView:
    data = result.to_portal_dict() if hasattr(result, "to_portal_dict") else {}
    return UsefulGodView(
        useful_god=str(data.get("useful_god") or ""),
        useful_ten_god=str(data.get("useful_ten_god") or ""),
        useful_stem=str(data.get("useful_stem") or ""),
        useful_element=str(data.get("useful_element") or ""),
        useful_display=str(data.get("useful_display") or ""),
        favorable_gods=list(data.get("favorable_gods") or []),
        unfavorable_gods=list(data.get("unfavorable_gods") or []),
        favorable_roles=[dict(item) for item in (data.get("favorable_roles") or [])],
        unfavorable_roles=[dict(item) for item in (data.get("unfavorable_roles") or [])],
        favorable_display=str(data.get("favorable_display") or ""),
        unfavorable_display=str(data.get("unfavorable_display") or ""),
        winning_rule_id=str(data.get("winning_rule_id") or ""),
        winning_rule_group=str(data.get("winning_rule_group") or ""),
        candidate_list=[dict(item) for item in (data.get("candidate_list") or [])],
        reasoning=str(data.get("reasoning") or ""),
        confidence=float(data.get("confidence") or 0.0),
        matched_rules=[str(x) for x in (data.get("matched_rules") or [])],
    )
