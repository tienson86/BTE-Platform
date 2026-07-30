"""Input and result validators for ShenSha Engine."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.runtime.models import AnalysisContext, StageResult
from engines.analysis_engine.shensha_engine.exceptions import (
    ShenShaPrerequisiteError,
    ShenShaValidationError,
)
from engines.analysis_engine.shensha_engine.knowledge_access import (
    MODULE_ID,
    REQUIRED_ASSETS,
    KnowledgeSession,
    require_knowledge_session,
)
from engines.analysis_engine.shensha_engine.models import ShenShaResult

REQUIRED_UPSTREAM: tuple[str, ...] = (
    "strength",
    "temperature",
    "pattern",
    "useful_god",
    "ten_gods",
    "combination",
)


def validate_context(context: AnalysisContext) -> None:
    """Validate AnalysisContext admission for ShenSha evaluation."""
    if context is None:
        raise ShenShaValidationError("AnalysisContext is required")
    if not context.request_id:
        raise ShenShaValidationError("AnalysisContext.request_id is required")
    if not context.chart:
        raise ShenShaValidationError("AnalysisContext.chart is required")

    day_stem = _resolve_path(context, "stems.day") or context.chart.get("day_master")
    year_branch = _resolve_path(context, "branches.year")
    if not day_stem:
        raise ShenShaValidationError(
            "chart day stem / day_master is required for ShenSha anchors",
        )
    if not year_branch and not _resolve_path(context, "branches.day"):
        raise ShenShaValidationError(
            "chart branches are required for ShenSha lookup",
        )


def validate_upstream(context: AnalysisContext) -> dict[str, StageResult]:
    """Require published upstream StageResults; fail closed if missing."""
    missing: list[str] = []
    results: dict[str, StageResult] = {}
    for stage_id in REQUIRED_UPSTREAM:
        result = context.get_stage_result(stage_id)
        if result is None:
            missing.append(stage_id)
        else:
            results[stage_id] = result
    if missing:
        raise ShenShaPrerequisiteError(
            f"Missing required upstream results: {missing}",
            details={"missing": missing},
        )
    return results


def validate_knowledge_session(context: AnalysisContext) -> KnowledgeSession:
    """Validate Knowledge SDK session and required ShenSha assets."""
    session = require_knowledge_session(context.knowledge_session)
    module = session.get_module(MODULE_ID)
    if module.module_id != MODULE_ID:
        raise ShenShaValidationError(
            "Unexpected knowledge module identity",
            details={"module_id": module.module_id},
        )
    for asset_id in REQUIRED_ASSETS:
        session.get_asset(asset_id)
    return session


def validate_result(result: ShenShaResult) -> None:
    """Validate ShenShaResult schema before publication."""
    if result.confidence.score is None:
        raise ShenShaValidationError("ShenShaResult.confidence.score is required")
    if not result.evidence:
        raise ShenShaValidationError(
            "ShenShaResult.evidence must include KnowledgeReferences",
        )


def _resolve_path(context: AnalysisContext, dotted: str) -> str | None:
    chart: dict[str, Any] = dict(context.chart)
    parts = dotted.split(".")
    if len(parts) == 2 and parts[0] in {"stems", "branches"}:
        bucket = chart.get(parts[0])
        if isinstance(bucket, dict) and bucket.get(parts[1]):
            return str(bucket[parts[1]])
        pillars = chart.get("pillars")
        field = "stem" if parts[0] == "stems" else "branch"
        if isinstance(pillars, dict):
            node = pillars.get(parts[1]) or {}
            if isinstance(node, dict) and node.get(field):
                return str(node[field])
    return None
