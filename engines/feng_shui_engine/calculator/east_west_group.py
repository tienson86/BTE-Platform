"""Đông / Tây Tứ Trạch grouping (V1)."""

from __future__ import annotations

from engines.feng_shui_engine.data import load_json
from engines.feng_shui_engine.exceptions import FengShuiValidationError


def group_for_gua_number(gua_number: int) -> str:
    """
    Return ``Đông Tứ Trạch`` or ``Tây Tứ Trạch`` for a gua number.

    Does not compute directions or other Dương Trạch features.
    """
    table = load_json("east_west_group.json")
    east = table.get("east") or {}
    west = table.get("west") or {}
    east_nums = {int(n) for n in (east.get("gua_numbers") or [])}
    west_nums = {int(n) for n in (west.get("gua_numbers") or [])}
    if gua_number in east_nums:
        return str(east.get("label") or "Đông Tứ Trạch")
    if gua_number in west_nums:
        return str(west.get("label") or "Tây Tứ Trạch")
    raise FengShuiValidationError(f"gua number not in east/west groups: {gua_number}")
