"""
Layered Dayun → Liunian → Liuyue → Liuri → Liushi evaluators (Sprint 4.4–4.7).

Preserves prior layer evaluators; merges into a single evaluation result
without changing LuckContext schema or pipeline slots.
"""

from __future__ import annotations

import json
from typing import Any

from ..context import LuckContext
from ..dayun_validation import dayun_runtime_snapshot, validate_dayun_runtime
from ..evaluation_models import (
    UNKNOWN,
    AttackEvaluation,
    StageEvaluation,
    StrengthEvaluation,
    SummaryEvaluation,
    SupportEvaluation,
)
from ..liunian_validation import (
    liunian_runtime_snapshot,
    validate_liunian_runtime,
)
from ..liuri_validation import liuri_runtime_snapshot, validate_liuri_runtime
from ..liushi_validation import (
    liushi_runtime_snapshot,
    validate_liushi_runtime,
)
from ..liuyue_validation import (
    liuyue_runtime_snapshot,
    validate_liuyue_runtime,
)
from .dayun import (
    DayunAttackEvaluator,
    DayunLuckStageEvaluator,
    DayunLuckStrengthEvaluator,
    DayunSupportEvaluator,
)
from .liunian import (
    LiunianAttackEvaluator,
    LiunianLuckStageEvaluator,
    LiunianLuckStrengthEvaluator,
    LiunianSupportEvaluator,
)
from .liuri import (
    LiuriAttackEvaluator,
    LiuriLuckStageEvaluator,
    LiuriLuckStrengthEvaluator,
    LiuriSupportEvaluator,
)
from .liushi import (
    LiushiAttackEvaluator,
    LiushiLuckStageEvaluator,
    LiushiLuckStrengthEvaluator,
    LiushiSupportEvaluator,
)
from .liuyue import (
    LiuyueAttackEvaluator,
    LiuyueLuckStageEvaluator,
    LiuyueLuckStrengthEvaluator,
    LiuyueSupportEvaluator,
)

MappingLike = Any

LAYER_ORDER: tuple[str, ...] = (
    "dayun",
    "liunian",
    "liuyue",
    "liuri",
    "liushi",
)


def _merge_levels(*levels: str | None) -> str | None:
    """Merge layer levels without inventing a combined taxonomy."""
    concrete = [level for level in levels if level not in (None, UNKNOWN)]
    if not concrete:
        return UNKNOWN
    if len(set(concrete)) == 1:
        return concrete[0]
    return UNKNOWN


def _merge_confidence(*confidences: float | None) -> float | None:
    """Runtime confidence = min of available layer validation rates."""
    values = [value for value in confidences if value is not None]
    if not values:
        return None
    return min(values)


def _merge_strength_values(*values: float | None) -> float | None:
    """Keep a strength value only when all non-null values agree."""
    concrete = [value for value in values if value is not None]
    if not concrete:
        return None
    if len(set(concrete)) == 1:
        return concrete[0]
    return None


def _run_layers(
    dayun: Any,
    liunian: Any,
    liuyue: Any,
    liuri: Any,
    liushi: Any,
    *,
    luck: LuckContext,
    rule_context: MappingLike | None,
    score: Any | None,
    pattern: Any | None,
) -> tuple[Any, Any, Any, Any, Any]:
    """Evaluate five layers in frozen order."""
    kwargs = {
        "luck": luck,
        "rule_context": rule_context,
        "score": score,
        "pattern": pattern,
    }
    return (
        dayun.evaluate(**kwargs),
        liunian.evaluate(**kwargs),
        liuyue.evaluate(**kwargs),
        liuri.evaluate(**kwargs),
        liushi.evaluate(**kwargs),
    )


class LayeredSupportEvaluator:
    """Dayun → Liunian → Liuyue → Liuri → Liushi Support."""

    def __init__(
        self,
        *,
        dayun: DayunSupportEvaluator | None = None,
        liunian: LiunianSupportEvaluator | None = None,
        liuyue: LiuyueSupportEvaluator | None = None,
        liuri: LiuriSupportEvaluator | None = None,
        liushi: LiushiSupportEvaluator | None = None,
    ) -> None:
        """Inject layer evaluators."""
        self.dayun = dayun or DayunSupportEvaluator()
        self.liunian = liunian or LiunianSupportEvaluator()
        self.liuyue = liuyue or LiuyueSupportEvaluator()
        self.liuri = liuri or LiuriSupportEvaluator()
        self.liushi = liushi or LiushiSupportEvaluator()

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> SupportEvaluation:
        """Run five layers; merge UNKNOWN-safe support fields."""
        d, n, y, r, s = _run_layers(
            self.dayun,
            self.liunian,
            self.liuyue,
            self.liuri,
            self.liushi,
            luck=luck,
            rule_context=rule_context,
            score=score,
            pattern=pattern,
        )
        elements = tuple(
            dict.fromkeys(
                list(d.elements)
                + list(n.elements)
                + list(y.elements)
                + list(r.elements)
                + list(s.elements)
            )
        )
        reasons = (
            tuple(d.reasons)
            + tuple(n.reasons)
            + tuple(y.reasons)
            + tuple(r.reasons)
            + tuple(s.reasons)
        )
        return SupportEvaluation(
            elements=elements,
            level=_merge_levels(d.level, n.level, y.level, r.level, s.level),
            reasons=reasons,
            confidence=None,
            reason="layered_five_layer_support",
            metadata={
                "layer_order": list(LAYER_ORDER),
                "dayun": d.to_dict(),
                "liunian": n.to_dict(),
                "liuyue": y.to_dict(),
                "liuri": r.to_dict(),
                "liushi": s.to_dict(),
                "evaluator": "LayeredSupportEvaluator",
            },
        )


