"""
BTE Integration Orchestrator.

Điều phối toàn bộ Pipeline của BTE Platform.

Calendar
    ↓
Bazi
    ↓
Score
    ↓
Pattern
    ↓
Interpretation
    ↓
Report
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Callable

from .context import IntegrationContext
from .result import IntegrationResult

# Engine
from engines.calendar_engine.engine import CalendarEngine
from engines.bazi_engine.engine import BaziEngine
from engines.score_engine.engine import ScoreEngine
from engines.pattern_engine.engine import PatternEngine
from engines.interpretation_engine.engine import InterpretationEngine
from engines.report_engine.engine import ReportEngine


class IntegrationOrchestrator:

    def __init__(self):

        self.calendar_engine = CalendarEngine()
        self.bazi_engine = BaziEngine()
        self.score_engine = ScoreEngine()
        self.pattern_engine = PatternEngine()
        self.interpretation_engine = InterpretationEngine()
        self.report_engine = ReportEngine()

        self.stages = OrderedDict({

            "calendar": self._calendar,

            "bazi": self._bazi,

            "score": self._score,

            "pattern": self._pattern,

            "interpretation": self._interpretation,

            "report": self._report,

        })

    # ==========================================================
    # Public API
    # ==========================================================

    def execute(
        self,
        context: IntegrationContext
    ) -> IntegrationResult:

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

    def reset(self):

        """
        Reset trạng thái Pipeline.
        """

        pass

    # ==========================================================
    # Pipeline Stage
    # ==========================================================

    def _calendar(

        self,

        context,

        result,

    ) -> bool:

        calendar_result = self.calendar_engine.execute(

            context.calendar

        )

        result.calendar = calendar_result

        context.calendar_result = calendar_result

        return calendar_result.success

    def _bazi(

        self,

        context,

        result,

    ) -> bool:

        bazi_result = self.bazi_engine.execute(

            context.bazi

        )

        result.bazi = bazi_result

        context.bazi_result = bazi_result

        return bazi_result.success

    def _score(

        self,

        context,

        result,

    ) -> bool:

        score_result = self.score_engine.execute(

            context.score

        )

        result.score = score_result

        context.score_result = score_result

        return score_result.success

    def _pattern(

        self,

        context,

        result,

    ) -> bool:

        pattern_result = self.pattern_engine.execute(

            context.pattern

        )

        result.pattern = pattern_result

        context.pattern_result = pattern_result

        return pattern_result.success

    def _interpretation(

        self,

        context,

        result,

    ) -> bool:

        interpretation_result = (

            self.interpretation_engine.execute(

                context.interpretation

            )

        )

        result.interpretation = interpretation_result

        context.interpretation_result = interpretation_result

        return interpretation_result.success

    def _report(

        self,

        context,

        result,

    ) -> bool:

        report_result = self.report_engine.execute(

            context.report

        )

        result.report = report_result

        context.report_result = report_result

        return report_result.success
