"""P1: canonical calendar truth and recovered analytical data."""

from __future__ import annotations

from applications.api.models.analysis_result import AnalysisResult, BaziView, PillarView, ScoreView
from applications.api.services.five_elements_truth import build_five_elements_payload
from applications.api.services.luck_truth import shape_luck_payload
from applications.api.services.orchestrator import OrchestratorService
from applications.production.engine_runner import ProductionEngineRunner
from applications.production.models import ProductionRequest
from engines.calendar_engine.engine import CalendarEngine
from engines.report_engine.adapters.report_input_v1_adapter import (
    ReportInputV1Adapter,
    ReportInputV1Source,
)

HUYNH = {
    "year": 1966,
    "month": 9,
    "day": 24,
    "hour": 4,
    "minute": 15,
    "gender": "male",
}


def test_calendar_result_returns_lunar_ymd() -> None:
    """A. CalendarResult returns lunar Y/M/D."""
    result = CalendarEngine().build(1966, 9, 24, 4, 15)
    assert result.lunar_year == result.lunar.year
    assert result.lunar_month == result.lunar.month
    assert result.lunar_day == result.lunar.day
    assert result.lunar_date == f"{result.lunar_day:02d}/{result.lunar_month:02d}/{result.lunar_year:04d}"
    payload = result.to_dict()
    assert payload["lunar"]["year"] == result.lunar_year
    assert payload["lunar"]["day"] == result.lunar_day


def test_leap_month_flag_survives_downstream() -> None:
    """B. Leap-month flag survives CalendarResult and API calendar."""
    result = CalendarEngine().build(2020, 5, 23)
    assert result.leap_month is True
    assert result.lunar.is_leap_month is True or result.lunar.leap is True
    assert "nhuận" in (result.lunar_date or "")
    payload = OrchestratorService().run_stage(
        "calendar",
        year=2020,
        month=5,
        day=23,
        hour=0,
        minute=0,
        gender="male",
    )
    assert payload["calendar"]["lunar"]["is_leap_month"] is True
    assert payload["calendar"]["is_leap_month"] is True


def test_api_lunar_is_not_bazi_pillars() -> None:
    """C. Public calendar lunar birth is CalendarResult, not BaZi pillars."""
    payload = OrchestratorService().analyze(**HUYNH)
    calendar = payload["calendar"]
    bazi = payload["bazi"]
    lunar_date = calendar["lunar_date"]
    year_pillar = f"{bazi['year_pillar']['stem']} {bazi['year_pillar']['branch']}"
    assert calendar["lunar"]["year"]
    assert calendar["lunar"]["month"]
    assert calendar["lunar"]["day"]
    assert str(calendar["lunar"]["year"]) in lunar_date
    assert year_pillar not in lunar_date
    assert calendar.get("bazi_can_chi", {}).get("year") == year_pillar


def test_pdf_lunar_uses_calendar_result() -> None:
    """D. PDF/report lunar birth uses CalendarResult.lunar."""
    output = _production()
    report = ReportInputV1Adapter().build(output.report_source)
    lunar = output.calendar["lunar"]
    assert report.calendar.lunar_year == lunar["year"]
    assert report.calendar.lunar_month == lunar["month"]
    assert report.calendar.lunar_day == lunar["day"]
    assert str(lunar["year"]) in report.calendar.lunar_date
    assert report.calendar.lunar_date == output.calendar["lunar_date"]
    assert report.calendar.leap_month is bool(lunar.get("is_leap_month"))


def test_five_elements_adapter_uses_element_values() -> None:
    """E/F. Five Elements adapter consumes labels/counts, never wuxing_score."""
    pillar = PillarView(stem="Bính", branch="Tuất")
    analysis = AnalysisResult(
        bazi=BaziView(
            year_pillar=pillar,
            month_pillar=pillar,
            day_pillar=pillar,
            hour_pillar=pillar,
            day_master="Bính",
            day_master_element="Hỏa",
            day_master_yin_yang="Dương",
        )
    )
    analysis.score = ScoreView(
        success=True,
        total_score=61.25,
        strength_score=0.66,
        pattern_score=0.0,
        ten_god_score=100.0,
        wuxing_score=0.0,
        wuxing_series=[
            {"label": "Mộc", "value": 2},
            {"label": "Hỏa", "value": 7},
            {"label": "Thổ", "value": 4},
            {"label": "Kim", "value": 4},
            {"label": "Thủy", "value": 0},
        ],
    )
    report = ReportInputV1Adapter().build(ReportInputV1Source(analysis=analysis))
    assert report.five_elements.wood == 2
    assert report.five_elements.fire == 7
    assert report.five_elements.earth == 4
    assert report.five_elements.metal == 4
    assert report.five_elements.water == 0
    assert report.five_elements.wood != analysis.score.wuxing_score or report.five_elements.fire == 7


