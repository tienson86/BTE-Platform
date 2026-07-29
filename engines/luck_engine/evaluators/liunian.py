"""
Liunian-spec evaluators (Sprint 4.4).

Driven only by written sections of ``LIUNIAN_SPEC.md``.

Support / Attack / Strength / Stage remain UNKNOWN or NULL where the SPEC
does not define level taxonomies or scoring (§§21–33 incomplete). Validation
and structured AnnualContext snapshot follow §§7–13 / §18.
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
from ..liunian_validation import validate_liunian_runtime

MappingLike = Any

_SPEC = "LIUNIAN_SPEC.md"
_SPEC_VERSION = "1.0"

_SUPPORT_REASONS = (
    "liunian_spec_no_support_level_taxonomy_in_written_sections",
    "liunian_spec_sections_27_28_incomplete",
    "liunian_spec_avoids_interpretation",
)
_ATTACK_REASONS = (
    "liunian_spec_no_attack_level_taxonomy_in_written_sections",
    "liunian_spec_clash_harm_require_rule_database",
    "liunian_spec_sections_21_33_incomplete",
)
_STRENGTH_REASON = "liunian_spec_section_27_annual_strength_not_written"
_STAGE_REASON = "liunian_spec_does_not_define_luck_stage_taxonomy"


class LiunianSupportEvaluator:
    """SupportEvaluator — UNKNOWN until SPEC defines support levels."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> SupportEvaluation:
        """Return UNKNOWN support; attach Liunian validation metadata."""
        del rule_context, score, pattern
        validation = validate_liunian_runtime(
            luck.current_liunian,
            dayun=luck.current_dayun,
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
                "evaluator": "LiunianSupportEvaluator",
                "layer": "liunian",
                "liunian_validation": validation.to_dict(),
            },
        )


class LiunianAttackEvaluator:
    """AttackEvaluator — UNKNOWN until clash/harm rules are fully specified."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> AttackEvaluation:
        """Return UNKNOWN attack; attach Liunian validation metadata."""
        del rule_context, score, pattern
        validation = validate_liunian_runtime(
            luck.current_liunian,
            dayun=luck.current_dayun,
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
                "evaluator": "LiunianAttackEvaluator",
                "layer": "liunian",
                "liunian_validation": validation.to_dict(),
            },
        )


class LiunianLuckStrengthEvaluator:
    """LuckStrengthEvaluator — NULL; §27 Annual Strength not written."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> StrengthEvaluation:
        """Return NULL strength; confidence from Liunian validation only."""
        del rule_context, score, pattern
        validation = validate_liunian_runtime(
            luck.current_liunian,
            dayun=luck.current_dayun,
        )
        return StrengthEvaluation(
            value=None,
            confidence=validation.confidence,
            reason=_STRENGTH_REASON,
            metadata={
                "spec": _SPEC,
                "spec_version": _SPEC_VERSION,
                "evaluator": "LiunianLuckStrengthEvaluator",
                "layer": "liunian",
                "liunian_validation": validation.to_dict(),
                "confidence_source": "liunian_validation_pass_rate",
            },
        )


class LiunianLuckStageEvaluator:
    """LuckStageEvaluator — UNKNOWN; no stage taxonomy in LIUNIAN_SPEC."""

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
        validation = validate_liunian_runtime(
            luck.current_liunian,
            dayun=luck.current_dayun,
        )
        return StageEvaluation(
            stage=UNKNOWN,
            confidence=validation.confidence,
            reason=_STAGE_REASON,
            metadata={
                "spec": _SPEC,
                "spec_version": _SPEC_VERSION,
                "evaluator": "LiunianLuckStageEvaluator",
                "layer": "liunian",
                "liunian_validation": validation.to_dict(),
            },
        )
