"""Known example 27/08/2026 against canonical Calendar Engine."""

from __future__ import annotations

from engines.date_selection.constants import BRANCH_INDEX
from engines.date_selection.liu_ren import day_value, hour_value, ke_value, six_state_from_value
from engines.date_selection.service import DateSelectionService


def test_known_example_27_aug_2026() -> None:
    service = DateSelectionService()
    day = service.inspect_day(2026, 8, 27)

    assert day.calendar.solar_label == "27/08/2026"
    assert day.calendar.lunar_day == 15
    assert day.calendar.lunar_month == 7
    assert day.calendar.year_ganzhi == "Bính Ngọ"
    assert day.calendar.year_branch == "Ngọ"
    assert BRANCH_INDEX["Ngọ"] == 7

    expected_day_value = 7 + 7 + 15
    assert day_value(7, 7, 15) == expected_day_value
    assert day.day_value == expected_day_value
    assert six_state_from_value(expected_day_value).label == "Tiểu Cát"
    assert day.six_state.label == "Tiểu Cát"

    thin = next(item for item in day.hours if item.window.branch == "Thìn")
    assert thin.window.branch_index == 5
    assert hour_value(expected_day_value, 5) == 34
    assert thin.hour_value == 34
    assert thin.six_state.label == "Xích Khẩu"

    ke1 = next(item for item in thin.ke_slots if item.ke_index == 1)
    assert ke_value(34, 1) == 35
    assert ke1.six_state.label == "Tiểu Cát"

    # Canonical day Ganzhi / Cung Phi from BTE runtime (do not override).
    assert day.calendar.day_ganzhi == "Nhâm Thân"
    assert day.trach.cung == "Khôn"
    assert day.trach.element_label == "Thổ"
    assert day.trach.trach_group_label == "Tây Tứ Trạch"
    assert thin.ganzhi == "Giáp Thìn"
