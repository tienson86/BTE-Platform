"""Input and result validators for Combination Engine."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.combination_engine.exceptions import (
    CombinationPrerequisiteError,
    CombinationValidationError,
)
from engines.analysis_engine.combination_engine.knowledge_access import (
    MODULE_ID,
    REQUIRED_ASSETS,
    KnowledgeSession,
    require_knowledge_session,
)
from engines.analysis_engine.combination_engine.models import CombinationResult
from engines.analysis_engine.runtime.models import AnalysisContext, StageResult

REQUIRED_UPSTREAM: tuple[str, ...] = (
    "strength",
    "temperature",
    "pattern",
    "useful_god",
    "ten_gods",
)


def validate_context(context: AnalysisContext) -> None:
    """Validate AnalysisContext admission for Combination evaluation."""
    if context is None:
        raise CombinationValidationError("AnalysisContext is required")
    if not context.request_id:
        raise CombinationValidationError("AnalysisContext.request_id is required")
    if not context.chart:
        raise CombinationValidationError("AnalysisContext.chart is required")
    stems = _pillar_map(context, "stems", "stem")
    branches = _pillar_map(context, "branches", "branch")
    if len(stems) < 2 and len(branches) < 2:
        raise CombinationValidationError(
            "chart must provide at least two stems or two branches",
            details={
                "stem_pillars": sorted(stems.keys()),
                "branch_pillars": sorted(branches.keys()),
            },
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
        raise CombinationPrerequisiteError(
            f"Missing required upstream results: {missing}",
            details={"missing": missing},
        )
    return results


def validate_knowledge_session(context: AnalysisContext) -> KnowledgeSession:
    """Validate Knowledge SDK session and required Combination assets."""
    session = require_knowledge_session(context.knowledge_session)
    module = session.get_module(MODULE_ID)
    if module.module_id != MODULE_ID:
        raise CombinationValidationError(
            "Unexpected knowledge module identity",
            details={"module_id": module.module_id},
        )
    for asset_id in REQUIRED_ASSETS:
        session.get_asset(asset_id)
    return session


def validate_result(result: CombinationResult) -> None:
    """Validate CombinationResult schema before publication."""
    if result.confidence.score is None:
        raise CombinationValidationError(
            "CombinationResult.confidence.score is required"
        )
    if not result.evidence:
        raise CombinationValidationError(
            "CombinationResult.evidence must include KnowledgeReferences",
        )


def _pillar_map(
    context: AnalysisContext,
    key: str,
    pillar_field: str,
) -> dict[str, str]:
    chart: dict[str, Any] = dict(context.chart)
    direct = chart.get(key)
    result: dict[str, str] = {}
    if isinstance(direct, dict):
        for pillar, value in direct.items():
            if value:
                result[str(pillar)] = str(value)
        return result

    pillars = chart.get("pillars")
    if isinstance(pillars, dict):
        for pillar, node in pillars.items():
            if isinstance(node, dict) and node.get(pillar_field):
                result[str(pillar)] = str(node[pillar_field])
    return result