class LayeredAttackEvaluator:
    """Dayun → Liunian → Liuyue → Liuri → Liushi Attack."""

    def __init__(
        self,
        *,
        dayun: DayunAttackEvaluator | None = None,
        liunian: LiunianAttackEvaluator | None = None,
        liuyue: LiuyueAttackEvaluator | None = None,
        liuri: LiuriAttackEvaluator | None = None,
        liushi: LiushiAttackEvaluator | None = None,
    ) -> None:
        """Inject layer evaluators."""
        self.dayun = dayun or DayunAttackEvaluator()
        self.liunian = liunian or LiunianAttackEvaluator()
        self.liuyue = liuyue or LiuyueAttackEvaluator()
        self.liuri = liuri or LiuriAttackEvaluator()
        self.liushi = liushi or LiushiAttackEvaluator()

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> AttackEvaluation:
        """Run five layers; merge UNKNOWN-safe attack fields."""
        d, n, y, r, s = _run_layers(
            self.dayun,
            self.liunian,
            self.liuyue,
            self.liuri,
            self.liushi,
            luck=luck,
            rule_context=rule_context,
            score=score,
            pattern=pattern,
        )
        elements = tuple(
            dict.fromkeys(
                list(d.elements)
                + list(n.elements)
                + list(y.elements)
                + list(r.elements)
                + list(s.elements)
            )
        )
        reasons = (
            tuple(d.reasons)
            + tuple(n.reasons)
            + tuple(y.reasons)
            + tuple(r.reasons)
            + tuple(s.reasons)
        )
        return AttackEvaluation(
            elements=elements,
            level=_merge_levels(d.level, n.level, y.level, r.level, s.level),
            reasons=reasons,
            confidence=None,
            reason="layered_five_layer_attack",
            metadata={
                "layer_order": list(LAYER_ORDER),
                "dayun": d.to_dict(),
                "liunian": n.to_dict(),
                "liuyue": y.to_dict(),
                "liuri": r.to_dict(),
                "liushi": s.to_dict(),
                "evaluator": "LayeredAttackEvaluator",
            },
        )


class LayeredLuckStrengthEvaluator:
    """Five-layer Strength (NULL until specs define scoring)."""

    def __init__(
        self,
        *,
        dayun: DayunLuckStrengthEvaluator | None = None,
        liunian: LiunianLuckStrengthEvaluator | None = None,
        liuyue: LiuyueLuckStrengthEvaluator | None = None,
        liuri: LiuriLuckStrengthEvaluator | None = None,
        liushi: LiushiLuckStrengthEvaluator | None = None,
    ) -> None:
        """Inject layer evaluators."""
        self.dayun = dayun or DayunLuckStrengthEvaluator()
        self.liunian = liunian or LiunianLuckStrengthEvaluator()
        self.liuyue = liuyue or LiuyueLuckStrengthEvaluator()
        self.liuri = liuri or LiuriLuckStrengthEvaluator()
        self.liushi = liushi or LiushiLuckStrengthEvaluator()

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> StrengthEvaluation:
        """Merge strengths without inventing a formula; confidence = min."""
        d, n, y, r, s = _run_layers(
            self.dayun,
            self.liunian,
            self.liuyue,
            self.liuri,
            self.liushi,
            luck=luck,
            rule_context=rule_context,
            score=score,
            pattern=pattern,
        )
        return StrengthEvaluation(
            value=_merge_strength_values(d.value, n.value, y.value, r.value, s.value),
            confidence=_merge_confidence(
                d.confidence,
                n.confidence,
                y.confidence,
                r.confidence,
                s.confidence,
            ),
            reason="layered_five_layer_strength_null_until_spec",
            metadata={
                "layer_order": list(LAYER_ORDER),
                "dayun": d.to_dict(),
                "liunian": n.to_dict(),
                "liuyue": y.to_dict(),
                "liuri": r.to_dict(),
                "liushi": s.to_dict(),
                "evaluator": "LayeredLuckStrengthEvaluator",
            },
        )