def test_luck_sequence_survives_public_api() -> None:
    """G/H. Luck sequence is published and mapped into report cycles."""
    payload = OrchestratorService().analyze(**HUYNH)
    luck = payload["luck"]
    assert luck["available"] is True
    assert len(luck["cycles"]) >= 8
    assert luck["current_cycle"]["gan_zhi"]
    output = _production()
    report = ReportInputV1Adapter().build(output.report_source)
    assert len(report.luck_cycles.cycles) >= 8
    first = report.luck_cycles.cycles[0]
    assert first.start_year
    assert first.summary


def test_production_feng_shui_matches_api() -> None:
    """I. Production Feng Shui matches API Feng Shui."""
    api = OrchestratorService().analyze(**HUYNH)["calendar"]
    production = _production().calendar
    assert production["cung_phi"] == api["cung_phi"] == "Đoài"
    assert production["menh_quai"] == api["menh_quai"] == "Đoài"
    assert production["nhom_trach"] == api["nhom_trach"] == "Tây Tứ Trạch"


def test_ten_gods_customer_model_not_score() -> None:
    """J. Ten Gods customer model uses analytical names, not ten_god_score."""
    payload = OrchestratorService().analyze(**HUYNH)
    visible = payload["ten_gods"]["visible"]
    assert "Tỷ Kiên" in visible or any(name for name in visible)
    assert 100 not in visible
    assert payload["score"]["ten_god_score"] == 100.0
    report = ReportInputV1Adapter().build(_production().report_source)
    assert report.ten_gods.visible
    assert "100" not in report.ten_gods.summary


def test_p0_strength_and_useful_god_unchanged() -> None:
    """K/L. P0 Strength and Useful God/Hỷ/Kỵ remain after P1."""
    payload = OrchestratorService().analyze(**HUYNH)
    assert payload["strength"]["strength_level"] == "strong"
    assert abs(float(payload["strength"]["strength_score"]) - 0.66) < 0.01
    assert payload["pattern"]["than_vuong_nhuoc"] == "Thân vượng"
    assert payload["pattern"]["cach_cuc"] == "Chính Tài"
    useful = payload["useful_god"]
    assert useful["useful_god"] == "Đinh"
    assert useful["favorable_gods"] == ["Đinh", "Bính", "Ất"]
    assert useful["unfavorable_gods"] == ["Canh", "Tân"]
    assert "sea_004" in useful["matched_rules"]
    assert payload["pattern"]["hy_than"] == "Đinh, Bính, Ất"
    assert payload["pattern"]["ky_than"] == "Canh, Tân"


def test_five_elements_payload_from_wuxing_counts() -> None:
    """Five Elements fact builder keeps raw counts and ignores score."""
    payload = build_five_elements_payload(
        {
            "counts": {"wood": 2, "fire": 7, "earth": 4, "metal": 4, "water": 0},
            "wood": {"status": "STRONG", "count": 2},
            "fire": {"status": "EXCESS", "count": 7},
            "earth": {"status": "EXCESS", "count": 4},
            "metal": {"status": "EXCESS", "count": 4},
            "water": {"status": "MISSING", "count": 0},
            "status": "EXCESS",
        }
    )
    assert payload["counts"]["fire"] == 7
    assert payload["water"]["count"] == 0
    assert payload["dominant"] == "fire"
    assert "water" in payload["missing"]


def test_luck_shaper_reads_current_dayun_sequence() -> None:
    """Luck shaper reads engine sequence, not metadata.dayun_periods."""
    shaped = shape_luck_payload(
        {
            "available": True,
            "current_dayun": {
                "index": 5,
                "start_age": 55,
                "end_age": 64,
                "start_year": 2021,
                "end_year": 2030,
                "heavenly_stem": "Quý",
                "earthly_branch": "Mão",
                "ganzhi": "Quý Mão",
                "metadata": {
                    "direction": "forward",
                    "sequence": [
                        {
                            "index": 0,
                            "start_age": 5,
                            "end_age": 14,
                            "start_year": 1971,
                            "end_year": 1980,
                            "heavenly_stem": "Mậu",
                            "earthly_branch": "Tuất",
                            "ganzhi": "Mậu Tuất",
                        }
                    ],
                },
            },
        }
    )
    assert shaped["direction"] == "forward"
    assert shaped["start_age"] == 5
    assert shaped["cycles"][0]["gan_zhi"] == "Mậu Tuất"
    assert shaped["current_cycle"]["gan_zhi"] == "Quý Mão"


def _production():
    return ProductionEngineRunner().run(
        ProductionRequest(
            year=1966,
            month=9,
            day=24,
            hour=4,
            minute=15,
            gender="male",
            full_name="Lương Ngọc Huỳnh",
            birth_place="Hà Nội, Việt Nam",
        )
    )
