"""MC-01 Pattern Grade. Distinct from ScoreEngine customer grade."""

from __future__ import annotations

from engines.mingju.constants import GRADE_BANDS
from engines.mingju.enums import AnalysisState, IntegrityState, PatternGrade
from engines.mingju.evidence import RecordBook
from engines.mingju.models import PatternGradeResult, StructuralIntegrityResult
from engines.mingju.serialization import band_for_score, clamp_confidence

_STATE_CAP: dict[str, str] = {
    IntegrityState.FAILED.value: PatternGrade.D.value,
    IntegrityState.DAMAGED.value: PatternGrade.C.value,
    IntegrityState.DAMAGED_BUT_RESCUED.value: PatternGrade.B.value,
    IntegrityState.MIXED.value: PatternGrade.B.value,
    IntegrityState.CONDITIONALLY_COMPLETE.value: PatternGrade.A.value,
    IntegrityState.SUBSTANTIALLY_COMPLETE.value: PatternGrade.S.value,
    IntegrityState.COMPLETE.value: PatternGrade.SS.value,
}

_GRADE_ORDER = ("D", "C", "B", "A", "S", "SS")


def _cap_grade(grade: str, ceiling: str) -> str:
    if grade == PatternGrade.UNRESOLVED.value:
        return grade
    if _GRADE_ORDER.index(grade) > _GRADE_ORDER.index(ceiling):
        return ceiling
    return grade


def evaluate_grade(
    integrity: StructuralIntegrityResult,
    book: RecordBook,
) -> PatternGradeResult:
    """Grade is a summary of Integrity. Unresolved Integrity forbids a resolved Grade."""
    if integrity.state == IntegrityState.UNRESOLVED.value or integrity.score is None:
        book.add_warning("grade_unresolved_integrity", "mc01.grade.requires_integrity")
        return PatternGradeResult(
            state=AnalysisState.UNRESOLVED.value,
            grade=PatternGrade.UNRESOLVED.value,
            score=None,
            confidence=0.0,
            integrity_state=integrity.state,
        )
    raw = band_for_score(integrity.score, GRADE_BANDS)
    ceiling = _STATE_CAP.get(integrity.state, PatternGrade.B.value)
    grade = _cap_grade(raw, ceiling)
    evidence_id = book.add_evidence(
        "grade",
        "mc01.grade.from_integrity",
        source="mingju.grade",
        integrity_score=integrity.score,
        integrity_state=integrity.state,
        uncapped_grade=raw,
        grade=grade,
        note="not_score_engine_grade",
    )
    book.add_trace("grade", "MC-GRD-000", "mc01.grade.resolved", (evidence_id,))
    return PatternGradeResult(
        state=AnalysisState.RESOLVED.value,
        grade=grade,
        score=integrity.score,
        confidence=clamp_confidence(integrity.confidence),
        basis="structural_integrity",
        integrity_state=integrity.state,
        evidence_ids=(evidence_id,),
        warnings=(),
    )
