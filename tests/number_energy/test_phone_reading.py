"""Phone Number Reading V1.1 — purpose_context=phone_number only."""

from __future__ import annotations

from engines.number_energy import NumberEnergyEngine
from engines.number_energy.constants import PHONE_INTERIOR_ZERO_NOTE, PHONE_LIFTED_NOTE


def _phone(number: str):
    return NumberEnergyEngine().analyze(number, purpose_context="phone_number")


def test_leading_zero_is_prefix_not_unknown() -> None:
    result = _phone("0328278786")
    assert result.leading_phone_zero is True
    assert result.analyzed_input == "328278786"
    assert result.input_raw == "0328278786"
    assert result.sequence_state != "UNKNOWN_OR_NOT_DEFINED"
    assert not result.undefined_segments
    reading = result.reading or {}
    assert reading["analyzed_number"] == "328278786"
    assert "UNKNOWN_OR_NOT_DEFINED" not in reading["summary"]
    assert [item["pair_digits"] for item in reading["pairs"]] == [
        "32",
        "28",
        "82",
        "27",
        "78",
        "87",
        "78",
        "86",
    ]
    assert [item["display_name"] for item in reading["pairs"]] == [
        "Họa Hại",
        "Sinh Khí",
        "Sinh Khí",
        "Thiên Y",
        "Diên Niên",
        "Diên Niên",
        "Diên Niên",
        "Thiên Y",
    ]


def test_phone_dominant_and_ending() -> None:
    reading = _phone("0328278786").reading or {}
    assert reading["dominant"]["display_name"] == "Diên Niên"
    assert reading["ending"]["pair_digits"] == "86"
    assert reading["ending"]["display_name"] == "Thiên Y"
    assert reading["supportive_group_count"] == 3
    assert reading["challenging_group_count"] == 1
    assert reading["lifted"] is True
    assert reading["lifted_note"] == PHONE_LIFTED_NOTE
    assert "NEUTRALIZED" not in str(reading)
    assert reading["triplets"][0]["digits"] == "328"
    assert reading["triplets"][0]["left_name"] == "Họa Hại"
    assert reading["triplets"][0]["right_name"] == "Sinh Khí"


def test_phone_summary_mentions_prefix_and_lift() -> None:
    summary = (_phone("0328278786").reading or {})["summary"]
    assert "đầu số 0 hợp lệ" in summary
    assert "Diên Niên" in summary
    assert "Họa Hại" in summary
    assert "Sinh Khí" in summary


def test_interior_zero_soft_warning() -> None:
    result = _phone("103")
    reading = result.reading or {}
    assert result.analyzed_input == "103"
    assert reading["interior_zero_note"] == PHONE_INTERIOR_ZERO_NOTE
    assert result.occurrences[0].display_name == "Thiên Y"
    assert result.occurrences[0].state == "HIDDEN"
    assert "unused modifier" not in str(reading).lower()


def test_generic_leading_zero_still_uses_full_string() -> None:
    result = NumberEnergyEngine().analyze("0328278786", purpose_context="generic_number")
    assert result.analyzed_input == "0328278786"
    assert result.leading_phone_zero is False
