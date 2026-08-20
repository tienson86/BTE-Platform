"""Useful God view adapters for API contract."""

from __future__ import annotations

from applications.api.models.analysis_result import UsefulGodView
from engines.useful_god_engine.presentation import (
    KY_SCOPE_NOTE,
    build_customer_hy_presentation,
    customer_reason_from_result,
    dung_role_from_result,
)


def useful_god_source_fingerprint() -> dict[str, str]:
    return {
        "layer": "applications.api.services.useful_god_truth",
        "contract": "analysis_result.UsefulGodView@1.5",
        "owner": "api_ssot",
    }


def build_useful_god_view(result) -> UsefulGodView:
    data = result.to_portal_dict() if hasattr(result, "to_portal_dict") else {}
    canonical_hy = str(data.get("favorable_display") or "")
    dung = (
        dung_role_from_result(result)
        if not isinstance(result, dict)
        else {
            "element": str(data.get("useful_element") or ""),
            "stem": str(data.get("useful_stem") or ""),
            "ten_god": str(data.get("useful_ten_god") or ""),
        }
    )
    rule_id = str(data.get("winning_rule_id") or "")
    hy_pack = build_customer_hy_presentation(
        dung,
        [dict(item) for item in (data.get("favorable_roles") or [])],
        winning_rule_id=rule_id,
    )
    reason = customer_reason_from_result(result) if not isinstance(result, dict) else {}
    customer_hy = hy_pack.display
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
        favorable_display=customer_hy,
        canonical_favorable_display=canonical_hy,
        unfavorable_display=str(data.get("unfavorable_display") or ""),
        winning_rule_id=str(data.get("winning_rule_id") or ""),
        winning_rule_group=str(data.get("winning_rule_group") or ""),
        candidate_list=[dict(item) for item in (data.get("candidate_list") or [])],
        reasoning=str(data.get("reasoning") or ""),
        short_reason=str(reason.get("short_reason") or ""),
        reason_archetype=str(reason.get("reason_archetype") or ""),
        customer_reason=dict(reason),
        hy_role_status=hy_pack.role_status,
        ky_scope_note=KY_SCOPE_NOTE,
        confidence=float(data.get("confidence") or 0.0),
        matched_rules=[str(x) for x in (data.get("matched_rules") or [])],
        success=bool(data.get("success", True)),
        overall_incomplete=bool(data.get("overall_incomplete")),
        error=str(data.get("error") or ""),
        overall_useful_god=str(data.get("overall_useful_god") or data.get("useful_god") or ""),
        overall_candidate_list=[dict(item) for item in (data.get("overall_candidate_list") or [])],
        climate_candidate_list=[dict(item) for item in (data.get("climate_candidate_list") or [])],
        climate_candidate=str(data.get("climate_candidate") or ""),
        climate_display=str(data.get("climate_display") or ""),
        climate_stem=str(data.get("climate_stem") or ""),
        climate_element=str(data.get("climate_element") or ""),
        climate_ten_god=str(data.get("climate_ten_god") or ""),
        climate_rule_id=str(data.get("climate_rule_id") or ""),
        climate_rule_group=str(data.get("climate_rule_group") or ""),
        climate_reason=str(data.get("climate_reason") or ""),
        climate_preference_label=str(data.get("climate_preference_label") or ""),
    )
