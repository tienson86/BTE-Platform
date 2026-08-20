"""UG-R2 — Điều hậu / climate cannot win Overall Useful God."""

from __future__ import annotations

from applications.api.services.orchestrator import OrchestratorService
from engines.useful_god_engine.context import UsefulGodContext
from engines.useful_god_engine.engine import UsefulGodEngine
from engines.useful_god_engine.layers import OVERALL_INCOMPLETE_MESSAGE


def _calculate(context: UsefulGodContext):
    return UsefulGodEngine().calculate(context)


def test_climate_rules_never_win_overall() -> None:
    result = _calculate(
        UsefulGodContext(
            day_master="Canh",
            strength_level="strong",
            season="winter",
            temperature_type="cold",
        )
    )
    assert result.winning_rule_group not in {"season", "temperature"}
    assert result.climate_rule_group in {"season", "temperature"}
    assert result.winning_rule_id == "str_004"
    assert result.climate_rule_id == "sea_001"
    assert result.useful_god != result.climate_candidate


def test_no_silent_fallback_to_climate_when_structure_missing() -> None:
    result = _calculate(
        UsefulGodContext(
            day_master="Canh",
            season="summer",
            temperature_type="hot",
        )
    )
    assert result.overall_incomplete is True
    assert result.success is False
    assert result.useful_god is None
    assert result.winning_rule_id == ""
    assert result.useful_display == OVERALL_INCOMPLETE_MESSAGE
    assert result.error == OVERALL_INCOMPLETE_MESSAGE
    assert result.climate_rule_id == "sea_002"
    assert result.climate_candidate == "Nhâm"
    assert result.favorable_gods == []
    assert result.unfavorable_gods == []


def test_tuyen_structural_overall_is_not_sea_002() -> None:
    payload = OrchestratorService().analyze(
        year=1984, month=7, day=13, hour=21, minute=1, gender="female"
    )
    useful = payload["useful_god"]
    assert useful["winning_rule_id"] != "sea_002"
    assert useful["winning_rule_group"] not in {"season", "temperature"}
    assert useful["winning_rule_id"] == "str_003"
    assert useful["useful_stem"] == "Ất"
    assert useful["useful_element"] == "Mộc"
    assert useful["useful_ten_god"] == "Chính Quan"
    assert useful["climate_rule_id"] == "sea_002"
    assert useful["climate_candidate"] == "Nhâm"
    assert useful["climate_element"] == "Thủy"
    assert useful["climate_preference_label"] == "Điều hậu ưu tiên Thủy"
    assert useful["useful_god"] != useful["climate_candidate"]
    assert "Chính Quan" in useful["favorable_gods"]
    assert "Thực Thần" in useful["favorable_gods"]
    assert "Tỷ Kiên" in useful["unfavorable_gods"]
    assert useful["favorable_gods"] != ["Nhâm", "Quý", "Canh"]
