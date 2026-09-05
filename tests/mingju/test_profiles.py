"""Achievement, Wealth, and Career profile tests."""

from __future__ import annotations

from engines.mingju import analyze_mingju
from tests.mingju.conftest import context_from


def test_achievement_is_multidimensional_not_biography() -> None:
    result = analyze_mingju(context_from())
    ids = {item.dimension for item in result.achievement.dimensions}
    assert {
        "authority",
        "institutional_career",
        "leadership",
        "management",
        "entrepreneurship",
        "academic",
        "technical",
        "creative",
        "public_visibility",
        "independence",
        "stability",
    } <= ids
    assert result.achievement.dominant_capabilities
    assert "biography" not in result.achievement.structural_risks


def test_wealth_preserves_frozen_dimensions_and_volatility_polarity() -> None:
    result = analyze_mingju(context_from())
    by_name = {item.dimension: item for item in result.wealth.dimensions}
    assert {
        "wealth_creation",
        "wealth_accumulation",
        "wealth_retention",
        "business_expansion",
        "financial_volatility",
    } <= set(by_name)
    assert by_name["financial_volatility"].polarity == "higher_is_riskier"
    assert by_name["wealth_creation"].polarity == "higher_is_better"


def test_career_does_not_emit_exact_professions() -> None:
    result = analyze_mingju(context_from())
    ids = {item.dimension for item in result.career.dimensions}
    assert "entrepreneurial_fit" in ids
    assert "institutional_fit" in ids
    joined = " ".join(result.career.dominant_work_styles)
    assert "kỹ sư" not in joined.lower()
    assert "bác sĩ" not in joined.lower()
    assert "công chức" not in joined.lower()
