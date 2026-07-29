"""
Luck Engine — Stage Luck (Sprint 4 → 4.2).

Consumes Calendar / BaZi / Pattern / RuleContext / ScoreResult.
Produces LuckContext. Does not calculate BaZi, Pattern, Useful God,
Strength, Temperature, or Combination. Does not mutate RuleContext.

Sprint 4.1: runtime providers.
Sprint 4.2: evaluation framework.
Sprint 4.3: Dayun-spec evaluators.
Sprint 4.4: Dayun → Liunian layered evaluators.
Sprint 4.5: Dayun → Liunian → Liuyue layered evaluators.
Sprint 4.6: Dayun → Liunian → Liuyue → Liuri layered evaluators.
Sprint 4.7: five-layer Dayun…Liushi evaluators + combined summary.
"""

from __future__ import annotations

import logging
from dataclasses import replace
from typing import Any

from .context import LuckContext
from .evaluators import (
    CombinedLuckSummaryBuilder,
    LayeredAttackEvaluator,
    LayeredLuckStageEvaluator,
    LayeredLuckStrengthEvaluator,
    LayeredSupportEvaluator,
)
from .exceptions import LuckContextError
from .interfaces import (
    AttackEvaluator,
    DayunProvider,
    LiunianProvider,
    LiuriProvider,
    LiushiProvider,
    LiuyueProvider,
    LuckEvaluator,
    LuckStageEvaluator,
    LuckStrengthEvaluator,
    LuckSummaryBuilder,
    SupportEvaluator,
)
from .providers import (
    DefaultDayunProvider,
    DefaultLiunianProvider,
    DefaultLiuriProvider,
    DefaultLiushiProvider,
    DefaultLiuyueProvider,
)

logger = logging.getLogger(__name__)


