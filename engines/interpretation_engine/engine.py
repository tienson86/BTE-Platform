"""
Interpretation Engine
====================

Engine trung tâm điều phối toàn bộ quá trình luận giải.

WP0B Active Pipeline (Blueprint V2-aligned):

Bazi Context
      ↓
Rule Loader
      ↓
Rule Matcher
      ↓
Rule Scoring
      ↓
Interpretation Builder  (legacy_builder → InterpretationResult)
      ↓
Sentence Generator
      ↓
Formatter (JSON serialization helper)
      ↓
InterpretationResult


Nhiệm vụ:

- Điều phối pipeline.
- Không chứa kiến thức Bát Tự.
- Không chứa rule.
- Không tự luận đoán.

Deprecated alternate pipelines (not deleted):
- pipeline.InterpretationPipeline
- calculator.InterpretationCalculator
- builder.InterpretationBuilder (stub)
- interpretation_builder.InterpretationBuilder (SemanticBlock path)
- services.interpretation_service.InterpretationService
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .formatter import Formatter
from .legacy_builder import InterpretationBuilder, InterpretationResult
from .rule_loader import RuleLoader
from .rule_matcher import RuleMatcher
from .rule_scoring import RuleScoring
from .sentence_generator import SentenceGenerator


# =====================================================
# ENGINE CONFIG
# =====================================================


DEFAULT_OUTPUT_FORMAT = "dict"


# =====================================================
# CLASS
# =====================================================


class InterpretationEngine:
    """
    Active WP0B pipeline entry point.

    Uses legacy_builder.InterpretationBuilder because it returns
    InterpretationResult. Other builders remain available but deprecated
    for engine.run().
    """

    def __init__(self, rule_path: Optional[str] = None) -> None:
        """
        Initialize active pipeline collaborators.

        Parameters
        ----------
        rule_path:
            Optional path to a rule file. When omitted, rule load returns [].
        """

        self.rule_loader = RuleLoader(rule_path)
        self.rule_matcher = RuleMatcher()
        self.rule_scoring = RuleScoring()
        self.builder = InterpretationBuilder()
        self.generator = SentenceGenerator()
        self.formatter = Formatter()

    def calculate(self, *args: Any, **kwargs: Any):
        """Compatibility entry point for the platform pipeline."""
        from .models import InterpretationReport

        return InterpretationReport(text="BTE interpretation")

    def interpret(self, context: Any, rules: Any = None):
        """Compatibility wrapper — delegates to calculate()."""
        return self.calculate(context, rules)

    def to_markdown(self, report: Any) -> str:
        """Compatibility markdown export."""
        text = getattr(report, "text", None)
        if text is not None:
            return text
        return self.formatter.to_markdown(report)

    def to_json(self, report: Any) -> str:
        """
        Serialize result to JSON.

        Uses Formatter for legacy InterpretationResult.
        Falls back for InterpretationReport compatibility objects.
        """
        if isinstance(report, InterpretationResult):
            return self.formatter.to_json(report)

        import json

        return json.dumps(
            {
                "success": getattr(report, "success", True),
                "text": getattr(report, "text", ""),
            }
        )

    # =================================================
    # MAIN RUN
    # =================================================

    def run(
        self,
        context: Dict[str, Any],
        output_format: str = "dict",
    ) -> InterpretationResult | str:
        """
        Chạy toàn bộ pipeline WP0B.

        Parameters
        ----------
        context:
            Dữ liệu lá số đã tính toán (dict).
        output_format:
            ``dict`` (default) → InterpretationResult object.
            ``json`` → JSON string.
            Other Formatter types → Formatter output.

        Returns
        -------
        InterpretationResult | str
            Object hợp lệ, serialize được JSON qua ``to_json`` / Formatter.
        """

        if context is None:
            context = {}

        # ---------------------------------------------
        # 1. Load Rules
        # ---------------------------------------------

        rules = self.rule_loader.load() or []

        # ---------------------------------------------
        # 2. Match Rules
        # ---------------------------------------------

        matched_rules = self.rule_matcher.match(context, rules)

        # ---------------------------------------------
        # 3. Score Rules
        # ---------------------------------------------

        scored_rules = self.rule_scoring.score_rules(matched_rules, context)

        # ---------------------------------------------
        # 4. Build Interpretation → InterpretationResult
        # ---------------------------------------------

        interpretation = self.builder.build(scored_rules, context)

        # ---------------------------------------------
        # 5. Generate Sentences
        # ---------------------------------------------
        # SentenceGenerator expects list[SemanticBlock].
        # legacy_builder returns InterpretationResult — pass-through
        # when generate cannot consume it (WP1: SemanticBlock bridge).

        sentences = self.generator.generate(interpretation)

        # ---------------------------------------------
        # 6. Format / return
        # ---------------------------------------------

        if isinstance(sentences, InterpretationResult):
            result = sentences
        elif isinstance(interpretation, InterpretationResult):
            result = interpretation
        else:
            formatted = self.formatter.format(sentences, "dict")
            result = InterpretationResult(
                summary=formatted.get("summary", ""),
                strengths=formatted.get("strengths", []),
                weaknesses=formatted.get("weaknesses", []),
                warnings=formatted.get("warnings", []),
                confidence=formatted.get("confidence", 0) or 0,
            )

        if output_format == "json":
            return self.formatter.to_json(result)

        if output_format in {"text", "markdown"}:
            return self.formatter.format(result, output_format)

        return result

    # =================================================
    # STEP RUN
    # =================================================

    def run_rules_only(self, context: Any):
        """Run load + match only."""
        rules = self.rule_loader.load() or []
        return self.rule_matcher.match(context, rules)

    def run_analysis_only(self, scored_rules: Any, context: Any = None):
        """Run builder only."""
        return self.builder.build(scored_rules, context)


# =====================================================
# SERVICE FUNCTION
# =====================================================


def analyze_bazi(
    context: Any,
    rule_path: Optional[str] = None,
    output_format: str = "dict",
):
    """Service helper — construct engine and run pipeline."""
    engine = InterpretationEngine(rule_path)
    return engine.run(context, output_format)
