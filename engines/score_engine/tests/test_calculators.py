import unittest

from engines.score_engine.calculators.wuxing_score import (
    WuxingScoreCalculator,
)


class TestCalculators(unittest.TestCase):

    def test_create(self):

        calc = WuxingScoreCalculator(None)

        self.assertEqual(
            calc.module_name,
            "wuxing"
        )


if __name__ == "__main__":
    unittest.main()
