"""GD-CAL-01: lunar calendar month vs BaZi solar-term month pillar.

Does not change BaZi Jie Qi month-pillar rules or Calendar lunar Y/M/D truth.
"""

from __future__ import annotations

import inspect
from datetime import date, timedelta
from pathlib import Path

from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.calendar_engine.month_pillar import lunar_month_ganzhi
from engines.calendar_engine.solar_terms.engine import SolarTermEngine
from engines.date_selection.constants import BRANCH_INDEX, SIX_STATE_BY_REMAINDER
from engines.date_selection.liu_ren import day_value, six_state_from_value
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
ADAPTER = REPO / "engines" / "date_selection" / "calendar_adapter.py"
SERVICE = REPO / "engines" / "date_selection" / "service.py"
LIU_REN = REPO / "engines" / "date_selection" / "liu_ren.py"

UI_BINDING_SOURCES = {
    "Ngày dương": "calendar.solar_label",
    "Ngày âm": "calendar.lunar_label",
    "Can Chi năm âm": "calendar.lunar_year_ganzhi (lunar year, not Lập Xuân year pillar)",
    "Can Chi tháng âm": "calendar.lunar_month_ganzhi (lunar month number + lunar year stem)",
    "Can Chi ngày": "calendar.lunar_day_ganzhi / calendar.day_ganzhi",
    "Nạp âm ngày": "hoa_giap_view(day_ganzhi).nayin",
    "Cung Phi ngày": "trach_for_date_ganzhi(day_ganzhi).cung",
    "Hành Cung": "trach.element_label",
    "Nhóm Trạch": "trach.trach_group_label",
    "Kết quả ngày": "liu_ren.day_value(year_branch_index, lunar_month, lunar_day)",
    "CAN CHI NGÀY Năm": "good_date_identity.year_can_chi ← calendar.lunar_year_ganzhi",
    "CAN CHI NGÀY Tháng": "good_date_identity.month_can_chi ← calendar.lunar_month_ganzhi",
    "CAN CHI NGÀY Ngày": "good_date_identity.day_can_chi ← calendar.lunar_day_ganzhi",
}


def _trace(year: int, month: int, day: int) -> dict[str, object]:
    calendar = CalendarEngine().build(year, month, day)
    chart = BaziEngine().build(year, month, day, 12, 0)
    result = DateSelectionService().inspect_day(year, month, day)
    payload = result.to_dict()
    year_branch = result.calendar.year_branch
    year_index = BRANCH_INDEX[year_branch]
    lunar_month = result.calendar.lunar_month
    lunar_day = result.calendar.lunar_day
    total = day_value(year_index, lunar_month, lunar_day)
    remainder = total % 6
    return {
        "gregorian": f"{day:02d}/{month:02d}/{year:04d}",
        "lunar_year": result.calendar.lunar_year,
        "lunar_month": lunar_month,
        "lunar_day": lunar_day,
        "lunar_leap": result.calendar.lunar_leap,
        "lunar_label": result.calendar.lunar_label,
        "lunar_year_can_chi": result.calendar.lunar_year_ganzhi,
        "lunar_month_can_chi": result.calendar.lunar_month_ganzhi,
        "lunar_day_can_chi": result.calendar.lunar_day_ganzhi,
        "bazi_year_pillar": f"{chart.year_pillar.stem} {chart.year_pillar.branch}",
        "bazi_month_pillar": f"{chart.month_pillar.stem} {chart.month_pillar.branch}",
        "bazi_day_pillar": f"{chart.day_pillar.stem} {chart.day_pillar.branch}",
        "calendar_month_can_chi_bazi": calendar.month_can_chi,
        "year_branch": year_branch,
        "year_branch_index": year_index,
        "lunar_month_numeric_input": lunar_month,
        "lunar_day_numeric_input": lunar_day,
        "modulo_expression": f"({year_index} + {lunar_month} + {lunar_day}) % 6 = {remainder}",
        "tieu_luc_nham": result.six_state.label,
        "payload_bazi_month_pillar": payload["bazi"]["month_pillar"],
        "payload_lunar_month_can_chi": payload["calendar"]["lunar_month_can_chi"],
        "ui_binding_sources": UI_BINDING_SOURCES,
    }


