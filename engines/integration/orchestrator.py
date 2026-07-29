"""
BTE Integration Orchestrator.

Legacy entry point aligned to the canonical Stage order (Sprint 1 / N-04).

Production SSOT remains ``applications.api.services.orchestrator.OrchestratorService``.
This module preserves the IntegrationContext API while matching:

Calendar → BaZi → Pattern → RuleContext → Score → Interpretation → Report
"""

from __future__ import annotations

from collections import OrderedDict

from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.interpretation_engine.engine import InterpretationEngine
from engines.pattern_engine.engine import PatternEngine
from engines.pattern_engine.rule_context_bridge import (
    build_rule_context,
    enrich_result_from_rule_context,
)
from engines.report_engine.engine import ReportEngine
from engines.score_engine.engine import ScoreEngine

from .context import IntegrationContext
from .result import IntegrationResult


class IntegrationOrchestrator:
    """
    Integration-layer coordinator.

    Stage order matches production (Pattern before Score; RuleContext Stage 5).
    """

    # Canonical production SSOT — callers should prefer this for API/runtime.
    PRODUCTION_ORCHESTRATOR = (
        "applications.api.services.orchestrator.OrchestratorService"
    )

    def __init__(self) -> None:
        self.calendar_engine = CalendarEngine()
        self.bazi_engine = BaziEngine()
        self.pattern_engine = PatternEngine()
        self.score_engine = ScoreEngine()
        self.interpretation_engine = InterpretationEngine()
        self.report_engine = ReportEngine()

        self.stages = OrderedDict(
            {
                "calendar": self._calendar,
                "bazi": self._bazi,
                "pattern": self._pattern,
                "rule_context": self._rule_context,
                "score": self._score,
                "interpretation": self._interpretation,
                "report": self._report,
            }
        )

    def execute(self, context: IntegrationContext) -> IntegrationResult:
        """Run all stages in canonical order."""
        result = IntegrationResult()
        for stage_name, stage in self.stages.items():
            ok = stage(context, result)
            if not ok:
                result.success = False
                result.failed_stage = stage_name
                return result
        result.success = True
        return result

    def execute_until(
        self,
        context: IntegrationContext,
        stage: str,
    ) -> IntegrationResult:
        """Run stages until ``stage`` inclusive."""
        result = IntegrationResult()
        for stage_name, handler in self.stages.items():
            ok = handler(context, result)
            if not ok:
                result.success = False
                result.failed_stage = stage_name
                return result
            if stage_name == stage:
                break
        result.success = True
        return result

    def reset(self) -> None:
        """Reset pipeline state (stateless — no-op)."""
        return None

    def _calendar(self, context, result) -> bool:
        calendar_result = self.calendar_engine.execute(context.calendar)
        result.calendar = calendar_result
        context.calendar_result = calendar_result
        return calendar_result.success

    def _bazi(self, context, result) -> bool:
        bazi_result = self.bazi_engine.execute(context.bazi)
        result.bazi = bazi_result
        context.bazi_result = bazi_result
        return bazi_result.success

    def _pattern(self, context, result) -> bool:
        pattern_result = self.pattern_engine.execute(context.pattern)
        result.pattern = pattern_result
        context.pattern_result = pattern_result
        return pattern_result.success

    def _rule_context(self, context, result) -> bool:
        """Stage 5: publish RuleContext (sole producer on this path)."""
        calendar = context.calendar_result
        bazi = context.bazi_result
        pattern = context.pattern_result
        if calendar is None or bazi is None or pattern is None:
            result.success = False
            return False
        # Prefer underlying chart/result objects when execute wrappers nest them.
        calendar_obj = getattr(calendar, "data", calendar)
        bazi_obj = getattr(bazi, "data", bazi)
        pattern_obj = getattr(pattern, "data", pattern)
        try:
            rule_context = build_rule_context(
                calendar=calendar_obj,
                bazi=bazi_obj,
                pattern=pattern_obj,
            )
            enrich_result_from_rule_context(pattern_obj, rule_context)
        except Exception:
            return False
        context.set("rule_context", rule_context)
        context.score = rule_context
        context.interpretation = rule_context
        return True

    def _score(self, context, result) -> bool:
        # Prefer Stage 5 published RuleContext when present.
        score_input = context.get("rule_context") or context.score
        score_result = self.score_engine.execute(score_input)
        result.score = score_result
        context.score_result = score_result
        published = context.get("rule_context")
        if (
            isinstance(published, dict)
            and score_result is not None
            and hasattr(self.score_engine, "append_score_to_rule_context")
            and hasattr(score_result, "total_score")
        ):
            composed = self.score_engine.append_score_to_rule_context(
                published,
                score_result,
            )
            context.set("interpretation_context", composed)
            context.interpretation = composed
        return bool(getattr(score_result, "success", True))

    def _interpretation(self, context, result) -> bool:
        interpretation_result = self.interpretation_engine.execute(
            context.interpretation
        )
        result.interpretation = interpretation_result
        context.interpretation_result = interpretation_result
        return interpretation_result.success

    def _report(self, context, result) -> bool:
        report_result = self.report_engine.execute(context.report)
        result.report = report_result
        context.report_result = report_result
        return report_result.success
