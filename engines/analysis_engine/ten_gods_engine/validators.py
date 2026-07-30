"""Input and result validators for Ten Gods Engine."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.runtime.models import AnalysisContext, StageResult
from engines.analysis_engine.ten_gods_engine.exceptions import (
    TenGodsPrerequisiteError,
    TenGodsValidationError,
)
from engines.analysis_engine.ten_gods_engine.knowledge_access import (
    MODULE_ID,
    REQUIRED_ASSETS,
    KnowledgeSession,
    require_knowledge_session,
)
from engines.analysis_engine.ten_gods_engine.models import TenGodsResult

REQUIRED_UPSTREAM: tuple[str, ...] = (
    "strength",
    "temperature",
    "pattern",
    "useful_god",
)


def validate_context(context: AnalysisContext) -> None:
    """Validate AnalysisContext admission for Ten Gods evaluation."""
    if context is None:
        raise TenGodsValidationError("AnalysisContext is required")
    if not context.request_id:
        raise TenGodsValidationError("AnalysisContext.request_id is required")
    if not context.chart:
        raise TenGodsValidationError("AnalysisContext.chart is required")
    day_master = _day_master(context)
    if not day_master:
        raise TenGodsValidationError(
            "AnalysisContext.chart.day_master is required",
            details={"chart_keys": sorted(context.chart.keys())},
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
        raise TenGodsPrerequisiteError(
            f"Missing required upstream results: {missing}",
            details={"missing": missing},
        )
    return results


def validate_knowledge_session(context: AnalysisContext) -> KnowledgeSession:
    """Validate Knowledge SDK session and required Ten Gods assets."""
    session = require_knowledge_session(context.knowledge_session)
    module = session.get_module(MODULE_ID)
    if module.module_id != MODULE_ID:
        raise TenGodsValidationError(
            "Unexpected knowledge module identity",
            details={"module_id": module.module_id},
        )
    for asset_id in REQUIRED_ASSETS:
        session.get_asset(asset_id)
    return session


def validate_result(result: TenGodsResult) -> None:
    """Validate TenGodsResult schema before publication."""
    if result.confidence.score is None:
        raise TenGodsValidationError("TenGodsResult.confidence.score is required")
    if not result.evidence:
        raise TenGodsValidationError(
            "TenGodsResult.evidence must include KnowledgeReferences",
        )
    for presence in result.presence:
        if not presence.god_id:
            raise TenGodsValidationError("presence.god_id is required")


def _day_master(context: AnalysisContext) -> str:
    chart: dict[str, Any] = dict(context.chart)
    value = chart.get("day_master") or chart.get("day_stem")
    if value:
        return str(value)
    stems = chart.get("stems") or {}
    if isinstance(stems, dict) and stems.get("day"):
        return str(stems["day"])
    pillars = chart.get("pillars") or {}
    if isinstance(pillars, dict):
        day = pillars.get("day") or {}
        if isinstance(day, dict) and day.get("stem"):
            return str(day["stem"])
    return ""
