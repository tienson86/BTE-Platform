"""
Score Engine

Điều phối toàn bộ quá trình chấm điểm lá số.

Production input: RuleContext only (Stage 5 published context).
Production output: ScoreResult (sole producer).
Does not mutate published RuleContext.
"""

from __future__ import annotations

from typing import Any

from .result import ScoreResult
from .loader import ScoreLoader
from .analysis import AnalysisResult, AnalysisResultBuilder

from .calculators import (
    WuxingScoreCalculator,
    SeasonScoreCalculator,
    TemperatureScoreCalculator,
    StrengthScoreCalculator,
    TenGodScoreCalculator,
    PatternScoreCalculator,
    UsefulGodScoreCalculator,
    ShenshaScoreCalculator,
    LuckScoreCalculator,
    FinalScoreCalculator,
)

_ELEMENT_LABELS: dict[str, str] = {
    "wood": "Mộc",
    "fire": "Hỏa",
    "earth": "Thổ",
    "metal": "Kim",
    "water": "Thủy",
}


class ScoreEngine:
    """
    Engine chính của Score Engine.

    Sole producer of ScoreResult for the production pipeline.
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
            SeasonScoreCalculator(self.loader),
            TemperatureScoreCalculator(self.loader),
            StrengthScoreCalculator(self.loader),
            TenGodScoreCalculator(self.loader),
            PatternScoreCalculator(self.loader),
            UsefulGodScoreCalculator(self.loader),
            ShenshaScoreCalculator(self.loader),
            LuckScoreCalculator(self.loader),
            FinalScoreCalculator(self.loader),
        ]

    @staticmethod
    def is_rule_context(context: Any) -> bool:
        """Return True when input is a production RuleContext dict."""
        return isinstance(context, dict) and "bazi" in context and "wuxing" in context

    def calculate(self, context):
        """
        Public API.

        Production: ``context`` must be the Stage 5 published RuleContext.
        Legacy ScoreContext / chart-like inputs still accepted via compatibility
        adapter (does not run on the production orchestrator path).
        """
        if hasattr(context, "validate"):
            context.validate()

        rule_context = self._resolve_rule_context(context)
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
        result.season_score = module_scores.get("season", 0.0)
        result.temperature_score = module_scores.get("temperature", 0.0)
        result.strength_score = module_scores.get("strength", 0.0)
        result.ten_god_score = module_scores.get("ten_gods", 0.0)
        result.pattern_score = module_scores.get("pattern", 0.0)
        result.useful_god_score = module_scores.get("useful_god", 0.0)
        result.shensha_score = module_scores.get("shensha", 0.0)
        result.luck_score = module_scores.get("luck", 0.0)

        # Working copy for FinalScoreCalculator only — never mutates caller RuleContext.
        # Season / Temperature are first-class Pack 03 dimensions but are omitted from
        # dimension_weight.csv so overall total stays backward compatible.
        enriched = dict(rule_context)
        score_section = dict(enriched.get("score") or {})
        score_section.update(
            {
                "wuxing_score": result.wuxing_score,
                "season_score": result.season_score,
                "temperature_score": result.temperature_score,
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
        result.wuxing_series = self._build_wuxing_series(rule_context)
        result.ten_god_series = self._build_ten_god_series(rule_context)
        result.success = True
        return result

    def analyze(self, context) -> AnalysisResult:
        """
        Pack 03 entry: run scoring then build AnalysisResult aggregate.

        Production orchestrator continues to use ``calculate`` → ScoreResult.
        """
        rule_context = self._resolve_rule_context(context)
        score_result = self.calculate(rule_context)
        return AnalysisResultBuilder().build(score_result, rule_context)

    # Compatibility alias requested by platform docs
    def run(self, context):
        """Alias of ``calculate`` for callers expecting ``run()`` → ScoreResult."""
        return self.calculate(context)

    def append_score_to_rule_context(
        self,
        rule_context: dict[str, Any],
        result: ScoreResult,
    ) -> dict[str, Any]:
        """
        Compose a NEW context dict with ScoreResult applied for downstream matching.

        Does not mutate ``rule_context`` (Stage 5 published RuleContext stays
        immutable). Callers must use the returned dict for Interpretation.
        """
        composed: dict[str, Any] = dict(rule_context)
        section = dict(composed.get("score") or {})
        section.update(
            {
                "total_score": float(result.total_score or 0.0),
                "overall_score": float(result.overall_score or 0.0),
                "strength_score": float(result.strength_score or 0.0),
                "ten_god_score": float(result.ten_god_score or 0.0),
                "pattern_score": float(result.pattern_score or 0.0),
                "useful_god_score": float(result.useful_god_score or 0.0),
                "shensha_score": float(result.shensha_score or 0.0),
                "luck_score": float(result.luck_score or 0.0),
                "wuxing_score": float(result.wuxing_score or 0.0),
                "five_elements_score": float(result.five_elements_score or 0.0),
                "season_score": float(result.season_score or 0.0),
                "temperature_score": float(result.temperature_score or 0.0),
                "grade": result.grade or "",
                "confidence": result.confidence or "",
                "recommendation": result.recommendation or "",
                "success": result.success,
            }
        )
        composed["score"] = section
        composed["strength_score"] = section["strength_score"]

        # Score-owned strength.level on the composed (non-published) dict only.
        strength = dict(composed.get("strength") or {})
        score_value = float(result.strength_score or 0.0)
        strength["score"] = score_value
        if score_value >= 70:
            level = "strong"
        elif score_value >= 40:
            level = "balanced"
        elif score_value > 0:
            level = "weak"
        else:
            level = strength.get("level") or "unknown"
        strength["level"] = level
        composed["strength"] = strength

        facts = dict(composed.get("facts") or {})
        facts["day_master_strength_calculated"] = level not in {None, "unknown"}
        facts["than_vuong_nhuoc_da_xac_dinh"] = level not in {None, "unknown"}
        facts["than_score_da_tinh"] = level not in {None, "unknown"} or score_value > 0
        facts["strong_day_master"] = level == "strong"
        facts["strength_vuong"] = level == "strong"
        facts["weak_day_master"] = level == "weak"
        facts["strength_nhuoc"] = level == "weak"
        facts["balanced_day_master"] = level == "balanced"
        facts["strength_balanced"] = level == "balanced"
        facts["day_master_extremely_strong"] = score_value >= 80
        facts["day_master_extremely_weak"] = 0 < score_value <= 20
        facts["extremely_strong_day_master"] = facts["day_master_extremely_strong"]
        facts["extremely_weak_day_master"] = facts["day_master_extremely_weak"]
        composed["facts"] = facts
        for key, value in facts.items():
            if value is True:
                composed[key] = True

        return composed

    def _resolve_rule_context(self, context: Any) -> dict[str, Any]:
        """
        Resolve input to RuleContext.

        Production path: return the shared RuleContext as-is (no rebuild).
        Legacy path: adapt ScoreContext / chart-like objects for unit tests.
        """
        if self.is_rule_context(context):
            return context

        # LEGACY compatibility — not used by applications.api orchestrator.
        return self._legacy_to_rule_context(context)

    def _legacy_to_rule_context(self, context: Any) -> dict[str, Any]:
        """Build RuleContext for non-production callers (ScoreContext / chart)."""
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

    # Backward-compatible name used by older call sites / docs.
    _to_rule_context = _resolve_rule_context

    @staticmethod
    def _build_wuxing_series(rule_context: dict[str, Any]) -> list[dict[str, Any]]:
        """Derive optional Ngũ hành series from RuleContext wuxing counts."""
        wuxing = rule_context.get("wuxing") or {}
        counts = wuxing.get("counts") or {}
        series: list[dict[str, Any]] = []
        for key, label in _ELEMENT_LABELS.items():
            entry = wuxing.get(key) or {}
            value = counts.get(key)
            if value is None:
                value = entry.get("count")
            if value is None:
                continue
            series.append({"label": label, "value": float(value)})
        return series

    @staticmethod
    def _build_ten_god_series(rule_context: dict[str, Any]) -> list[dict[str, Any]]:
        """Derive optional Thập thần series from RuleContext ten_gods items."""
        ten_gods = rule_context.get("ten_gods") or {}
        items = list(ten_gods.get("items") or [])
        if not items:
            return []
        counts: dict[str, int] = {}
        for name in items:
            label = str(name or "").strip()
            if not label or label == "Nhật Chủ":
                continue
            counts[label] = counts.get(label, 0) + 1
        return [
            {"label": label, "value": float(count)}
            for label, count in counts.items()
        ]
