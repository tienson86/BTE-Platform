"""Phase 4: unified Score truth — RuleContext → ScoreResult → AnalysisResult → API."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.api.app import create_app
from applications.api.models.analysis_result import AnalysisResult
from applications.api.services.bazi_truth import build_bazi_view
from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.pattern_truth import build_pattern_view
from applications.api.services.score_truth import build_score_view
from applications.api.tests.unified_stack import CRITICAL, production_rule_context
from engines.score_engine.engine import ScoreEngine


def _rule_context_for_critical() -> tuple[dict, object, object]:
    """Reuse orchestrator-aligned RuleContext (canonical Pattern + Strength overlay)."""
    return production_rule_context()


def test_score_engine_reads_rule_context_without_rebuild() -> None:
    rule_context, _, _ = _rule_context_for_critical()
    assert ScoreEngine.is_rule_context(rule_context)
    engine = ScoreEngine()
    # Snapshot identity of pattern/bazi slices before score.
    pattern_before = dict(rule_context.get("pattern") or {})
    bazi_before = dict(rule_context.get("bazi") or {})
    result = engine.calculate(rule_context)
    assert result.success
    assert rule_context.get("pattern") == pattern_before
    assert rule_context.get("bazi") == bazi_before
    # Production path must not rebuild — input already has wuxing.
    assert "wuxing" in rule_context


def test_score_result_matches_score_view() -> None:
    rule_context, _, _ = _rule_context_for_critical()
    result = ScoreEngine().calculate(rule_context)
    view = build_score_view(result)
    portal = result.to_portal_dict()
    assert view.to_dict() == portal
    assert "details" not in portal
    assert "modules" not in portal
    assert "total_score" in portal
    assert "strength_score" in portal
    assert "wuxing_score" in portal


def test_append_score_only_mutates_score_section() -> None:
    rule_context, _, _ = _rule_context_for_critical()
    engine = ScoreEngine()
    result = engine.calculate(rule_context)
    pattern_before = dict(rule_context.get("pattern") or {})
    bazi_before = dict(rule_context.get("bazi") or {})
    wuxing_before = dict(rule_context.get("wuxing") or {})
    composed = engine.append_score_to_rule_context(rule_context, result)
    assert rule_context["pattern"] == pattern_before
    assert rule_context["bazi"] == bazi_before
    assert rule_context["wuxing"] == wuxing_before
    assert composed["score"]["total_score"] == result.total_score
    assert composed["score"]["strength_score"] == result.strength_score
    assert composed["pattern"] == pattern_before
    assert composed["bazi"] == bazi_before
    assert composed["wuxing"] == wuxing_before


def test_orchestrator_score_payload_matches_engine() -> None:
    service = OrchestratorService()
    payload = service.run_stage(
        "score",
        year=CRITICAL["year"],
        month=CRITICAL["month"],
        day=CRITICAL["day"],
        hour=CRITICAL["hour"],
        minute=CRITICAL["minute"],
        gender=CRITICAL["gender"],
    )
    rule_context, _, _ = _rule_context_for_critical()
    engine_result = ScoreEngine().calculate(rule_context)
    api_score = payload["score"]
    assert api_score["total_score"] == engine_result.total_score
    assert api_score["strength_score"] == engine_result.strength_score
    assert api_score["pattern_score"] == engine_result.pattern_score
    assert api_score["wuxing_score"] == engine_result.wuxing_score
    assert api_score["ten_god_score"] == engine_result.ten_god_score
    assert api_score["grade"] == engine_result.grade
    assert "details" not in api_score
    assert "modules" not in api_score
    assert "build_score_view" in payload["score_source"]["view"]


def test_api_analyze_score_matches_engine() -> None:
    client = TestClient(create_app())
    response = client.post("/api/v1/analyze", json=CRITICAL)
    assert response.status_code == 200
    data = response.json()["data"]
    score = data["score"]
    rule_context, _, _ = _rule_context_for_critical()
    engine_result = ScoreEngine().calculate(rule_context)
    assert score["total_score"] == engine_result.total_score
    assert score["wuxing_score"] == engine_result.wuxing_score
    assert score["grade"] == engine_result.grade
    assert "details" not in score


def test_analysis_result_score_slice() -> None:
    rule_context, chart, pattern = _rule_context_for_critical()
    result = ScoreEngine().calculate(rule_context)
    view = build_score_view(result)
    analysis = AnalysisResult(
        bazi=build_bazi_view(chart),
        pattern=build_pattern_view(pattern),
        score=view,
    )
    assert analysis.score_dict() == view.to_dict()
