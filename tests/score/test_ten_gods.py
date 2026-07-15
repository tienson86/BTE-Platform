"""
Unit Test cho TenGodScoreCalculator.
"""

import unittest

from engines.score_engine.loader import ScoreLoader
from engines.score_engine.context import ScoreContext
from engines.score_engine.calculators.ten_god_score import (
    TenGodScoreCalculator,
)


class TestTenGodScoreCalculator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.loader = ScoreLoader("database/13_score_engine")

    def test_calculate(self):

        calculator = TenGodScoreCalculator(self.loader)

        result = calculator.safe_execute(ScoreContext())

        self.assertTrue(result.success)
        self.assertGreaterEqual(result.score, 0)


if __name__ == "__main__":
    unittest.main()
