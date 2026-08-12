"""Live StrengthResult → PublishedStrengthFacts adapter tests."""

from __future__ import annotations

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from engines.interpretation_engine_v2.strength.runtime.case_0001 import load_case_0001_facts
from engines.interpretation_engine_v2.strength.runtime.published_facts_adapter import (
    build_published_strength_facts,
)


def test_live_adapter_builds_published_facts() -> None:
    """Generic adapter produces PublishedStrengthFacts from live engine output."""
    output = ProductionEngineRunner().run(CASE_0001_REQUEST)
    published = build_published_strength_facts(
        case_id=CASE_0001_REQUEST.case_id,
        strength_result=output.strength_result,
        strength_context=output.strength_context,
    )
    assert published.case_id == "CASE-0001"
    assert published.class_id == output.strength_result.strength_level
    assert published.strength_score == output.strength_result.strength_score
    assert "classification" in published.facts
    assert "season" in published.facts


def test_case_0001_live_adapter_matches_calibration_core() -> None:
    """Live adapter core fields align with frozen CASE-0001 calibration."""
    output = ProductionEngineRunner().run(CASE_0001_REQUEST)
    live = build_published_strength_facts(
        case_id=CASE_0001_REQUEST.case_id,
        strength_result=output.strength_result,
        strength_context=output.strength_context,
    )
    golden = load_case_0001_facts()
    assert live.class_id == golden.class_id
    assert abs(live.strength_score - golden.strength_score) < 0.01
    assert live.facts["season"] == golden.facts["season"]
    assert live.facts["root"] == golden.facts["root"]
    assert live.facts["support"] == golden.facts["support"]
    assert live.facts["control"] == golden.facts["control"]
    assert live.facts["special"] == golden.facts["special"]
    assert live.facts["drain"] == golden.facts["drain"]
