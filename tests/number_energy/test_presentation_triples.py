"""RB05-B triple occurrences, meaning keys, and customer-safe chain."""

from __future__ import annotations

from engines.number_energy import NumberEnergyEngine

FORBIDDEN_TRIPLE_KEYS = {
    "occurrence_id",
    "source_span",
    "energy_id",
    "strength_rank",
    "state",
    "classification",
    "effect_type",
    "start_index",
    "end_index",
}

GOLDEN_TRIPLE_ORDER = ["328", "282", "827", "278", "787", "878", "786"]
GOLDEN_TITLES = {
    "328": "Khẩu tài tốt",
    "282": "Quý nhân và cơ hội được tăng cường",
    "827": "Quý nhân mang đến Tài vận",
    "278": "Tài đi vào sự nghiệp",
    "787": "Năng lực nghề nghiệp được tăng cường",
    "878": "Năng lực nghề nghiệp được tăng cường",
    "786": "Năng lực nghề nghiệp tạo Tài",
}
FEATURED = {"827", "278", "786"}
STANDARD = {"328", "282"}
COMPACT = {"787", "878"}


def _phone(number: str = "0328278786"):
    return NumberEnergyEngine().analyze(number, purpose_context="phone_number")


def test_golden_phone_triple_order_titles_and_priority() -> None:
    triples = [item.to_dict() for item in _phone().triple_occurrences]
    assert len(triples) == 7
    assert [item["digits"] for item in triples] == GOLDEN_TRIPLE_ORDER
    for item in triples:
        digits = item["digits"]
        assert item["customer_title"] == GOLDEN_TITLES[digits]
        assert item["interpretation_status"] == "DEFINED"
        assert item["canonical_meaning_key"]
        assert item["customer_summary_key"]
        assert item["customer_summary"]
        assert " → " in item["interaction_label"]
        assert FORBIDDEN_TRIPLE_KEYS.isdisjoint(item.keys())
        if digits in FEATURED:
            assert item["priority"] == "FEATURED"
        elif digits in STANDARD:
            assert item["priority"] == "STANDARD"
        elif digits in COMPACT:
            assert item["priority"] == "COMPACT"
    assert triples[0]["left_pair_digits"] == "32"
    assert triples[0]["right_pair_digits"] == "28"
    assert triples[0]["left_energy_label"] == "Họa Hại"
    assert triples[0]["right_energy_label"] == "Sinh Khí"
    assert triples[0]["interaction_label"] == "Họa Hại → Sinh Khí"
    assert triples[-1]["digits"] == "786"
    assert triples[-1]["interaction_label"] == "Diên Niên → Thiên Y"


def test_golden_phone_chain_primary_and_terminal() -> None:
    chain = _phone().chain
    assert chain is not None
    payload = chain.to_dict()
    assert payload["primary_energy_label"] == "Diên Niên"
    assert payload["primary_energy_pairs"] == ["78", "87", "78"]
    assert payload["secondary_energy_labels"] == ["Sinh Khí", "Thiên Y"]
    assert payload["terminal_pair_digits"] == "86"
    assert payload["terminal_energy_label"] == "Thiên Y"
    assert payload["terminal_triple_digits"] == "786"
    assert payload["terminal_interaction_label"] == "Diên Niên → Thiên Y"
    assert payload["dominant_flow_summary"] == "Diên Niên chủ đạo, kết Thiên Y"
    assert "energy_id" not in payload


def test_short_phone_has_no_triples_but_has_terminal_pair() -> None:
    result = _phone("103")
    assert result.triple_occurrences == ()
    assert result.chain is not None
    assert result.chain.terminal_pair_digits == "13"
    assert result.chain.terminal_energy_label == "Thiên Y"
    assert result.chain.terminal_triple_digits is None
