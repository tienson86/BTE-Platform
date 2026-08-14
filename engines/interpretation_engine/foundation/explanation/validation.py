"""Validation for Decision Explanation Framework."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation import diagnostics as diag
from engines.interpretation_engine.foundation.explanation.metrics import compute_explainability_metrics
from engines.interpretation_engine.foundation.explanation.models import DecisionExplanationResult
from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """One framework validation issue."""

    code: str
    message: str
    severity: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize validation issue."""
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
        }


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Outcome of framework validation."""

    passed: bool
    issues: tuple[ValidationIssue, ...]
    status: DataAvailability

    def to_dict(self) -> dict[str, Any]:
        """Serialize validation result."""
        return {
            "passed": self.passed,
            "issues": [item.to_dict() for item in self.issues],
            "status": self.status.value,
        }


def validate_decision_explanation(
    result: DecisionExplanationResult,
    *,
    analytical_selected: str | None = None,
    score_fields_used: tuple[str, ...] = (),
) -> ValidationResult:
    """Validate decision explanation structure and ownership."""
    issues: list[ValidationIssue] = []
    evidence_ids = {item.evidence_id for item in result.evidence}

    if result.confidence > 1.0:
        issues.append(
            ValidationIssue(
                code="confidence_out_of_range",
                message="confidence exceeds 1.0",
                severity="error",
            )
        )

    if analytical_selected and result.decision is not None:
        if result.decision.selected != analytical_selected:
            issues.append(
                ValidationIssue(
                    code="decision_ownership_violation",
                    message=(
                        f"decision.selected={result.decision.selected!r} "
                        f"!= analytical owner {analytical_selected!r}"
                    ),
                    severity="error",
                )
            )

    if result.decision is not None and not result.evidence:
        issues.append(
            ValidationIssue(
                code="decision_without_evidence",
                message="decision exists but evidence is missing",
                severity="warning",
            )
        )

    if result.decision is not None:
        for ref in result.decision.supporting_evidence_ids:
            if ref not in evidence_ids:
                issues.append(
                    ValidationIssue(
                        code="missing_evidence_reference",
                        message=f"decision references missing evidence {ref!r}",
                        severity="error",
                    )
                )

    selected_alts = [alt for alt in result.alternatives if alt.status == "selected"]
    rejected_alts = [alt for alt in result.alternatives if alt.status == "rejected"]
    if len(selected_alts) > 1:
        issues.append(
            ValidationIssue(
                code="multiple_selected_alternatives",
                message="more than one alternative marked selected",
                severity="error",
            )
        )
    for alt in result.alternatives:
        if alt.status == "selected" and alt.rejection_reason:
            issues.append(
                ValidationIssue(
                    code="alternative_contradiction",
                    message=f"alternative {alt.alternative_id} selected and rejected",
                    severity="error",
                )
            )

    if not result.decision_path and result.status == DataAvailability.AVAILABLE:
        issues.append(
            ValidationIssue(
                code="empty_decision_path",
                message="decision path empty for available explanation",
                severity="warning",
            )
        )

    _check_duplicate_steps(result, issues)

    if score_fields_used:
        issues.append(
            ValidationIssue(
                code=diag.SCORE_USED_AS_STRENGTH_TRUTH,
                message=f"analysis uses score fields: {', '.join(score_fields_used)}",
                severity="error",
            )
        )

    has_error = any(item.severity == "error" for item in issues)
    if not result.analysis and result.status == DataAvailability.AVAILABLE:
        status = DataAvailability.MISSING
    elif has_error:
        status = DataAvailability.INVALID
    elif issues:
        status = DataAvailability.PARTIAL
    else:
        status = result.status

    return ValidationResult(
        passed=not has_error,
        issues=tuple(issues),
        status=status,
    )


def _check_duplicate_steps(
    result: DecisionExplanationResult,
    issues: list[ValidationIssue],
) -> None:
    """Detect normalized duplicate decision path outcomes."""
    seen: set[str] = set()
    for step in result.decision_path:
        key = _normalize_step_key(step)
        if key in seen:
            issues.append(
                ValidationIssue(
                    code="duplicate_decision_path_step",
                    message=f"duplicate outcome at step {step.step_id}",
                    severity="warning",
                )
            )
        seen.add(key)


def _normalize_step_key(step: Any) -> str:
    """Normalize step for duplicate detection."""
    return "|".join(
        [
            step.title.strip().lower(),
            step.condition.strip().lower(),
            step.outcome.strip().lower(),
        ]
    )
