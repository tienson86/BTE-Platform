"""Sprint B1 — Useful God interpreter tests."""

from __future__ import annotations

import pytest

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.models import ProductionRequest
from engines.interpretation_engine.foundation.facts.useful_god import (
    UsefulGodCandidateFact,
    UsefulGodInterpretationFacts,
)
from engines.interpretation_engine.foundation.interpreters.useful_god import (
    UsefulGodInterpreter,
)
from engines.interpretation_engine.foundation.interpreters.useful_god.templates import (
    IMPACT_DOMAINS,
    RECOMMENDATION_CATEGORIES,
)
from engines.interpretation_engine.foundation.status import DataAvailability

HUYNH = ProductionRequest(
    year=1966,
    month=9,
    day=24,
    hour=4,
    minute=15,
    gender="male",
    full_name="Lương Ngọc Huỳnh",
)


@pytest.fixture(scope="module")
def huynh_interpretation():
    """Useful God interpretation for Lương Ngọc Huỳnh."""
    output = ProductionEngineRunner().run(HUYNH)
    foundation = output.interpretation_foundation
    assert foundation is not None
    assert foundation.useful_god_interpretation is not None
    return foundation.useful_god_interpretation


@pytest.fixture(scope="module")
def case0001_interpretation():
    """Useful God interpretation for CASE-0001."""
    output = ProductionEngineRunner().run(CASE_0001_REQUEST)
    foundation = output.interpretation_foundation
    assert foundation is not None
    assert foundation.useful_god_interpretation is not None
    return foundation.useful_god_interpretation


def test_observation_generated(huynh_interpretation) -> None:
    """Observation section contains fact-only lines."""
    obs = huynh_interpretation.observations
    assert len(obs) >= 7
    joined = " ".join(obs)
    assert "Nhật chủ" in joined
    assert "Bính" in joined
    assert "Dụng thần" in joined
    assert "Hỷ thần" in joined
    assert "Kỵ thần" in joined
    assert "Chính Tài" in joined


def test_reasoning_generated(huynh_interpretation) -> None:
    """Reasoning explains selection and rejection."""
    reasoning = " ".join(huynh_interpretation.reasoning)
    assert "Chính Tài" in reasoning
    assert len(huynh_interpretation.reasoning) >= 3
    assert "Engine chọn" in reasoning or "Engine chọn" in reasoning


def test_evidence_preserved(huynh_interpretation) -> None:
    """Evidence preserves rule IDs and candidate scores."""
    ev = huynh_interpretation.evidence
    assert "str_005" in ev.selected_rule_id
    assert "str_005" in ev.rule_ids
    assert ev.confidence == pytest.approx(0.72, abs=0.01)
    assert ev.engine_source == "UsefulGodEngine"
    assert len(ev.candidate_scores) >= 4
    rule_ids = {item.rule_id for item in ev.candidate_scores}
    assert "tmp_003" in rule_ids


def test_conclusion_generated(huynh_interpretation) -> None:
    """Conclusion summarizes main useful god and Hỷ/Kỵ."""
    text = " ".join(huynh_interpretation.conclusions)
    assert "Chính Tài" in text
    assert "Hỷ thần" in text
    assert "Kỵ thần" in text
    assert "Kiếp Tài" in text


def test_impacts_generated(huynh_interpretation) -> None:
    """Impacts cover required life domains."""
    domains = {item.domain for item in huynh_interpretation.impacts}
    assert domains >= set(IMPACT_DOMAINS)
    assert all(item.text for item in huynh_interpretation.impacts)


def test_recommendations_generated(huynh_interpretation) -> None:
    """Recommendations are structured by category."""
    categories = {group.category for group in huynh_interpretation.recommendations}
    assert categories >= set(RECOMMENDATION_CATEGORIES)
    assert all(group.items for group in huynh_interpretation.recommendations)


def test_warnings_generated(huynh_interpretation) -> None:
    """Warnings reference unfavorable elements and useful god."""
    text = " ".join(huynh_interpretation.warnings)
    assert "Kỵ thần" in text or "Kiếp Tài" in text
    assert "Chính Tài" in text


def test_rejected_candidate_explanation(huynh_interpretation) -> None:
    """Rejected candidates (Bính, Canh, Nhâm) are explained."""
    reasoning = " ".join(huynh_interpretation.reasoning)
    assert "Bính" in reasoning
    assert "Canh" in reasoning or "Nhâm" in reasoning
    assert "tmp_003" not in reasoning or "Bính" in reasoning


def test_huynh_why_dinh_not_binh(huynh_interpretation) -> None:
    """Huỳnh acceptance: explain why Đinh won and Bính lost."""
    reasoning = " ".join(huynh_interpretation.reasoning)
    assert "Chính Tài" in reasoning
    assert "Bính" in reasoning
    assert "mùa" in reasoning.lower() or "lệnh tháng" in reasoning.lower() or "season" in reasoning.lower()


