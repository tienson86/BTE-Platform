"""Phase 2: unified Bazi truth — engine, AnalysisResult, and API must agree."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.api.app import create_app
from applications.api.models.analysis_result import AnalysisMeta, AnalysisResult
from applications.api.services.bazi_truth import (
    build_bazi_view,
    sync_chart_from_view,
)
from applications.api.services.orchestrator import OrchestratorService
from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine

CRITICAL_CASE = {
    "year": 1987,
    "month": 1,
    "day": 21,
    "hour": 4,
    "minute": 30,
    "gender": "male",
}

EXPECTED_PILLARS = (
    ("Bính", "Dần"),
    ("Tân", "Sửu"),
    ("Canh", "Ngọ"),
    ("Mậu", "Dần"),
)


def _pillar_pair(bazi: dict, key: str) -> tuple[str, str]:
    pillar = bazi[key]
    return pillar["stem"], pillar["branch"]


def test_engine_chart_matches_critical_case() -> None:
    bazi_engine = BaziEngine()
    chart = bazi_engine.build(
        CRITICAL_CASE["year"],
        CRITICAL_CASE["month"],
        CRITICAL_CASE["day"],
        CRITICAL_CASE["hour"],
        CRITICAL_CASE["minute"],
        gender=CRITICAL_CASE["gender"],
    )
    actual = (
        (chart.year_pillar.stem, chart.year_pillar.branch),
        (chart.month_pillar.stem, chart.month_pillar.branch),
        (chart.day_pillar.stem, chart.day_pillar.branch),
        (chart.hour_pillar.stem, chart.hour_pillar.branch),
    )
    assert actual == tuple(EXPECTED_PILLARS)


def test_bazi_view_and_chart_stay_aligned() -> None:
    calendar = CalendarEngine().build(
        CRITICAL_CASE["year"],
        CRITICAL_CASE["month"],
        CRITICAL_CASE["day"],
        CRITICAL_CASE["hour"],
        CRITICAL_CASE["minute"],
    )
    chart = BaziEngine().build(calendar, gender=CRITICAL_CASE["gender"])
    view = build_bazi_view(chart)
    sync_chart_from_view(chart, view)

    analysis = AnalysisResult(
        bazi=view,
        meta=AnalysisMeta(contract_version="1.0"),
    )
    payload = analysis.bazi_dict()

    for key, expected in zip(
        ("year_pillar", "month_pillar", "day_pillar", "hour_pillar"),
        EXPECTED_PILLARS,
    ):
        assert _pillar_pair(payload, key) == expected
        assert payload[key]["ten_god"] == view.to_dict()[key]["ten_god"]

    assert chart.ten_gods == view.pillar_ten_gods()
    assert payload["ten_gods"] == view.pillar_ten_gods()
    assert chart.ten_gods != ["Tỷ Kiên", "Tỷ Kiên", "Tỷ Kiên", "Tỷ Kiên"]


def test_orchestrator_payload_matches_engine() -> None:
    service = OrchestratorService()
    payload = service.run_stage(
        "bazi",
        year=CRITICAL_CASE["year"],
        month=CRITICAL_CASE["month"],
        day=CRITICAL_CASE["day"],
        hour=CRITICAL_CASE["hour"],
        minute=CRITICAL_CASE["minute"],
        gender=CRITICAL_CASE["gender"],
    )
    bazi = payload["bazi"]

    chart = BaziEngine().build(
        CRITICAL_CASE["year"],
        CRITICAL_CASE["month"],
        CRITICAL_CASE["day"],
        CRITICAL_CASE["hour"],
        CRITICAL_CASE["minute"],
        gender=CRITICAL_CASE["gender"],
    )
    engine_pairs = (
        (chart.year_pillar.stem, chart.year_pillar.branch),
        (chart.month_pillar.stem, chart.month_pillar.branch),
        (chart.day_pillar.stem, chart.day_pillar.branch),
        (chart.hour_pillar.stem, chart.hour_pillar.branch),
    )
    api_pairs = (
        _pillar_pair(bazi, "year_pillar"),
        _pillar_pair(bazi, "month_pillar"),
        _pillar_pair(bazi, "day_pillar"),
        _pillar_pair(bazi, "hour_pillar"),
    )
    assert api_pairs == engine_pairs == tuple(EXPECTED_PILLARS)

    assert payload["bazi_source"]["engine"] == "engines.bazi_engine.engine.BaziEngine"
    assert "build_bazi_view" in payload["bazi_source"]["view"]


def test_api_analyze_matches_engine_for_critical_case() -> None:
    client = TestClient(create_app())
    response = client.post("/api/v1/analyze", json=CRITICAL_CASE)
    assert response.status_code == 200
    data = response.json()["data"]

    bazi = data["bazi"]
    for key, expected in zip(
        ("year_pillar", "month_pillar", "day_pillar", "hour_pillar"),
        EXPECTED_PILLARS,
    ):
        assert _pillar_pair(bazi, key) == expected

    calendar = data["calendar"]
    assert calendar["lunar"]["year"] == 1986
    assert calendar["lunar"]["month"] == 12
    assert calendar["lunar"]["day"] == 22
    assert calendar["lunar"]["is_leap_month"] is False
    assert calendar["lunar_date"] == "22/12/1986"
    assert calendar["year_can_chi"] == "Bính Dần"
    assert calendar["bazi_can_chi"]["year"] == "Bính Dần"
    assert calendar["bazi_can_chi"]["month"] == "Tân Sửu"
    assert calendar["bazi_can_chi"]["day"] == "Canh Ngọ"
    assert calendar["bazi_can_chi"]["hour"] == "Mậu Dần"
    assert bazi["hour_pillar"]["ten_god"] == "Thiên Ấn"
