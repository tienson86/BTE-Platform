"""
Default Luck evaluators (Sprint 4.2).

Framework-only: return UNKNOWN / NULL until knowledge specs define
business rules. Never fabricate favorable/unfavorable conclusions.
"""

from __future__ import annotations

from typing import Any

from ..context import LuckContext
from ..evaluation_models import (
    NO_BUSINESS_RULE,
    UNKNOWN,
    AttackEvaluation,
    StageEvaluation,
    StrengthEvaluation,
    SummaryEvaluation,
    SupportEvaluation,
)

MappingLike = Any

_FRAMEWORK_META = {
    "sprint": "4.2",
    "mode": "framework_null",
}


class NullSupportEvaluator:
    """SupportEvaluator default — no business rule yet."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> SupportEvaluation:
        """Return UNKNOWN support level with empty elements."""
        del luck, rule_context, score, pattern
        return SupportEvaluation(
            elements=(),
            level=UNKNOWN,
            confidence=None,
            reason=NO_BUSINESS_RULE,
            metadata={**_FRAMEWORK_META, "evaluator": "NullSupportEvaluator"},
        )


class NullAttackEvaluator:
    """AttackEvaluator default — no business rule yet."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> AttackEvaluation:
        """Return UNKNOWN attack level with empty elements."""
        del luck, rule_context, score, pattern
        return AttackEvaluation(
            elements=(),
            level=UNKNOWN,
            confidence=None,
            reason=NO_BUSINESS_RULE,
            metadata={**_FRAMEWORK_META, "evaluator": "NullAttackEvaluator"},
        )


class NullLuckStrengthEvaluator:
    """LuckStrengthEvaluator default — strength remains NULL."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> StrengthEvaluation:
        """Return NULL strength until a rule defines a scale."""
        del luck, rule_context, score, pattern
        return StrengthEvaluation(
            value=None,
            confidence=None,
            reason=NO_BUSINESS_RULE,
            metadata={
                **_FRAMEWORK_META,
                "evaluator": "NullLuckStrengthEvaluator",
            },
        )


class NullLuckStageEvaluator:
    """LuckStageEvaluator default — stage is UNKNOWN."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> StageEvaluation:
        """Return UNKNOWN stage until knowledge defines stages."""
        del luck, rule_context, score, pattern
        return StageEvaluation(
            stage=UNKNOWN,
            confidence=None,
            reason=NO_BUSINESS_RULE,
            metadata={**_FRAMEWORK_META, "evaluator": "NullLuckStageEvaluator"},
        )


class NullLuckSummaryBuilder:
    """LuckSummaryBuilder default — summary remains NULL (no narrative)."""

    def build(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> SummaryEvaluation:
        """Return NULL summary; does not invent interpretation text."""
        del luck, rule_context, score, pattern
        return SummaryEvaluation(
            summary=None,
            confidence=None,
            reason=NO_BUSINESS_RULE,
            metadata={
                **_FRAMEWORK_META,
                "evaluator": "NullLuckSummaryBuilder",
            },
        )
