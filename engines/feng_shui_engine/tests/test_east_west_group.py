"""Unit tests for east_west_group."""

from __future__ import annotations

import pytest

from engines.feng_shui_engine.calculator.east_west_group import group_for_gua_number
from engines.feng_shui_engine.exceptions import FengShuiValidationError


@pytest.mark.parametrize(
    ("gua_number", "expected"),
    [
        (1, "Đông Tứ Trạch"),
        (3, "Đông Tứ Trạch"),
        (4, "Đông Tứ Trạch"),
        (9, "Đông Tứ Trạch"),
        (2, "Tây Tứ Trạch"),
        (6, "Tây Tứ Trạch"),
        (7, "Tây Tứ Trạch"),
        (8, "Tây Tứ Trạch"),
    ],
)
def test_group_for_gua_number(gua_number: int, expected: str) -> None:
    assert group_for_gua_number(gua_number) == expected


def test_invalid_gua_raises() -> None:
    with pytest.raises(FengShuiValidationError):
        group_for_gua_number(5)
