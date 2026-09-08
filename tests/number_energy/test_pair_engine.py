"""Pair-engine tests: line difference plus frozen pair table."""

from __future__ import annotations

from engines.number_energy.constants import (
    ENERGY_DISPLAY_NAMES,
    ENERGY_PAIR_RANKS,
    ORDINARY_GUA_DIGITS,
    PAIR_LOOKUP,
)
from engines.number_energy.pair_engine import (
    derive_energy_id,
    generate_adjacent_pairs,
    resolve_pair,
)
from engines.number_energy.parser import parse_number_string


def test_line_difference_matches_frozen_pair_table() -> None:
    for energy_id, ranks in ENERGY_PAIR_RANKS.items():
        for rank, pairs in ranks.items():
            for pair in pairs:
                left, right = int(pair[0]), int(pair[1])
                assert derive_energy_id(left, right) == energy_id
                assert resolve_pair(left, right) == (energy_id, rank)
                assert PAIR_LOOKUP[pair] == (energy_id, rank)


def test_all_ordinary_pairs_are_covered() -> None:
    expected = {f"{left}{right}" for left in ORDINARY_GUA_DIGITS for right in ORDINARY_GUA_DIGITS}
    assert set(PAIR_LOOKUP) == expected
    assert len(PAIR_LOOKUP) == 64


def test_modifiers_are_not_ordinary_pairs() -> None:
    parsed = parse_number_string("103")
    occurrences, undefined = generate_adjacent_pairs(parsed)
    assert occurrences == ()
    assert undefined == ()


def test_adjacent_pairs_for_141319() -> None:
    parsed = parse_number_string("141319")
    occurrences, undefined = generate_adjacent_pairs(parsed)
    assert undefined == ()
    assert [item.pair_digits for item in occurrences] == ["14", "41", "13", "31", "19"]
    assert [item.display_name for item in occurrences] == [
        ENERGY_DISPLAY_NAMES["sheng_qi"],
        ENERGY_DISPLAY_NAMES["sheng_qi"],
        ENERGY_DISPLAY_NAMES["tian_yi"],
        ENERGY_DISPLAY_NAMES["tian_yi"],
        ENERGY_DISPLAY_NAMES["yan_nian"],
    ]
    assert all(item.state == "NORMAL" for item in occurrences)
    assert all(item.strength_rank == 1 for item in occurrences)
