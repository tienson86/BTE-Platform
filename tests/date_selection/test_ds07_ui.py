"""DS-07 commercial layout polish — presentation only.

Does not change ranking, Calendar, Ganzhi, Hạ Nguyên, or khắc arithmetic.
"""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from applications.api.app import create_app as create_api_app
from applications.customer_portal.app import create_app as create_portal_app
from engines.date_selection.ranking import rank_dates
from engines.date_selection.service import DateSelectionService
from tests.date_selection.test_ds06c_evidence import _day

REPO = Path(__file__).resolve().parents[2]
JS = REPO / "applications" / "customer_portal" / "static" / "js" / "date_selection.js"
CSS = REPO / "applications" / "customer_portal" / "static" / "css" / "date_selection.css"
HTML = REPO / "applications" / "customer_portal" / "templates" / "choose_date.html"
TSX = (
    REPO
    / "applications"
    / "customer_portal"
    / "src"
    / "features"
    / "date_selection"
    / "components.tsx"
)


def test_gender_is_radio_not_combobox() -> None:
    html = HTML.read_text(encoding="utf-8")
    assert 'type="radio"' in html
    assert 'name="gender"' in html
    assert 'value="male" checked' in html
    assert 'value="female"' in html
    assert "<select" not in html
    portal = TestClient(create_portal_app())
    page = portal.get("/choose-date")
    assert page.status_code == 200
    assert 'type="radio"' in page.text
    assert 'select id="dsGender"' not in page.text


def test_two_column_desktop_search_row() -> None:
    html = HTML.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    tsx = TSX.read_text(encoding="utf-8")
    assert 'class="ds-search-row"' in html
    assert "ds-search-row" in tsx
    assert "minmax(0, 1.15fr) minmax(0, 0.85fr)" in css
    assert "@media (min-width: 1024px)" in css


def test_responsive_stacking_rules() -> None:
    css = CSS.read_text(encoding="utf-8")
    assert "@media (max-width: 1023px)" in css
    assert "@media (max-width: 767px)" in css
    assert ".ds-search-row { grid-template-columns: 1fr; }" in css
    assert ".ds-form-grid { grid-template-columns: 1fr; }" in css


def test_no_duplicate_trach_confirmation() -> None:
    js = JS.read_text(encoding="utf-8")
    tsx = TSX.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8")
    assert "✓ Phù hợp Nhóm Trạch của bạn" not in js
    assert "✓ Phù hợp Nhóm Trạch của bạn" not in tsx
    assert 'data-testid="trach-match"' not in js
    assert 'data-testid="trach-match"' not in tsx
    assert "Giờ phù hợp Nhóm Trạch của bạn" in js or "date_selection.compatible_hours" in js
    assert "Giờ phù hợp Nhóm Trạch của bạn" in tsx
    assert "Kết quả giờ" not in html


def test_cung_and_hour_row_presentation() -> None:
    js = JS.read_text(encoding="utf-8")
    tsx = TSX.read_text(encoding="utf-8")
    assert "cungWithElement" in js
    assert "hour.cung_element" in js
    assert "hourRowLabel" in tsx
    assert "cung_element" in tsx


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


def test_calculations_unchanged() -> None:
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
