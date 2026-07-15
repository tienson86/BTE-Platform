"""
Kiểm thử toàn bộ Pipeline.
"""

import unittest

from engines.calendar_engine.engine import CalendarEngine
from engines.bazi_engine.engine import BaziEngine
from engines.score_engine.engine import ScoreEngine
from engines.pattern.engine import PatternEngine
from engines.interpretation_engine.engine import InterpretationEngine
from engines.report_engine.engine import ReportEngine


class TestPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.calendar = CalendarEngine()
        cls.bazi = BaziEngine()
        cls.score = ScoreEngine()
        cls.pattern = PatternEngine()
        cls.interpretation = InterpretationEngine()
        cls.report = ReportEngine()

    def test_full_pipeline(self):

        calendar = self.calendar.build(
            year=1987,
            month=1,
            day=21,
            hour=4,
            minute=10
        )

        self.assertIsNotNone(calendar)

        chart = self.bazi.build(calendar)

        self.assertIsNotNone(chart)

        score = self.score.calculate(chart)

        self.assertTrue(score.success)

        pattern = self.pattern.calculate(chart)

        self.assertTrue(pattern.success)

        interpretation = self.interpretation.calculate(
            chart,
            score,
            pattern
        )

        self.assertTrue(interpretation.success)

        report = self.report.generate(
            chart,
            score,
            pattern,
            interpretation
        )

        self.assertTrue(report.success)


if __name__ == "__main__":
    unittest.main()
