"""
Unit Test cho UsefulGodScoreCalculator.
"""

import unittest

from engines.score_engine.loader import ScoreLoader
from engines.score_engine.context import ScoreContext
from engines.score_engine.calculators.useful_god_score import (
    UsefulGodScoreCalculator,
)


class TestUsefulGodScoreCalculator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.loader = ScoreLoader("database/13_score_engine")

    def test_useful_god(self):

        calculator = UsefulGodScoreCalculator(self.loader)

        result = calculator.safe_execute(ScoreContext())

        self.assertTrue(result.success)


if __name__ == "__main__":
    unittest.main()
