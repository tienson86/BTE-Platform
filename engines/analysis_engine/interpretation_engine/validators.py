"""Input / output validators for Interpretation Engine."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.interpretation_engine.exceptions import (
    InterpretationKnowledgeError,
    InterpretationPrerequisiteError,
    InterpretationValidationError,
)
from engines.analysis_engine.interpretation_engine.knowledge_access import (
    MODULE_ID,
    REQUIRED_ASSETS,
    KnowledgeSession,
    require_knowledge_session,
)
from engines.analysis_engine.interpretation_engine.models import (
    REQUIRED_ANALYSIS_STAGES,
    InterpretationContext,
    InterpretationResult,
)
from engines.analysis_engine.runtime.models import AnalysisResult


def validate_context(context: InterpretationContext) -> None:
    """Validate InterpretationContext admission requirements."""
    if not isinstance(context, InterpretationContext):
        raise InterpretationValidationError(
            "InterpretationContext is required",
            details={"type": type(context).__name__},
        )
    if not context.request_id:
        raise InterpretationValidationError("request_id is required")
    if context.analysis_result is None:
        raise InterpretationPrerequisiteError("analysis_result is required")
    if not isinstance(context.analysis_result, AnalysisResult):
        raise InterpretationValidationError(
            "analysis_result must be AnalysisResult",
            details={"type": type(context.analysis_result).__name__},
        )


def validate_analysis_result(analysis: AnalysisResult) -> None:
    """Require successful publication of mandatory analytical stages."""
    missing = [
        stage_id
        for stage_id in REQUIRED_ANALYSIS_STAGES
        if analysis.get_stage_result(stage_id) is None
    ]
    if missing:
        raise InterpretationPrerequisiteError(
            "AnalysisResult is missing required stage results",
            details={"missing": missing},
        )
    failed = [
        stage_id
        for stage_id in REQUIRED_ANALYSIS_STAGES
        if (analysis.get_stage_result(stage_id) or None) is not None
        and analysis.get_stage_result(stage_id).status != "success"  # type: ignore[union-attr]
    ]
    if failed:
        raise InterpretationPrerequisiteError(
            "AnalysisResult contains non-success stage results",
            details={"failed": failed},
        )


def validate_knowledge_session(context: InterpretationContext) -> KnowledgeSession:
    """Validate and bind the Interpretation Knowledge session."""
    session = require_knowledge_session(context.knowledge_session)
    module = session.get_module(MODULE_ID)
    missing_assets = [
        asset_id for asset_id in REQUIRED_ASSETS if asset_id not in module.assets
    ]
    if missing_assets:
        # Still attempt asset fetch for fail-closed clarity.
        for asset_id in REQUIRED_ASSETS:
            session.get_asset(asset_id)
        raise InterpretationKnowledgeError(
            "interpretation_knowledge module is missing required assets",
            details={"missing_assets": missing_assets},
        )
    for asset_id in REQUIRED_ASSETS:
        session.get_asset(asset_id)
    return session


def validate_result(result: InterpretationResult) -> None:
    """Validate published InterpretationResult invariants."""
    if not result.request_id:
        raise InterpretationValidationError("InterpretationResult.request_id is required")
    if not result.sections:
        raise InterpretationValidationError(
            "InterpretationResult.sections must not be empty"
        )
    if not result.overview.strip():
        raise InterpretationValidationError(
            "InterpretationResult.overview must not be empty"
        )
    seen: set[str] = set()
    for section in result.sections:
        if section.section_id in seen:
            raise InterpretationValidationError(
                "Duplicate section_id in InterpretationResult",
                details={"section_id": section.section_id},
            )
        seen.add(section.section_id)
        if not section.body.strip():
            raise InterpretationValidationError(
                "Interpretation section body must not be empty",
                details={"section_id": section.section_id},
            )


def stage_payload(analysis: AnalysisResult, stage_id: str) -> dict[str, Any]:
    """Return a shallow copy of a stage payload."""
    stage = analysis.get_stage_result(stage_id)
    if stage is None:
        return {}
    return dict(stage.payload)