class LuckEngine:
    """
    Standalone Luck Engine.

    Flow
    ----
    Providers → Support → Attack → Strength → Stage → Summary → LuckContext

    Default evaluators layer Dayun then Liunian inside each pipeline slot.
    """

    def __init__(
        self,
        *,
        dayun_provider: DayunProvider | None = None,
        liunian_provider: LiunianProvider | None = None,
        liuyue_provider: LiuyueProvider | None = None,
        liuri_provider: LiuriProvider | None = None,
        liushi_provider: LiushiProvider | None = None,
        support_evaluator: SupportEvaluator | None = None,
        attack_evaluator: AttackEvaluator | None = None,
        strength_evaluator: LuckStrengthEvaluator | None = None,
        stage_evaluator: LuckStageEvaluator | None = None,
        summary_builder: LuckSummaryBuilder | None = None,
        luck_evaluator: LuckEvaluator | None = None,
        use_default_providers: bool = True,
        use_default_evaluators: bool = True,
    ) -> None:
        """
        Inject providers and evaluators.

        Defaults (Sprint 4.7): five-layer Dayun → … → Liushi evaluators and a
        combined machine-readable summary. Prior layers remain unchanged.
        """
        if use_default_providers:
            dayun_provider = dayun_provider or DefaultDayunProvider()
            liunian_provider = liunian_provider or DefaultLiunianProvider()
            liuyue_provider = liuyue_provider or DefaultLiuyueProvider()
            liuri_provider = liuri_provider or DefaultLiuriProvider()
            liushi_provider = liushi_provider or DefaultLiushiProvider()

        if use_default_evaluators:
            support_evaluator = support_evaluator or LayeredSupportEvaluator()
            attack_evaluator = attack_evaluator or LayeredAttackEvaluator()
            strength_evaluator = (
                strength_evaluator or LayeredLuckStrengthEvaluator()
            )
            stage_evaluator = stage_evaluator or LayeredLuckStageEvaluator()
            summary_builder = summary_builder or CombinedLuckSummaryBuilder()

        self.dayun_provider = dayun_provider
        self.liunian_provider = liunian_provider
        self.liuyue_provider = liuyue_provider
        self.liuri_provider = liuri_provider
        self.liushi_provider = liushi_provider
        self.support_evaluator = support_evaluator
        self.attack_evaluator = attack_evaluator
        self.strength_evaluator = strength_evaluator
        self.stage_evaluator = stage_evaluator
        self.summary_builder = summary_builder
        self.luck_evaluator = luck_evaluator

    def build(
        self,
        *,
        calendar: Any = None,
        bazi: Any = None,
        pattern: Any = None,
        rule_context: dict[str, Any] | None = None,
        score: Any = None,
    ) -> LuckContext:
        """
        Build LuckContext from upstream runtime objects.

        Never mutates ``rule_context``. Evaluation fields are populated
        only through evaluators (UNKNOWN / NULL when no business rule).
        """
        if rule_context is not None and not isinstance(rule_context, dict):
            raise LuckContextError("rule_context must be a dict when provided.")

        current_dayun = self._safe_provide(
            self.dayun_provider,
            calendar=calendar,
            bazi=bazi,
            rule_context=rule_context,
        )
        current_liunian = self._safe_provide(
            self.liunian_provider,
            calendar=calendar,
            bazi=bazi,
            dayun=current_dayun,
        )
        current_liuyue = self._safe_provide(
            self.liuyue_provider,
            calendar=calendar,
            bazi=bazi,
            liunian=current_liunian,
        )
        current_liuri = self._safe_provide(
            self.liuri_provider,
            calendar=calendar,
            bazi=bazi,
            liuyue=current_liuyue,
        )
        current_liushi = self._safe_provide(
            self.liushi_provider,
            calendar=calendar,
            bazi=bazi,
            liuri=current_liuri,
        )

        has_any = any(
            value is not None
            for value in (
                current_dayun,
                current_liunian,
                current_liuyue,
                current_liuri,
                current_liushi,
            )
        )

        luck = LuckContext(
            current_dayun=current_dayun,
            current_liunian=current_liunian,
            current_liuyue=current_liuyue,
            current_liuri=current_liuri,
            current_liushi=current_liushi,
            available=bool(has_any),
            reason=None if has_any else "luck_providers_unavailable",
            metadata={
                "engine": "engines.luck_engine.engine.LuckEngine",
                "sprint": "4.7_liushi_rule_evaluation",
                "providers_injected": {
                    "dayun": self.dayun_provider is not None,
                    "liunian": self.liunian_provider is not None,
                    "liuyue": self.liuyue_provider is not None,
                    "liuri": self.liuri_provider is not None,
                    "liushi": self.liushi_provider is not None,
                },
                "evaluators_injected": {
                    "support": self.support_evaluator is not None,
                    "attack": self.attack_evaluator is not None,
                    "strength": self.strength_evaluator is not None,
                    "stage": self.stage_evaluator is not None,
                    "summary": self.summary_builder is not None,
                    "legacy_luck": self.luck_evaluator is not None,
                },
                "upstream": {
                    "has_calendar": calendar is not None,
                    "has_bazi": bazi is not None,
                    "has_pattern": pattern is not None,
                    "has_rule_context": rule_context is not None,
                    "has_score": score is not None,
                },
            },
        )

        luck = self._run_evaluation_pipeline(
            luck,
            rule_context=rule_context,
            score=score,
            pattern=pattern,
        )

        if self.luck_evaluator is not None:
            try:
                luck = self.luck_evaluator.evaluate(
                    luck=luck,
                    rule_context=rule_context,
                    score=score,
                    pattern=pattern,
                )
            except Exception as exc:
                logger.warning(
                    "Legacy LuckEvaluator %s failed: %s",
                    type(self.luck_evaluator).__name__,
                    exc,
                )

        logger.debug(
            "LuckEngine.build available=%s reason=%s stage=%s strength=%s",
            luck.available,
            luck.reason,
            luck.luck_stage,
            luck.luck_strength,
        )
        return luck

    def _run_evaluation_pipeline(
        self,
        luck: LuckContext,
        *,
        rule_context: dict[str, Any] | None,
        score: Any,
        pattern: Any,
    ) -> LuckContext:
        """
        Support → Attack → Strength → Stage → Summary.

        Each step returns a new LuckContext via ``dataclasses.replace``.
        """
        evaluation_trace: dict[str, Any] = {}

        if self.support_evaluator is not None:
            support = self._safe_evaluate(
                self.support_evaluator.evaluate,
                luck=luck,
                rule_context=rule_context,
                score=score,
                pattern=pattern,
            )
            if support is not None:
                luck = replace(
                    luck,
                    support_elements=tuple(support.elements or ()),
                    support_level=support.level,
                )
                evaluation_trace["support"] = support.to_dict()

        if self.attack_evaluator is not None:
            attack = self._safe_evaluate(
                self.attack_evaluator.evaluate,
                luck=luck,
                rule_context=rule_context,
                score=score,
                pattern=pattern,
            )
            if attack is not None:
                luck = replace(
                    luck,
                    attack_elements=tuple(attack.elements or ()),
                    attack_level=attack.level,
                )
                evaluation_trace["attack"] = attack.to_dict()

        if self.strength_evaluator is not None:
            strength = self._safe_evaluate(
                self.strength_evaluator.evaluate,
                luck=luck,
                rule_context=rule_context,
                score=score,
                pattern=pattern,
            )
            if strength is not None:
                luck = replace(
                    luck,
                    luck_strength=strength.value,
                    confidence=strength.confidence,
                )
                evaluation_trace["strength"] = strength.to_dict()

        if self.stage_evaluator is not None:
            stage = self._safe_evaluate(
                self.stage_evaluator.evaluate,
                luck=luck,
                rule_context=rule_context,
                score=score,
                pattern=pattern,
            )
            if stage is not None:
                luck = replace(luck, luck_stage=stage.stage)
                evaluation_trace["stage"] = stage.to_dict()

        if self.summary_builder is not None:
            summary = self._safe_evaluate(
                self.summary_builder.build,
                luck=luck,
                rule_context=rule_context,
                score=score,
                pattern=pattern,
            )
            if summary is not None:
                luck = replace(luck, luck_summary=summary.summary)
                evaluation_trace["summary"] = summary.to_dict()

        if evaluation_trace:
            meta = dict(luck.metadata)
            meta["evaluation"] = {
                "pipeline": [
                    "support",
                    "attack",
                    "strength",
                    "stage",
                    "summary",
                ],
                "status": "five_layer_luck_evaluation_executed",
                "business_rules": [
                    "DAYUN_SPEC.md",
                    "LIUNIAN_SPEC.md",
                    "LIUYUE_SPEC.md",
                    "LIURI_SPEC.md",
                    "LIUSHI_SPEC.md",
                ],
                "layer_order": [
                    "dayun",
                    "liunian",
                    "liuyue",
                    "liuri",
                    "liushi",
                ],
                "results": evaluation_trace,
            }
            luck = replace(luck, metadata=meta)

        return luck

    @staticmethod
    def _safe_provide(provider: Any, **kwargs: Any) -> Any | None:
        """Call provider when present; return None on absence or soft failure."""
        if provider is None:
            return None
        try:
            return provider.provide(**kwargs)
        except Exception as exc:
            logger.warning(
                "Luck provider %s failed: %s",
                type(provider).__name__,
                exc,
            )
            return None

    @staticmethod
    def _safe_evaluate(fn: Any, **kwargs: Any) -> Any | None:
        """Call evaluator step; return None on soft failure."""
        try:
            return fn(**kwargs)
        except Exception as exc:
            logger.warning("Luck evaluator step failed: %s", exc)
            return None
