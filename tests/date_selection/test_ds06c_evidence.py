"""DS-06C recommended date/hour evidence view-model.

Does not change ranking selection, Hạ Nguyên mapping, or /good-date arithmetic.
"""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from applications.api.app import create_app as create_api_app
from applications.customer_portal.app import create_app as create_portal_app
from engines.date_selection.cung_phi import trach_for_date_ganzhi
from engines.date_selection.exceptions import DateSelectionError
from engines.date_selection.hour import window_for_branch
from engines.date_selection.identity import hoa_giap_view
from engines.date_selection.liu_ren import six_state_from_value
from engines.date_selection.models import (
    CalendarSnapshot,
    DaySelection,
    HourRecommendation,
    HourSelection,
    KeSlot,
    RankedDate,
    SearchResult,
)
from engines.date_selection.ranking import rank_dates
from engines.date_selection.service import DateSelectionService
from engines.date_selection.trach import trach_from_cung

REPO = Path(__file__).resolve().parents[2]
JS = REPO / "applications" / "customer_portal" / "static" / "js" / "date_selection.js"
CSS = REPO / "applications" / "customer_portal" / "static" / "css" / "date_selection.css"
GOOD_DATE = REPO / "applications" / "customer_portal" / "templates" / "good_date.html"


def _snapshot(day: int, ganzhi: str = "Tân Tỵ") -> CalendarSnapshot:
    return CalendarSnapshot(
        solar_year=2026,
        solar_month=9,
        solar_day=day,
        solar_label=f"{day:02d}/09/2026",
        lunar_year=2026,
        lunar_month=7,
        lunar_day=day,
        lunar_leap=False,
        lunar_label=f"{day:02d}/07/2026",
        year_ganzhi="Bính Ngọ",
        month_ganzhi="Giáp Thân",
        day_ganzhi=ganzhi,
        year_branch="Ngọ",
        weekday=1,
    )


def _hour(cung: str, ke_code: str, branch: str = "Tỵ", ganzhi: str = "Canh Tỵ") -> HourSelection:
    window = window_for_branch(branch)
    return HourSelection(
        window=window,
        ganzhi=ganzhi,
        hour_value=10,
        six_state=six_state_from_value(5),
        trach=trach_from_cung(cung),
        ke_slots=[
            KeSlot(
                ke_index=1,
                time_range="09:00–09:19" if branch == "Tỵ" else "03:01–03:20",
                start_minute_of_day=540,
                six_state=six_state_from_value(
                    {
                        "dai_an": 1,
                        "toc_hy": 3,
                        "tieu_cat": 5,
                        "luu_lien": 2,
                        "xich_khau": 4,
                        "khong_vong": 0,
                    }[ke_code]
                ),
            )
        ],
    )


def _day(
    solar_day: int,
    cung: str,
    remainder: int,
    ke_code: str = "dai_an",
    hour_cung: str | None = None,
) -> DaySelection:
    label = six_state_from_value(remainder)
    return DaySelection(
        calendar=_snapshot(solar_day),
        day_value=remainder,
        six_state=label,
        trach=trach_from_cung(cung),
        hours=[_hour(hour_cung or cung, ke_code)],
    )


def test_mau_dan_canonical_hour_metadata() -> None:
    trach = trach_for_date_ganzhi("Mậu Dần")
    view = hoa_giap_view("Mậu Dần", trach)
    assert view["ganzhi"] == "Mậu Dần"
    assert view["nayin"] == "Thổ"
    assert view["cung"] == "Khôn"
    assert view["cung_element"] == "Thổ"
    assert view["trach_group"] == "tay"
    assert view["trach_group_label"] == "Tây Tứ Trạch"
    assert view["nayin"] != "Ngũ hành"
    assert view["cung_element"] != view["cung"]


def test_ranked_payload_exposes_day_and_hour_evidence() -> None:
    hour = _hour("Khôn", "dai_an", branch="Dần", ganzhi="Mậu Dần")
    day = DaySelection(
        calendar=_snapshot(4, "Tân Tỵ"),
        day_value=1,
        six_state=six_state_from_value(1),
        trach=trach_from_cung("Cấn"),
        hours=[hour],
    )
    ranked = RankedDate(
        day=day,
        recommendations=[
            HourRecommendation(
                branch="Dần",
                time_range="03:01–03:20",
                ke_index=1,
                classification="Đại An",
                primary=True,
            )
        ],
    )
    payload = ranked.to_dict()
    card = payload["day"]
    assert card["calendar"]["year_ganzhi"] == "Bính Ngọ"
    assert card["calendar"]["month_ganzhi"] == "Giáp Thân"
    assert card["calendar"]["day_ganzhi"] == "Tân Tỵ"
    assert card["nayin"]
    assert card["cung"]
    assert card["cung_element"]
    assert card["trach_group_label"]
    rec = payload["recommendations"][0]
    assert rec["branch"] == "Dần"
    assert rec["full_time_range"] == hour.window.time_range
    assert rec["ganzhi"] == "Mậu Dần"
    assert rec["hour_result"]
    assert rec["nayin"] == "Thổ"
    assert rec["cung"] == "Khôn"
    assert rec["cung_element"] == "Thổ"
    assert rec["trach_group"] == "tay"
    assert rec["trach_group_label"] == "Tây Tứ Trạch"
    assert rec["ke_result"] == "Đại An"
    assert rec["recommended_ke"]["result"] == "Đại An"
    assert rec["recommended_ke"]["time_range"] == "03:01–03:20"
    blob = str(payload)
    assert "Ngũ hành" not in blob


