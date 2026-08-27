"""Gender-based 60 Hoa Giáp Cung Phi lookup."""

from __future__ import annotations

import pytest

from engines.date_selection.cung_phi import cung_for_ganzhi, normalize_gender, trach_for_ganzhi
from engines.date_selection.exceptions import DateSelectionValidationError


@pytest.mark.parametrize(
    ("ganzhi", "male_cung", "female_cung"),
    [
        ("Giáp Tý", "Tốn", "Khôn"),
        ("Bính Ngọ", "Đoài", "Cấn"),
        ("Canh Ngọ", "Đoài", "Cấn"),
        ("Nhâm Thân", "Khôn", "Khảm"),
        ("Quý Hợi", "Cấn", "Đoài"),
        ("Mậu Thìn", "Ly", "Càn"),
    ],
)
def test_male_female_cung_phi(ganzhi: str, male_cung: str, female_cung: str) -> None:
    assert cung_for_ganzhi(ganzhi, "male") == male_cung
    assert cung_for_ganzhi(ganzhi, "female") == female_cung
    assert cung_for_ganzhi(ganzhi, "Nam") == male_cung
    assert cung_for_ganzhi(ganzhi, "Nữ") == female_cung


def test_missing_gender_raises() -> None:
    with pytest.raises(DateSelectionValidationError):
        normalize_gender(None)
    with pytest.raises(DateSelectionValidationError):
        normalize_gender("")


def test_trach_follows_cung() -> None:
    male = trach_for_ganzhi("Bính Ngọ", "male")
    female = trach_for_ganzhi("Bính Ngọ", "female")
    assert male.cung == "Đoài"
    assert male.trach_group_label == "Tây Tứ Trạch"
    assert female.cung == "Cấn"
    assert female.trach_group_label == "Tây Tứ Trạch"
