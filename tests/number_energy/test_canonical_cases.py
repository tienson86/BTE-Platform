"""Canonical sequence tests from NUMBER_ENERGY_INTERACTION_RULES_V1."""

from __future__ import annotations

import pytest

from engines.number_energy import NumberEnergyEngine, NumberEnergyValidationError
from engines.number_energy.constants import FORBIDDEN_CUSTOMER_PHRASES


def _analyze(number: str, purpose_context: str = "generic_number"):
    return NumberEnergyEngine().analyze(number, purpose_context=purpose_context)


def test_103_tian_yi_rank_1_hidden() -> None:
    result = _analyze("103")
    assert len(result.occurrences) == 1
    item = result.occurrences[0]
    assert item.energy_id == "tian_yi"
    assert item.display_name == "Thiên Y"
    assert item.strength_rank == 1
    assert item.classification == "supportive"
    assert item.state == "HIDDEN"
    assert item.source_span == (0, 2)
    assert item.source_digits == "103"
    assert item.pair_digits == "13"
    assert result.sequence_state == "HIDDEN"
    assert "NEUTRALIZED" not in result.sequence_states


def test_153_tian_yi_rank_1_amplified() -> None:
    result = _analyze("153")
    item = result.occurrences[0]
    assert item.energy_id == "tian_yi"
    assert item.display_name == "Thiên Y"
    assert item.strength_rank == 1
    assert item.state == "AMPLIFIED"
    assert item.via_modifier == 5
    assert result.sequence_state == "AMPLIFIED"


def test_108_wu_gui_rank_1_hidden() -> None:
    result = _analyze("108")
    item = result.occurrences[0]
    assert item.energy_id == "wu_gui"
    assert item.display_name == "Ngũ Quỷ"
    assert item.strength_rank == 1
    assert item.state == "HIDDEN"
    assert item.pair_digits == "18"
    assert result.sequence_state == "HIDDEN"


def test_1414_sheng_qi_repeated() -> None:
    result = _analyze("1414")
    assert [item.energy_id for item in result.occurrences] == [
        "sheng_qi",
        "sheng_qi",
        "sheng_qi",
    ]
    assert [item.pair_digits for item in result.occurrences] == ["14", "41", "14"]
    assert all(item.strength_rank == 1 for item in result.occurrences)
    assert any(item.state == "REPEATED" for item in result.occurrences)
    assert result.sequence_state == "REPEATED"
    assert result.summary.repeated_energy_ids == ("sheng_qi",)


def test_141319_supportive_chain() -> None:
    result = _analyze("141319")
    assert [item.pair_digits for item in result.occurrences] == [
        "14",
        "41",
        "13",
        "31",
        "19",
    ]
    first_seen: list[str] = []
    for item in result.occurrences:
        if item.energy_id not in first_seen:
            first_seen.append(item.energy_id)
    assert first_seen == ["sheng_qi", "tian_yi", "yan_nian"]
    assert [item.display_name for item in result.occurrences] == [
        "Sinh Khí",
        "Sinh Khí",
        "Thiên Y",
        "Thiên Y",
        "Diên Niên",
    ]
    assert all(item.strength_rank == 1 for item in result.occurrences)
    assert "approved_supportive_chain" in result.approved_patterns
    assert result.summary.approved_supportive_chain is True
    assert "REPEATED" in result.sequence_states


def test_219_jue_ming_and_yan_nian_not_neutralized() -> None:
    result = _analyze("219")
    assert [item.energy_id for item in result.occurrences] == ["jue_ming", "yan_nian"]
    assert [item.strength_rank for item in result.occurrences] == [1, 1]
    assert result.occurrences[0].display_name == "Tuyệt Mệnh"
    assert result.occurrences[1].display_name == "Diên Niên"
    assert all(item.state == "NORMAL" for item in result.occurrences)
    assert "NEUTRALIZED" not in result.sequence_states
    assert "CONTROLLED" not in result.sequence_states
    assert "jue_ming" in result.summary.challenging_without_control
    text = result.narrative.summary
    assert "Thiên Y" in text
    assert "Diên Niên" in text


def test_216_jue_ming_and_liu_sha_without_control() -> None:
    result = _analyze("216")
    assert [item.energy_id for item in result.occurrences] == ["jue_ming", "liu_sha"]
    assert [item.display_name for item in result.occurrences] == ["Tuyệt Mệnh", "Lục Sát"]
    assert all(item.state == "NORMAL" for item in result.occurrences)
    assert result.summary.controlled_energy_ids == ()
    assert "jue_ming" in result.summary.challenging_without_control
    assert "liu_sha" in result.summary.challenging_without_control
    assert "NEUTRALIZED" not in result.sequence_states
    assert "CONTROLLED" not in result.sequence_states


@pytest.mark.parametrize("number", ["1003", "1553", "1053", "1503", "505", "000", "555"])
def test_undefined_consecutive_modifiers(number: str) -> None:
    result = _analyze(number)
    assert result.sequence_state == "UNKNOWN_OR_NOT_DEFINED"
    assert result.undefined_segments
    assert all(
        item.state == "UNKNOWN_OR_NOT_DEFINED" for item in result.undefined_segments
    )
    assert "UNKNOWN_OR_NOT_DEFINED" in (result.narrative.unknown_notice or "")


def test_unlisted_chain_extension_is_not_approved() -> None:
    result = _analyze("14131914")
    assert "approved_supportive_chain" not in result.approved_patterns
    assert result.summary.approved_supportive_chain is False


def test_narrative_uses_system_name_and_both_sides() -> None:
    result = _analyze("1414", purpose_context="phone_number")
    narrative = result.narrative
    assert narrative.system_name == "Bát Cực Linh Số"
    assert narrative.system_short_name == "Năng lượng số"
    assert "Bát Cực Linh Số" in narrative.summary
    assert narrative.strengths
    assert narrative.watchouts
    assert narrative.health_disclaimer
    assert "không phải chẩn đoán y khoa" in narrative.health_disclaimer
    blob = " ".join(
        [
            narrative.summary,
            *narrative.paragraphs,
            *narrative.strengths,
            *narrative.watchouts,
        ]
    ).lower()
    for phrase in FORBIDDEN_CUSTOMER_PHRASES:
        assert phrase.lower() not in blob
    assert "đây là supportive" not in blob
    assert "đây là challenging" not in blob
    assert "trường khí hỗ trợ" in " ".join(narrative.paragraphs).lower()


def test_unknown_sequence_still_has_health_disclaimer() -> None:
    result = _analyze("1003")
    assert result.narrative.health_disclaimer
    assert "không phải chẩn đoán y khoa" in result.narrative.health_disclaimer
    assert result.narrative.unknown_notice


def test_challenging_copy_uses_control_framing() -> None:
    result = _analyze("108")
    blob = " ".join(result.narrative.paragraphs).lower()
    assert "trường khí cần kiểm soát" in blob
    assert "đây là challenging" not in blob


def test_invalid_purpose_context_is_rejected() -> None:
    with pytest.raises(NumberEnergyValidationError):
        _analyze("1414", purpose_context="lottery_number")
