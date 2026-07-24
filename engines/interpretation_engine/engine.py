"""
Interpretation Engine
====================

Engine trung tâm điều phối toàn bộ quá trình luận giải.

WP5 Active Pipeline:

RuleContext
      ↓
Rule Loader  (Knowledge Base)
      ↓
Rule Adapter + Rule Matcher
      ↓
Rule Scoring
      ↓
Priority Engine  (Matched → Resolved → Discarded)
      ↓
Interpretation Builder  (legacy_builder → InterpretationResult)
      ↓
Sentence Generator
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

import logging
from typing import Any, Dict, List, Optional

from .formatter import Formatter
from .legacy_builder import InterpretationBuilder, InterpretationResult
from .rule_loader import RuleLoader
from .rule_matcher import RuleMatcher
from .rule_scoring import RuleScoring
from .sentence_generator import SentenceGenerator

logger = logging.getLogger(__name__)


DEFAULT_OUTPUT_FORMAT = "dict"


class InterpretationEngine:
    """
    Active WP5 pipeline entry point.

    Consumes RuleContext (or builds it from calendar/bazi/pattern/score).
    Priority Engine resolves matched rules before the Sentence Builder.
    """

    def __init__(self, rule_path: Optional[str] = None) -> None:
        """
        Initialize active pipeline collaborators.

        Parameters
        ----------
        rule_path:
            Optional path to a rule file or Knowledge Base directory.
            When omitted, loads ``knowledge/05_rule_database``.
        """

        self.rule_loader = RuleLoader(rule_path)
        self.rule_matcher = RuleMatcher()
        self.rule_scoring = RuleScoring()
        self.builder = InterpretationBuilder()
        self.generator = SentenceGenerator()
        self.formatter = Formatter()
        self._last_priority_resolution: Dict[str, Any] = {}

    def calculate(self, *args: Any, **kwargs: Any):
        """Compatibility entry point for the platform pipeline (stub report)."""
        from .models import InterpretationReport

        return InterpretationReport(text="BTE interpretation")

    def interpret(self, context: Any, rules: Any = None):
        """Compatibility wrapper — prefers run(RuleContext) when dict-like."""
        if isinstance(context, dict) and ("bazi" in context or "wuxing" in context):
            return self.run(context)
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
        context: Dict[str, Any] | Any,
        output_format: str = "dict",
    ) -> InterpretationResult | str:
        """
        Chạy toàn bộ pipeline WP5 trên RuleContext.

        Priority Engine runs after scoring and before Interpretation Builder /
        Sentence Generator.
        """

        if context is None:
            context = {}

        rule_context = self._to_rule_context(context)
        all_rules = self.rule_loader.load() or []

        # Loader → Adapter → Matcher
        matched_rules = self.rule_matcher.match(rule_context, all_rules)

        # Scoring
        scored_rules = self.rule_scoring.score_rules(matched_rules, rule_context)

        # WP5 Priority Resolution (before builder / sentences)
        ordered_rules = self._apply_priority(scored_rules, rule_context)
        priority_payload = dict(self._last_priority_resolution)

        # Builder → sections
        interpretation = self.builder.build(ordered_rules, rule_context)

        # Sentence pass / enrich
        sentences = self.generator.generate(interpretation)
        if isinstance(sentences, InterpretationResult):
            result = sentences
        elif isinstance(interpretation, InterpretationResult):
            result = interpretation
        else:
            result = InterpretationResult(
                summary="",
                confidence=0,
            )

        # WP5 resolution report
        result.priority_resolution = priority_payload
        result.discarded_rules = list(priority_payload.get("discarded_rules") or [])
        result.resolved_rule_count = int(
            priority_payload.get("resolved_count", len(ordered_rules))
        )
        result.matched_rule_count = int(
            priority_payload.get("matched_count", len(scored_rules))
        )

        # Coverage metrics
        used_ids = set(result.rules_used or [])
        unused = [
            str(rule.get("rule_id"))
            for rule in all_rules
            if str(rule.get("rule_id")) not in used_ids
        ]
        total = len(all_rules)
        result.unused_rules = unused
        result.coverage = round(len(used_ids) / total, 4) if total else 0.0
        if not result.sentence_count:
            result.sentence_count = len(result.sentences or [])
        if not result.section_count:
            result.section_count = sum(
                1 for section in (result.sections or {}).values() if section.rules
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
        rule_context = self._to_rule_context(context)
        rules = self.rule_loader.load() or []
        return self.rule_matcher.match(rule_context, rules)

    def run_analysis_only(self, scored_rules: Any, context: Any = None):
        """Run builder only."""
        rule_context = self._to_rule_context(context) if context is not None else {}
        return self.builder.build(scored_rules, rule_context)

    # =================================================
    # RuleContext + Priority helpers
    # =================================================

    def _to_rule_context(self, context: Any) -> dict[str, Any]:
        """Normalize input to RuleContext without changing public API."""
        if isinstance(context, dict) and "bazi" in context and "wuxing" in context:
            return context

        from engines.rule_contract import RuleContextBuilder

        builder = RuleContextBuilder()

        if isinstance(context, dict):
            keys = (
                "calendar",
                "bazi",
                "pattern",
                "score",
                "luck",
                "shensha",
                "useful_god",
                "temperature",
            )
            if any(key in context for key in keys):
                payload = {key: context.get(key) for key in keys if key in context}
                metadata = context.get("metadata") or {
                    key: value
                    for key, value in context.items()
                    if key not in keys and key not in {"facts", "wuxing", "strength"}
                }
                return builder.build(metadata=metadata, **payload)

            # Flat legacy dict → metadata hints only
            return builder.build(metadata={"raw_context": context})

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

    def _apply_priority(
        self,
        rules: List[Dict[str, Any]],
        rule_context: dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        WP5: Priority Engine resolves matched knowledge rules.

        Falls back to priority/confidence sort only if Priority Engine errors.
        """
        del rule_context  # reserved for future PR* context activation
        ordered = self.rule_matcher.sort_by_priority(list(rules))
        self._last_priority_resolution = {
            "matched_rules": [
                str(r.get("rule_id")) for r in ordered if r.get("rule_id")
            ],
            "resolved_rules": [
                str(r.get("rule_id")) for r in ordered if r.get("rule_id")
            ],
            "discarded_rules": [],
            "matched_count": len(ordered),
            "resolved_count": len(ordered),
            "discarded_count": 0,
            "discard_reasons": {},
        }

        try:
            from engines.priority_engine import PriorityService

            service = PriorityService.for_matched_rules()
            resolution = service.resolve_matched_interpretation_rules(ordered)
            self._last_priority_resolution = resolution.to_dict()
            return list(resolution.resolved_rules)
        except Exception:
            logger.exception(
                "Priority engine resolution failed; using priority/confidence sort"
            )
            return ordered


def analyze_bazi(
    context: Any,
    rule_path: Optional[str] = None,
    output_format: str = "dict",
):
    """Service helper — construct engine and run pipeline."""
    engine = InterpretationEngine(rule_path)
    return engine.run(context, output_format)
