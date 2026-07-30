"""Input and result validators for Summary Engine."""

from __future__ import annotations

from engines.analysis_engine.runtime.models import AnalysisContext, StageResult
from engines.analysis_engine.summary_engine.exceptions import (
    SummaryPrerequisiteError,
    SummaryValidationError,
)
from engines.analysis_engine.summary_engine.models import UPSTREAM_STAGES, SummaryResult


def validate_context(context: AnalysisContext) -> None:
    """Validate AnalysisContext admission for Summary aggregation."""
    if context is None:
        raise SummaryValidationError("AnalysisContext is required")
    if not context.request_id:
        raise SummaryValidationError("AnalysisContext.request_id is required")


def validate_upstream(context: AnalysisContext) -> dict[str, StageResult]:
    """Require all eight upstream StageResults; fail closed if missing."""
    missing: list[str] = []
    results: dict[str, StageResult] = {}
    for stage_id in UPSTREAM_STAGES:
        result = context.get_stage_result(stage_id)
        if result is None:
            missing.append(stage_id)
        else:
            results[stage_id] = result
    if missing:
        raise SummaryPrerequisiteError(
            f"Missing required upstream results: {missing}",
            details={"missing": missing},
        )
    return results


def validate_upstream_schema(upstream: dict[str, StageResult]) -> None:
    """Verify each upstream result matches expected stage contract basics."""
    for stage_id, result in upstream.items():
        if result.stage_id != stage_id:
            raise SummaryValidationError(
                "Upstream StageResult.stage_id mismatch",
                details={"expected": stage_id, "actual": result.stage_id},
            )
        if result.status != "success":
            raise SummaryValidationError(
                f"Upstream stage '{stage_id}' is not successful",
                details={"status": result.status},
            )


def validate_result(result: SummaryResult) -> None:
    """Validate SummaryResult schema before publication."""
    if result.confidence.score is None:
        raise SummaryValidationError("SummaryResult.confidence.score is required")
    if result.consistency.status not in {"pass", "warn", "fail"}:
        raise SummaryValidationError(
            f"Illegal consistency status: {result.consistency.status}",
        )
    views = result.domain_views()
    if len(views) != len(UPSTREAM_STAGES):
        raise SummaryValidationError("SummaryResult missing domain views")
    for expected, view in zip(UPSTREAM_STAGES, views, strict=True):
        if view.stage_id != expected:
            raise SummaryValidationError(
                "Domain summary view order/identity mismatch",
                details={"expected": expected, "actual": view.stage_id},
            )