def test_huynh_hy_ky_meaning(huynh_interpretation) -> None:
    """Huỳnh acceptance: Hỷ and Kỵ meaning in conclusions/impacts."""
    conclusion = " ".join(huynh_interpretation.conclusions)
    assert "Chính Tài" in conclusion
    assert "Kiếp Tài" in conclusion
    impacts = " ".join(item.text for item in huynh_interpretation.impacts)
    assert "Hỷ" in impacts or "Chính Tài" in impacts


def test_huynh_domain_implications(huynh_interpretation) -> None:
    """Huỳnh acceptance: career, wealth, relationship, health implications."""
    by_domain = {item.domain: item.text for item in huynh_interpretation.impacts}
    assert "career" in by_domain and by_domain["career"]
    assert "wealth" in by_domain and by_domain["wealth"]
    assert "relationships" in by_domain and by_domain["relationships"]
    assert "health" in by_domain and by_domain["health"]


def test_no_score_derived_explanation(huynh_interpretation) -> None:
    """No score-derived explanation in output."""
    full = huynh_interpretation.to_dict()
    text = str(full)
    assert "total_score" not in text
    assert "wuxing_score" not in text
    assert "grade" not in text.lower() or "grade" not in " ".join(huynh_interpretation.observations)


def test_no_html_dependency(huynh_interpretation) -> None:
    """Output contains no HTML markup."""
    import re

    text = " ".join(
        list(huynh_interpretation.observations)
        + list(huynh_interpretation.reasoning)
        + list(huynh_interpretation.conclusions)
        + list(huynh_interpretation.warnings)
    )
    assert not re.search(r"<\s*(html|div|span|p|br|table|script)\b", text, re.I)


def test_no_ui_dependency() -> None:
    """Interpreter module does not import portal/UI layers."""
    import engines.interpretation_engine.foundation.interpreters.useful_god.interpreter as mod

    source_path = mod.__file__ or ""
    assert "customer_portal" not in source_path
    assert "static" not in source_path


def test_partial_when_missing_facts() -> None:
    """Missing evidence yields partial status — no hallucination."""
    facts = UsefulGodInterpretationFacts(
        selected="",
        candidate_type="",
        confidence=0.0,
        reason="",
        favorable_gods=(),
        unfavorable_gods=(),
        candidates=(),
        rule_ids=(),
        presence=DataAvailability.MISSING,
        status=DataAvailability.MISSING,
        day_master="Bính",
        day_master_element="Hỏa",
        month_branch="Dậu",
        season="Thu",
        strength_level="strong",
        strength_score=0.66,
        temperature_level="cool",
        five_elements={"wood": 2, "fire": 7, "earth": 4, "metal": 4, "water": 0},
    )
    result = UsefulGodInterpreter().interpret(facts)
    assert result.status == DataAvailability.PARTIAL
    assert result.reasoning == ()
    assert "Thiếu cơ sở" in result.warnings[0]


def test_case0001_generic(case0001_interpretation) -> None:
    """CASE-0001 gets interpretation without Huỳnh-specific hardcoding."""
    assert case0001_interpretation.status == DataAvailability.AVAILABLE
    assert len(case0001_interpretation.observations) >= 5
    assert len(case0001_interpretation.reasoning) >= 2
    assert case0001_interpretation.evidence.selected_rule_id
    joined = " ".join(case0001_interpretation.reasoning)
    assert "Lương Ngọc Huỳnh" not in joined
    assert "1966" not in joined


def test_interpreter_consumes_facts_only() -> None:
    """Interpreter accepts only UsefulGodInterpretationFacts."""
    facts = UsefulGodInterpretationFacts(
        selected="Giáp",
        candidate_type="season",
        confidence=0.8,
        reason="test reason",
        favorable_gods=("Giáp",),
        unfavorable_gods=("Canh",),
        candidates=(
            UsefulGodCandidateFact(
                useful_god="Giáp",
                rule_id="sea_001",
                confidence=0.8,
                reason="test",
                rule_group="season",
            ),
        ),
        rule_ids=("sea_001",),
        presence=DataAvailability.AVAILABLE,
        status=DataAvailability.AVAILABLE,
        day_master="Canh",
        day_master_element="Kim",
        month_branch="Dần",
        season="Xuân",
        strength_level="weak",
        strength_score=0.3,
        temperature_level="cool",
        five_elements={"wood": 3, "fire": 1, "earth": 2, "metal": 2, "water": 2},
    )
    result = UsefulGodInterpreter().interpret(facts)
    assert result.status == DataAvailability.AVAILABLE
    assert "Giáp" in result.conclusions[0]
