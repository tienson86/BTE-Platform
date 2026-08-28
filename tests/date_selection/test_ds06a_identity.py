"""DS-06A view-model identity fields and layout contracts.

Does not change six-state, hour convention, or Hạ Nguyên lookup.
"""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from applications.api.app import create_app as create_api_app
from applications.customer_portal.app import create_app as create_portal_app
from engines.date_selection.cung_phi import trach_for_date_ganzhi
from engines.date_selection.identity import hoa_giap_view, nayin_for_ganzhi
from engines.date_selection.service import DateSelectionService

REPO = Path(__file__).resolve().parents[2]
CSS = REPO / "applications" / "customer_portal" / "static" / "css" / "date_selection.css"
GOOD_DATE = REPO / "applications" / "customer_portal" / "templates" / "good_date.html"


def test_mau_thin_nayin_is_wood_not_cung_element() -> None:
    name, menh = nayin_for_ganzhi("Mậu Thìn")
    trach = trach_for_date_ganzhi("Mậu Thìn")
    view = hoa_giap_view("Mậu Thìn", trach)
    assert "Mộc" in name or menh == "Mộc"
    assert view["nayin"] == "Mộc"
    assert view["nayin_element"] == "Mộc"
    assert view["cung"] == "Chấn"
    assert view["cung_element"] == "Mộc"
    assert view["trach_group_label"] == "Đông Tứ Trạch"


def test_canh_thin_nayin_differs_from_hanh_cung() -> None:
    view = hoa_giap_view("Canh Thìn", trach_for_date_ganzhi("Canh Thìn"))
    assert view["nayin"] == "Kim"
    assert view["cung"] == "Ly"
    assert view["cung_element"] == "Hỏa"
    assert view["nayin"] != view["cung_element"]
    assert view["trach_group_label"] == "Đông Tứ Trạch"


def test_day_payload_exposes_canonical_identity_fields() -> None:
    day = DateSelectionService().inspect_day(2026, 8, 27)
    payload = day.to_dict()
    assert payload["calendar"]["month_ganzhi"] == "Bính Thân"
    assert payload["month_ganzhi"] == "Bính Thân"
    assert payload["ganzhi"] == "Quý Dậu"
    assert payload["nayin"] == "Kim"
    assert payload["nayin_element"] == "Kim"
    assert payload["cung"] == "Đoài"
    assert payload["cung_element"] == "Kim"
    assert payload["trach_group_label"] == "Tây Tứ Trạch"
    hour = next(item for item in payload["hours"] if item["window"]["branch"] == "Thìn")
    assert hour["ganzhi"] == "Bính Thìn"
    assert hour["nayin"] == "Thổ"
    assert hour["cung"] == "Ly"
    assert hour["cung_element"] == "Hỏa"
    assert hour["nayin"] != hour["cung_element"]


def test_calculations_and_routes_unchanged() -> None:
    day = DateSelectionService().inspect_day(2026, 8, 27)
    assert day.six_state.label == "Tiểu Cát"
    thin = next(item for item in day.hours if item.window.branch == "Thìn")
    assert thin.six_state.label == "Xích Khẩu"
    assert thin.window.time_range == "07:01–09:00"
    portal = TestClient(create_portal_app())
    assert portal.get("/good-date").status_code == 200
    assert portal.get("/choose-date").status_code == 200
    api = TestClient(create_api_app())
    body = api.post(
        "/api/v1/date-selection/day",
        json={"year": 2026, "month": 8, "day": 27, "hour_branch": "Thìn"},
    ).json()["data"]
    assert body["month_ganzhi"] == "Bính Thân"
    assert body["nayin"] == "Kim"
    assert body["cung_element"] == "Kim"
    assert body["selected_hour"]["nayin"] == "Thổ"
    assert body["selected_hour"]["cung_element"] == "Hỏa"


def test_layout_clock_below_calendar_and_right_column_order() -> None:
    html = GOOD_DATE.read_text(encoding="utf-8")
    left = html.find('data-ds-col="left"')
    right = html.find('data-ds-col="right"')
    assert 0 <= left < right
    assert html.find("ds-calendar-card") < html.find("ds-clock-card")
    right_html = html[right:]
    assert right_html.find("ds-detail") < right_html.find("ds-hour") < right_html.find("ds-ke")
    css = CSS.read_text(encoding="utf-8")
    assert "display: contents" in css
    assert ".ds-calendar-card { order: 1; }" in css
    assert ".ds-detail { order: 2; }" in css
    assert ".ds-clock-card { order: 3; }" in css
    assert ".ds-hour { order: 4; }" in css
    assert ".ds-ke { order: 5; }" in css
    page = TestClient(create_portal_app()).get("/good-date")
    assert page.status_code == 200
    text = page.text
    assert "ds-left" in text and "ds-right" in text
    assert text.find("ds-calendar-card") < text.find("ds-clock-card")
