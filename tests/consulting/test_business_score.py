"""Business scoring is separate, explainable and cautious with missing evidence."""

from dataclasses import replace
import math

import pytest

from consulting.business.score import project_business_score, recommendation_for_score
from consulting.marriage.models.matrix import MarriageCompatibilityMatrix, MarriageMatrixRow, MarriageMatrixSection


def _row(key, status="supportive", confidence=0.8, available=True):
    return MarriageMatrixRow(key, key, "A", "B", "Quan hệ đối chiếu", status, confidence, "Cơ sở", available=available)


def _matrix(status="supportive", confidence=0.8):
    return MarriageCompatibilityMatrix("test", [
        MarriageMatrixSection("useful_god", "Dụng thần", "", (_row("a_to_b", status, confidence), _row("b_to_a", status, confidence))),
        MarriageMatrixSection("cung_phi", "Cung Phi", "", tuple(_row(key, status, confidence) for key in ("personal", "year", "month", "day", "hour"))),
        MarriageMatrixSection("structure", "Cấu trúc", "", (_row("day_master", status, confidence), _row("stem_branch_1", status, confidence), _row("pattern", "reference", confidence))),
    ])


@pytest.mark.parametrize("status,score,key", [("supportive", 82, "recommended"), ("balanced", 65, "conditional"), ("mixed", 50, "trial"), ("pressured", 35, "not_recommended")])
def test_score_and_advice_match_evidence(status, score, key):
    result = project_business_score(_matrix(status))
    assert result.score == score
    assert result.recommendation_key == key
    assert result.coverage == 100 and result.provisional is False
    assert sum(group.configured_weight for group in result.groups) == 100
    assert sum(group.contribution for group in result.groups) == pytest.approx(score)
    assert result.groups[-1].score is None
    assert "không phải phần trăm" in result.disclaimer


@pytest.mark.parametrize("score,key", [(100, "recommended"), (75, "recommended"), (74.9, "conditional"), (60, "conditional"), (59.9, "trial"), (45, "trial"), (44.9, "not_recommended"), (0, "not_recommended")])
def test_recommendation_thresholds(score, key):
    assert recommendation_for_score(score)[0] == key


def test_missing_rows_reduce_coverage_not_points_and_reference_rows_do_not_score():
    matrix = _matrix()
    section = matrix.sections[1]
    matrix.sections[1] = replace(section, rows=(*section.rows[:-1], replace(section.rows[-1], available=False, status="unavailable", confidence=0)))
    result = project_business_score(matrix)
    assert result.score == 82 and result.coverage == 98
    assert result.provisional is True
    assert result.recommendation_key == "recommended"
    assert sum(group.effective_weight for group in result.groups) == pytest.approx(100, abs=0.001)
    structure = matrix.sections[2]
    matrix.sections[2] = replace(structure, rows=tuple(replace(row, status="pressured") if row.key == "pattern" else row for row in structure.rows))
    assert project_business_score(matrix).score == result.score


def test_one_missing_core_group_prevents_an_overconfident_recommendation():
    matrix = _matrix()
    matrix.sections[0] = replace(matrix.sections[0], rows=tuple(replace(row, available=False) for row in matrix.sections[0].rows))
    result = project_business_score(matrix)
    assert result.score == 82
    assert result.coverage == 65 and result.provisional is True
    assert result.recommendation_key == "insufficient"


def test_no_core_evidence_has_no_score_even_when_cung_phi_exists():
    assert project_business_score(None).score is None
    matrix = _matrix()
    matrix.sections = [matrix.sections[1]]
    result = project_business_score(matrix)
    assert result.score is None and result.recommendation_key == "insufficient"


def test_core_pressure_overrides_high_aggregate_without_changing_the_score():
    matrix = _matrix()
    structure = matrix.sections[2]
    matrix.sections[2] = replace(structure, rows=tuple(replace(row, status="pressured") if row.key == "day_master" else row for row in structure.rows))
    result = project_business_score(matrix)
    assert result.score == 70.2
    assert result.recommendation_key == "trial"
    assert any("Nhật Chủ" in reason for reason in result.reasons)


@pytest.mark.parametrize("confidence,key", [(0.49, "insufficient"), (0.5, "conditional"), (0.69, "conditional"), (0.7, "recommended")])
def test_low_confidence_restricts_advice(confidence, key):
    result = project_business_score(_matrix(confidence=confidence))
    assert result.score == 82 and result.recommendation_key == key


@pytest.mark.parametrize("confidence", [0, -0.1, 1.1, math.nan, math.inf])
def test_invalid_confidence_is_not_scored(confidence):
    result = project_business_score(_matrix(confidence=confidence))
    assert result.score is None
    assert result.coverage == 0


def test_row_order_does_not_change_score_and_confidence_weights_are_auditable():
    matrix = _matrix()
    useful = matrix.sections[0]
    matrix.sections[0] = replace(useful, rows=(_row("a_to_b", "supportive", 0.8), _row("b_to_a", "pressured", 0.2)))
    first = project_business_score(matrix)
    assert first.groups[0].score == 72.6
    matrix.sections = [replace(section, rows=tuple(reversed(section.rows))) for section in reversed(matrix.sections)]
    assert project_business_score(matrix) == first
