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


def test_601_keeps_source_digits_for_liu_sha() -> None:
    parsed = parse_number_string("601")
    occurrences, _undefined = generate_modifier_pairs(parsed)
    item = occurrences[0]
    assert item.energy_id == "liu_sha"
    assert item.pair_digits == "61"
    assert item.source_digits == "601"


def test_120_is_one_post_modified_jue_ming_occurrence() -> None:
    parsed = parse_number_string("120")
    occurrences, undefined = generate_modifier_pairs(parsed)
    assert undefined == ()
    assert len(occurrences) == 1
    item = occurrences[0]
    assert item.source_digits == "120"
    assert item.pair_digits == "12"
    assert item.energy_id == "jue_ming"
    assert item.state == "HIDDEN"
    assert item.via_modifier == 0


def test_125_is_one_post_amplified_jue_ming_occurrence() -> None:
    parsed = parse_number_string("125")
    occurrences, undefined = generate_modifier_pairs(parsed)
    assert undefined == ()
    assert len(occurrences) == 1
    assert occurrences[0].source_digits == "125"
    assert occurrences[0].state == "AMPLIFIED"


def test_1205_preserves_supported_zero_five_tail_chain() -> None:
    parsed = parse_number_string("1205")
    occurrences, undefined = generate_modifier_pairs(parsed)
    assert undefined == ()
    assert len(occurrences) == 1
    assert occurrences[0].source_digits == "1205"
    assert occurrences[0].pair_digits == "12"
    assert occurrences[0].via_modifier == 0


def test_6058_preserves_supported_interposed_zero_five_chain() -> None:
    parsed = parse_number_string("6058")
    occurrences, undefined = generate_modifier_pairs(parsed)

    assert undefined == ()
    assert len(occurrences) == 1
    assert occurrences[0].source_digits == "6058"
    assert occurrences[0].pair_digits == "68"
    assert occurrences[0].energy_id == "tian_yi"
    assert occurrences[0].via_modifier == 0


def test_consecutive_modifiers_are_undefined() -> None:
    parsed = parse_number_string("1003")
    occurrences, undefined = generate_modifier_pairs(parsed)
    assert occurrences == ()
    assert undefined
    assert all(item.state == "UNKNOWN_OR_NOT_DEFINED" for item in undefined)
