"""Shared helpers for knowledge-package integration stages."""

from __future__ import annotations

from typing import Any, Mapping

from engines.analysis_engine.pipeline.execution_context import AnalysisExecutionContext
from engines.analysis_engine.pipeline.package_loader import LoadedPackage


def chart_subset(chart: Mapping[str, Any], keys: tuple[str, ...]) -> dict[str, Any]:
    """Copy selected chart facts without transforming analytical values."""
    return {key: chart[key] for key in keys if key in chart}


def bind_package_payload(
    *,
    stage_id: str,
    package: LoadedPackage,
    produced_signals: tuple[str, ...],
    consumed_signals: tuple[str, ...],
    chart_facts: Mapping[str, Any],
    upstream_stages: tuple[str, ...],
) -> dict[str, Any]:
    """Build a structured binding result. Does not evaluate package rules."""
    return {
        "stage_id": stage_id,
        "package_id": package.package_id,
        "package_version": package.package_version,
        "schema_version": package.schema_version,
        "knowledge_version": package.knowledge_version,
        "compatibility_version": package.compatibility_version,
        "status": "bound",
        "rule_count": package.rule_count,
        "produced_signals": produced_signals,
        "consumed_signals": consumed_signals,
        "upstream_stages": upstream_stages,
        "chart_facts": dict(chart_facts),
    }


def require_upstream(
    context: AnalysisExecutionContext,
    stage_id: str,
    required_stages: tuple[str, ...],
) -> None:
    """Reject execution when required upstream outputs are absent."""
    from engines.analysis_engine.exceptions.pipeline_error import (
        DependencyViolationError,
    )

    missing = [item for item in required_stages if not context.has_result(item)]
    if missing:
        raise DependencyViolationError(
            f"missing_inputs:{stage_id}:{','.join(missing)}"
        )
