"""Modifier-engine tests for frozen A-0-B and A-5-B windows."""

from __future__ import annotations

from engines.number_energy.modifier_engine import generate_modifier_pairs
from engines.number_energy.parser import parse_number_string


def test_103_hidden_tian_yi() -> None:
    parsed = parse_number_string("103")
    occurrences, undefined = generate_modifier_pairs(parsed)
    assert undefined == ()
    assert len(occurrences) == 1
    item = occurrences[0]
    assert item.pair_digits == "13"
    assert item.source_digits == "103"
    assert item.energy_id == "tian_yi"
    assert item.strength_rank == 1
    assert item.state == "HIDDEN"
    assert item.via_modifier == 0


def test_153_amplified_tian_yi() -> None:
    parsed = parse_number_string("153")
    occurrences, _undefined = generate_modifier_pairs(parsed)
    item = occurrences[0]
    assert item.energy_id == "tian_yi"
    assert item.strength_rank == 1
    assert item.state == "AMPLIFIED"
    assert item.via_modifier == 5


def test_108_hidden_wu_gui() -> None:
    parsed = parse_number_string("108")
    occurrences, _undefined = generate_modifier_pairs(parsed)
    item = occurrences[0]
    assert item.energy_id == "wu_gui"
    assert item.pair_digits == "18"
    assert item.strength_rank == 1
    assert item.state == "HIDDEN"


def test_consecutive_modifiers_are_undefined() -> None:
    parsed = parse_number_string("1003")
    occurrences, undefined = generate_modifier_pairs(parsed)
    assert occurrences == ()
    assert undefined
    assert all(item.state == "UNKNOWN_OR_NOT_DEFINED" for item in undefined)
