"""
BTE Platform

API Services

File: pipeline_service.py
Version: 1.0
"""

from __future__ import annotations

from engines.base.context import EngineContext
from engines.base.pipeline import EnginePipeline

from engines.calendar_engine.engine import CalendarEngine
from engines.bazi_engine.engine import BaziEngine
from engines.pattern.engine import PatternEngine
from engines.score_engine.engine import ScoreEngine
from engines.interpretation_engine.engine import InterpretationEngine
from engines.report_engine.engine import ReportEngine


class PipelineService:
    """
    Điều phối toàn bộ Engine Pipeline.
    """

    def __init__(self) -> None:

        self.pipeline = EnginePipeline()

        self._register_engines()

    # =====================================================
    # Register
    # =====================================================

    def _register_engines(self) -> None:
        """
        Đăng ký toàn bộ Engine.
        """

        self.pipeline.register(
            CalendarEngine()
        )

        self.pipeline.register(
            BaziEngine()
        )

        self.pipeline.register(
            PatternEngine()
        )

        self.pipeline.register(
            ScoreEngine()
        )

        self.pipeline.register(
            InterpretationEngine()
        )

        self.pipeline.register(
            ReportEngine()
        )

    # =====================================================
    # Helpers
    # =====================================================

    def create_context(
        self,
        data: dict,
    ) -> EngineContext:
        """
        Tạo EngineContext.
        """

        context = EngineContext()

        for key, value in data.items():

            context.set(
                key,
                value,
            )

        return context

    # =====================================================
    # Run Pipeline
    # =====================================================

    def analyze(
        self,
        data: dict,
    ):
        """
        Chạy toàn bộ Pipeline.
        """

        context = self.create_context(
            data
        )

        return self.pipeline.execute(
            context
        )

    # =====================================================
    # Run Calendar
    # =====================================================

    def calendar(
        self,
        data: dict,
    ):

        context = self.create_context(
            data
        )

        return CalendarEngine().execute(
            context
        )

    # =====================================================
    # Run Bazi
    # =====================================================

    def bazi(
        self,
        data: dict,
    ):

        context = self.create_context(
            data
        )

        return BaziEngine().execute(
            context
        )

    # =====================================================
    # Run Pattern
    # =====================================================

    def pattern(
        self,
        data: dict,
    ):

        context = self.create_context(
            data
        )

        return PatternEngine().execute(
            context
        )

    # =====================================================
    # Run Score
    # =====================================================

    def score(
        self,
        data: dict,
    ):

        context = self.create_context(
            data
        )

        return ScoreEngine().execute(
            context
        )

    # =====================================================
    # Run Interpretation
    # =====================================================

    def interpretation(
        self,
        data: dict,
    ):

        context = self.create_context(
            data
        )

        return InterpretationEngine().execute(
            context
        )

    # =====================================================
    # Run Report
    # =====================================================

    def report(
        self,
        data: dict,
    ):

        context = self.create_context(
            data
        )

        return ReportEngine().execute(
            context
        )
