"""Day six-state remainder mapping."""

from __future__ import annotations

import pytest

from engines.date_selection.liu_ren import day_value, six_state_from_value


@pytest.mark.parametrize(
    ("remainder", "code", "label"),
    [
        (1, "dai_an", "Đại An"),
        (2, "luu_lien", "Lưu Liên"),
        (3, "toc_hy", "Tốc Hỷ"),
        (4, "xich_khau", "Xích Khẩu"),
        (5, "tieu_cat", "Tiểu Cát"),
        (0, "khong_vong", "Không Vong"),
    ],
)
def test_remainder_mapping(remainder: int, code: str, label: str) -> None:
    result = six_state_from_value(remainder)
    assert result.remainder == remainder
    assert result.code == code
    assert result.label == label


def test_divisible_by_six_is_khong_vong_not_six() -> None:
    result = six_state_from_value(30)
    assert result.remainder == 0
    assert result.code == "khong_vong"


def test_day_value_sum() -> None:
    assert day_value(7, 7, 15) == 29
    assert six_state_from_value(29).label == "Tiểu Cát"