def test_gd_cal_01_a_07_oct_2026() -> None:
    """TEST GD-CAL-01-A."""
    result = DateSelectionService().inspect_day(2026, 10, 7)
    payload = result.to_dict()
    assert result.calendar.solar_label == "07/10/2026"
    assert result.calendar.lunar_day == 27
    assert result.calendar.lunar_month == 8
    assert result.calendar.lunar_leap is False
    assert result.calendar.lunar_year_ganzhi == "Bính Ngọ"
    assert result.calendar.lunar_month_ganzhi == "Đinh Dậu"
    assert payload["calendar"]["lunar_month_can_chi"] == "Đinh Dậu"
    assert payload["calendar"]["lunar_date"]["month"] == 8
    assert result.six_state.label == "Không Vong"
    assert result.day_value == 7 + 8 + 27
    assert result.day_value % 6 == 0


def test_gd_cal_01_b_08_oct_2026() -> None:
    """TEST GD-CAL-01-B."""
    result = DateSelectionService().inspect_day(2026, 10, 8)
    payload = result.to_dict()
    assert result.calendar.solar_label == "08/10/2026"
    assert result.calendar.lunar_day == 28
    assert result.calendar.lunar_month == 8
    assert result.calendar.lunar_leap is False
    assert result.calendar.lunar_year_ganzhi == "Bính Ngọ"
    assert result.calendar.lunar_month_ganzhi == "Đinh Dậu"
    assert payload["calendar"]["lunar_month_can_chi"] == "Đinh Dậu"
    assert result.six_state.label == "Đại An"
    assert result.day_value == 7 + 8 + 28
    assert result.day_value % 6 == 1


def test_gd_cal_01_c_han_lo_does_not_switch_lunar_month() -> None:
    """TEST GD-CAL-01-C: Hàn Lộ may switch BaZi month; lunar month stays 8 / Đinh Dậu."""
    before = DateSelectionService().inspect_day(2026, 10, 7)
    after = DateSelectionService().inspect_day(2026, 10, 8)
    assert before.calendar.lunar_month == after.calendar.lunar_month == 8
    assert before.calendar.lunar_month_ganzhi == after.calendar.lunar_month_ganzhi == "Đinh Dậu"
    assert before.to_dict()["bazi"]["month_pillar"] != after.to_dict()["bazi"]["month_pillar"]
    assert before.to_dict()["bazi"]["month_pillar"] == "Đinh Dậu"
    assert after.to_dict()["bazi"]["month_pillar"] == "Mậu Tuất"
    assert before.calendar.month_ganzhi == "Đinh Dậu"
    assert after.calendar.month_ganzhi == "Mậu Tuất"
    assert SolarTermEngine().get_bazi_month(2026, 10, 8).start_term == "Hàn Lộ"


def test_gd_cal_01_d_november_solar_term_vs_lunar() -> None:
    """TEST GD-CAL-01-D: 06/11 and 07/11/2026 lunar continuity vs BaZi month switch."""
    sixth = DateSelectionService().inspect_day(2026, 11, 6)
    seventh = DateSelectionService().inspect_day(2026, 11, 7)
    assert sixth.calendar.lunar_month == seventh.calendar.lunar_month
    assert sixth.calendar.lunar_month_ganzhi == seventh.calendar.lunar_month_ganzhi
    assert sixth.calendar.lunar_year_ganzhi == seventh.calendar.lunar_year_ganzhi
    assert seventh.calendar.lunar_day == sixth.calendar.lunar_day + 1
    assert sixth.to_dict()["bazi"]["month_pillar"] != seventh.to_dict()["bazi"]["month_pillar"]
    assert SolarTermEngine().get_bazi_month(2026, 11, 7).start_term == "Lập Đông"


