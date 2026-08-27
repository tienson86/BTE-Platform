"""All eight Cung → element / trạch mappings."""

from __future__ import annotations

import pytest

from engines.date_selection.trach import cung_to_element, cung_to_trach_group, trach_from_cung


@pytest.mark.parametrize(
    ("cung", "element_code", "element_label", "group_code", "group_label"),
    [
        ("Khảm", "thuy", "Thủy", "dong", "Đông Tứ Trạch"),
        ("Ly", "hoa", "Hỏa", "dong", "Đông Tứ Trạch"),
        ("Chấn", "moc", "Mộc", "dong", "Đông Tứ Trạch"),
        ("Tốn", "moc", "Mộc", "dong", "Đông Tứ Trạch"),
        ("Càn", "kim", "Kim", "tay", "Tây Tứ Trạch"),
        ("Khôn", "tho", "Thổ", "tay", "Tây Tứ Trạch"),
        ("Cấn", "tho", "Thổ", "tay", "Tây Tứ Trạch"),
        ("Đoài", "kim", "Kim", "tay", "Tây Tứ Trạch"),
    ],
)
def test_cung_mappings(
    cung: str,
    element_code: str,
    element_label: str,
    group_code: str,
    group_label: str,
) -> None:
    assert cung_to_element(cung) == (element_code, element_label)
    assert cung_to_trach_group(cung) == (group_code, group_label)
    info = trach_from_cung(cung)
    assert info.cung == cung
    assert info.element_code == element_code
    assert info.trach_group_code == group_code
