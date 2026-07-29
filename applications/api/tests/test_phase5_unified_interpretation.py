"""Phase 5: unified Interpretation truth — RuleContext → Result → AnalysisResult → API."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.api.app import create_app
from applications.api.models.analysis_result import AnalysisResult
from applications.api.services.bazi_truth import build_bazi_view
from applications.api.services.interpretation_truth import build_interpretation_view
from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.pattern_truth import build_pattern_view
from applications.api.services.score_truth import build_score_view
from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.interpretation_engine.engine import InterpretationEngine
from engines.pattern_engine.context import PatternContext
from engines.pattern_engine.engine import PatternEngine
from engines.score_engine.engine import ScoreEngine

CRITICAL = {
    "year": 1987,
    "month": 1,
    "day": 21,
    "hour": 4,
    "minute": 30,
    "gender": "male",
}


def _pipeline_ctx_for_critical() -> tuple[dict, object, object, object]:
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
    return pipeline_ctx, chart, pattern, score


def test_interpretation_reads_rule_context_without_rebuild() -> None:
    pipeline_ctx, _, _, _ = _pipeline_ctx_for_critical()
    assert InterpretationEngine.is_rule_context(pipeline_ctx)
    pattern_before = dict(pipeline_ctx.get("pattern") or {})
    bazi_before = dict(pipeline_ctx.get("bazi") or {})
    score_before = dict(pipeline_ctx.get("score") or {})
    result = InterpretationEngine().run(pipeline_ctx)
    assert result is not None
    assert pipeline_ctx.get("pattern") == pattern_before
    assert pipeline_ctx.get("bazi") == bazi_before
    assert pipeline_ctx.get("score") == score_before


def test_interpretation_result_matches_view() -> None:
    pipeline_ctx, _, _, _ = _pipeline_ctx_for_critical()
    result = InterpretationEngine().run(pipeline_ctx)
    view = build_interpretation_view(result)
    portal = result.to_portal_dict()
    assert view.to_dict() == portal
    assert "summary" not in portal
    assert "matched_rule_count" not in portal
    assert "resolved_rule_count" not in portal
    assert "rules_used" not in portal
    assert isinstance(portal["sections"], list)
    assert portal["section_count"] == len(portal["sections"])


def test_orchestrator_interpretation_matches_engine() -> None:
    service = OrchestratorService()
    payload = service.run_stage(
        "interpretation",
        year=CRITICAL["year"],
        month=CRITICAL["month"],
        day=CRITICAL["day"],
        hour=CRITICAL["hour"],
        minute=CRITICAL["minute"],
        gender=CRITICAL["gender"],
    )
    pipeline_ctx, _, _, _ = _pipeline_ctx_for_critical()
    engine_result = InterpretationEngine().run(pipeline_ctx)
    engine_portal = engine_result.to_portal_dict()
    api_interp = payload["interpretation"]
    assert api_interp["section_count"] == engine_portal["section_count"]
    assert api_interp["sentence_count"] == engine_portal["sentence_count"]
    assert api_interp["confidence"] == engine_portal["confidence"]
    assert [s["id"] for s in api_interp["sections"]] == [
        s["id"] for s in engine_portal["sections"]
    ]
    assert "matched_rule_count" not in api_interp
    assert "build_interpretation_view" in payload["interpretation_source"]["view"]


def test_api_analyze_interpretation_matches_engine() -> None:
    client = TestClient(create_app())
    response = client.post("/api/v1/analyze", json=CRITICAL)
    assert response.status_code == 200
    data = response.json()["data"]
    interp = data["interpretation"]
    pipeline_ctx, _, _, _ = _pipeline_ctx_for_critical()
    engine_portal = InterpretationEngine().run(pipeline_ctx).to_portal_dict()
    assert interp["section_count"] == engine_portal["section_count"]
    assert interp["confidence"] == engine_portal["confidence"]
    assert "summary" not in interp
    assert interp["sections"]


def test_analysis_result_interpretation_slice() -> None:
    pipeline_ctx, chart, pattern, score = _pipeline_ctx_for_critical()
    result = InterpretationEngine().run(pipeline_ctx)
    view = build_interpretation_view(result)
    analysis = AnalysisResult(
        bazi=build_bazi_view(chart),
        pattern=build_pattern_view(pattern),
        score=build_score_view(score),
        interpretation=view,
    )
    assert analysis.interpretation_dict() == view.to_dict()
