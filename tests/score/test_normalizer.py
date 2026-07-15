"""
Unit Test cho ScoreNormalizer.
"""

import unittest

from engines.score_engine.utils.normalizer import ScoreNormalizer


class TestScoreNormalizer(unittest.TestCase):

    def setUp(self):
        self.normalizer = ScoreNormalizer()

    def test_clamp_max(self):
        self.assertEqual(
            self.normalizer.clamp(120),
            100
        )

    def test_clamp_min(self):
        self.assertEqual(
            self.normalizer.clamp(-20),
            0
        )

    def test_clamp_normal(self):
        self.assertEqual(
            self.normalizer.clamp(75),
            75
        )

    def test_percentage(self):
        self.assertEqual(
            self.normalizer.percentage(
                50,
                100
            ),
            50
        )

    def test_weight(self):
        self.assertEqual(
            self.normalizer.weighted(
                80,
                0.5
            ),
            40
        )


if __name__ == "__main__":
    unittest.main()
