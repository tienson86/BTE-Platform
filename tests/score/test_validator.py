"""
Unit Test cho ScoreValidator.
"""

import unittest

import pandas as pd

from engines.score_engine.utils.validator import ScoreValidator


class TestScoreValidator(unittest.TestCase):

    def setUp(self):
        self.validator = ScoreValidator()

    def test_valid_dataframe(self):

        df = pd.DataFrame({

            "rule_code": ["R001"],

            "condition": [

                "strength >= 70"

            ],

            "score": [10]

        })

        self.assertTrue(

            self.validator.validate_dataframe(df)

        )

    def test_missing_column(self):

        df = pd.DataFrame({

            "condition": [

                "strength >= 70"

            ]

        })

        with self.assertRaises(Exception):

            self.validator.validate_dataframe(df)

    def test_empty_dataframe(self):

        df = pd.DataFrame()

        with self.assertRaises(Exception):

            self.validator.validate_dataframe(df)

    def test_none_dataframe(self):

        with self.assertRaises(Exception):

            self.validator.validate_dataframe(None)


if __name__ == "__main__":
    unittest.main()
