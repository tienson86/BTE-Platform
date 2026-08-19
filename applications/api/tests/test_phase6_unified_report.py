"""Phase 6: unified Report truth — AnalysisResult → ReportResult → API."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.api.app import create_app
from applications.api.models.analysis_result import AnalysisResult
from applications.api.services.bazi_truth import build_bazi_view
from applications.api.services.interpretation_truth import build_interpretation_view
from applications.api.services.narrative_result_truth import build_narrative_result_dict
from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.pattern_truth import build_pattern_view
from applications.api.services.report_truth import (
    build_narrative_view,
    build_report_view,
)
from applications.api.services.score_truth import build_score_view
from applications.api.tests.unified_stack import CRITICAL, production_interpretation_stage
from engines.report_engine.engine import ReportEngine


def _analysis_for_critical() -> AnalysisResult:
    """AnalysisResult from the same Pattern → Score → Interpretation stack as production."""
    interpretation, _ctx, chart, pattern, score = production_interpretation_stage()
    return AnalysisResult(
        bazi=build_bazi_view(chart),
        pattern=build_pattern_view(pattern),
        score=build_score_view(score),
        interpretation=build_interpretation_view(interpretation),
    )


def _narrative_for(analysis: AnalysisResult) -> dict:
    return build_narrative_result_dict(
        analysis={
            "bazi": analysis.bazi_dict(),
            "pattern": analysis.pattern_dict(),
            "strength": analysis.strength_dict(),
            "useful_god": analysis.useful_god_dict(),
            "score": analysis.score_dict(),
        },
        interpretation=analysis.interpretation_dict(),
        run_id="phase6",
    )


def test_report_engine_reads_analysis_result_only() -> None:
    analysis = _analysis_for_critical()
    before = analysis.interpretation_dict()
    result = ReportEngine().render_from_analysis(analysis, include_narrative=True)
    assert analysis.interpretation_dict() == before
    assert result.to_portal_report_dict()["title"] == "Bản luận Bát tự"
    assert result.to_portal_narrative_dict()["title"] == "Bản luận Bát tự"


def test_report_result_matches_view() -> None:
    analysis = _analysis_for_critical()
    narrative_result = _narrative_for(analysis)
    result = ReportEngine().render_from_analysis(
        analysis,
        include_narrative=True,
        narrative_result=narrative_result,
    )
    report_view = build_report_view(result)
    narrative_view = build_narrative_view(result)
    assert report_view.to_dict() == result.to_portal_report_dict()
    assert narrative_view.to_dict() == result.to_portal_narrative_dict()
    assert "templates_used" not in report_view.to_dict()
    assert report_view.section_count == report_view.to_dict()["section_count"]
    assert report_view.section_count >= 1
    assert analysis.pattern.cach_cuc == "Chính Ấn"
    assert analysis.pattern.pattern == "chinh_an"
    assert result.source == "pack05_narrative_result_v1"


def test_orchestrator_report_matches_engine() -> None:
    service = OrchestratorService()
    payload = service.run_stage(
        "report",
        year=CRITICAL["year"],
        month=CRITICAL["month"],
        day=CRITICAL["day"],
        hour=CRITICAL["hour"],
        minute=CRITICAL["minute"],
        gender=CRITICAL["gender"],
    )
    analysis = _analysis_for_critical()
    engine_report = build_report_view(
        ReportEngine().render_from_analysis(
            analysis,
            narrative_result=payload["narrative_result"],
        )
    )
    api_report = payload["report"]
    assert api_report == engine_report.to_dict()
    assert "build_report_view" in payload["report_source"]["view"]
    assert "narrative" not in payload


def test_api_analyze_report_and_narrative_match_engine() -> None:
    client = TestClient(create_app())
    response = client.post("/api/v1/analyze", json=CRITICAL)
    assert response.status_code == 200
    data = response.json()["data"]
    analysis = _analysis_for_critical()
    engine_result = ReportEngine().render_from_analysis(
        analysis,
        include_narrative=True,
        narrative_result=data["narrative_result"],
    )
    assert data["report"] == engine_result.to_portal_report_dict()
    assert data["narrative"] == engine_result.to_portal_narrative_dict()
    assert "FPR" not in data["narrative"]["markdown"]
    assert "templates_used" not in data["report"]


def test_analysis_result_report_slices() -> None:
    analysis = _analysis_for_critical()
    result = ReportEngine().render_from_analysis(
        analysis,
        include_narrative=True,
        narrative_result=_narrative_for(analysis),
    )
    analysis.report = build_report_view(result)
    analysis.narrative = build_narrative_view(result)
    assert analysis.report_dict() == result.to_portal_report_dict()
    assert analysis.narrative_dict() == result.to_portal_narrative_dict()
