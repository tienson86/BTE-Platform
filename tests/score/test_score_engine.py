"""
Integration Test cho ScoreEngine.
"""

import unittest

from engines.score_engine.engine import ScoreEngine
from engines.score_engine.loader import ScoreLoader
from engines.score_engine.context import ScoreContext


class TestScoreEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        loader = ScoreLoader("database/13_score_engine")
        cls.engine = ScoreEngine(loader)

    def test_engine_created(self):
        self.assertIsNotNone(self.engine)

    def test_calculate(self):

        context = ScoreContext()

        context.day_master = "Canh"
        context.strength = 75

        result = self.engine.calculate(context)

        self.assertTrue(result.success)

    def test_modules(self):

        context = ScoreContext()

        result = self.engine.calculate(context)

        self.assertGreaterEqual(
            len(result.modules),
            1
        )

    def test_total_score(self):

        context = ScoreContext()

        result = self.engine.calculate(context)

        self.assertGreaterEqual(
            result.total_score,
            0
        )

        self.assertLessEqual(
            result.total_score,
            100
        )


if __name__ == "__main__":
    unittest.main()
