"""GD-CAL-01B: /good-date visible month stays on lunar month Can Chi.

Does not change BaZi Jie Qi month-pillar rules or Tiểu Lục Nhâm.
"""

from __future__ import annotations

import inspect
from pathlib import Path

from engines.bazi_engine.engine import BaziEngine
from engines.date_selection.constants import BRANCH_INDEX
from engines.date_selection.identity import good_date_identity_payloads
from engines.date_selection.liu_ren import day_value
from engines.date_selection.service import DateSelectionService

REPO = Path(__file__).resolve().parents[2]
JS = REPO / "applications" / "customer_portal" / "static" / "js" / "date_selection.js"
TSX = (
    REPO
    / "applications"
    / "customer_portal"
    / "src"
    / "features"
    / "date_selection"
    / "components.tsx"
)
HTML = REPO / "applications" / "customer_portal" / "templates" / "good_date.html"
LIU_REN = REPO / "engines" / "date_selection" / "liu_ren.py"
IDENTITY = REPO / "engines" / "date_selection" / "identity.py"

VISIBLE_MONTH_CASES = (
    (2026, 9, 6, "Bính Thân"),
    (2026, 9, 7, "Bính Thân"),
    (2026, 10, 7, "Đinh Dậu"),
    (2026, 10, 8, "Đinh Dậu"),
    (2026, 11, 6, "Mậu Tuất"),
    (2026, 11, 7, "Mậu Tuất"),
)

SOLAR_TERM_PAIRS = (
    ((2026, 9, 6), (2026, 9, 7)),
    ((2026, 10, 7), (2026, 10, 8)),
    ((2026, 11, 6), (2026, 11, 7)),
)


def _payload(year: int, month: int, day: int) -> dict:
    return DateSelectionService().inspect_day(year, month, day).to_dict()


def _visible_month(payload: dict) -> str:
    identity = payload["good_date_identity"]
    good_date_visible_month_can_chi = identity["month_can_chi"]
    lunar = payload["calendar"]["lunar_month_can_chi"]
    assert good_date_visible_month_can_chi == lunar
    return good_date_visible_month_can_chi


def test_gd_cal_01b_visible_month_stays_on_lunar_across_jie_qi() -> None:
    for year, month, day, expected in VISIBLE_MONTH_CASES:
        payload = _payload(year, month, day)
        visible = _visible_month(payload)
        assert visible == expected, f"{day:02d}/{month:02d}/{year}: {visible!r} != {expected!r}"
        assert payload["lunar_month_ganzhi"] == expected
        assert payload["good_date_identity"]["month"]["can_chi"] == expected
        assert payload["good_date_identity"]["month"]["ganzhi_system"] == "lunar_calendar"


def test_gd_cal_01b_internal_bazi_month_may_differ() -> None:
    engine = BaziEngine()
    for before, after in SOLAR_TERM_PAIRS:
        left = _payload(*before)
        right = _payload(*after)
        assert _visible_month(left) == _visible_month(right)
        left_bazi = left["bazi"]["month_pillar"]
        right_bazi = right["bazi"]["month_pillar"]
        assert left["month"]["can_chi"] == left_bazi
        assert right["month"]["can_chi"] == right_bazi
        chart_right = engine.build(after[0], after[1], after[2], 12, 0)
        assert right_bazi == f"{chart_right.month_pillar.stem} {chart_right.month_pillar.branch}"
        assert right_bazi != _visible_month(right)


def test_gd_cal_01b_ui_equality_visible_month_is_lunar_month() -> None:
    for year, month, day, expected in VISIBLE_MONTH_CASES:
        payload = _payload(year, month, day)
        good_date_visible_month_can_chi = payload["good_date_identity"]["month_can_chi"]
        assert good_date_visible_month_can_chi == payload["calendar"]["lunar_month_can_chi"]
        assert good_date_visible_month_can_chi == expected


def test_gd_cal_01b_oct_liu_ren_results_unchanged() -> None:
    oct7 = _payload(2026, 10, 7)
    oct8 = _payload(2026, 10, 8)
    assert oct7["six_state"]["label"] == "Không Vong"
    assert oct8["six_state"]["label"] == "Đại An"
    cal7 = oct7["calendar"]
    cal8 = oct8["calendar"]
    assert oct7["day_value"] == day_value(
        BRANCH_INDEX[cal7["year_branch"]],
        cal7["lunar_month"],
        cal7["lunar_day"],
    )
    assert oct8["day_value"] == day_value(
        BRANCH_INDEX[cal8["year_branch"]],
        cal8["lunar_month"],
        cal8["lunar_day"],
    )


def test_gd_cal_01b_tieu_luc_nham_formula_frozen() -> None:
    source = inspect.getsource(day_value)
    assert "return int(year_branch_index) + int(lunar_month) + int(lunar_day)" in source
    assert "month_pillar" not in source
    assert "month_ganzhi" not in LIU_REN.read_text(encoding="utf-8")
    identity_src = IDENTITY.read_text(encoding="utf-8")
    assert "lunar_month_ganzhi" in identity_src
    assert "month_can_chi = (getattr(calendar, \"lunar_month_ganzhi\"" in identity_src


def test_gd_cal_01b_presentation_binds_identity_not_bazi_month() -> None:
    js = JS.read_text(encoding="utf-8")
    tsx = TSX.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8")
    assert "good_date_identity" in js
    assert "identity.month || { can_chi: lunarMonthGanzhi(day) }" in js
    assert "tuTruPillar(day && day.month)" not in js
    assert "cal.month_ganzhi" not in js
    assert "CAN CHI NGÀY" in js
    assert "CAN CHI NGÀY" in tsx
    assert "title: \"CAN CHI NGÀY\"" in tsx
    assert "tu-tru-month-note" not in tsx
    assert "Trụ tháng theo tiết khí" not in js
    assert "Trụ tháng theo tiết khí" not in tsx
    assert "dsTuTruNote" not in html
    assert good_date_identity_payloads is not None
