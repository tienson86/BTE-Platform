"""Validation gateway for Analysis Runtime."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Sequence

from engines.analysis_engine.runtime.constants import CANONICAL_STAGES
from engines.analysis_engine.runtime.exceptions import (
    AdmissionError,
    PrerequisiteError,
    ValidationError,
)
from engines.analysis_engine.runtime.models import (
    AnalysisContext,
    AnalysisResult,
    DiagnosticInfo,
    StageResult,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ValidationReport:
    """Outcome of validate(context) without full pipeline execution."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    diagnostics: list[DiagnosticInfo] = field(default_factory=list)


class ValidationManager:
    """Pre/post/final validation for the Analysis Runtime."""

    def __init__(
        self,
        *,
        required_stages: Sequence[str] | None = None,
    ) -> None:
        self._required_stages = tuple(required_stages or CANONICAL_STAGES)

    def validate_admission(self, context: AnalysisContext) -> None:
        """Fail closed when input context is not request-ready."""
        if not context.request_id:
            raise AdmissionError("AnalysisContext.request_id is required")
        if context.chart is None:
            raise AdmissionError("AnalysisContext.chart is required")
        logger.debug(
            "admission_validated",
            extra={"request_id": context.request_id},
        )

    def validate_preconditions(
        self,
        context: AnalysisContext,
        *,
        stage_id: str,
        dependencies: Sequence[str],
    ) -> None:
        """Verify prerequisite StageResults before stage execution."""
        missing = [
            dep for dep in dependencies if not context.has_stage_result(dep)
        ]
        if missing:
            raise PrerequisiteError(
                f"Missing prerequisites for stage '{stage_id}': {missing}",
                stage_id=stage_id,
                details={"missing": missing},
            )

    def validate_stage_result(
        self,
        result: StageResult,
        *,
        expected_stage_id: str,
    ) -> None:
        """Validate StageResult contract after module evaluate."""
        if not isinstance(result, StageResult):
            raise ValidationError(
                "Module must return StageResult",
                stage_id=expected_stage_id,
            )
        if result.stage_id != expected_stage_id:
            raise ValidationError(
                "StageResult.stage_id mismatch",
                stage_id=expected_stage_id,
                details={
                    "expected": expected_stage_id,
                    "actual": result.stage_id,
                },
            )
        if result.status not in {"success", "failed", "skipped"}:
            raise ValidationError(
                f"Illegal StageResult.status: {result.status}",
                stage_id=expected_stage_id,
            )
        if result.status != "success":
            raise ValidationError(
                f"Stage '{expected_stage_id}' did not succeed",
                stage_id=expected_stage_id,
                details={"status": result.status},
            )

    def validate_final(
        self,
        context: AnalysisContext,
        *,
        required_stages: Sequence[str] | None = None,
    ) -> None:
        """Verify all required stages are published before assembly."""
        stages = tuple(required_stages or self._required_stages)
        missing = [
            stage_id
            for stage_id in stages
            if not context.has_stage_result(stage_id)
        ]
        if missing:
            raise ValidationError(
                f"Final validation missing stages: {missing}",
                details={"missing": missing},
            )

    def validate_analysis_result(
        self,
        result: AnalysisResult,
        *,
        required_stages: Sequence[str] | None = None,
    ) -> None:
        """Verify assembled AnalysisResult handoff contract."""
        if not result.request_id:
            raise ValidationError("AnalysisResult.request_id is required")
        if result.execution_metadata is None:
            raise ValidationError("AnalysisResult.execution_metadata is required")
        stages = tuple(required_stages or self._required_stages)
        missing = [
            stage_id
            for stage_id in stages
            if result.get_stage_result(stage_id) is None
        ]
        if missing:
            raise ValidationError(
                f"AnalysisResult missing stages: {missing}",
                details={"missing": missing},
            )

    def validate_context(self, context: AnalysisContext) -> ValidationReport:
        """Admission-style validation without executing the pipeline."""
        errors: list[str] = []
        warnings: list[str] = []
        diagnostics: list[DiagnosticInfo] = []
        try:
            self.validate_admission(context)
        except AdmissionError as exc:
            errors.append(exc.message)
            diagnostics.append(
                DiagnosticInfo(
                    code="admission_error",
                    message=exc.message,
                    level="error",
                )
            )
        if not context.chart:
            warnings.append("AnalysisContext.chart is empty")
            diagnostics.append(
                DiagnosticInfo(
                    code="empty_chart",
                    message="AnalysisContext.chart is empty",
                    level="warning",
                )
            )
        is_valid = not errors
        logger.info(
            "context_validated",
            extra={
                "request_id": context.request_id,
                "is_valid": is_valid,
                "error_count": len(errors),
            },
        )
        return ValidationReport(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            diagnostics=diagnostics,
        )
