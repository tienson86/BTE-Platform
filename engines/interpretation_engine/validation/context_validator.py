"""Context validator for Pack 03 PackInterpretationContext.

Infrastructure only. No BaZi logic.
"""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.validation.models import (
    ValidationDomain,
    ValidationIssue,
    ValidationReport,
    ValidationSeverity,
)


class ContextValidator:
    """Validate PackInterpretationContext structural integrity."""

    def validate(self, context: Any) -> ValidationReport:
        """Validate a PackInterpretationContext instance."""
        domain = ValidationDomain.CONTEXT.value
        if context is None:
            issue = ValidationIssue(
                code="context_required",
                domain=domain,
                message="interpretation context is required",
            )
            return ValidationReport(
                success=False,
                messages=("context_required",),
                issues=(issue,),
                domain=domain,
            )
        if not isinstance(context, PackInterpretationContext):
            issue = ValidationIssue(
                code="context_type_invalid",
                domain=domain,
                message="PackInterpretationContext required",
                severity=ValidationSeverity.ERROR,
                attributes={"type": type(context).__name__},
            )
            return ValidationReport(
                success=False,
                messages=("context_type_invalid",),
                issues=(issue,),
                domain=domain,
            )
        if not context.validate():
            issue = ValidationIssue(
                code="context_integrity_failed",
                domain=domain,
                message="context structural validation failed",
                attributes={
                    "id": context.id,
                    "source_final_result_id": context.source_final_result_id,
                },
            )
            return ValidationReport(
                success=False,
                messages=("context_integrity_failed",),
                issues=(issue,),
                domain=domain,
            )
        return ValidationReport(
            success=True,
            messages=("context_ok",),
            details={
                "id": context.id,
                "pipeline_id": context.pipeline_id,
                "source_final_result_id": context.source_final_result_id,
            },
            domain=domain,
        )