def test_gd_cal_01_e_full_2026_lunar_month_only_at_lunar_boundaries() -> None:
    """TEST GD-CAL-01-E: lunar month identity never mutates at Jie Qi alone."""
    engine = CalendarEngine()
    service = DateSelectionService()
    cursor = date(2026, 1, 1)
    end = date(2026, 12, 31)
    previous = None
    bazi_switches_with_stable_lunar = 0
    while cursor <= end:
        calendar = engine.build(cursor.year, cursor.month, cursor.day)
        snapshot = service.inspect_day(cursor.year, cursor.month, cursor.day).calendar
        assert snapshot.lunar_year == calendar.lunar_year
        assert snapshot.lunar_month == calendar.lunar_month
        assert snapshot.lunar_day == calendar.lunar_day
        assert snapshot.lunar_leap == bool(calendar.leap_month)
        expected_lunar_month = lunar_month_ganzhi(
            (calendar.lunar_year_can_chi or "").split()[0],
            int(calendar.lunar_month),
        )
        assert snapshot.lunar_month_ganzhi == expected_lunar_month
        assert calendar.lunar_month_can_chi == expected_lunar_month
        assert snapshot.month_ganzhi == calendar.month_can_chi
        if previous is not None:
            lunar_id = (
                snapshot.lunar_year,
                snapshot.lunar_month,
                snapshot.lunar_leap,
            )
            prev_id = (
                previous.lunar_year,
                previous.lunar_month,
                previous.lunar_leap,
            )
            if lunar_id == prev_id:
                assert snapshot.lunar_month_ganzhi == previous.lunar_month_ganzhi
                assert snapshot.lunar_day == previous.lunar_day + 1
            else:
                assert snapshot.lunar_day == 1
                month_delta = snapshot.lunar_month - previous.lunar_month
                if snapshot.lunar_year == previous.lunar_year:
                    assert month_delta in (0, 1)
                    if month_delta == 0:
                        assert snapshot.lunar_leap != previous.lunar_leap
                else:
                    assert snapshot.lunar_year == previous.lunar_year + 1
                    assert snapshot.lunar_month == 1
                    assert previous.lunar_month == 12
            if (
                snapshot.month_ganzhi != previous.month_ganzhi
                and snapshot.lunar_month == previous.lunar_month
                and snapshot.lunar_year == previous.lunar_year
                and snapshot.lunar_leap == previous.lunar_leap
            ):
                bazi_switches_with_stable_lunar += 1
                assert snapshot.lunar_month_ganzhi == previous.lunar_month_ganzhi
        previous = snapshot
        cursor += timedelta(days=1)
    assert bazi_switches_with_stable_lunar >= 1


def test_gd_cal_01_f_tieu_luc_nham_uses_lunar_month_number() -> None:
    """TEST GD-CAL-01-F: published six-state equals frozen lunar formula every day."""
    service = DateSelectionService()
    cursor = date(2026, 1, 1)
    end = date(2026, 12, 31)
    while cursor <= end:
        day = service.inspect_day(cursor.year, cursor.month, cursor.day)
        year_index = BRANCH_INDEX[day.calendar.year_branch]
        recomputed = day_value(year_index, day.calendar.lunar_month, day.calendar.lunar_day)
        assert day.day_value == recomputed
        assert day.six_state.label == six_state_from_value(recomputed).label
        remainder = recomputed % 6
        assert day.six_state.remainder == remainder
        assert day.six_state.label == SIX_STATE_BY_REMAINDER[remainder][1]
        cursor += timedelta(days=1)


def test_gd_cal_01_solar_term_windows_keep_lunar_month() -> None:
    engine = CalendarEngine()
    terms = SolarTermEngine()
    cursor = date(2026, 1, 2)
    end = date(2026, 12, 31)
    previous_branch = terms.get_bazi_month(2026, 1, 1).branch
    boundaries: list[date] = []
    while cursor <= end:
        branch = terms.get_bazi_month(cursor.year, cursor.month, cursor.day).branch
        if branch != previous_branch:
            boundaries.append(cursor)
            previous_branch = branch
        cursor += timedelta(days=1)
    assert len(boundaries) == 12
    for boundary in boundaries:
        for delta in range(-2, 3):
            probe = boundary + timedelta(days=delta)
            if probe.year != 2026:
                continue
            calendar = engine.build(probe.year, probe.month, probe.day)
            snapshot = DateSelectionService().inspect_day(
                probe.year, probe.month, probe.day
            ).calendar
            assert snapshot.lunar_month == calendar.lunar_month
            assert snapshot.lunar_month_ganzhi == calendar.lunar_month_can_chi
            stem = (calendar.lunar_year_can_chi or "").split()[0]
            assert snapshot.lunar_month_ganzhi == lunar_month_ganzhi(
                stem, int(calendar.lunar_month)
            )


