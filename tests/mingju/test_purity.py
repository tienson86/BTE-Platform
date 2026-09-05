"""MC-01 Pattern Purity tests."""

from __future__ import annotations

from engines.mingju import analyze_mingju
from tests.mingju.conftest import base_payload, context_from, hidden, visible


def test_purity_resolves_when_pattern_is_identified() -> None:
    result = analyze_mingju(context_from())
    assert result.purity.state == "resolved"
    assert result.purity.classification in {
        "very_pure",
        "pure",
        "moderately_pure",
        "mixed",
        "heavily_mixed",
        "structurally_impure",
    }
    assert result.purity.score is not None
    assert 0 <= result.purity.score <= 100
    assert result.purity.evidence_ids


def test_counterpart_mixing_lowers_purity() -> None:
    clean = analyze_mingju(context_from())
    mixed = analyze_mingju(
        context_from(
            ten_gods={
                "visible": [
                    visible("month", "zheng_yin", "Chính Ấn", "Ất"),
                    visible("hour", "pian_yin", "Thiên Ấn", "Bính"),
                    visible("year", "pian_yin", "Thiên Ấn", "Mậu"),
                ],
                "hidden": [hidden("month", "zheng_yin", "Chính Ấn", "primary")],
            }
        )
    )
    assert mixed.purity.score is not None
    assert clean.purity.score is not None
    assert mixed.purity.score < clean.purity.score
    assert any(factor.factor_type == "counterpart_mixing" for factor in mixed.purity.factors)


def test_unresolved_pattern_does_not_score_purity() -> None:
    result = analyze_mingju(
        context_from(pattern={"success": False, "pattern": "", "cach_cuc": ""})
    )
    assert result.purity.state == "unresolved"
    assert result.purity.score is None
    assert result.purity.classification == "unresolved"
