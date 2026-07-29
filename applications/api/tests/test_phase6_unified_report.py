"""Phase 6: unified Report truth — AnalysisResult → ReportResult → API."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.api.app import create_app
from applications.api.models.analysis_result import AnalysisResult
from applications.api.services.bazi_truth import build_bazi_view
from applications.api.services.interpretation_truth import build_interpretation_view
from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.pattern_truth import build_pattern_view
from applications.api.services.report_truth import (
    build_narrative_view,
    build_report_view,
)
from applications.api.services.score_truth import build_score_view
from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.interpretation_engine.engine import InterpretationEngine
from engines.pattern_engine.context import PatternContext
from engines.pattern_engine.engine import PatternEngine
from engines.report_engine.engine import ReportEngine
from engines.score_engine.engine import ScoreEngine

CRITICAL = {
    "year": 1987,
    "month": 1,
    "day": 21,
    "hour": 4,
    "minute": 30,
    "gender": "male",
}


def _analysis_for_critical() -> AnalysisResult:
    calendar = CalendarEngine().build(
        CRITICAL["year"],
        CRITICAL["month"],
        CRITICAL["day"],
        CRITICAL["hour"],
        CRITICAL["minute"],
    )
    chart = BaziEngine().build(calendar, gender=CRITICAL["gender"])
    pattern_context = PatternContext(
        year_pillar=f"{chart.year_pillar.stem} {chart.year_pillar.branch}",
        month_pillar=f"{chart.month_pillar.stem} {chart.month_pillar.branch}",
        day_pillar=f"{chart.day_pillar.stem} {chart.day_pillar.branch}",
        hour_pillar=f"{chart.hour_pillar.stem} {chart.hour_pillar.branch}",
        day_master=chart.day_master,
        ten_gods={"list": list(chart.ten_gods or [])},
        shensha=list(chart.shensha or []),
        calendar=calendar,
        bazi=chart,
    )
    pattern = PatternEngine().calculate(pattern_context)
    pipeline_ctx = dict(pattern.rule_context or {})
    score = ScoreEngine().calculate(pipeline_ctx)
    ScoreEngine().append_score_to_rule_context(pipeline_ctx, score)
    interpretation = InterpretationEngine().run(pipeline_ctx)
    return AnalysisResult(
        bazi=build_bazi_view(chart),
        pattern=build_pattern_view(pattern),
        score=build_score_view(score),
        interpretation=build_interpretation_view(interpretation),
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
    result = ReportEngine().render_from_analysis(analysis, include_narrative=True)
    report_view = build_report_view(result)
    narrative_view = build_narrative_view(result)
    assert report_view.to_dict() == result.to_portal_report_dict()
    assert narrative_view.to_dict() == result.to_portal_narrative_dict()
    assert "templates_used" not in report_view.to_dict()
    assert report_view.section_count == len(analysis.interpretation_dict()["sections"])


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
        ReportEngine().render_from_analysis(analysis)
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
        analysis, include_narrative=True
    )
    assert data["report"] == engine_result.to_portal_report_dict()
    assert data["narrative"] == engine_result.to_portal_narrative_dict()
    assert "FPR" not in data["narrative"]["markdown"]
    assert "templates_used" not in data["report"]


def test_analysis_result_report_slices() -> None:
    analysis = _analysis_for_critical()
    result = ReportEngine().render_from_analysis(analysis, include_narrative=True)
    analysis.report = build_report_view(result)
    analysis.narrative = build_narrative_view(result)
    assert analysis.report_dict() == result.to_portal_report_dict()
    assert analysis.narrative_dict() == result.to_portal_narrative_dict()