def test_gd_cal_01_leap_month_keeps_number_and_can_chi() -> None:
    """Leap month 4/2020 keeps month number 4; Tiểu Lục Nhâm does not +1 from Can Chi."""
    service = DateSelectionService()
    leap = service.inspect_day(2020, 5, 23)
    assert leap.calendar.lunar_month == 4
    assert leap.calendar.lunar_leap is True
    assert leap.calendar.lunar_month_ganzhi == "Tân Tỵ"
    regular = None
    cursor = date(2020, 4, 20)
    while cursor <= date(2020, 5, 22):
        probe = service.inspect_day(cursor.year, cursor.month, cursor.day)
        if probe.calendar.lunar_month == 4 and not probe.calendar.lunar_leap:
            regular = probe
        cursor += timedelta(days=1)
    assert regular is not None
    assert regular.calendar.lunar_month == 4
    assert regular.calendar.lunar_month_ganzhi == leap.calendar.lunar_month_ganzhi
    assert leap.day_value == day_value(
        BRANCH_INDEX[leap.calendar.year_branch],
        4,
        leap.calendar.lunar_day,
    )
    assert leap.day_value != day_value(
        BRANCH_INDEX[leap.calendar.year_branch],
        5,
        leap.calendar.lunar_day,
    )


def test_gd_cal_01_good_date_does_not_consume_bazi_month_for_liu_ren() -> None:
    service_src = inspect.getsource(DateSelectionService._build_day)
    liu_src = LIU_REN.read_text(encoding="utf-8")
    adapter_src = ADAPTER.read_text(encoding="utf-8")
    assert "snapshot.lunar_month" in service_src
    assert "snapshot.lunar_day" in service_src
    assert "month_ganzhi" not in service_src
    assert "month_pillar" not in service_src
    assert "lunar_month" in liu_src
    assert "month_pillar" not in liu_src
    assert "lunar_month_ganzhi" in adapter_src
    assert "solar-term" in adapter_src
    js = JS.read_text(encoding="utf-8")
    tsx = TSX.read_text(encoding="utf-8")
    assert "lunar_month_ganzhi" in js
    assert "lunar_month_ganzhi" in tsx
    assert "Can Chi tháng âm" in js
    assert "Can Chi tháng âm" in tsx
    assert "good_date_identity" in js
    assert "CAN CHI NGÀY" in js
    assert "CAN CHI NGÀY" in tsx
    assert "Trụ tháng theo tiết khí" not in js
    assert "Trụ tháng theo tiết khí" not in tsx


def test_gd_cal_01_traces_oct_and_nov() -> None:
    traces = [
        _trace(2026, 10, 7),
        _trace(2026, 10, 8),
        _trace(2026, 11, 6),
        _trace(2026, 11, 7),
    ]
    for item in traces:
        print("\nGD-CAL-01 TRACE", item["gregorian"])
        for key, value in item.items():
            if key == "ui_binding_sources":
                print("  UI bindings:")
                for label, source in value.items():
                    print(f"    {label}: {source}")
            else:
                print(f"  {key}: {value}")
    oct7, oct8, nov6, nov7 = traces
    assert oct7["lunar_month"] == oct8["lunar_month"] == 8
    assert oct7["lunar_month_can_chi"] == oct8["lunar_month_can_chi"] == "Đinh Dậu"
    assert oct7["bazi_month_pillar"] != oct8["bazi_month_pillar"]
    assert oct7["tieu_luc_nham"] == "Không Vong"
    assert oct8["tieu_luc_nham"] == "Đại An"
    assert nov6["lunar_month"] == nov7["lunar_month"]
    assert nov6["lunar_month_can_chi"] == nov7["lunar_month_can_chi"]
    assert nov6["bazi_month_pillar"] != nov7["bazi_month_pillar"]
