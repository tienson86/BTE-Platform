"""
Generic Score Calculator

Template Method cho các Score Calculator.

WP2C:
    Loader → Adapter → RuleContract → Matcher → Calculator
    Uses RuleContext (not raw BaziChart).
"""

from __future__ import annotations

from typing import Any

from .base_calculator import BaseCalculator
from ..matcher import RuleMatcher
from ..utils.normalizer import ScoreNormalizer
from ..utils.scorer import RuleScorer
from ..utils.validator import ScoreValidator


class GenericScoreCalculator(BaseCalculator):
    """Score calculator driven by Rule Contract V1."""

    RULE_FOLDER = ""

    def __init__(self, loader):
        super().__init__(loader)
        self.matcher = RuleMatcher()
        self.validator = ScoreValidator()
        self.scorer = RuleScorer()
        self.normalizer = ScoreNormalizer()

    # ==================================================

    def load_rules(self):
        return self.loader.load_group(self.RULE_FOLDER)

    def validate_rules(self, dataframe):
        """
        Soft validation.

        WP2C: do not require ``condition`` column — Adapter builds RuleContract
        from implicit metadata when needed.
        """
        if dataframe is None:
            raise ValueError("DataFrame khong duoc None.")

        if "score" not in dataframe.columns:
            raise ValueError("Thiếu cột bắt buộc: score")

        return True

    def match_rules(self, dataframe, context):
        """
        Match every row via Score RuleMatcher
        (Adapter → RuleContract → Matcher V1).
        """
        return self.matcher.match(dataframe, context)

    def calculate_score(self, matched_rules):
        self.scorer.reset()

        for rule in matched_rules:
            score = float(rule.get("score", 0) or 0)
            code = str(
                rule.get("rule_code")
                or rule.get("id")
                or rule.get("rule_id")
                or ""
            )
            description = str(rule.get("description", "") or "")

            if score >= 0:
                self.scorer.add(score, code, description)
            else:
                self.scorer.subtract(abs(score), code, description)

        return self.scorer.score

    def normalize_score(self, score):
        return self.normalizer.clamp(score)

    def build_result(self, result, matched_rules, score):
        result.score = score
        result.weighted_score = score
        result.weight = 1.0
        result.matched_rules = matched_rules
        result.history = self.scorer.history
        return result

    def post_process(self, result, context):
        return result

    # ==================================================

    def calculate(self, context):
        result = self.create_result()
        rule_context = self.resolve_rule_context(context)

        try:
            groups = self.load_rules()
        except Exception as exc:
            result.success = False
            result.add_error(str(exc))
            return result

        matched: list[dict[str, Any]] = []

        for _, dataframe in groups.items():
            # Skip helper files without a numeric score column
            # (priority / weight tables). Do NOT skip missing condition.
            if "score" not in dataframe.columns:
                continue

            try:
                self.validate_rules(dataframe)
            except ValueError:
                continue

            matched.extend(self.match_rules(dataframe, rule_context))

        score = self.calculate_score(matched)
        score = self.normalize_score(score)
        result = self.build_result(result, matched, score)
        return self.post_process(result, rule_context)

    # ==================================================

    def resolve_rule_context(self, context: Any) -> dict[str, Any]:
        """
        Ensure calculator receives a RuleContext dict.

        Accepts:
        - RuleContext dict (already built)
        - ScoreContext
        - BaziChart-like object
        """
        if isinstance(context, dict) and self._looks_like_rule_context(context):
            return context

        from engines.rule_contract import RuleContextBuilder

        builder = RuleContextBuilder()

        # ScoreContext
        if hasattr(context, "bazi_chart"):
            return builder.build(
                bazi=getattr(context, "bazi_chart", None),
                pattern=getattr(context, "pattern_result", None),
                luck=getattr(context, "luck_result", None),
                shensha=getattr(context, "shensha_result", None),
                metadata=getattr(context, "metadata", None) or {},
            )

        # BaziChart / chart-like
        if hasattr(context, "day_master") or hasattr(context, "day_pillar"):
            return builder.build(bazi=context)

        if context is None:
            return builder.build()

        # Fallback: try normalize as empty-ish context
        return builder.build(metadata={"raw_context_type": type(context).__name__})

    @staticmethod
    def _looks_like_rule_context(context: dict[str, Any]) -> bool:
        return "bazi" in context and "wuxing" in context
