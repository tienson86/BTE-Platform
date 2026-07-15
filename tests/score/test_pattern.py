"""
Unit Test cho PatternScoreCalculator.
"""

import unittest

from engines.score_engine.loader import ScoreLoader
from engines.score_engine.context import ScoreContext
from engines.score_engine.calculators.pattern_score import (
    PatternScoreCalculator,
)


class TestPatternScoreCalculator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.loader = ScoreLoader("database/13_score_engine")

    def test_pattern(self):

        calculator = PatternScoreCalculator(self.loader)

        result = calculator.safe_execute(ScoreContext())

        self.assertTrue(result.success)


if __name__ == "__main__":
    unittest.main()
