"""Customer-safe zero/five meanings by energy and modifier position."""

from __future__ import annotations

import pytest

from engines.number_energy import NumberEnergyEngine


def _pair(number: str):
    result = NumberEnergyEngine().analyze(number, purpose_context="id_number")
    assert len(result.pair_occurrences) == 1
    return result.pair_occurrences[0]


@pytest.mark.parametrize(
    ("number", "energy", "phrase"),
    [
        ("102", "Tuyệt Mệnh", "đầu tư bị mắc kẹt"),
        ("107", "Họa Hại", "khó truyền đạt trọn ý"),
        ("601", "Lục Sát", "u buồn"),
        ("108", "Ngũ Quỷ", "suy nghĩ nhiều"),
        ("103", "Thiên Y", "chậm quay vòng"),
        ("104", "Sinh Khí", "quý nhân và cơ hội ở trạng thái ẩn"),
        ("109", "Diên Niên", "sự nghiệp dễ bị đình trệ"),
    ],
)
def test_zero_interposed_meanings(number: str, energy: str, phrase: str) -> None:
    item = _pair(number)
    assert item.pair_digits == number
    assert item.display_name == energy
    assert phrase in (item.modifier_note or "")


@pytest.mark.parametrize(
    ("number", "energy", "phrase"),
    [
        ("152", "Tuyệt Mệnh", "biểu hiện nổi bật"),
        ("157", "Họa Hại", "phát sinh liên tiếp"),
        ("651", "Lục Sát", "cảm xúc và quan hệ biểu hiện rõ"),
        ("158", "Ngũ Quỷ", "tư duy và biến động"),
        ("153", "Thiên Y", "đòi hỏi nhiều công sức"),
        ("154", "Sinh Khí", "quý nhân và cơ hội nổi bật"),
        ("159", "Diên Niên", "thực lực được nhìn thấy rõ"),
    ],
)
def test_five_interposed_meanings(number: str, energy: str, phrase: str) -> None:
    item = _pair(number)
    assert item.pair_digits == number
    assert item.display_name == energy
    assert phrase in (item.modifier_note or "")


def test_tian_yi_13_31_gets_relationship_qualifier() -> None:
    assert "mối quan hệ thứ ba" in (_pair("103").modifier_note or "")
    assert "hạn chế thị phi" in (_pair("153").modifier_note or "")


def test_post_zero_five_have_distinct_meanings_and_keep_digits() -> None:
    post_zero = _pair("120")
    post_five = _pair("125")
    post_zero_five = _pair("1205")

    assert post_zero.pair_digits == "120"
    assert "thành quả cuối cùng khó tích tụ" in (post_zero.modifier_note or "")
    assert post_five.pair_digits == "125"
    assert "xu hướng đầu tư kéo dài" in (post_five.modifier_note or "")
    assert post_zero_five.pair_digits == "1205"
    assert "thành quả sau cùng dễ bị rút bớt" in (
        post_zero_five.modifier_note or ""
    )


def test_interposed_zero_five_keeps_all_digits_and_combined_meaning() -> None:
    item = _pair("6058")

    assert item.pair_digits == "6058"
    assert item.display_name == "Thiên Y"
    assert "tài nguyên ban đầu dễ bị ẩn" in (item.modifier_note or "")
    assert "được làm lộ và tăng cường" in (item.modifier_note or "")


@pytest.mark.parametrize(
    ("purpose_context", "number", "expected_digits", "phrase"),
    [
        ("phone_number", "0102123456", "102", "đầu tư bị mắc kẹt"),
        ("phone_number", "0912345120", "120", "thành quả cuối cùng khó tích tụ"),
        ("phone_number", "0912345152", "152", "biểu hiện nổi bật"),
        ("phone_number", "0912345125", "125", "xu hướng đầu tư kéo dài"),
        ("phone_number", "0912341205", "1205", "thành quả sau cùng dễ bị rút bớt"),
        ("car_plate", "30A-102", "102", "đầu tư bị mắc kẹt"),
        ("car_plate", "30A-120", "120", "thành quả cuối cùng khó tích tụ"),
        ("car_plate", "30A-152", "152", "biểu hiện nổi bật"),
        ("car_plate", "30A-125", "125", "xu hướng đầu tư kéo dài"),
        ("car_plate", "30A-1205", "1205", "thành quả sau cùng dễ bị rút bớt"),
        ("motorbike_plate", "30A1-102", "102", "đầu tư bị mắc kẹt"),
        ("motorbike_plate", "30A1-125", "125", "xu hướng đầu tư kéo dài"),
        ("id_number", "00102", "102", "đầu tư bị mắc kẹt"),
        ("id_number", "00120", "120", "thành quả cuối cùng khó tích tụ"),
        ("id_number", "00152", "152", "biểu hiện nổi bật"),
        ("id_number", "00125", "125", "xu hướng đầu tư kéo dài"),
        ("id_number", "001205", "1205", "thành quả sau cùng dễ bị rút bớt"),
        ("id_number", "B102", "102", "đầu tư bị mắc kẹt"),
    ],
)
def test_zero_five_rules_apply_to_every_customer_input_type(
    purpose_context: str,
    number: str,
    expected_digits: str,
    phrase: str,
) -> None:
    result = NumberEnergyEngine().analyze(number, purpose_context=purpose_context)
    item = next(
        pair for pair in result.pair_occurrences if pair.pair_digits == expected_digits
    )

    assert phrase in (item.modifier_note or "")
