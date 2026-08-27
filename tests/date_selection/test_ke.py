"""Khắc six-state and Date Selection hour-window tests."""

from __future__ import annotations

from engines.date_selection.hour import window_for_branch
from engines.date_selection.ke import ke_slots_for_hour
from engines.date_selection.liu_ren import ke_value, six_state_from_value


def test_ke1_tieu_cat() -> None:
    assert ke_value(34, 1) == 35
    assert six_state_from_value(35).label == "Tiểu Cát"


def test_thin_ke_ranges_follow_date_selection_convention() -> None:
    window = window_for_branch("Thìn")
    assert window.time_range == "07:01–09:00"
    slots = ke_slots_for_hour(window, 34)
    assert [slot.ke_index for slot in slots] == [1, 2, 3, 4, 5, 6]
    assert slots[0].time_range == "07:01–07:20"
    assert slots[1].time_range == "07:21–07:40"
    assert slots[2].time_range == "07:41–08:00"
    assert slots[3].time_range == "08:01–08:20"
    assert slots[4].time_range == "08:21–08:40"
    assert slots[5].time_range == "08:41–09:00"
    assert slots[0].six_state.label == "Tiểu Cát"
