"""
Unified Pattern truth — PatternResult → PatternView for AnalysisResult.pattern.
"""

from __future__ import annotations

from engines.pattern_engine.engine import PatternResult

from applications.api.models.analysis_result import PatternView


def build_pattern_view(result: PatternResult) -> PatternView:
    """Build authoritative PatternView from PatternEngine result."""
    portal = result.to_portal_dict()
    return PatternView(
        success=bool(portal.get("success", False)),
        pattern=str(portal.get("pattern") or ""),
        cach_cuc=str(portal.get("cach_cuc") or ""),
        score=float(portal.get("score") or 0.0),
        priority=int(portal.get("priority") or 0),
        than=str(portal.get("than") or result.than or ""),
        than_vuong_nhuoc=str(
            portal.get("than_vuong_nhuoc") or result.than_vuong_nhuoc or ""
        ),
        tong_cach=str(portal.get("tong_cach") or result.tong_cach or ""),
        dung_than=str(portal.get("dung_than") or result.dung_than or ""),
        hy_than=str(portal.get("hy_than") or result.hy_than or ""),
        ky_than=str(portal.get("ky_than") or result.ky_than or ""),
        dieu_hau=str(portal.get("dieu_hau") or result.dieu_hau or ""),
        success_reason=str(portal.get("success_reason") or result.success_reason or ""),
        winning_rule_id=str(portal.get("winning_rule_id") or result.winning_rule_id or ""),
        evidence_compact=str(
            portal.get("evidence_compact") or result.evidence_compact or ""
        ),
        month_branch=str(portal.get("month_branch") or result.month_branch or ""),
        month_main_qi=str(portal.get("month_main_qi") or result.month_main_qi or ""),
        month_main_qi_ten_god=str(
            portal.get("month_main_qi_ten_god") or result.month_main_qi_ten_god or ""
        ),
        month_hidden_stems=[
            str(item)
            for item in (
                portal.get("month_hidden_stems") or result.month_hidden_stems or []
            )
        ],
        day_master=str(portal.get("day_master") or result.day_master or ""),
        penetration_exact=(
            portal["penetration_exact"]
            if portal.get("penetration_exact") is not None
            else result.penetration_exact
        ),
        penetration_related=list(
            portal.get("penetration_related") or result.penetration_related or []
        ),
        candidate_patterns=[
            str(item)
            for item in (
                portal.get("candidate_patterns") or result.candidate_patterns or []
            )
        ],
        fallback_used=bool(portal.get("fallback_used", result.fallback_used)),
    )


def pattern_source_fingerprint() -> dict[str, str]:
    """Provenance block for API meta."""
    return {
        "engine": "engines.pattern_engine.engine.PatternEngine",
        "method": "calculate",
        "contract": "pattern_rule_context_v1",
        "view": "applications.api.services.pattern_truth.build_pattern_view",
    }
