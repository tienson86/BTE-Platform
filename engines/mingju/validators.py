"""Fail-closed MC-01 validators. Do not silently repair."""

from __future__ import annotations

from engines.mingju.enums import AnalysisState, IntegrityState, PatternGrade
from engines.mingju.exceptions import MingJuValidationError, MingJuVersionError
from engines.mingju.models import MingJuContext, MingJuDecisionResult
from engines.mingju.versions import RULESET_VERSION, SCHEMA_CONTEXT, SCHEMA_DECISION


def validate_context(context: MingJuContext) -> None:
    """Reject unsupported context schema."""
    if context.schema_version != SCHEMA_CONTEXT:
        raise MingJuVersionError(f"unsupported context schema: {context.schema_version}")


def validate_result(result: MingJuDecisionResult, context: MingJuContext) -> None:
    """Fail closed on corrupt references, missing Grade inputs, and version errors."""
    if result.schema_version != SCHEMA_DECISION:
        raise MingJuVersionError(f"unsupported decision schema: {result.schema_version}")
    if result.ruleset_version != RULESET_VERSION:
        raise MingJuVersionError(f"unsupported ruleset: {result.ruleset_version}")
    if result.analysis_id and context.analysis_id and result.analysis_id != context.analysis_id:
        raise MingJuValidationError("analysis_id mismatch")
    if result.pattern.state == AnalysisState.RESOLVED.value and not result.pattern.pattern_id:
        raise MingJuValidationError("invalid Pattern reference")
    if result.pattern.state == AnalysisState.RESOLVED.value and not result.pattern.family:
        raise MingJuValidationError("invalid Pattern family")
    damage_ids = {item.damage_id for item in result.damage.findings}
    if len(damage_ids) != len(result.damage.findings):
        raise MingJuValidationError("duplicate Damage ids")
    for item in result.damage.findings:
        if not item.damage_id or not item.source or not item.target:
            raise MingJuValidationError("corrupt Damage reference")
        if not item.evidence_ids or not item.trace_ids:
            raise MingJuValidationError("Damage missing evidence or trace")
    for rescue_item in result.rescue.findings:
        if not rescue_item.rescue_id or not rescue_item.target_damage_ids:
            raise MingJuValidationError("corrupt Rescue reference")
        if any(target not in damage_ids for target in rescue_item.target_damage_ids):
            raise MingJuValidationError("Rescue targets unknown Damage")
        if not rescue_item.evidence_ids:
            raise MingJuValidationError("Rescue missing evidence")
    if result.grade.state == AnalysisState.RESOLVED.value:
        if result.integrity.state == IntegrityState.UNRESOLVED.value:
            raise MingJuValidationError("Grade without required Integrity")
        if result.grade.grade == PatternGrade.UNRESOLVED.value:
            raise MingJuValidationError("resolved Grade cannot be UNRESOLVED")
        if result.purity.state != AnalysisState.RESOLVED.value:
            raise MingJuValidationError("Grade without required Purity")
        if result.pattern_strength.state != AnalysisState.RESOLVED.value:
            raise MingJuValidationError("Grade without required Pattern Strength")
        if result.grade.grade not in {item.value for item in PatternGrade if item is not PatternGrade.UNRESOLVED}:
            raise MingJuValidationError("unknown MC-01 Grade")
    if result.grade.score is not None and not 0 <= result.grade.score <= 100:
        raise MingJuValidationError("Grade score out of range")
    if result.confidence < 0 or result.confidence > 1:
        raise MingJuValidationError("confidence out of range")
    for dimension in result.wealth.dimensions:
        if dimension.dimension == "financial_volatility" and dimension.polarity != "higher_is_riskier":
            raise MingJuValidationError("wealth volatility polarity must be higher_is_riskier")
    if result.career.state == AnalysisState.RESOLVED.value and result.achievement.state != AnalysisState.RESOLVED.value:
        raise MingJuValidationError("Career requires Achievement")
