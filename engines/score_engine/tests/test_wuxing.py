import unittest

from engines.score_engine.loader import ScoreLoader
from engines.score_engine.context import ScoreContext
from engines.score_engine.calculators.wuxing_score import (
    WuxingScoreCalculator,
)


class TestWuxingCalculator(unittest.TestCase):

    def setUp(self):

        self.loader = ScoreLoader(
            "database/13_score_engine"
        )

        self.context = ScoreContext()

        #
        # Dữ liệu test
        #

        self.context.day_master = "Canh"

        self.context.season = "Winter"

        self.context.pattern = "ChinhQuan"

        self.context.strength = 72

    def test_calculate(self):

        calc = WuxingScoreCalculator(
            self.loader
        )

        result = calc.safe_execute(
            self.context
        )

        print(result.to_dict())

        self.assertTrue(result.success)

        self.assertGreaterEqual(
            result.score,
            0
        )

        self.assertLessEqual(
            result.score,
            100
        )


if __name__ == "__main__":

    unittest.main()
