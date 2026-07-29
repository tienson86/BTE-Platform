"""
Liuyue-spec evaluators (Sprint 4.5).

Driven only by written sections of ``LIUYUE_SPEC.md``.

Support / Attack / Strength / Stage remain UNKNOWN or NULL where the SPEC
does not define taxonomies or scoring (§§21–36 incomplete).
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
from ..liuyue_validation import validate_liuyue_runtime

MappingLike = Any

_SPEC = "LIUYUE_SPEC.md"
_SPEC_VERSION = "1.0"

_SUPPORT_REASONS = (
    "liuyue_spec_no_support_level_taxonomy_in_written_sections",
    "liuyue_spec_sections_26_28_incomplete",
    "liuyue_spec_avoids_interpretation",
)
_ATTACK_REASONS = (
    "liuyue_spec_no_attack_level_taxonomy_in_written_sections",
    "liuyue_spec_clash_harm_require_rule_database",
    "liuyue_spec_sections_21_32_incomplete",
)
_STRENGTH_REASON = "liuyue_spec_section_26_seasonal_strength_not_written"
_STAGE_REASON = "liuyue_spec_does_not_define_luck_stage_taxonomy"


class LiuyueSupportEvaluator:
    """SupportEvaluator — UNKNOWN until SPEC defines support levels."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> SupportEvaluation:
        """Return UNKNOWN support; attach Liuyue validation metadata."""
        del rule_context, score, pattern
        validation = validate_liuyue_runtime(
            luck.current_liuyue,
            dayun=luck.current_dayun,
            liunian=luck.current_liunian,
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
                "evaluator": "LiuyueSupportEvaluator",
                "layer": "liuyue",
                "liuyue_validation": validation.to_dict(),
            },
        )


class LiuyueAttackEvaluator:
    """AttackEvaluator — UNKNOWN until clash/harm rules are fully specified."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> AttackEvaluation:
        """Return UNKNOWN attack; attach Liuyue validation metadata."""
        del rule_context, score, pattern
        validation = validate_liuyue_runtime(
            luck.current_liuyue,
            dayun=luck.current_dayun,
            liunian=luck.current_liunian,
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
                "evaluator": "LiuyueAttackEvaluator",
                "layer": "liuyue",
                "liuyue_validation": validation.to_dict(),
            },
        )


class LiuyueLuckStrengthEvaluator:
    """LuckStrengthEvaluator — NULL; seasonal strength §26 not written."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> StrengthEvaluation:
        """Return NULL strength; confidence from Liuyue validation only."""
        del rule_context, score, pattern
        validation = validate_liuyue_runtime(
            luck.current_liuyue,
            dayun=luck.current_dayun,
            liunian=luck.current_liunian,
        )
        return StrengthEvaluation(
            value=None,
            confidence=validation.confidence,
            reason=_STRENGTH_REASON,
            metadata={
                "spec": _SPEC,
                "spec_version": _SPEC_VERSION,
                "evaluator": "LiuyueLuckStrengthEvaluator",
                "layer": "liuyue",
                "liuyue_validation": validation.to_dict(),
                "confidence_source": "liuyue_validation_pass_rate",
            },
        )


class LiuyueLuckStageEvaluator:
    """LuckStageEvaluator — UNKNOWN; no stage taxonomy in LIUYUE_SPEC."""

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
        validation = validate_liuyue_runtime(
            luck.current_liuyue,
            dayun=luck.current_dayun,
            liunian=luck.current_liunian,
        )
        return StageEvaluation(
            stage=UNKNOWN,
            confidence=validation.confidence,
            reason=_STAGE_REASON,
            metadata={
                "spec": _SPEC,
                "spec_version": _SPEC_VERSION,
                "evaluator": "LiuyueLuckStageEvaluator",
                "layer": "liuyue",
                "liuyue_validation": validation.to_dict(),
            },
        )
