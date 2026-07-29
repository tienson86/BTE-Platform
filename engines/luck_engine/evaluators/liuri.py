"""
Liuri-spec evaluators (Sprint 4.6).

Driven only by ``LIURI_SPEC.md``. Support/Attack/Strength/Stage stay
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
from ..liuri_validation import validate_liuri_runtime

MappingLike = Any

_SPEC = "LIURI_SPEC.md"
_SPEC_VERSION = "1.0"

_SUPPORT_REASONS = (
    "liuri_spec_no_support_level_taxonomy",
    "liuri_spec_sections_27_28_are_flags_not_support_level",
    "liuri_spec_avoids_interpretation",
)
_ATTACK_REASONS = (
    "liuri_spec_no_attack_level_taxonomy",
    "liuri_spec_clash_harm_require_rule_database",
    "liuri_spec_sections_17_25_incomplete_without_rule_db",
)
_STRENGTH_REASON = "liuri_spec_no_numeric_strength_formula"
_STAGE_REASON = "liuri_spec_section_29_risk_flags_are_not_luck_stage_taxonomy"


class LiuriSupportEvaluator:
    """SupportEvaluator — UNKNOWN until SPEC defines support levels."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> SupportEvaluation:
        """Return UNKNOWN support; attach Liuri validation metadata."""
        del rule_context, score, pattern
        validation = validate_liuri_runtime(
            luck.current_liuri,
            dayun=luck.current_dayun,
            liunian=luck.current_liunian,
            liuyue=luck.current_liuyue,
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
                "evaluator": "LiuriSupportEvaluator",
                "layer": "liuri",
                "liuri_validation": validation.to_dict(),
            },
        )


class LiuriAttackEvaluator:
    """AttackEvaluator — UNKNOWN until clash/harm rules are fully specified."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> AttackEvaluation:
        """Return UNKNOWN attack; attach Liuri validation metadata."""
        del rule_context, score, pattern
        validation = validate_liuri_runtime(
            luck.current_liuri,
            dayun=luck.current_dayun,
            liunian=luck.current_liunian,
            liuyue=luck.current_liuyue,
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
                "evaluator": "LiuriAttackEvaluator",
                "layer": "liuri",
                "liuri_validation": validation.to_dict(),
            },
        )


class LiuriLuckStrengthEvaluator:
    """LuckStrengthEvaluator — NULL; no numeric strength formula in SPEC."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> StrengthEvaluation:
        """Return NULL strength; confidence from Liuri validation only."""
        del rule_context, score, pattern
        validation = validate_liuri_runtime(
            luck.current_liuri,
            dayun=luck.current_dayun,
            liunian=luck.current_liunian,
            liuyue=luck.current_liuyue,
        )
        return StrengthEvaluation(
            value=None,
            confidence=validation.confidence,
            reason=_STRENGTH_REASON,
            metadata={
                "spec": _SPEC,
                "spec_version": _SPEC_VERSION,
                "evaluator": "LiuriLuckStrengthEvaluator",
                "layer": "liuri",
                "liuri_validation": validation.to_dict(),
                "confidence_source": "liuri_validation_pass_rate",
            },
        )


class LiuriLuckStageEvaluator:
    """LuckStageEvaluator — UNKNOWN; §29 risk flags ≠ luck_stage taxonomy."""

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
        validation = validate_liuri_runtime(
            luck.current_liuri,
            dayun=luck.current_dayun,
            liunian=luck.current_liunian,
            liuyue=luck.current_liuyue,
        )
        return StageEvaluation(
            stage=UNKNOWN,
            confidence=validation.confidence,
            reason=_STAGE_REASON,
            metadata={
                "spec": _SPEC,
                "spec_version": _SPEC_VERSION,
                "evaluator": "LiuriLuckStageEvaluator",
                "layer": "liuri",
                "liuri_validation": validation.to_dict(),
            },
        )
