"""Sprint B2 — Decision Explanation Framework tests."""

from __future__ import annotations

import re

import pytest

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.models import ProductionRequest
from engines.interpretation_engine.foundation.explanation import (
    DecisionExplanationResult,
    validate_decision_explanation,
)
from engines.interpretation_engine.foundation.explanation.metrics import compute_explainability_metrics
from engines.interpretation_engine.foundation.explanation.models import (
    AdviceItem,
    AnalysisFact,
    Decision,
    DecisionAlternative,
    DecisionPathStep,
    DomainApplication,
    DomainMeaningItem,
    EvidenceItem,
    WarningItem,
)
from engines.interpretation_engine.foundation.explanation.validation import ValidationIssue
from engines.interpretation_engine.foundation.facts.useful_god import UsefulGodInterpretationFacts
from engines.interpretation_engine.foundation.interpreters.useful_god import UsefulGodInterpreter
from engines.interpretation_engine.foundation.status import DataAvailability

HUYNH = ProductionRequest(
    year=1966,
    month=9,
    day=24,
    hour=4,
    minute=15,
    gender="male",
)


@pytest.fixture(scope="module")
def huynh_explanation():
    """Framework explanation for Huỳnh."""
    output = ProductionEngineRunner().run(HUYNH)
    assert output.interpretation_foundation is not None
    assert output.interpretation_foundation.useful_god_explanation is not None
    return output.interpretation_foundation.useful_god_explanation


@pytest.fixture(scope="module")
def case0001_explanation():
    """Framework explanation for CASE-0001."""
    output = ProductionEngineRunner().run(CASE_0001_REQUEST)
    assert output.interpretation_foundation.useful_god_explanation is not None
    return output.interpretation_foundation.useful_god_explanation


def test_a_decision_explanation_contract(huynh_explanation) -> None:
    """A. DecisionExplanationResult contract works."""
    exp = huynh_explanation
    assert isinstance(exp, DecisionExplanationResult)
    assert exp.domain == "useful_god"
    assert exp.analysis
    assert exp.decision_path
    assert exp.evidence
    assert exp.decision is not None
    payload = exp.to_dict()
    assert "decision_path" in payload
    assert "metrics" in payload


def test_b_decision_path_ordered_deterministic(huynh_explanation) -> None:
    """B. Decision path is ordered and deterministic."""
    orders = [step.order for step in huynh_explanation.decision_path]
    assert orders == sorted(orders)
    assert orders[0] == 1
    assert len(orders) == len(set(orders))
    ids = [step.step_id for step in huynh_explanation.decision_path]
    assert "read_day_master_season" in ids
    assert "select_winner" in ids


def test_c_decision_references_valid_evidence(huynh_explanation) -> None:
    """C. Every decision references valid evidence."""
    evidence_ids = {item.evidence_id for item in huynh_explanation.evidence}
    assert huynh_explanation.decision is not None
    for ref in huynh_explanation.decision.supporting_evidence_ids:
        assert ref in evidence_ids
    validation = validate_decision_explanation(
        huynh_explanation,
        analytical_selected=huynh_explanation.decision.selected,
    )
    assert validation.passed is True
    assert not any(
        issue.code == "missing_evidence_reference" for issue in validation.issues
    )


def test_d_alternatives_accepted_rejected(huynh_explanation) -> None:
    """D. Alternatives support accepted/rejected states."""
    alts = huynh_explanation.alternatives
    assert len(alts) >= 2
    selected = [a for a in alts if a.status == "selected"]
    rejected = [a for a in alts if a.status == "rejected"]
    assert len(selected) == 1
    assert len(rejected) >= 1
    assert selected[0].candidate == "Đinh"
    binh = [a for a in alts if a.candidate == "Bính" and a.status == "rejected"]
    assert binh
    assert binh[0].rejection_reason


def test_e_analytical_truth_ownership(huynh_explanation) -> None:
    """E. Analytical truth ownership cannot be overwritten."""
    validation = validate_decision_explanation(
        huynh_explanation,
        analytical_selected="Đinh",
    )
    assert validation.passed is True
    bad = _mutate_decision(huynh_explanation, selected="Canh")
    bad_validation = validate_decision_explanation(
        bad,
        analytical_selected="Đinh",
    )
    assert bad_validation.passed is False
    assert any(
        issue.code == "decision_ownership_violation" for issue in bad_validation.issues
    )


def test_f_invalid_contradictions_detected() -> None:
    """F. Invalid contradictions are detected."""
    evidence = (
        EvidenceItem(
            evidence_id="ev1",
            source_engine="test",
            source_field="f",
            rule_id="r1",
            fact="x",
            value="1",
            confidence=0.5,
            relevance="primary",
        ),
    )
    result = DecisionExplanationResult(
        domain="test",
        status=DataAvailability.AVAILABLE,
        analysis=(),
        decision_path=(),
        evidence=evidence,
        decision=Decision(
            selected="A",
            selected_type="t",
            reason="r",
            confidence=2.0,
            supporting_evidence_ids=("missing_id",),
            rejected_alternatives=(),
        ),
        alternatives=(
            DecisionAlternative(
                alternative_id="a1",
                candidate="A",
                candidate_type="t",
                score=1.0,
                priority=1,
                supporting_evidence=(),
                opposing_evidence=(),
                rejection_reason="rejected",
                status="selected",
            ),
        ),
        domain_meaning=(),
        applications=(),
        advice=(),
        warnings=(),
        confidence=2.0,
        diagnostics=(),
    )
    validation = validate_decision_explanation(result)
    codes = {issue.code for issue in validation.issues}
    assert "confidence_out_of_range" in codes
    assert "missing_evidence_reference" in codes
    assert "alternative_contradiction" in codes


