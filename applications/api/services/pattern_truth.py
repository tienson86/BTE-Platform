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
    )


def pattern_source_fingerprint() -> dict[str, str]:
    """Provenance block for API meta."""
    return {
        "engine": "engines.pattern_engine.engine.PatternEngine",
        "method": "calculate",
        "contract": "pattern_rule_context_v1",
        "view": "applications.api.services.pattern_truth.build_pattern_view",
    }
