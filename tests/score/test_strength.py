"""
Unit Test cho StrengthScoreCalculator.
"""

import unittest

from engines.score_engine.loader import ScoreLoader
from engines.score_engine.context import ScoreContext
from engines.score_engine.calculators.strength_score import (
    StrengthScoreCalculator,
)


class TestStrengthScoreCalculator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.loader = ScoreLoader("database/13_score_engine")

    def test_strength(self):

        context = ScoreContext()
        context.day_master = "Canh"

        calculator = StrengthScoreCalculator(self.loader)

        result = calculator.safe_execute(context)

        self.assertTrue(result.success)
        self.assertGreaterEqual(result.score, 0)
        self.assertLessEqual(result.score, 100)


if __name__ == "__main__":
    unittest.main()
