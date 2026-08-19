"""Strength V1.0 classification boundary tests. Does not change thresholds."""

from __future__ import annotations

from engines.strength_engine.context import StrengthContext
from engines.strength_engine.loader import StrengthLoader
from engines.strength_engine.matcher import StrengthMatcher
from engines.strength_engine.priority import StrengthPriorityResolver


def _classify(score: float) -> str:
    loader = StrengthLoader("database/12_strength")
    ctx = StrengthContext()
    ctx.strength_score = score
    winner = StrengthPriorityResolver(loader.load_priority_rules()).resolve_level(
        ctx,
        loader.load_level_rules(),
        StrengthMatcher(),
    )
    assert winner is not None
    return str(winner.get("strength_level"))


def test_taxonomy_is_three_classes_only() -> None:
    loader = StrengthLoader("database/12_strength")
    levels = {
        str(row.get("strength_level"))
        for row in loader.load_level_rules()
        if row.get("strength_level")
    }
    assert levels == {"strong", "weak", "balanced"}


def test_strong_lower_boundary_inclusive() -> None:
    assert _classify(0.65) == "strong"
    assert _classify(0.651) == "strong"
    assert _classify(0.649) == "balanced"


def test_weak_upper_boundary_inclusive() -> None:
    assert _classify(0.35) == "weak"
    assert _classify(0.349) == "weak"
    assert _classify(0.351) == "balanced"


def test_middle_and_extremes() -> None:
    assert _classify(0.50) == "balanced"
    assert _classify(0.0) == "weak"
    assert _classify(1.0) == "strong"


def test_no_gap_or_overlap_on_boundaries() -> None:
    """Adjacent samples around thresholds map to exactly one class."""
    samples = {
        0.35: "weak",
        0.351: "balanced",
        0.649: "balanced",
        0.65: "strong",
    }
    for score, expected in samples.items():
        assert _classify(score) == expected
