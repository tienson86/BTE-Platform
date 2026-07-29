import unittest

from engines.interpretation_engine.sentence_generator import (
    SentenceGenerator,
)


class TestSentenceGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = SentenceGenerator()

    def test_generate(self):
        text = self.generator.generate(
            {}
        )

        self.assertIsInstance(text, str)

    def test_not_none(self):
        self.assertIsNotNone(
            self.generator.generate({})
        )


if __name__ == "__main__":
    unittest.main()
