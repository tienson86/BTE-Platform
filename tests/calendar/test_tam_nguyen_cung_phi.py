"""G1-10: Tam Nguyên Cửu Vận (180-year cycle) and Cung Phi digit-sum."""

from __future__ import annotations

import pytest

from engines.calendar_engine.cung_phi import (
    calculate_cung_phi,
    cung_for_ganzhi,
    gregorian_digit_sum,
    remainder_from_year,
)
from engines.calendar_engine.engine import CalendarEngine
from engines.calendar_engine.exceptions import CalendarValidationError
from engines.calendar_engine.tam_nguyen import (
    HA_NGUYEN,
    THUONG_NGUYEN,
    TRUNG_NGUYEN,
    calculate_tam_nguyen,
    tam_nguyen_for_year,
)
from engines.date_selection.loader import load_ha_nguyen_cung


@pytest.mark.parametrize(
    ("year", "expected_yuan", "expected_van"),
    [
        (1864, THUONG_NGUYEN, 1),
        (1884, THUONG_NGUYEN, 2),
        (1904, THUONG_NGUYEN, 3),
        (1924, TRUNG_NGUYEN, 4),
        (1944, TRUNG_NGUYEN, 5),
        (1966, TRUNG_NGUYEN, 6),
        (1983, TRUNG_NGUYEN, 6),
        (1984, HA_NGUYEN, 7),
        (2004, HA_NGUYEN, 8),
        (2026, HA_NGUYEN, 9),
        (2043, HA_NGUYEN, 9),
        (2044, THUONG_NGUYEN, 1),
        (1684, THUONG_NGUYEN, 1),
    ],
)
def test_180_year_cycle_yuan_and_period(year: int, expected_yuan: str, expected_van: int) -> None:
    result = calculate_tam_nguyen(year)
    assert tam_nguyen_for_year(year) == expected_yuan
    assert result.tam_nguyen == expected_yuan
    assert result.cuu_van == expected_van
    assert result.period_end_year - result.period_start_year == 19


def test_male_1966_digit_sum_doai() -> None:
    assert gregorian_digit_sum(1966) == 22
    assert remainder_from_year(1966) == 4
    result = calculate_cung_phi(year=1966, gender="male")
    assert result.cung_phi == "Đoài"
    assert result.menh_quai == "Đoài"
    assert result.house_group == "Tây Tứ Trạch"
    assert result.gua_number == 7


@pytest.mark.parametrize(
    ("year", "gender", "cung", "group", "yuan", "van"),
    [
        (1966, "male", "Đoài", "Tây Tứ Trạch", TRUNG_NGUYEN, 6),
        (1966, "female", "Cấn", "Tây Tứ Trạch", TRUNG_NGUYEN, 6),
        (1984, "male", "Đoài", "Tây Tứ Trạch", HA_NGUYEN, 7),
        (1984, "female", "Cấn", "Tây Tứ Trạch", HA_NGUYEN, 7),
        (2026, "male", "Khảm", "Đông Tứ Trạch", HA_NGUYEN, 9),
        (2026, "female", "Cấn", "Tây Tứ Trạch", HA_NGUYEN, 9),
    ],
)
def test_verification_years_calendar_result(
    year: int,
    gender: str,
    cung: str,
    group: str,
    yuan: str,
    van: int,
) -> None:
    calendar = CalendarEngine().build(year, 6, 15, gender=gender)
    payload = calendar.to_dict()
    assert calendar.tam_nguyen == yuan
    assert calendar.cuu_van == van
    assert calendar.cung_phi == cung
    assert calendar.menh_quai == cung
    assert calendar.house_group == group
    assert calendar.nhom_trach == group
    assert payload["tam_nguyen"] == yuan
    assert payload["cuu_van"] == van
    assert payload["cung_phi"] == cung
    assert payload["house_group"] == group
    assert payload["nhom_trach"] == group


def test_ganzhi_cung_is_not_always_ha_nguyen() -> None:
    giap_ty_ha = cung_for_ganzhi("Giáp Tý", tam_nguyen=HA_NGUYEN, reference_year=1984)
    giap_ty_trung = cung_for_ganzhi("Giáp Tý", tam_nguyen=TRUNG_NGUYEN, reference_year=1924)
    giap_ty_thuong = cung_for_ganzhi("Giáp Tý", tam_nguyen=THUONG_NGUYEN, reference_year=1864)
    assert giap_ty_ha == "Đoài"
    assert giap_ty_trung != giap_ty_ha
    assert giap_ty_thuong != giap_ty_ha
    assert giap_ty_trung == "Tốn"
    assert giap_ty_thuong == "Khảm"


def test_ha_nguyen_ganzhi_matches_approved_table() -> None:
    table = load_ha_nguyen_cung()
    for ganzhi, row in table.items():
        computed = cung_for_ganzhi(ganzhi, tam_nguyen=HA_NGUYEN, reference_year=1984)
        assert computed == row["ha_nguyen_cung"]


def test_missing_gender_skips_cung_phi_but_keeps_cycle() -> None:
    calendar = CalendarEngine().build(1966, 9, 24)
    assert calendar.tam_nguyen == TRUNG_NGUYEN
    assert calendar.cuu_van == 6
    assert calendar.cung_phi is None
    assert calendar.house_group is None


def test_invalid_gender_raises() -> None:
    with pytest.raises(CalendarValidationError):
        calculate_cung_phi(year=1966, gender="unknown")