def test_search_same_trach_assertion_and_fields() -> None:
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
    assert payload["person"]["trach_group"] == person_group
    assert payload["dates"]
    assert len(payload["dates"]) <= 5
    for item in payload["dates"]:
        assert item["day"]["trach_group"] == person_group
        assert item["day"]["calendar"]["year_ganzhi"]
        assert item["day"]["calendar"]["month_ganzhi"]
        assert item["day"]["calendar"]["day_ganzhi"]
        assert item["day"]["nayin"]
        assert item["day"]["cung"]
        assert item["day"]["cung_element"]
        assert item["day"]["trach_group_label"]
        assert item["recommendations"]
        primary = item["recommendations"][0]
        assert primary["branch"]
        assert primary["ganzhi"]
        assert primary["nayin"]
        assert primary["cung"]
        assert primary["cung_element"]
        assert primary["trach_group"] == person_group
        assert primary["ke_result"] or primary["classification"]
        for rec in item["recommendations"]:
            assert rec["trach_group"] == person_group
    assert "Ngũ hành" not in str(payload)


def test_west_person_east_hour_never_recommended() -> None:
    day = _day(1, "Đoài", 1, hour_cung="Khảm")
    ranked = rank_dates([day], "tay")
    assert ranked == []


def test_east_person_west_hour_never_recommended() -> None:
    day = _day(1, "Khảm", 1, hour_cung="Đoài")
    ranked = rank_dates([day], "dong")
    assert ranked == []


def test_top5_ranking_unchanged() -> None:
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
    assert [item.day.six_state.code for item in ranked] == [
        "dai_an",
        "tieu_cat",
        "toc_hy",
        "dai_an",
    ]


def test_good_date_regression_unchanged() -> None:
    day = DateSelectionService().inspect_day(2026, 8, 27)
    payload = day.to_dict()
    assert payload["calendar"]["year_ganzhi"] == "Bính Ngọ"
    assert payload["calendar"]["month_ganzhi"] == "Giáp Thân"
    assert payload["calendar"]["day_ganzhi"] == "Quý Dậu"
    assert payload["six_state"]["label"] == "Tiểu Cát"
    assert payload["nayin"] == "Kim"
    assert payload["cung"] == "Đoài"
    assert payload["cung_element"] == "Kim"
    html = GOOD_DATE.read_text(encoding="utf-8")
    assert "ds-detail" in html
    assert "data-ds-col" in html
    portal = TestClient(create_portal_app())
    page = portal.get("/good-date")
    assert page.status_code == 200
    assert "ds-calendar-card" in page.text
    api = TestClient(create_api_app())
    body = api.post(
        "/api/v1/date-selection/day",
        json={"year": 2026, "month": 8, "day": 27, "hour_branch": "Thìn"},
    ).json()["data"]
    assert body["calendar"]["day_ganzhi"] == "Quý Dậu"
    assert body["six_state"]["label"] == "Tiểu Cát"


def test_choose_date_ui_source_has_evidence_labels() -> None:
    js = JS.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    assert "date_selection.year_ganzhi" in js
    assert "date_selection.month_ganzhi" in js
    assert "date_selection.nayin_hour" in js
    assert "date_selection.cung_phi_hour" in js
    assert "date_selection.trach_group_hour" in js
    assert "date_selection.best_ke" in js
    assert "date_selection.other_good_windows" in js
    assert "trach-match" in js
    assert "Ngũ hành" not in js
    assert "ds-hour-block" in css
    assert "grid-template-columns: 1fr" in css
    portal = TestClient(create_portal_app())
    page = portal.get("/choose-date")
    assert page.status_code == 200
    assert "dsResults" in page.text


def test_search_result_rejects_mismatched_hour_at_runtime() -> None:
    person = DateSelectionService().person_profile(
        full_name="A",
        gender="male",
        birth_year=1987,
        birth_month=1,
        birth_day=21,
    )
    opposite = "Khảm" if person.trach.trach_group_code == "tay" else "Đoài"
    day = _day(1, person.trach.cung, 1, hour_cung=opposite)
    bogus = RankedDate(
        day=day,
        recommendations=[
            HourRecommendation(
                branch="Tỵ",
                time_range="09:00–09:19",
                ke_index=1,
                classification="Đại An",
            )
        ],
    )
    result = SearchResult(
        person=person,
        target_year=2026,
        target_month=9,
        dates=[bogus],
    )
    try:
        result.to_dict()
        raised = False
    except DateSelectionError:
        raised = True
    assert raised is True