class LayeredLuckStageEvaluator:
    """Dayun → Liunian → Liuyue → Liuri → Liushi Stage."""

    def __init__(
        self,
        *,
        dayun: DayunLuckStageEvaluator | None = None,
        liunian: LiunianLuckStageEvaluator | None = None,
        liuyue: LiuyueLuckStageEvaluator | None = None,
        liuri: LiuriLuckStageEvaluator | None = None,
        liushi: LiushiLuckStageEvaluator | None = None,
    ) -> None:
        """Inject layer evaluators."""
        self.dayun = dayun or DayunLuckStageEvaluator()
        self.liunian = liunian or LiunianLuckStageEvaluator()
        self.liuyue = liuyue or LiuyueLuckStageEvaluator()
        self.liuri = liuri or LiuriLuckStageEvaluator()
        self.liushi = liushi or LiushiLuckStageEvaluator()

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> StageEvaluation:
        """Merge stages without inventing taxonomy."""
        d, n, y, r, s = _run_layers(
            self.dayun,
            self.liunian,
            self.liuyue,
            self.liuri,
            self.liushi,
            luck=luck,
            rule_context=rule_context,
            score=score,
            pattern=pattern,
        )
        return StageEvaluation(
            stage=_merge_levels(d.stage, n.stage, y.stage, r.stage, s.stage),
            confidence=_merge_confidence(
                d.confidence,
                n.confidence,
                y.confidence,
                r.confidence,
                s.confidence,
            ),
            reason="layered_five_layer_stage",
            metadata={
                "layer_order": list(LAYER_ORDER),
                "dayun": d.to_dict(),
                "liunian": n.to_dict(),
                "liuyue": y.to_dict(),
                "liuri": r.to_dict(),
                "liushi": s.to_dict(),
                "evaluator": "LayeredLuckStageEvaluator",
            },
        )


class CombinedLuckSummaryBuilder:
    """
    Machine-readable summary with all five runtime layers.

    No natural-language interpretation. Preserves prior runtime keys for
    Sprint 4.4–4.6 consumers.
    """

    def build(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> SummaryEvaluation:
        """Serialize five-layer structured snapshot as JSON."""
        del rule_context, score, pattern
        dayun_validation = validate_dayun_runtime(luck.current_dayun)
        liunian_validation = validate_liunian_runtime(
            luck.current_liunian,
            dayun=luck.current_dayun,
        )
        liuyue_validation = validate_liuyue_runtime(
            luck.current_liuyue,
            dayun=luck.current_dayun,
            liunian=luck.current_liunian,
        )
        liuri_validation = validate_liuri_runtime(
            luck.current_liuri,
            dayun=luck.current_dayun,
            liunian=luck.current_liunian,
            liuyue=luck.current_liuyue,
        )
        liushi_validation = validate_liushi_runtime(
            luck.current_liushi,
            dayun=luck.current_dayun,
            liunian=luck.current_liunian,
            liuyue=luck.current_liuyue,
            liuri=luck.current_liuri,
        )
        payload = {
            "kind": "five_layer_luck_runtime_summary",
            "specs": {
                "dayun": "DAYUN_SPEC.md",
                "liunian": "LIUNIAN_SPEC.md",
                "liuyue": "LIUYUE_SPEC.md",
                "liuri": "LIURI_SPEC.md",
                "liushi": "LIUSHI_SPEC.md",
            },
            "layer_order": list(LAYER_ORDER),
            "dayun_runtime": dayun_runtime_snapshot(luck.current_dayun),
            "liunian_runtime": liunian_runtime_snapshot(luck.current_liunian),
            "liuyue_runtime": liuyue_runtime_snapshot(luck.current_liuyue),
            "liuri_runtime": liuri_runtime_snapshot(
                luck.current_liuri,
                liuyue=luck.current_liuyue,
            ),
            "liushi_runtime": liushi_runtime_snapshot(
                luck.current_liushi,
                liuyue=luck.current_liuyue,
                liuri=luck.current_liuri,
            ),
            "validation": {
                "dayun": dayun_validation.to_dict(),
                "liunian": liunian_validation.to_dict(),
                "liuyue": liuyue_validation.to_dict(),
                "liuri": liuri_validation.to_dict(),
                "liushi": liushi_validation.to_dict(),
            },
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
                "five_luck_layers_coexist",
                "interaction_detection_deferred_pending_rule_database",
            ],
        }
        return SummaryEvaluation(
            summary=json.dumps(payload, ensure_ascii=False, sort_keys=True),
            confidence=_merge_confidence(
                dayun_validation.confidence,
                liunian_validation.confidence,
                liuyue_validation.confidence,
                liuri_validation.confidence,
                liushi_validation.confidence,
            ),
            reason="combined_five_layer_runtime_output_contract",
            metadata={
                "evaluator": "CombinedLuckSummaryBuilder",
                "format": "application/json",
                "dayun_validation": dayun_validation.to_dict(),
                "liunian_validation": liunian_validation.to_dict(),
                "liuyue_validation": liuyue_validation.to_dict(),
                "liuri_validation": liuri_validation.to_dict(),
                "liushi_validation": liushi_validation.to_dict(),
            },
        )
