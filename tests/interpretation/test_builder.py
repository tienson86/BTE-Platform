import unittest

from engines.interpretation_engine.builder import (
    InterpretationBuilder,
)


class TestBuilder(unittest.TestCase):

    def setUp(self):
        self.builder = InterpretationBuilder()

    def test_build(self):
        result = self.builder.build(
            {}
        )

        self.assertIsNotNone(result)

    def test_success(self):
        result = self.builder.build(
            {}
        )

        self.assertTrue(result.success)


if __name__ == "__main__":
    unittest.main()
