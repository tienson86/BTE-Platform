"""
Score Engine

Điều phối toàn bộ quá trình chấm điểm lá số.

Pipeline:

Context
    ↓
Wuxing Calculator
    ↓
Strength Calculator
    ↓
Ten God Calculator
    ↓
Pattern Calculator
    ↓
Useful God Calculator
    ↓
ShenSha Calculator
    ↓
Luck Calculator
    ↓
Final Score Calculator
    ↓
ScoreResult
"""

from __future__ import annotations

from typing import Any

from .result import ScoreResult
from .loader import ScoreLoader

from .calculators import (
    WuxingScoreCalculator,
    StrengthScoreCalculator,
    TenGodScoreCalculator,
    PatternScoreCalculator,
    UsefulGodScoreCalculator,
    ShenshaScoreCalculator,
    LuckScoreCalculator,
    FinalScoreCalculator,
)


class ScoreEngine:
    """
    Engine chính của Score Engine.
    """

    def __init__(self, loader=None):
        self.loader = loader or ScoreLoader(
            "database/15_score_engine"
        )
        self.calculators = self._build_pipeline()

    def _build_pipeline(self):
        """
        Khởi tạo Pipeline.

        Thứ tự rất quan trọng.
        """
        return [
            WuxingScoreCalculator(self.loader),
            StrengthScoreCalculator(self.loader),
            TenGodScoreCalculator(self.loader),
            PatternScoreCalculator(self.loader),
            UsefulGodScoreCalculator(self.loader),
            ShenshaScoreCalculator(self.loader),
            LuckScoreCalculator(self.loader),
            FinalScoreCalculator(self.loader),
        ]

    def calculate(self, context):
        """
        Public API (unchanged signature).

        WP2C: normalize to RuleContext, run module calculators, then
        FinalScoreCalculator with weighted aggregation.
        """
        if hasattr(context, "validate"):
            context.validate()

        rule_context = self._to_rule_context(context)
        result = ScoreResult()
        calculator_results: dict[str, Any] = {}
        module_scores: dict[str, float] = {}

        final_calculators = []
        module_calculators = []
        for calculator in self.calculators:
            if calculator.module_name == "final_score":
                final_calculators.append(calculator)
            else:
                module_calculators.append(calculator)

        for calculator in module_calculators:
            calc_result = calculator.safe_execute(rule_context)
            calculator_results[calculator.module_name] = calc_result
            module_scores[calculator.module_name] = float(
                getattr(calc_result, "weighted_score", 0.0) or 0.0
            )

        # Publish module scores into ScoreResult fields
        result.wuxing_score = module_scores.get("wuxing", 0.0)
        result.strength_score = module_scores.get("strength", 0.0)
        result.ten_god_score = module_scores.get("ten_gods", 0.0)
        result.pattern_score = module_scores.get("pattern", 0.0)
        result.useful_god_score = module_scores.get("useful_god", 0.0)
        result.shensha_score = module_scores.get("shensha", 0.0)
        result.luck_score = module_scores.get("luck", 0.0)

        # Enrich RuleContext for FinalScoreCalculator
        enriched = dict(rule_context)
        score_section = dict(enriched.get("score") or {})
        score_section.update(
            {
                "wuxing_score": result.wuxing_score,
                "strength_score": result.strength_score,
                "ten_god_score": result.ten_god_score,
                "pattern_score": result.pattern_score,
                "useful_god_score": result.useful_god_score,
                "shensha_score": result.shensha_score,
                "luck_score": result.luck_score,
                "module_scores": module_scores,
            }
        )
        enriched["score"] = score_section
        enriched["strength_score"] = result.strength_score

        for calculator in final_calculators:
            calc_result = calculator.safe_execute(enriched)
            calculator_results[calculator.module_name] = calc_result
            result.total_score = float(getattr(calc_result, "score", 0.0) or 0.0)
            details = getattr(calc_result, "details", {}) or {}
            result.grade = details.get("grade", "") or ""
            result.confidence = details.get("confidence", "") or ""
            result.recommendation = details.get("recommendation", "") or ""

        result.details = calculator_results
        result.success = True
        return result

    # Compatibility alias requested by platform docs
    def run(self, context):
        """Alias of ``calculate`` for callers expecting ``run()``."""
        return self.calculate(context)

    def _to_rule_context(self, context: Any) -> dict[str, Any]:
        """Build RuleContext once for the whole pipeline."""
        if isinstance(context, dict) and "bazi" in context and "wuxing" in context:
            return context

        from engines.rule_contract import RuleContextBuilder

        builder = RuleContextBuilder()

        if hasattr(context, "bazi_chart"):
            return builder.build(
                bazi=getattr(context, "bazi_chart", None),
                pattern=getattr(context, "pattern_result", None),
                luck=getattr(context, "luck_result", None),
                shensha=getattr(context, "shensha_result", None),
                metadata=getattr(context, "metadata", None) or {},
            )

        if hasattr(context, "day_master") or hasattr(context, "day_pillar"):
            return builder.build(bazi=context)

        return builder.build()