def test_g_duplicate_steps_detected() -> None:
    """G. Duplicate structural steps are detected."""
    step = DecisionPathStep(
        step_id="s1",
        order=1,
        title="Same",
        input_facts=(),
        rule_refs=(),
        condition="c",
        outcome="o",
        effect="e",
        status="passed",
    )
    result = DecisionExplanationResult(
        domain="test",
        status=DataAvailability.AVAILABLE,
        analysis=(),
        decision_path=(step, step),
        evidence=(),
        decision=None,
        alternatives=(),
        domain_meaning=(),
        applications=(),
        advice=(),
        warnings=(),
        confidence=0.5,
        diagnostics=(),
    )
    validation = validate_decision_explanation(result)
    assert any(
        issue.code == "duplicate_decision_path_step" for issue in validation.issues
    )


def test_h_explainability_metrics(huynh_explanation) -> None:
    """H. Explainability metrics are produced."""
    metrics = huynh_explanation.metrics or compute_explainability_metrics(huynh_explanation)
    assert metrics.fact_count >= 8
    assert metrics.decision_step_count == 10
    assert metrics.evidence_count >= 6
    assert metrics.alternative_count >= 4
    assert metrics.evidence_coverage_ratio > 0
    assert metrics.unsupported_decision_count == 0


def test_i_useful_god_b1_migrated(huynh_explanation) -> None:
    """I. Useful God B1 migrates to framework."""
    output = ProductionEngineRunner().run(HUYNH)
    foundation = output.interpretation_foundation
    assert foundation.useful_god_explanation is not None
    assert foundation.useful_god_interpretation is not None
    assert foundation.useful_god_interpretation.evidence.selected_rule_id == "sea_004"
    assert foundation.useful_god_interpretation.confidence == pytest.approx(0.85, abs=0.01)


def test_j_huynh_selects_dinh(huynh_explanation) -> None:
    """J. Lương Ngọc Huỳnh decision path selects Đinh."""
    assert huynh_explanation.decision is not None
    assert huynh_explanation.decision.selected == "Đinh"
    select_step = next(
        s for s in huynh_explanation.decision_path if s.step_id == "select_winner"
    )
    assert "Đinh" in select_step.outcome
    assert "sea_004" in select_step.rule_refs or any(
        e.rule_id == "sea_004" for e in huynh_explanation.evidence
    )


def test_k_binh_rejection_structural(huynh_explanation) -> None:
    """K. Bính rejection is structurally explainable."""
    binh = [
        alt
        for alt in huynh_explanation.alternatives
        if alt.candidate == "Bính" and alt.status == "rejected"
    ]
    assert binh
    assert binh[0].candidate_type == "temperature"
    assert "tmp_003" in str(binh[0].supporting_evidence) or any(
        e.rule_id == "tmp_003" for e in huynh_explanation.evidence if e.fact == "Bính"
    )
    reject_step = next(
        s for s in huynh_explanation.decision_path if s.step_id == "explain_rejected"
    )
    assert "Bính" in reject_step.outcome


def test_l_case0001_same_framework(case0001_explanation) -> None:
    """L. CASE-0001 uses the same framework."""
    assert case0001_explanation.decision_path
    assert case0001_explanation.decision is not None
    assert case0001_explanation.metrics is not None
    joined = str(case0001_explanation.to_dict())
    assert "1966" not in joined
    assert "Lương Ngọc Huỳnh" not in joined


def test_m_no_ui_dependency() -> None:
    """M. No UI dependency."""
    import engines.interpretation_engine.foundation.explanation.models as mod

    assert "customer_portal" not in (mod.__file__ or "")


def test_n_no_html_markdown(huynh_explanation) -> None:
    """N. No HTML/markdown dependency."""
    text = " ".join(
        step.outcome for step in huynh_explanation.decision_path
    )
    assert not re.search(r"<\s*(html|div|span|p)\b", text, re.I)


def test_o_portal_unchanged() -> None:
    """O. Existing production analysis contract unchanged."""
    output = ProductionEngineRunner().run(HUYNH)
    analysis = output.analysis
    assert analysis.useful_god.useful_god == "Đinh"
    assert analysis.strength.strength_level == "strong"


def test_huynh_decision_chain(huynh_explanation) -> None:
    """Huỳnh machine-readable decision chain."""
    analysis = {item.fact: item.value for item in huynh_explanation.analysis}
    assert "Bính" in analysis["day_master"]
    assert analysis["season"] == "Thu" or "Thu" in analysis["season"]
    assert "strong" in analysis["strength"]
    assert analysis["temperature"] == "cool"
    assert huynh_explanation.decision.selected == "Đinh"
    hy = analysis["favorable_gods"]
    ky = analysis["unfavorable_gods"]
    assert "Đinh" in hy and "Bính" in hy
    assert "Canh" in ky and "Tân" in ky


def _mutate_decision(
    original: DecisionExplanationResult,
    *,
    selected: str,
) -> DecisionExplanationResult:
    """Clone explanation with mutated decision for validation tests."""
    assert original.decision is not None
    new_decision = Decision(
        selected=selected,
        selected_type=original.decision.selected_type,
        reason=original.decision.reason,
        confidence=original.decision.confidence,
        supporting_evidence_ids=original.decision.supporting_evidence_ids,
        rejected_alternatives=original.decision.rejected_alternatives,
    )
    return DecisionExplanationResult(
        domain=original.domain,
        status=original.status,
        analysis=original.analysis,
        decision_path=original.decision_path,
        evidence=original.evidence,
        decision=new_decision,
        alternatives=original.alternatives,
        domain_meaning=original.domain_meaning,
        applications=original.applications,
        advice=original.advice,
        warnings=original.warnings,
        confidence=original.confidence,
        diagnostics=original.diagnostics,
        metrics=original.metrics,
    )
