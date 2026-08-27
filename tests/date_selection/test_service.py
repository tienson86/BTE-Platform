"""Service-level smoke for Date Selection."""

from __future__ import annotations

import pytest

from engines.date_selection.exceptions import DateSelectionValidationError
from engines.date_selection.service import DateSelectionService


def test_month_calendar_real_length() -> None:
    service = DateSelectionService()
    feb = service.month_calendar(2026, 2)
    assert len(feb.cells) == 28
    july = service.month_calendar(2026, 7)
    assert len(july.cells) == 31
    assert july.cells[0].solar_day == 1
    assert july.cells[-1].solar_day == 31


def test_person_profile_shows_lunar() -> None:
    profile = DateSelectionService().person_profile(
        full_name="Nguyễn Văn A",
        gender="Nam",
        birth_year=1990,
        birth_month=5,
        birth_day=15,
    )
    assert profile.gender == "male"
    assert profile.gender_label == "Nam"
    assert profile.lunar_label
    assert profile.ganzhi
    assert profile.trach.cung


def test_search_requires_gender() -> None:
    with pytest.raises(DateSelectionValidationError):
        DateSelectionService().search(
            full_name="A",
            gender="",
            birth_year=1990,
            birth_month=5,
            birth_day=15,
            target_year=2026,
            target_month=8,
        )


def test_search_returns_at_most_five() -> None:
    result = DateSelectionService().search(
        full_name="Nguyễn Văn A",
        gender="male",
        birth_year=1990,
        birth_month=5,
        birth_day=15,
        target_year=2026,
        target_month=8,
    )
    assert len(result.dates) <= 5
    for item in result.dates:
        assert item.day.trach is not None
        assert item.day.trach.trach_group_code == result.person.trach.trach_group_code
        assert item.day.six_state.code in {"dai_an", "toc_hy", "tieu_cat"}
