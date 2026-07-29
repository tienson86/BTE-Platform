"""
Dayun-spec evaluators (Sprint 4.3).

Driven only by ``knowledge/luck_engine/01_dayun/DAYUN_SPEC.md``.

DAYUN_SPEC explicitly excludes cát hung scoring (§2 / §4). Therefore
Support / Attack / Strength / Stage remain UNKNOWN or NULL, while
validation (§§13–14) and structured DayunRuntime summary (§§6–7) are applied.
"""

from __future__ import annotations

import json
from typing import Any

from ..context import LuckContext
from ..dayun_validation import (
    dayun_runtime_snapshot,
    validate_dayun_runtime,
)
from ..evaluation_models import (
    UNKNOWN,
    AttackEvaluation,
    StageEvaluation,
    StrengthEvaluation,
    SummaryEvaluation,
    SupportEvaluation,
)

MappingLike = Any

_SPEC = "DAYUN_SPEC.md"
_SPEC_VERSION = "1.0"

# DAYUN_SPEC §2 / §4 — module does not evaluate cát hung / scoring.
_SUPPORT_REASONS = (
    "dayun_spec_excludes_cat_hung_evaluation",
    "dayun_spec_section_2_out_of_scope_scoring",
    "dayun_spec_section_4_no_cat_hung",
)
_ATTACK_REASONS = (
    "dayun_spec_excludes_cat_hung_evaluation",
    "dayun_spec_section_2_out_of_scope_scoring",
    "dayun_spec_section_4_no_cat_hung",
)
_STRENGTH_REASON = "dayun_spec_section_2_excludes_scoring"
_STAGE_REASON = "dayun_spec_does_not_define_luck_stage_taxonomy"


class DayunSupportEvaluator:
    """SupportEvaluator — UNKNOWN per DAYUN_SPEC (no cát hung rules)."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> SupportEvaluation:
        """Return UNKNOWN support; attach Dayun validation metadata only."""
        del rule_context, score, pattern
        validation = validate_dayun_runtime(luck.current_dayun)
        return SupportEvaluation(
            elements=(),
            level=UNKNOWN,
            reasons=_SUPPORT_REASONS,
            confidence=None,
            reason=_SUPPORT_REASONS[0],
            metadata={
                "spec": _SPEC,
                "spec_version": _SPEC_VERSION,
                "evaluator": "DayunSupportEvaluator",
                "dayun_validation": validation.to_dict(),
            },
        )


class DayunAttackEvaluator:
    """AttackEvaluator — UNKNOWN per DAYUN_SPEC (no cát hung rules)."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> AttackEvaluation:
        """Return UNKNOWN attack; attach Dayun validation metadata only."""
        del rule_context, score, pattern
        validation = validate_dayun_runtime(luck.current_dayun)
        return AttackEvaluation(
            elements=(),
            level=UNKNOWN,
            reasons=_ATTACK_REASONS,
            confidence=None,
            reason=_ATTACK_REASONS[0],
            metadata={
                "spec": _SPEC,
                "spec_version": _SPEC_VERSION,
                "evaluator": "DayunAttackEvaluator",
                "dayun_validation": validation.to_dict(),
            },
        )


class DayunLuckStrengthEvaluator:
    """
    LuckStrengthEvaluator per DAYUN_SPEC.

    ``luck_strength`` stays NULL (scoring out of scope §2).
    ``confidence`` is DayunRuntime validation pass-rate (§7 / §13).
    """

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> StrengthEvaluation:
        """Return NULL strength; confidence from Dayun validation only."""
        del rule_context, score, pattern
        validation = validate_dayun_runtime(luck.current_dayun)
        return StrengthEvaluation(
            value=None,
            confidence=validation.confidence,
            reason=_STRENGTH_REASON,
            metadata={
                "spec": _SPEC,
                "spec_version": _SPEC_VERSION,
                "evaluator": "DayunLuckStrengthEvaluator",
                "dayun_validation": validation.to_dict(),
                "confidence_source": "dayun_validation_pass_rate",
            },
        )


class DayunLuckStageEvaluator:
    """LuckStageEvaluator — UNKNOWN until a stage taxonomy is specified."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> StageEvaluation:
        """Return UNKNOWN stage; record validation status in metadata."""
        del rule_context, score, pattern
        validation = validate_dayun_runtime(luck.current_dayun)
        return StageEvaluation(
            stage=UNKNOWN,
            confidence=validation.confidence,
            reason=_STAGE_REASON,
            metadata={
                "spec": _SPEC,
                "spec_version": _SPEC_VERSION,
                "evaluator": "DayunLuckStageEvaluator",
                "dayun_validation": validation.to_dict(),
            },
        )


class DayunLuckSummaryBuilder:
    """
    Build machine-readable DayunRuntime summary (DAYUN_SPEC §§6–7).

    No natural-language interpretation.
    """

    def build(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> SummaryEvaluation:
        """Serialize structured Dayun evaluation snapshot as JSON text."""
        del rule_context, score, pattern
        validation = validate_dayun_runtime(luck.current_dayun)
        payload = {
            "kind": "dayun_runtime_summary",
            "spec": _SPEC,
            "spec_version": _SPEC_VERSION,
            "current_dayun": dayun_runtime_snapshot(luck.current_dayun),
            "validation": validation.to_dict(),
            "evaluation": {
                "support_level": luck.support_level,
                "support_elements": list(luck.support_elements),
                "attack_level": luck.attack_level,
                "attack_elements": list(luck.attack_elements),
                "luck_strength": luck.luck_strength,
                "luck_stage": luck.luck_stage,
                "confidence": luck.confidence,
            },
            "notes": [
                "summary_is_machine_readable_only",
                "no_natural_language_interpretation",
                "cat_hung_not_evaluated_per_dayun_spec",
            ],
        }
        return SummaryEvaluation(
            summary=json.dumps(payload, ensure_ascii=False, sort_keys=True),
            confidence=validation.confidence,
            reason="dayun_spec_sections_6_7_runtime_output_contract",
            metadata={
                "spec": _SPEC,
                "spec_version": _SPEC_VERSION,
                "evaluator": "DayunLuckSummaryBuilder",
                "format": "application/json",
                "dayun_validation": validation.to_dict(),
            },
        )
