"""Interaction and control-relation tests."""

from __future__ import annotations

from engines.number_energy import NumberEnergyEngine


def test_sheng_qi_controls_wu_gui() -> None:
    result = NumberEnergyEngine().analyze("1418")
    names = {item.energy_id: item.state for item in result.occurrences}
    assert "sheng_qi" in names
    assert names["wu_gui"] == "CONTROLLED"
    assert "NEUTRALIZED" not in result.sequence_states
    assert "wu_gui" in result.summary.controlled_energy_ids


def test_tian_yi_controls_jue_ming() -> None:
    result = NumberEnergyEngine().analyze("1321")
    states = {
        item.energy_id: item.state
        for item in result.occurrences
        if item.energy_id == "jue_ming"
    }
    assert states["jue_ming"] == "CONTROLLED"
    assert "NEUTRALIZED" not in result.sequence_states


def test_yan_nian_controls_liu_sha() -> None:
    result = NumberEnergyEngine().analyze("1916")
    states = {
        item.energy_id: item.state
        for item in result.occurrences
        if item.energy_id == "liu_sha"
    }
    assert states["liu_sha"] == "CONTROLLED"
    assert "NEUTRALIZED" not in result.sequence_states


def test_huo_hai_has_no_direct_control() -> None:
    result = NumberEnergyEngine().analyze("1714")
    huo_hai = [item for item in result.occurrences if item.energy_id == "huo_hai"]
    assert huo_hai
    assert all(item.state != "CONTROLLED" for item in huo_hai)
    assert "huo_hai" not in result.summary.controlled_energy_ids


def test_fu_wei_supported_by_sheng_qi() -> None:
    result = NumberEnergyEngine().analyze("1114")
    assert result.summary.fu_wei_supported is True
    fu_wei = [item for item in result.occurrences if item.energy_id == "fu_wei"]
    assert fu_wei
    assert all(item.state != "NEUTRALIZED" for item in result.occurrences)
