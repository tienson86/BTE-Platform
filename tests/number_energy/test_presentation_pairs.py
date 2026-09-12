"""RB05-A customer-safe pair structure (engine)."""

from __future__ import annotations

from engines.number_energy import NumberEnergyEngine

FORBIDDEN_PAIR_KEYS = {
    "occurrence_id",
    "source_span",
    "energy_id",
    "strength_rank",
    "state",
    "classification",
    "classification_label",
    "via_modifier",
    "notes",
}

GOLDEN_PAIR_ORDER = ["32", "28", "82", "27", "78", "87", "78", "86"]
GOLDEN_DISTRIBUTION = [
    ("Sinh Khí", 2),
    ("Thiên Y", 2),
    ("Diên Niên", 3),
    ("Phục Vị", 0),
    ("Họa Hại", 1),
    ("Ngũ Quỷ", 0),
    ("Lục Sát", 0),
    ("Tuyệt Mệnh", 0),
]


def _phone(number: str = "0328278786"):
    return NumberEnergyEngine().analyze(number, purpose_context="phone_number")


def test_golden_phone_pair_occurrences_order_and_safety() -> None:
    result = _phone()
    pairs = [item.to_dict() for item in result.pair_occurrences]
    assert len(pairs) == 8
    assert [item["pair_digits"] for item in pairs] == GOLDEN_PAIR_ORDER
    assert [item["index"] for item in pairs] == list(range(8))
    first = pairs[0]
    last = pairs[-1]
    assert first["display_name"] == "Họa Hại"
    assert first["category"] == "HUNG"
    assert first["category_label"] == "Hung"
    assert first["strength_label"] == "Nhẹ"
    assert first["strength_slots"] == 1
    assert first["strength_visual"] == [True, False, False, False]
    assert last["display_name"] == "Thiên Y"
    assert last["category"] == "CAT"
    assert last["category_label"] == "Cát"
    assert last["strength_label"] == "Mạnh"
    assert last["strength_slots"] == 3
    assert last["strength_visual"] == [True, True, True, False]
    light = {"32", "28", "82", "27"}
    strong = {"78", "87", "86"}
    for item in pairs:
        assert FORBIDDEN_PAIR_KEYS.isdisjoint(item.keys())
        if item["pair_digits"] in light:
            assert item["strength_label"] == "Nhẹ"
        if item["pair_digits"] in strong:
            assert item["strength_label"] == "Mạnh"


def test_golden_phone_pair_summary_counts_pairs_not_groups() -> None:
    summary = _phone().pair_summary
    assert summary is not None
    payload = summary.to_dict()
    assert payload["pair_count"] == 8
    assert payload["supportive_pair_count"] == 7
    assert payload["challenging_pair_count"] == 1
    assert payload["primary_energy_label"] == "Diên Niên"
    assert payload["terminal_energy_label"] == "Thiên Y"
    assert payload["terminal_pair_digits"] == "86"


def test_golden_phone_distribution_has_eight_rows_and_zeros() -> None:
    rows = [item.to_dict() for item in _phone().energy_distribution]
    assert len(rows) == 8
    assert [(item["energy_label"], item["count"]) for item in rows] == GOLDEN_DISTRIBUTION
    assert all("energy_id" not in item for item in rows)


def test_086_pair_summary_does_not_use_group_counts() -> None:
    result = _phone("0868271327")
    summary = result.pair_summary
    assert summary is not None
    assert summary.pair_count == 8
    assert summary.challenging_pair_count == 2
    assert summary.supportive_pair_count == 6
    reading = result.reading or {}
    assert reading["challenging_group_count"] == 1
    assert reading["supportive_group_count"] == 2
