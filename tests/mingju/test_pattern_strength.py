"""MC-01 Pattern Strength is not Day Master Strength."""

from __future__ import annotations

from engines.mingju import analyze_mingju
from tests.mingju.conftest import context_from, hidden, visible


def test_pattern_strength_uses_pattern_deity_not_day_master_score() -> None:
    weak_dm = analyze_mingju(context_from(strength={"strength_level": "weak", "strength_score": 12.0}))
    strong_dm = analyze_mingju(
        context_from(strength={"strength_level": "extremely_strong", "strength_score": 96.0})
    )
    assert weak_dm.pattern_strength.state == "resolved"
    assert strong_dm.pattern_strength.state == "resolved"
    assert weak_dm.pattern_strength.score == strong_dm.pattern_strength.score
    assert weak_dm.pattern_strength.classification != "unresolved"


def test_month_command_alignment_raises_season_power() -> None:
    aligned = analyze_mingju(context_from())
    conflicted = analyze_mingju(
        context_from(
            pattern={
                "success": True,
                "pattern": "chinh_an",
                "cach_cuc": "Chính Ấn",
                "month_main_qi_ten_god": "Thương Quan",
                "day_master": "Canh",
            }
        )
    )
    assert aligned.pattern_strength.season_power is not None
    assert conflicted.pattern_strength.season_power is not None
    assert aligned.pattern_strength.season_power > conflicted.pattern_strength.season_power
