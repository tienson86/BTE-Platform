"""CP-BUG-002: personal Cung Phi follows Tam Nguyên year routing, not birth-year digits."""

from __future__ import annotations

from engines.calendar_engine.cung_phi import (
    EAST_CUNG,
    WEST_CUNG,
    calculate_cung_phi,
    element_label_for_cung,
    house_group_for_cung,
)
from engines.calendar_engine.engine import CalendarEngine
from engines.date_selection.service import DateSelectionService


def test_1987_male_personal_cung_is_khon_not_ton() -> None:
    calendar = CalendarEngine().build(1987, 1, 21, 4, 30, gender="male")
    routing = calendar.ganzhi_routing or {}
    year_route = routing.get("year") or {}
    birth_year_digits = calculate_cung_phi(year=1987, gender="male")
    assert year_route["cung_phi"] == "Khôn"
    assert calendar.cung_phi == "Khôn"
    assert calendar.menh_quai == "Khôn"
    assert calendar.hanh_cung == "Thổ"
    assert calendar.nhom_trach == "Tây Tứ Trạch"
    assert calendar.house_group == "Tây Tứ Trạch"
    assert birth_year_digits.cung_phi == "Tốn"
    assert calendar.cung_phi != birth_year_digits.cung_phi
    assert calendar.cung_phi == year_route["cung_phi"]


def test_1966_male_routing_cases_remain_doai() -> None:
    calendar = CalendarEngine().build(1966, 9, 24, 4, 15, gender="male")
    assert calendar.cung_phi == "Đoài"
    assert calendar.menh_quai == "Đoài"
    assert calendar.nhom_trach == "Tây Tứ Trạch"
    assert (calendar.ganzhi_routing or {})["year"]["cung_phi"] == "Đoài"


def test_1966_female_personal_cung_remains_can_not_year_male_palace() -> None:
    calendar = CalendarEngine().build(1966, 9, 24, 4, 15, gender="female")
    year_route = (calendar.ganzhi_routing or {}).get("year") or {}
    assert year_route["cung_phi"] == "Đoài"
    assert calendar.cung_phi == "Cấn"
    assert calendar.menh_quai == "Cấn"
    assert calendar.hanh_cung == "Thổ"
    assert calendar.nhom_trach == "Tây Tứ Trạch"


def test_cung_phi_element_trach_invariant() -> None:
    for cung in (*EAST_CUNG, *WEST_CUNG):
        group = house_group_for_cung(cung)
        element = element_label_for_cung(cung)
        if cung in EAST_CUNG:
            assert group == "Đông Tứ Trạch"
        else:
            assert group == "Tây Tứ Trạch"
        assert element
        if cung == "Khôn":
            assert element == "Thổ"
            assert group == "Tây Tứ Trạch"
        if cung == "Tốn":
            assert element == "Mộc"
            assert group == "Đông Tứ Trạch"


def test_good_date_person_matches_calendar_personal_cung() -> None:
    calendar = CalendarEngine().build(1987, 1, 21, gender="male")
    person = DateSelectionService().person_profile(
        full_name="Nguyen Tien Son",
        gender="male",
        birth_year=1987,
        birth_month=1,
        birth_day=21,
    )
    assert person.trach.cung == calendar.cung_phi == "Khôn"
    assert person.trach.element_label == "Thổ"
    assert person.trach.trach_group_label == "Tây Tứ Trạch"
