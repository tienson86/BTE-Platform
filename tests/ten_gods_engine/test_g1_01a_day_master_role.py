"""G1-01A: Nhật Chủ is a Day Pillar presentation role, not a same-stem overlay."""

from __future__ import annotations

import pytest

from engines.bazi_engine.ten_god import ten_god_name
from engines.ten_gods_engine import TenGodsEngine
from engines.ten_gods_engine.mapper import map_stem_to_ten_god

STEMS = (
    "Giáp",
    "Ất",
    "Bính",
    "Đinh",
    "Mậu",
    "Kỷ",
    "Canh",
    "Tân",
    "Nhâm",
    "Quý",
)

# One earthly branch that hides each heavenly stem.
HIDDEN_BRANCH: dict[str, str] = {
    "Giáp": "Dần",
    "Ất": "Mão",
    "Bính": "Tỵ",
    "Đinh": "Ngọ",
    "Mậu": "Thìn",
    "Kỷ": "Sửu",
    "Canh": "Thân",
    "Tân": "Dậu",
    "Nhâm": "Hợi",
    "Quý": "Tý",
}


@pytest.fixture
def engine() -> TenGodsEngine:
    return TenGodsEngine()


@pytest.mark.parametrize("day_master", STEMS)
def test_hidden_same_stem_is_ty_kien(
    engine: TenGodsEngine,
    day_master: str,
) -> None:
    """Hidden stem equal to Day Master is Tỷ Kiên, never Nhật Chủ."""
    index = STEMS.index(day_master)
    result = engine.calculate_from_stems(
        day_master=day_master,
        year_stem=STEMS[(index + 1) % 10],
        year_branch="Tuất",
        month_stem=STEMS[(index + 2) % 10],
        month_branch="Tuất",
        day_stem=day_master,
        day_branch="Tuất",
        hour_stem=STEMS[(index + 3) % 10],
        hour_branch=HIDDEN_BRANCH[day_master],
    )
    matches = [
        item
        for item in result.hidden
        if item.hidden_stem == day_master
    ]
    assert matches
    assert all(item.ten_god == "Tỷ Kiên" for item in matches)
    assert all(item.god_id == "bi_jian" for item in matches)


@pytest.mark.parametrize("day_master", STEMS)
def test_day_pillar_heavenly_stem_is_nhat_chu(
    engine: TenGodsEngine,
    day_master: str,
) -> None:
    """Only the Day Pillar heavenly stem presents as Nhật Chủ."""
    index = STEMS.index(day_master)
    year_stem = STEMS[(index + 1) % 10]
    result = engine.calculate_from_stems(
        day_master=day_master,
        year_stem=year_stem,
        year_branch="Tý",
        month_stem=STEMS[(index + 2) % 10],
        month_branch="Tý",
        day_stem=day_master,
        day_branch="Ngọ",
        hour_stem=STEMS[(index + 3) % 10],
        hour_branch="Tý",
    )
    by_pillar = {item.pillar: item for item in result.visible}
    assert by_pillar["day"].stem == day_master
    assert by_pillar["day"].ten_god == "Nhật Chủ"
    assert by_pillar["day"].god_id == "day_master"
    assert by_pillar["year"].ten_god != "Nhật Chủ"
    assert ten_god_name(day_master, day_master) == "Tỷ Kiên"


def test_visible_same_stem_outside_day_pillar_is_ty_kien(engine: TenGodsEngine) -> None:
    """Year / month / hour Canh with Day Master Canh remain Tỷ Kiên."""
    result = engine.calculate_from_stems(
        day_master="Canh",
        year_stem="Canh",
        year_branch="Tý",
        month_stem="Canh",
        month_branch="Tý",
        day_stem="Canh",
        day_branch="Ngọ",
        hour_stem="Canh",
        hour_branch="Tý",
    )
    by_pillar = {item.pillar: item.ten_god for item in result.visible}
    assert by_pillar["year"] == "Tỷ Kiên"
    assert by_pillar["month"] == "Tỷ Kiên"
    assert by_pillar["day"] == "Nhật Chủ"
    assert by_pillar["hour"] == "Tỷ Kiên"
    label, god_id = map_stem_to_ten_god("Canh", "Canh")
    assert label == "Tỷ Kiên"
    assert god_id == "bi_jian"
    presented, presented_id = map_stem_to_ten_god(
        "Canh",
        "Canh",
        pillar="day",
        visibility="visible",
    )
    assert presented == "Nhật Chủ"
    assert presented_id == "day_master"
