import unittest

from engines.score_engine.utils.normalizer import ScoreNormalizer


class TestNormalizer(unittest.TestCase):

    def test_clamp(self):

        self.assertEqual(
            ScoreNormalizer.clamp(120),
            100
        )

        self.assertEqual(
            ScoreNormalizer.clamp(-20),
            0
        )

        self.assertEqual(
            ScoreNormalizer.clamp(50),
            50
        )


if __name__ == "__main__":
    unittest.main()
