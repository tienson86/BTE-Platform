"""Canonical Analysis Result and pipeline contracts (AX-2)."""

from __future__ import annotations

from typing import Any, Mapping

from engines.analysis_engine.pipeline.execution_report import (
    CanonicalAnalysisResult,
    ExecutionTrace,
    StageTraceEntry,
)
from engines.analysis_engine.pipeline.stage_registry import (
    ACTIVE_CANONICAL_STAGES,
    CANONICAL_STAGE_ORDER_V2,
    INACTIVE_FUTURE_STAGES,
    PIPELINE_ID_V2,
    PIPELINE_VERSION_V2,
    StageRecord,
)

ANALYSIS_RESULT_FIELDS: tuple[str, ...] = (
    "seasonal",
    "strength",
    "temperature",
    "pattern",
    "pattern_evaluation",
    "useful_god",
    "diagnostics",
    "execution_trace",
    "pipeline_version",
    "package_versions",
)


def analysis_result_contract() -> dict[str, Any]:
    """Return the published Analysis Result field contract."""
    return {
        "pipeline_id": PIPELINE_ID_V2,
        "pipeline_version": PIPELINE_VERSION_V2,
        "fields": list(ANALYSIS_RESULT_FIELDS),
        "active_stages": list(ACTIVE_CANONICAL_STAGES),
        "inactive_stages": list(INACTIVE_FUTURE_STAGES),
        "canonical_order": list(CANONICAL_STAGE_ORDER_V2),
    }


def stage_contract_view(record: StageRecord) -> Mapping[str, Any]:
    """Return the public stage contract view."""
    return record.to_dict()


__all__ = [
    "ANALYSIS_RESULT_FIELDS",
    "ACTIVE_CANONICAL_STAGES",
    "CANONICAL_STAGE_ORDER_V2",
    "CanonicalAnalysisResult",
    "ExecutionTrace",
    "INACTIVE_FUTURE_STAGES",
    "PIPELINE_ID_V2",
    "PIPELINE_VERSION_V2",
    "StageRecord",
    "StageTraceEntry",
    "analysis_result_contract",
    "stage_contract_view",
]
