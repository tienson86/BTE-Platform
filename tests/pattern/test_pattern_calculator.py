import unittest

from engines.pattern.calculator import PatternCalculator
from engines.pattern.context import PatternContext


class TestPatternCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = PatternCalculator()

    def test_calculate(self):
        result = self.calculator.calculate(
            PatternContext()
        )

        self.assertIsNotNone(result)

    def test_score(self):
        result = self.calculator.calculate(
            PatternContext()
        )

        self.assertGreaterEqual(result.score, 0)


if __name__ == "__main__":
    unittest.main()
