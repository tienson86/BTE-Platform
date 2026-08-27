"""Personalized filtering and ranking."""

from __future__ import annotations

from engines.date_selection.liu_ren import six_state_from_value
from engines.date_selection.models import (
    CalendarSnapshot,
    DaySelection,
    HourSelection,
    HourWindow,
    KeSlot,
)
from engines.date_selection.ranking import is_candidate_day, rank_dates
from engines.date_selection.trach import trach_from_cung


def _snapshot(day: int, ganzhi: str = "Bính Ngọ") -> CalendarSnapshot:
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


def _hour(cung: str, ke_code: str, ke_label: str) -> HourSelection:
    window = HourWindow(
        branch="Tỵ",
        branch_index=6,
        start_hour=9,
        start_minute=0,
        end_hour=10,
        end_minute=59,
        time_range="09:00–10:59",
        is_cross_day=False,
    )
    return HourSelection(
        window=window,
        ganzhi="Canh Tỵ",
        hour_value=10,
        six_state=six_state_from_value(1),
        trach=trach_from_cung(cung),
        ke_slots=[
            KeSlot(
                ke_index=1,
                time_range="09:00–09:19",
                start_minute_of_day=540,
                six_state=six_state_from_value(
                    {"dai_an": 1, "toc_hy": 3, "tieu_cat": 5, "luu_lien": 2, "xich_khau": 4, "khong_vong": 0}[ke_code]
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
        hours=[_hour(hour_cung or cung, ke_code, label.label)],
    )


def test_same_trach_retained() -> None:
    day = _day(1, "Đoài", 1)
    assert is_candidate_day(day, "tay") is True


def test_opposite_trach_rejected() -> None:
    day = _day(1, "Khảm", 1)
    assert is_candidate_day(day, "tay") is False


def test_xich_khau_rejected() -> None:
    day = _day(2, "Đoài", 4)
    assert is_candidate_day(day, "tay") is False


def test_khong_vong_rejected() -> None:
    day = _day(3, "Đoài", 0)
    assert is_candidate_day(day, "tay") is False


def test_positive_ke_prioritized_and_diversity() -> None:
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
    codes = [item.day.six_state.code for item in ranked]
    assert "dai_an" in codes
    assert "tieu_cat" in codes
    assert "toc_hy" in codes
    assert all(item.recommendations[0].classification != "Xích Khẩu" for item in ranked)
    assert all(item.day.trach.trach_group_code == "tay" for item in ranked)
    assert len(ranked) <= 5
