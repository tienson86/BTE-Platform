"""DS-06D presentation alignment: hour identity only, six-state on day/khắc.

Does not change ranking, six-state arithmetic, or Hạ Nguyên mapping.
"""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from applications.api.app import create_app as create_api_app
from applications.customer_portal.app import create_app as create_portal_app
from engines.date_selection.service import DateSelectionService
from tests.date_selection.test_ds06c_evidence import _day
from engines.date_selection.ranking import rank_dates

REPO = Path(__file__).resolve().parents[2]
JS = REPO / "applications" / "customer_portal" / "static" / "js" / "date_selection.js"
I18N = REPO / "applications" / "customer_portal" / "static" / "i18n" / "vi.json"
GOOD_DATE = REPO / "applications" / "customer_portal" / "templates" / "good_date.html"
COMPONENTS = (
    REPO
    / "applications"
    / "customer_portal"
    / "src"
    / "features"
    / "date_selection"
    / "components.tsx"
)


def test_ui_no_longer_renders_ket_qua_gio() -> None:
    js = JS.read_text(encoding="utf-8")
    tsx = COMPONENTS.read_text(encoding="utf-8")
    i18n = I18N.read_text(encoding="utf-8")
    assert "Kết quả giờ" not in js
    assert "Kết quả giờ" not in tsx
    assert '"hour_result"' not in i18n
    assert "hour.six_state.label" not in js


def test_good_date_contains_no_hour_result_field() -> None:
    html = GOOD_DATE.read_text(encoding="utf-8")
    assert "Kết quả giờ" not in html
    portal = TestClient(create_portal_app())
    page = portal.get("/good-date")
    assert page.status_code == 200
    assert "Kết quả giờ" not in page.text
    assert "dsHourDetail" in page.text
    assert "dsKeList" in page.text


def test_choose_date_contains_no_hour_result_field() -> None:
    portal = TestClient(create_portal_app())
    page = portal.get("/choose-date")
    assert page.status_code == 200
    assert "Kết quả giờ" not in page.text
    js = JS.read_text(encoding="utf-8")
    assert "date_selection.hour_result" not in js
    assert "primary.hour_result" not in js


def test_recommendation_payload_omits_hour_result() -> None:
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
        day_label = item["day"]["six_state"]["label"]
        assert day_label
        for rec in item["recommendations"]:
            assert "hour_result" not in rec
            assert rec["ganzhi"]
            assert rec["nayin"]
            assert rec["cung"]
            assert rec["cung_element"]
            assert rec["trach_group"]
            assert rec["recommended_ke"]["result"]
            assert rec["recommended_ke"]["time_range"]


def test_hour_identity_labels_remain() -> None:
    js = JS.read_text(encoding="utf-8")
    tsx = COMPONENTS.read_text(encoding="utf-8")
    for key in (
        "date_selection.hour_ganzhi",
        "date_selection.nayin_hour",
        "date_selection.cung_phi_hour",
        "date_selection.hanh_cung_hour",
        "date_selection.trach_group_hour",
    ):
        assert key in js
    for label in (
        "Can Chi giờ",
        "Nạp âm giờ",
        "Cung Phi giờ",
        "Hành Cung giờ",
        "Nhóm Trạch giờ",
    ):
        assert label in tsx


def test_recommendation_wording() -> None:
    js = JS.read_text(encoding="utf-8")
    i18n = I18N.read_text(encoding="utf-8")
    tsx = COMPONENTS.read_text(encoding="utf-8")
    assert "Giờ phù hợp Nhóm Trạch của bạn" in js or "date_selection.compatible_hours" in js
    assert "Các thời điểm đẹp" in js
    assert "Các thời điểm đẹp" in i18n
    assert "Các thời điểm đẹp" in tsx
    assert "Giờ đề xuất" not in js
    assert "Giờ đề xuất" not in tsx
    assert "Kết quả giờ" not in js
    assert "Kết quả giờ" not in tsx


def test_ranking_unchanged() -> None:
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


def test_calendar_arithmetic_unchanged() -> None:
    day = DateSelectionService().inspect_day(2026, 8, 27)
    assert day.calendar.day_ganzhi == "Quý Dậu"
    assert day.calendar.month_ganzhi == "Bính Thân"
    assert day.six_state.label == "Tiểu Cát"
    thin = next(item for item in day.hours if item.window.branch == "Thìn")
    assert thin.window.time_range == "07:01–09:00"
    assert thin.six_state.label == "Xích Khẩu"
    assert thin.ke_slots[0].six_state.label == "Tiểu Cát"


def test_date_selection_regression_green() -> None:
    api = TestClient(create_api_app())
    body = api.post(
        "/api/v1/date-selection/day",
        json={"year": 2026, "month": 8, "day": 27, "hour_branch": "Thìn"},
    ).json()["data"]
    assert body["calendar"]["day_ganzhi"] == "Quý Dậu"
    assert body["six_state"]["label"] == "Tiểu Cát"
    assert body["selected_hour"]["window"]["branch"] == "Thìn"
    portal = TestClient(create_portal_app())
    assert portal.get("/good-date").status_code == 200
    assert portal.get("/choose-date").status_code == 200
