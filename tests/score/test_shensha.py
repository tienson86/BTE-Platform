"""
Unit Test cho ShenshaScoreCalculator.
"""

import unittest

from engines.score_engine.loader import ScoreLoader
from engines.score_engine.context import ScoreContext
from engines.score_engine.calculators.shensha_score import (
    ShenshaScoreCalculator,
)


class TestShenshaScoreCalculator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.loader = ScoreLoader("database/13_score_engine")

    def test_shensha(self):

        calculator = ShenshaScoreCalculator(self.loader)

        result = calculator.safe_execute(ScoreContext())

        self.assertTrue(result.success)


if __name__ == "__main__":
    unittest.main()
