"""Hour six-state tests."""

from __future__ import annotations

from engines.date_selection.hour import hour_ganzhi
from engines.date_selection.liu_ren import hour_value, six_state_from_value
from engines.date_selection.service import DateSelectionService


def test_hour_thin_xich_khau() -> None:
    assert hour_value(29, 5) == 34
    assert six_state_from_value(34).label == "Xích Khẩu"


def test_hour_ganzhi_uses_canonical_table() -> None:
    assert hour_ganzhi("Nhâm", "Thìn") == "Giáp Thìn"


def test_all_twelve_hours_present() -> None:
    day = DateSelectionService().inspect_day(2026, 8, 27)
    branches = [item.window.branch for item in day.hours]
    assert branches == [
        "Tý",
        "Sửu",
        "Dần",
        "Mão",
        "Thìn",
        "Tỵ",
        "Ngọ",
        "Mùi",
        "Thân",
        "Dậu",
        "Tuất",
        "Hợi",
    ]
