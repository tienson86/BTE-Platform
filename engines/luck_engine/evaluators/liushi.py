"""
Liushi-spec evaluators (Sprint 4.7).

Driven only by ``LIUSHI_SPEC.md``. Support/Attack/Strength/Stage stay
UNKNOWN or NULL where the SPEC defines no level taxonomy or numeric score.
"""

from __future__ import annotations

from typing import Any

from ..context import LuckContext
from ..evaluation_models import (
    UNKNOWN,
    AttackEvaluation,
    StageEvaluation,
    StrengthEvaluation,
    SupportEvaluation,
)
from ..liushi_validation import validate_liushi_runtime

MappingLike = Any

_SPEC = "LIUSHI_SPEC.md"
_SPEC_VERSION = "1.0"

_SUPPORT_REASONS = (
    "liushi_spec_no_support_level_taxonomy",
    "liushi_spec_sections_29_30_are_flags_not_support_level",
    "liushi_spec_avoids_interpretation",
)
_ATTACK_REASONS = (
    "liushi_spec_no_attack_level_taxonomy",
    "liushi_spec_clash_harm_require_rule_database",
    "liushi_spec_sections_18_28_incomplete_without_rule_db",
)
_STRENGTH_REASON = "liushi_spec_no_numeric_strength_formula"
_STAGE_REASON = "liushi_spec_section_31_risk_flags_are_not_luck_stage_taxonomy"


class LiushiSupportEvaluator:
    """SupportEvaluator — UNKNOWN until SPEC defines support levels."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> SupportEvaluation:
        """Return UNKNOWN support; attach Liushi validation metadata."""
        del rule_context, score, pattern
        validation = validate_liushi_runtime(
            luck.current_liushi,
            dayun=luck.current_dayun,
            liunian=luck.current_liunian,
            liuyue=luck.current_liuyue,
            liuri=luck.current_liuri,
        )
        return SupportEvaluation(
            elements=(),
            level=UNKNOWN,
            reasons=_SUPPORT_REASONS + tuple(validation.reasons),
            confidence=None,
            reason=_SUPPORT_REASONS[0],
            metadata={
                "spec": _SPEC,
                "spec_version": _SPEC_VERSION,
                "evaluator": "LiushiSupportEvaluator",
                "layer": "liushi",
                "liushi_validation": validation.to_dict(),
            },
        )


class LiushiAttackEvaluator:
    """AttackEvaluator — UNKNOWN until clash/harm rules are fully specified."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> AttackEvaluation:
        """Return UNKNOWN attack; attach Liushi validation metadata."""
        del rule_context, score, pattern
        validation = validate_liushi_runtime(
            luck.current_liushi,
            dayun=luck.current_dayun,
            liunian=luck.current_liunian,
            liuyue=luck.current_liuyue,
            liuri=luck.current_liuri,
        )
        return AttackEvaluation(
            elements=(),
            level=UNKNOWN,
            reasons=_ATTACK_REASONS + tuple(validation.reasons),
            confidence=None,
            reason=_ATTACK_REASONS[0],
            metadata={
                "spec": _SPEC,
                "spec_version": _SPEC_VERSION,
                "evaluator": "LiushiAttackEvaluator",
                "layer": "liushi",
                "liushi_validation": validation.to_dict(),
            },
        )


class LiushiLuckStrengthEvaluator:
    """LuckStrengthEvaluator — NULL; no numeric strength formula in SPEC."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> StrengthEvaluation:
        """Return NULL strength; confidence from Liushi validation only."""
        del rule_context, score, pattern
        validation = validate_liushi_runtime(
            luck.current_liushi,
            dayun=luck.current_dayun,
            liunian=luck.current_liunian,
            liuyue=luck.current_liuyue,
            liuri=luck.current_liuri,
        )
        return StrengthEvaluation(
            value=None,
            confidence=validation.confidence,
            reason=_STRENGTH_REASON,
            metadata={
                "spec": _SPEC,
                "spec_version": _SPEC_VERSION,
                "evaluator": "LiushiLuckStrengthEvaluator",
                "layer": "liushi",
                "liushi_validation": validation.to_dict(),
                "confidence_source": "liushi_validation_pass_rate",
            },
        )


class LiushiLuckStageEvaluator:
    """LuckStageEvaluator — UNKNOWN; §31 risk flags ≠ luck_stage taxonomy."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> StageEvaluation:
        """Return UNKNOWN stage; record validation in metadata."""
        del rule_context, score, pattern
        validation = validate_liushi_runtime(
            luck.current_liushi,
            dayun=luck.current_dayun,
            liunian=luck.current_liunian,
            liuyue=luck.current_liuyue,
            liuri=luck.current_liuri,
        )
        return StageEvaluation(
            stage=UNKNOWN,
            confidence=validation.confidence,
            reason=_STAGE_REASON,
            metadata={
                "spec": _SPEC,
                "spec_version": _SPEC_VERSION,
                "evaluator": "LiushiLuckStageEvaluator",
                "layer": "liushi",
                "liushi_validation": validation.to_dict(),
            },
        )
