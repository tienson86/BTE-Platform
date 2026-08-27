"""DS-05 Cases A–E: Ganzhi, gender separation, khắc convention, arithmetic."""

from __future__ import annotations

import pytest

from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm
from engines.calendar_engine.engine import CalendarEngine
from engines.calendar_engine.julian.julian import JulianDay
from engines.date_selection.cung_phi import cung_for_date_ganzhi, trach_for_person
from engines.date_selection.exceptions import DateSelectionMappingError
from engines.date_selection.hour import window_for_clock
from engines.date_selection.ke import current_ke_index, ke_slots_for_hour
from engines.date_selection.liu_ren import day_value, hour_value, ke_value, six_state_from_value
from engines.date_selection.service import DateSelectionService


def test_case_a_27_aug_2026_day_ganzhi() -> None:
    jdn = JulianDay.day_number(2026, 8, 27)
    jd_float = JulianDay.from_gregorian(2026, 8, 27)
    gz = GanzhiAlgorithm.day(jdn)
    day = DateSelectionService().inspect_day(2026, 8, 27)
    calendar = CalendarEngine().build(2026, 8, 27)
    chart = BaziEngine().build(2026, 8, 27, 12, 0)

    assert jdn == 2461280
    assert jd_float == 2461279.5
    assert int(jdn + 9) % 10 == 9
    assert int(jdn + 1) % 12 == 9
    assert gz["can"] == "Quý"
    assert gz["chi"] == "Dậu"
    assert GanzhiAlgorithm.STEM[9] == "Quý"
    assert GanzhiAlgorithm.BRANCH[9] == "Dậu"
    assert day.calendar.lunar_day == 15
    assert day.calendar.lunar_month == 7
    assert day.calendar.year_ganzhi == "Bính Ngọ"
    assert day.calendar.day_ganzhi == "Quý Dậu"
    assert f"{chart.day_pillar.stem} {chart.day_pillar.branch}" == "Quý Dậu"
    assert calendar.lunar_year == 2026
    assert calendar.lunar_month == 7
    assert calendar.lunar_day == 15
    with pytest.raises(DateSelectionMappingError, match="Hạ Nguyên"):
        cung_for_date_ganzhi("Quý Dậu")
    assert day.trach is None


def test_case_b_day_cung_identical_for_male_and_female_viewers() -> None:
    service = DateSelectionService()
    male_day = service.inspect_day(2026, 8, 27, gender="male")
    female_day = service.inspect_day(2026, 8, 27, gender="female")
    assert male_day.calendar.day_ganzhi == female_day.calendar.day_ganzhi == "Quý Dậu"
    assert male_day.trach == female_day.trach

    male = service.search(
        full_name="Nam",
        gender="male",
        birth_year=1990,
        birth_month=5,
        birth_day=15,
        target_year=2026,
        target_month=8,
    )
    female = service.search(
        full_name="Nữ",
        gender="female",
        birth_year=1990,
        birth_month=5,
        birth_day=15,
        target_year=2026,
        target_month=8,
    )
    assert male.person.trach.cung != female.person.trach.cung
    built = service._build_day(2026, 8, 27)
    assert built.trach == male_day.trach == female_day.trach


def test_case_c_hour_cung_identical_for_male_and_female_viewers() -> None:
    service = DateSelectionService()
    male_day = service.inspect_day(2026, 8, 27, gender="male")
    female_day = service.inspect_day(2026, 8, 27, gender="female")
    male_thin = next(item for item in male_day.hours if item.window.branch == "Thìn")
    female_thin = next(item for item in female_day.hours if item.window.branch == "Thìn")
    assert male_thin.ganzhi == female_thin.ganzhi
    assert male_thin.trach == female_thin.trach


def test_case_d_thin_ke_ranges() -> None:
    window = window_for_clock(7, 1)
    assert window.branch == "Thìn"
    slots = ke_slots_for_hour(window, 34)
    assert [slot.time_range for slot in slots] == [
        "07:01–07:20",
        "07:21–07:40",
        "07:41–08:00",
        "08:01–08:20",
        "08:21–08:40",
        "08:41–09:00",
    ]


@pytest.mark.parametrize(
    ("hour", "minute", "branch", "ke_index"),
    [
        (7, 0, "Mão", 6),
        (7, 1, "Thìn", 1),
        (7, 20, "Thìn", 1),
        (7, 21, "Thìn", 2),
        (8, 59, "Thìn", 6),
        (9, 0, "Thìn", 6),
        (9, 1, "Tỵ", 1),
        (23, 0, "Hợi", 6),
        (23, 1, "Tý", 1),
        (0, 0, "Tý", 3),
        (1, 0, "Tý", 6),
        (1, 1, "Sửu", 1),
    ],
)
def test_case_d_boundaries(hour: int, minute: int, branch: str, ke_index: int) -> None:
    window = window_for_clock(hour, minute)
    assert window.branch == branch
    assert current_ke_index(window, hour, minute) == ke_index


def test_every_minute_is_mapped() -> None:
    mapped = []
    for total in range(24 * 60):
        hour, minute = divmod(total, 60)
        mapped.append(window_for_clock(hour, minute).branch)
    assert len(mapped) == 1440
    assert set(mapped) == {
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
    }


def test_case_e_known_arithmetic_unchanged() -> None:
    assert day_value(7, 7, 15) == 29
    assert 29 % 6 == 5
    assert six_state_from_value(29).label == "Tiểu Cát"
    assert hour_value(29, 5) == 34
    assert 34 % 6 == 4
    assert six_state_from_value(34).label == "Xích Khẩu"
    assert ke_value(34, 1) == 35
    assert 35 % 6 == 5
    assert six_state_from_value(35).label == "Tiểu Cát"
    day = DateSelectionService().inspect_day(2026, 8, 27)
    assert day.six_state.label == "Tiểu Cát"
    thin = next(item for item in day.hours if item.window.branch == "Thìn")
    assert thin.six_state.label == "Xích Khẩu"
    assert thin.ke_slots[0].six_state.label == "Tiểu Cát"


def test_date_selection_day_ganzhi_matches_bazi_golden_1987() -> None:
    day = DateSelectionService().inspect_day(1987, 1, 21)
    chart = BaziEngine().build(1987, 1, 21, 3, 30)
    assert day.calendar.day_ganzhi == "Canh Ngọ"
    assert f"{chart.day_pillar.stem} {chart.day_pillar.branch}" == "Canh Ngọ"


def test_person_cung_uses_gender_and_birth_year() -> None:
    male = trach_for_person(lunar_year=1990, gender="male")
    female = trach_for_person(lunar_year=1990, gender="female")
    assert male.cung == "Khảm"
    assert female.cung == "Cấn"
    assert male.trach_group_code == "dong"
    assert female.trach_group_code == "tay"
