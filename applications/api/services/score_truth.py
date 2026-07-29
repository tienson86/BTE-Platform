"""
Unified Score truth — ScoreResult → ScoreView for AnalysisResult.score.
"""

from __future__ import annotations

from engines.score_engine.result import ScoreResult

from applications.api.models.analysis_result import ScoreView


def build_score_view(result: ScoreResult) -> ScoreView:
    """Build authoritative ScoreView from ScoreEngine result."""
    portal = result.to_portal_dict()
    return ScoreView(
        success=bool(portal.get("success", False)),
        total_score=float(portal.get("total_score") or 0.0),
        strength_score=float(portal.get("strength_score") or 0.0),
        pattern_score=float(portal.get("pattern_score") or 0.0),
        ten_god_score=float(portal.get("ten_god_score") or 0.0),
        wuxing_score=float(portal.get("wuxing_score") or 0.0),
        grade=str(portal.get("grade") or ""),
        confidence=str(portal.get("confidence") or ""),
        recommendation=str(portal.get("recommendation") or ""),
        useful_god_score=(
            float(portal["useful_god_score"])
            if "useful_god_score" in portal
            else None
        ),
        shensha_score=(
            float(portal["shensha_score"]) if "shensha_score" in portal else None
        ),
        luck_score=float(portal["luck_score"]) if "luck_score" in portal else None,
        interpretation_score=(
            float(portal["interpretation_score"])
            if "interpretation_score" in portal
            else None
        ),
        wuxing_series=list(portal.get("wuxing_series") or []),
        ten_god_series=list(portal.get("ten_god_series") or []),
    )


def score_source_fingerprint() -> dict[str, str]:
    """Provenance block for API meta."""
    return {
        "engine": "engines.score_engine.engine.ScoreEngine",
        "method": "calculate",
        "contract": "score_rule_context_v1",
        "view": "applications.api.services.score_truth.build_score_view",
    }
