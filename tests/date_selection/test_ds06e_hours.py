"""DS-06E: all matching-Trạch hours and complete positive khắc.

Day ranking is unchanged. Hour/khắc collection no longer truncates to four Đại An slots.
"""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from applications.api.app import create_app as create_api_app
from applications.customer_portal.app import create_app as create_portal_app
from engines.date_selection.models import (
    DaySelection,
    HourRecommendation,
    RankedDate,
)
from engines.date_selection.ranking import rank_dates
from engines.date_selection.service import DateSelectionService
from engines.date_selection.trach import trach_from_cung
from tests.date_selection.test_ds06c_evidence import _day

REPO = Path(__file__).resolve().parents[2]
JS = REPO / "applications" / "customer_portal" / "static" / "js" / "date_selection.js"
NEGATIVE_KE = {"Lưu Niên", "Lưu Liên", "Xích Khẩu", "Không Vong"}
POSITIVE_KE = {"Đại An", "Tốc Hỷ", "Tiểu Cát"}


def test_west_person_receives_all_west_hours() -> None:
    source = DateSelectionService().inspect_day(2026, 9, 4)
    day = DaySelection(
        calendar=source.calendar,
        day_value=source.day_value,
        six_state=source.six_state,
        trach=trach_from_cung("Cấn"),
        hours=source.hours,
    )
    hours = RankedDate(
        day=day,
        recommendations=[HourRecommendation("Dần", "03:01–03:20", 1, "Đại An", False)],
    ).to_dict()["compatible_hours"]
    expected = [
        hour.window.branch
        for hour in source.hours
        if hour.trach and hour.trach.trach_group_code == "tay"
    ]
    assert [item["branch"] for item in hours] == expected
    assert expected
    assert all(item["trach_group"] == "tay" for item in hours)


def test_east_person_receives_all_east_hours() -> None:
    source = DateSelectionService().inspect_day(2026, 9, 4)
    day = DaySelection(
        calendar=source.calendar,
        day_value=source.day_value,
        six_state=source.six_state,
        trach=trach_from_cung("Ly"),
        hours=source.hours,
    )
    hours = RankedDate(
        day=day,
        recommendations=[HourRecommendation("Mão", "05:01–05:20", 1, "Đại An", False)],
    ).to_dict()["compatible_hours"]
    expected = [
        hour.window.branch
        for hour in source.hours
        if hour.trach and hour.trach.trach_group_code == "dong"
    ]
    assert [item["branch"] for item in hours] == expected
    assert expected
    assert all(item["trach_group"] == "dong" for item in hours)


def test_opposite_group_hours_never_listed() -> None:
    result = DateSelectionService().search(
        full_name="Nguyễn Tiến Sơn",
        gender="male",
        birth_year=1987,
        birth_month=1,
        birth_day=21,
        target_year=2026,
        target_month=9,
    )
    person_group = result.person.trach.trach_group_code
    payload = result.to_dict()
    for item in payload["dates"]:
        for hour in item["compatible_hours"]:
            assert hour["trach_group"] == person_group


def test_positive_ke_contains_all_three_classes() -> None:
    result = DateSelectionService().search(
        full_name="Nguyễn Tiến Sơn",
        gender="male",
        birth_year=1987,
        birth_month=1,
        birth_day=21,
        target_year=2026,
        target_month=9,
    )
    payload = result.to_dict()
    labels: set[str] = set()
    for item in payload["dates"]:
        for hour in item["compatible_hours"]:
            for ke in hour["positive_ke"]:
                labels.add(ke["result"])
    assert "Đại An" in labels
    assert "Tốc Hỷ" in labels
    assert "Tiểu Cát" in labels


def test_positive_ke_never_contains_negatives() -> None:
    result = DateSelectionService().search(
        full_name="Nguyễn Tiến Sơn",
        gender="male",
        birth_year=1987,
        birth_month=1,
        birth_day=21,
        target_year=2026,
        target_month=9,
    )
    payload = result.to_dict()
    for item in payload["dates"]:
        for hour in item["compatible_hours"]:
            for ke in hour["positive_ke"]:
                assert ke["result"] in POSITIVE_KE
                assert ke["result"] not in NEGATIVE_KE


def test_compatible_hour_canonical_metadata() -> None:
    result = DateSelectionService().search(
        full_name="Nguyễn Tiến Sơn",
        gender="male",
        birth_year=1987,
        birth_month=1,
        birth_day=21,
        target_year=2026,
        target_month=9,
    )
    payload = result.to_dict()
    assert payload["dates"]
    for item in payload["dates"]:
        hours = item["compatible_hours"]
        inspect = DateSelectionService().inspect_day(
            2026,
            9,
            item["day"]["calendar"]["solar_day"],
        )
        expected = [
            hour.window.branch
            for hour in inspect.hours
            if hour.trach and hour.trach.trach_group_code == result.person.trach.trach_group_code
        ]
        assert [hour["branch"] for hour in hours] == expected
        for hour in hours:
            assert hour["branch"]
            assert hour["full_time_range"]
            assert hour["ganzhi"]
            assert hour["cung"]
            assert hour["cung_element"]
            assert hour["trach_group"]
            assert hour["nayin"]
            assert "hour_result" not in hour


def test_no_hour_result_in_choose_date() -> None:
    js = JS.read_text(encoding="utf-8")
    assert "Kết quả giờ" not in js
    assert "Thời điểm đẹp nhất" not in js
    portal = TestClient(create_portal_app())
    page = portal.get("/choose-date")
    assert page.status_code == 200
    assert "Kết quả giờ" not in page.text


def test_day_ranking_unchanged() -> None:
    days = [
        _day(1, "Đoài", 1, ke_code="dai_an"),
        _day(2, "Đoài", 5, ke_code="tieu_cat"),
        _day(3, "Đoài", 3, ke_code="toc_hy"),
        _day(4, "Đoài", 1, ke_code="dai_an"),
        _day(5, "Khảm", 1, ke_code="dai_an"),
        _day(6, "Đoài", 4, ke_code="dai_an"),
        _day(7, "Đoài", 0, ke_code="dai_an"),
        _day(8, "Đoài", 5, ke_code="xich_khau"),
    ]
    ranked = rank_dates(days, "tay")
    assert [item.day.calendar.solar_day for item in ranked] == [1, 2, 3, 4]


def test_good_date_and_arithmetic_regression() -> None:
    day = DateSelectionService().inspect_day(2026, 8, 27)
    assert day.calendar.day_ganzhi == "Quý Dậu"
    assert day.six_state.label == "Tiểu Cát"
    thin = next(item for item in day.hours if item.window.branch == "Thìn")
    assert thin.window.time_range == "07:01–09:00"
    api = TestClient(create_api_app())
    body = api.post(
        "/api/v1/date-selection/day",
        json={"year": 2026, "month": 8, "day": 27, "hour_branch": "Thìn"},
    ).json()["data"]
    assert body["calendar"]["day_ganzhi"] == "Quý Dậu"
    portal = TestClient(create_portal_app())
    assert portal.get("/good-date").status_code == 200
    assert portal.get("/choose-date").status_code == 200
