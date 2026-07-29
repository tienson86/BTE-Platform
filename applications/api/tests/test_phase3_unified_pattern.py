"""Phase 3: unified Pattern truth — engine, AnalysisResult, and API must agree."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.api.app import create_app
from applications.api.models.analysis_result import AnalysisResult
from applications.api.services.bazi_truth import build_bazi_view
from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.pattern_truth import build_pattern_view
from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.pattern_engine.context import PatternContext
from engines.pattern_engine.engine import PatternEngine

CRITICAL = {
    "year": 1987,
    "month": 1,
    "day": 21,
    "hour": 4,
    "minute": 30,
    "gender": "male",
}


def _build_pattern_stack() -> tuple[PatternEngine, PatternContext, object]:
    calendar = CalendarEngine().build(
        CRITICAL["year"],
        CRITICAL["month"],
        CRITICAL["day"],
        CRITICAL["hour"],
        CRITICAL["minute"],
    )
    chart = BaziEngine().build(calendar, gender=CRITICAL["gender"])
    context = PatternContext(
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
    return PatternEngine(), context, chart


def test_pattern_engine_produces_rule_context() -> None:
    engine, context, _ = _build_pattern_stack()
    result = engine.calculate(context)
    assert result.success
    assert result.pattern == "chinh_quan"
    assert result.cach_cuc == "Chính Quan"
    assert result.rule_context
    assert "wuxing" in result.rule_context
    assert result.rule_context["pattern"]["main_pattern"] == "chinh_quan"


def test_pattern_view_matches_engine() -> None:
    engine, context, _ = _build_pattern_stack()
    result = engine.calculate(context)
    view = build_pattern_view(result)
    portal = result.to_portal_dict()
    assert view.pattern == portal["pattern"]
    assert view.cach_cuc == portal["cach_cuc"]
    assert view.to_dict() == portal
    assert view.than == "Kim"
    assert view.dung_than == "Chính Quan"


def test_orchestrator_pattern_payload_matches_engine() -> None:
    service = OrchestratorService()
    payload = service.run_stage(
        "pattern",
        year=CRITICAL["year"],
        month=CRITICAL["month"],
        day=CRITICAL["day"],
        hour=CRITICAL["hour"],
        minute=CRITICAL["minute"],
        gender=CRITICAL["gender"],
    )
    engine, context, _ = _build_pattern_stack()
    engine_result = engine.calculate(context)
    api_pattern = payload["pattern"]
    assert api_pattern["pattern"] == engine_result.pattern
    assert api_pattern["cach_cuc"] == engine_result.cach_cuc
    assert api_pattern["success"] == engine_result.success
    assert "matched_rules" not in api_pattern
    assert "error" not in api_pattern
    assert "build_pattern_view" in payload["pattern_source"]["view"]


def test_api_analyze_pattern_matches_engine() -> None:
    client = TestClient(create_app())
    response = client.post("/api/v1/analyze", json=CRITICAL)
    assert response.status_code == 200
    data = response.json()["data"]
    pattern = data["pattern"]
    engine, context, _ = _build_pattern_stack()
    engine_result = engine.calculate(context)
    assert pattern["pattern"] == engine_result.pattern
    assert pattern["cach_cuc"] == "Chính Quan"
    assert pattern["than"] == "Kim"
    assert pattern["dung_than"] == "Chính Quan"


def test_analysis_result_pattern_slice() -> None:
    engine, context, chart = _build_pattern_stack()
    result = engine.calculate(context)
    view = build_pattern_view(result)
    analysis = AnalysisResult(
        bazi=build_bazi_view(chart),
        pattern=view,
    )
    assert analysis.pattern_dict() == view.to_dict()
