"""CD-02: /choose-date scans the whole month and returns every eligible date."""

from __future__ import annotations

import calendar as gregorian
from pathlib import Path

from engines.date_selection.constants import BRANCH_INDEX
from engines.date_selection.liu_ren import day_value, six_state_from_value
from engines.date_selection.ranking import (
    eligible_dates,
    exclusion_reason,
    rank_dates,
)
from engines.date_selection.service import DateSelectionService

from tests.date_selection.test_ranking import _day

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

PROFILE = {
    "full_name": "Nguyễn Thanh Bình",
    "gender": "male",
    "birth_year": 1978,
    "birth_month": 10,
    "birth_day": 25,
}

TRACE_DAYS = (1, 7, 10, 16, 20, 24)


def _search_november():
    return DateSelectionService().search(
        **PROFILE,
        target_year=2026,
        target_month=11,
    )


def _scan_november() -> dict:
    service = DateSelectionService()
    person = service.person_profile(**PROFILE)
    last_day = gregorian.monthrange(2026, 11)[1]
    days = [service._build_day(2026, 11, day) for day in range(1, last_day + 1)]
    person_trach = person.trach.trach_group_code
    reasons = {day.calendar.solar_day: exclusion_reason(day, person_trach) for day in days}
    eligible = eligible_dates(days, person_trach)
    ranked = rank_dates(days, person_trach)
    return {
        "person": person,
        "days": days,
        "generated": len(days),
        "reasons": reasons,
        "eligible": eligible,
        "ranked": ranked,
        "person_trach": person_trach,
    }


def test_cd_02_a_november_scans_all_30_days() -> None:
    scan = _scan_november()
    assert scan["generated"] == 30
    result = _search_november()
    assert result.total_days_scanned == 30


def test_cd_02_b_07_nov_is_evaluated() -> None:
    scan = _scan_november()
    solar_days = [day.calendar.solar_day for day in scan["days"]]
    assert 7 in solar_days
    assert 7 in scan["reasons"]


def test_cd_02_c_07_nov_toc_hy() -> None:
    day = DateSelectionService().inspect_day(2026, 11, 7)
    assert day.six_state.label == "Tốc Hỷ"
    year_index = BRANCH_INDEX[day.calendar.year_branch]
    assert year_index == 7
    assert day.calendar.lunar_month == 9
    assert day.calendar.lunar_day == 29
    assert day_value(year_index, 9, 29) % 6 == 3
    assert six_state_from_value(day_value(year_index, 9, 29)).label == "Tốc Hỷ"


def test_cd_02_d_07_nov_cung_ton() -> None:
    day = DateSelectionService().inspect_day(2026, 11, 7)
    assert day.trach is not None
    assert day.trach.cung == "Tốn"
    assert day.trach.element_label == "Mộc"
    assert day.trach.trach_group_label == "Đông Tứ Trạch"


def test_cd_02_e_07_nov_passes_frozen_rules() -> None:
    scan = _scan_november()
    assert scan["person"].trach.cung == "Tốn"
    assert scan["person"].trach.trach_group_label == "Đông Tứ Trạch"
    assert scan["reasons"][7] is None
    eligible_days = [item.day.calendar.solar_day for item in scan["eligible"]]
    ranked_days = [item.day.calendar.solar_day for item in scan["ranked"]]
    assert 7 in eligible_days
    assert 7 in ranked_days
    result_days = [item.day.calendar.solar_day for item in _search_november().dates]
    assert 7 in result_days


def test_cd_02_f_no_truncation_at_five() -> None:
    days = [_day(index, "Đoài", 1) for index in range(1, 8)]
    ranked = rank_dates(days, "tay")
    assert len(ranked) == 7
    assert [item.day.calendar.solar_day for item in ranked] == [1, 2, 3, 4, 5, 6, 7]


