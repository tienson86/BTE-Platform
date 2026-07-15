import unittest

from engines.score_engine.loader import ScoreLoader


class TestScoreLoader(unittest.TestCase):

    def test_create_loader(self):

        loader = ScoreLoader("database/13_score_engine")

        self.assertIsNotNone(loader)

    def test_cache_exists(self):

        loader = ScoreLoader("database/13_score_engine")

        self.assertEqual(loader.cache, {})


if __name__ == "__main__":
    unittest.main()
