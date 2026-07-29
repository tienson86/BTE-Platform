import unittest

from engines.pattern.engine import PatternEngine
from engines.pattern.context import PatternContext


class TestPatternEngine(unittest.TestCase):

    def setUp(self):
        self.engine = PatternEngine()

    def test_engine(self):
        result = self.engine.calculate(
            PatternContext()
        )

        self.assertTrue(result.success)

    def test_pattern(self):
        result = self.engine.calculate(
            PatternContext()
        )

        self.assertIsNotNone(result.pattern)


if __name__ == "__main__":
    unittest.main()