def test_cd_02_g_ranking_preserves_candidate_count() -> None:
    scan = _scan_november()
    assert len(scan["ranked"]) == len(scan["eligible"])
    result = _search_november()
    assert len(result.dates) == result.total_eligible
    payload = result.to_dict()
    assert len(payload["dates"]) == payload["total_eligible"]
    assert len(payload["featured_dates"]) <= len(payload["dates"])


def test_cd_02_h_frontend_renders_more_than_five_cards() -> None:
    js = JS.read_text(encoding="utf-8")
    tsx = TSX.read_text(encoding="utf-8")
    assert "slice(0, 5)" not in js
    assert "slice(0, 5)" not in tsx
    assert "found_in_month" in js
    assert "result-count" in js
    assert "result-count" in tsx
    assert "MAX_RANKED_DATES" not in js


def test_cd_02_i_total_days_scanned_equals_month_length() -> None:
    service = DateSelectionService()
    november = service.search(**PROFILE, target_year=2026, target_month=11)
    february = service.search(**PROFILE, target_year=2026, target_month=2)
    assert november.total_days_scanned == 30
    assert february.total_days_scanned == 28
    assert november.to_dict()["total_days_scanned"] == 30


def test_cd_02_j_good_date_choose_date_snapshot_parity() -> None:
    inspected = DateSelectionService().inspect_day(2026, 11, 7)
    result = _search_november()
    chosen = next(item.day for item in result.dates if item.day.calendar.solar_day == 7)
    assert chosen.calendar.lunar_label == inspected.calendar.lunar_label
    assert chosen.six_state.label == inspected.six_state.label == "Tốc Hỷ"
    assert chosen.trach is not None and inspected.trach is not None
    assert chosen.trach.cung == inspected.trach.cung == "Tốn"
    assert chosen.trach.trach_group_label == inspected.trach.trach_group_label
    assert chosen.calendar.day_ganzhi == inspected.calendar.day_ganzhi
    assert chosen.calendar.lunar_month_ganzhi == inspected.calendar.lunar_month_ganzhi


def test_cd_02_november_funnel_and_traces() -> None:
    scan = _scan_november()
    result = _search_november()
    eligible_days = [item.day.calendar.solar_day for item in scan["eligible"]]
    ranked_days = [item.day.calendar.solar_day for item in scan["ranked"]]
    api_days = [item.day.calendar.solar_day for item in result.dates]
    traces = []
    for solar_day in TRACE_DAYS:
        day = scan["days"][solar_day - 1]
        reason = scan["reasons"][solar_day]
        included = reason is None
        rank = ranked_days.index(solar_day) + 1 if included else None
        traces.append(
            {
                "gregorian": f"{solar_day:02d}/11/2026",
                "lunar": day.calendar.lunar_label,
                "liu_ren": day.six_state.label,
                "cung": day.trach.cung if day.trach else None,
                "hanh_cung": day.trach.element_label if day.trach else None,
                "nhom_trach": day.trach.trach_group_label if day.trach else None,
                "user_cung": scan["person"].trach.cung,
                "user_trach": scan["person"].trach.trach_group_label,
                "eligibility": "INCLUDED" if included else f"EXCLUDED:{reason}",
                "rank": rank,
            }
        )
    print("\nCD-02 NOVEMBER FUNNEL")
    print("generated", scan["generated"])
    print("eligible", len(scan["eligible"]), eligible_days)
    print("ranked", len(scan["ranked"]), ranked_days)
    print("api", len(api_days), api_days)
    for item in traces:
        print("TRACE", item)
    assert scan["generated"] == 30
    assert traces[1]["gregorian"] == "07/11/2026"
    assert traces[1]["liu_ren"] == "Tốc Hỷ"
    assert traces[1]["eligibility"] == "INCLUDED"
    assert 7 in api_days
    assert set(eligible_days) == set(ranked_days)
    assert set(api_days) == set(eligible_days)
    assert len(scan["ranked"]) == 7
    assert eligible_days == [1, 7, 10, 16, 20, 26, 28]
