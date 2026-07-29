import unittest

from engines.interpretation_engine.engine import (
    InterpretationEngine,
)


class TestInterpretationEngine(unittest.TestCase):

    def setUp(self):
        self.engine = InterpretationEngine()

    def test_calculate(self):
        result = self.engine.calculate(
            {}
        )

        self.assertTrue(result.success)

    def test_text(self):
        result = self.engine.calculate(
            {}
        )

        self.assertIsInstance(
            result.text,
            str
        )


if __name__ == "__main__":
    unittest.main()
