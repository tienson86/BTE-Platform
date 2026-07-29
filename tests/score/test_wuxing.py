"""
Unit Test cho WuxingScoreCalculator.
"""

import unittest

from engines.score_engine.loader import ScoreLoader
from engines.score_engine.context import ScoreContext
from engines.score_engine.calculators.wuxing_score import (
    WuxingScoreCalculator,
)


class TestWuxingScoreCalculator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.loader = ScoreLoader("database/13_score_engine")

    def setUp(self):
        self.context = ScoreContext()
        self.context.day_master = "Canh"
        self.context.strength = 75

    def test_calculate(self):

        calculator = WuxingScoreCalculator(self.loader)

        result = calculator.safe_execute(self.context)

        self.assertTrue(result.success)
        self.assertGreaterEqual(result.score, 0)
        self.assertLessEqual(result.score, 100)

    def test_rule_count(self):

        calculator = WuxingScoreCalculator(self.loader)

        result = calculator.safe_execute(self.context)

        self.assertGreaterEqual(result.rule_count, 0)


if __name__ == "__main__":
    unittest.main()
