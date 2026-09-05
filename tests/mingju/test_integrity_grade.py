"""Integrity and Grade contract tests."""

from __future__ import annotations

from engines.mingju import analyze_mingju
from engines.mingju.constants import SCORE_GRADE_LETTERS
from engines.mingju.enums import PatternGrade
from tests.mingju.conftest import context_from, visible


def test_integrity_consumes_purity_strength_damage_rescue() -> None:
    result = analyze_mingju(context_from())
    assert result.integrity.state != "unresolved"
    assert result.integrity.purity_component is not None
    assert result.integrity.strength_component is not None
    assert result.integrity.damage_component is not None
    assert result.integrity.rescue_component is not None
    assert result.integrity.score is not None


def test_grade_is_mc01_structural_grade_not_score_engine() -> None:
    result = analyze_mingju(context_from())
    assert result.grade.grade in {item.value for item in PatternGrade}
    assert result.grade.basis == "structural_integrity"
    assert "D+" not in {result.grade.grade}
    if result.grade.state == "resolved":
        assert result.grade.grade != "UNRESOLVED"
        assert result.grade.grade not in SCORE_GRADE_LETTERS - {"S", "A", "B", "C", "D"}


def test_unresolved_integrity_forbids_resolved_grade() -> None:
    result = analyze_mingju(
        context_from(pattern={"success": False, "pattern": "", "cach_cuc": ""})
    )
    assert result.integrity.state == "unresolved"
    assert result.grade.state == "unresolved"
    assert result.grade.grade == "UNRESOLVED"
    assert result.grade.score is None


def test_damaged_but_rescued_is_not_collapsed_to_complete() -> None:
    result = analyze_mingju(
        context_from(
            pattern={
                "success": True,
                "pattern": "chinh_quan",
                "cach_cuc": "Chính Quan",
                "month_main_qi_ten_god": "Chính Quan",
            },
            ten_gods={
                "visible": [
                    visible("month", "zheng_guan", "Chính Quan"),
                    visible("hour", "shang_guan", "Thương Quan"),
                    visible("year", "zheng_yin", "Chính Ấn"),
                ],
                "hidden": [],
            },
        )
    )
    if result.integrity.state == "damaged_but_rescued":
        assert result.integrity.state != "complete"
        assert result.grade.grade != "SS"
