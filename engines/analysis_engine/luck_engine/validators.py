"""Input and result validators for Luck Engine."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.luck_engine.exceptions import (
    LuckPrerequisiteError,
    LuckValidationError,
)
from engines.analysis_engine.luck_engine.knowledge_access import (
    MODULE_ID,
    REQUIRED_ASSETS,
    KnowledgeSession,
    require_knowledge_session,
)
from engines.analysis_engine.luck_engine.models import LuckResult
from engines.analysis_engine.runtime.models import AnalysisContext, StageResult

REQUIRED_UPSTREAM: tuple[str, ...] = (
    "strength",
    "temperature",
    "pattern",
    "useful_god",
    "ten_gods",
    "combination",
    "shensha",
)


def validate_context(context: AnalysisContext) -> None:
    """Validate AnalysisContext admission for Luck evaluation."""
    if context is None:
        raise LuckValidationError("AnalysisContext is required")
    if not context.request_id:
        raise LuckValidationError("AnalysisContext.request_id is required")
    if not context.chart:
        raise LuckValidationError("AnalysisContext.chart is required")

    luck = _luck_block(context)
    if not luck:
        raise LuckValidationError(
            "chart.luck timeline block is required",
            details={"chart_keys": sorted(dict(context.chart).keys())},
        )
    if not luck.get("da_yun_sequence"):
        raise LuckValidationError("chart.luck.da_yun_sequence is required")
    for key in ("liu_nian", "liu_yue", "liu_ri", "liu_shi"):
        node = luck.get(key)
        if not isinstance(node, dict) or not node.get("stem") or not node.get("branch"):
            raise LuckValidationError(
                f"chart.luck.{key} with stem/branch is required",
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
        raise LuckPrerequisiteError(
            f"Missing required upstream results: {missing}",
            details={"missing": missing},
        )
    return results


def validate_knowledge_session(context: AnalysisContext) -> KnowledgeSession:
    """Validate Knowledge SDK session and required Luck assets."""
    session = require_knowledge_session(context.knowledge_session)
    module = session.get_module(MODULE_ID)
    if module.module_id != MODULE_ID:
        raise LuckValidationError(
            "Unexpected knowledge module identity",
            details={"module_id": module.module_id},
        )
    for asset_id in REQUIRED_ASSETS:
        session.get_asset(asset_id)
    return session


def validate_result(result: LuckResult) -> None:
    """Validate LuckResult schema before publication."""
    if result.confidence.score is None:
        raise LuckValidationError("LuckResult.confidence.score is required")
    if not result.evidence:
        raise LuckValidationError(
            "LuckResult.evidence must include KnowledgeReferences",
        )
    if not result.da_yun:
        raise LuckValidationError("LuckResult.da_yun must not be empty")


def _luck_block(context: AnalysisContext) -> dict[str, Any]:
    chart = dict(context.chart)
    luck = chart.get("luck")
    if isinstance(luck, dict):
        return dict(luck)
    meta = dict(context.metadata)
    luck_meta = meta.get("luck")
    if isinstance(luck_meta, dict):
        return dict(luck_meta)
    return {}
