"""
Unit Test cho ScoreLoader.
"""

import unittest
from pathlib import Path

from engines.score_engine.loader import ScoreLoader


class TestScoreLoader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.database_path = Path("database") / "13_score_engine"
        cls.loader = ScoreLoader(cls.database_path)

    def test_loader_created(self):
        self.assertIsNotNone(self.loader)

    def test_database_exists(self):
        self.assertTrue(self.database_path.exists())

    def test_list_groups(self):
        groups = self.loader.list_groups()

        self.assertIsInstance(groups, list)
        self.assertGreater(len(groups), 0)

    def test_group_exists(self):
        self.assertTrue(
            self.loader.exists("02_wuxing")
        )

    def test_load_group(self):
        data = self.loader.load_group(
            "02_wuxing"
        )

        self.assertIsInstance(data, dict)
        self.assertGreater(len(data), 0)

    def test_cache(self):
        self.loader.load_group("02_wuxing")

        self.assertGreaterEqual(
            self.loader.cache_size(),
            1
        )

    def test_reload(self):
        self.loader.clear_cache()

        self.assertEqual(
            self.loader.cache_size(),
            0
        )

        self.loader.load_group("02_wuxing")

        self.assertGreater(
            self.loader.cache_size(),
            0
        )


if __name__ == "__main__":
    unittest.main()
