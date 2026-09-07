"""TV1-B03 evidence and decision validation. Does not replace B02 request validation."""

from __future__ import annotations

from consulting.marriage.exceptions import MarriageDecisionError, MarriageEvidenceError
from consulting.marriage.models.enums import DomainDecisionState
from consulting.marriage.models.evidence import MarriageEvidence
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.validation.runtime import MarriageRuntimeValidation

_FORBIDDEN_CONCLUSIONS = (
    "must marry",
    "must not marry",
    "certain divorce",
    "certain infidelity",
    "infertile",
    "spouse will die",
    "marriage guarantees wealth",
)


class MarriageDecisionValidation(MarriageRuntimeValidation):
    """Validate evidence traceability and decision factual contracts."""

    def validate_evidence(self, evidence: list[MarriageEvidence]) -> None:
        """Require canonical source refs and reject customer prose."""
        seen: set[str] = set()
        for item in evidence:
            if not item.evidence_id:
                raise MarriageEvidenceError("evidence_id_missing")
            if item.evidence_id in seen:
                raise MarriageEvidenceError(f"evidence_id_duplicate:{item.evidence_id}")
            seen.add(item.evidence_id)
            if not item.source_refs:
                raise MarriageEvidenceError(f"evidence_source_missing:{item.evidence_id}")
            for ref in item.source_refs:
                if not ref.analysis_id:
                    raise MarriageEvidenceError(f"evidence_analysis_id_missing:{item.evidence_id}")
            _reject_prose(item.description)
            _reject_prose(item.predicate)

    def validate_decision(self, result: MarriageDecisionResult) -> None:
        """Validate decision traceability. Score may be unavailable."""
        if not result.consultation_id:
            raise MarriageDecisionError("consultation_id_missing")
        if result.canonical_a.source_analysis_id != result.person_a.analysis_id:
            raise MarriageDecisionError("analysis_id_mismatch_a")
        if result.canonical_b.source_analysis_id != result.person_b.analysis_id:
            raise MarriageDecisionError("analysis_id_mismatch_b")
        evidence_ids = {item.evidence_id for item in result.evidence}
        for finding in result.findings:
            for evidence_id in finding.evidence_ids:
                if evidence_id not in evidence_ids:
                    raise MarriageDecisionError(f"finding_evidence_missing:{finding.finding_id}")
            _reject_prose(finding.technical_summary)
        if result.recommendations:
            raise MarriageDecisionError("recommendation_not_allowed")
        if result.overall.score is not None or result.overall.grade is not None:
            raise MarriageDecisionError("score_projection_must_remain_unavailable")
        if result.overall.state is None:
            raise MarriageDecisionError("overall_state_missing")
        if result.overall.state is DomainDecisionState.INSUFFICIENT:
            return
        _reject_prose(str(result.overall.state.value))


def _reject_prose(value: str | None) -> None:
    """Reject customer-facing hard conclusions."""
    if not value:
        return
    lowered = value.lower()
    for phrase in _FORBIDDEN_CONCLUSIONS:
        if phrase in lowered:
            raise MarriageDecisionError(f"forbidden_conclusion:{phrase}")
