"""
Kiểm tra tính toàn vẹn của Database.
"""

import unittest
from pathlib import Path


class TestDatabaseIntegrity(unittest.TestCase):

    def test_database_exists(self):

        self.assertTrue(
            Path("database").exists()
        )

    def test_score_database(self):

        self.assertTrue(

            Path(
                "database/13_score_engine"
            ).exists()

        )

    def test_rule_database(self):

        self.assertTrue(

            Path(
                "database/07_rule_database"
            ).exists()

        )
