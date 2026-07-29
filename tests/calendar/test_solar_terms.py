"""
Unit Test Tiết Khí.
"""

import unittest

from engines.calendar_engine.solar_terms.engine import SolarTermEngine


class TestSolarTerms(unittest.TestCase):

    def setUp(self):

        self.engine = SolarTermEngine()

    def test_find_term(self):

        term = self.engine.get_term(
            2025,
            6,
            21
        )

        self.assertIsNotNone(term)

    def test_list_year(self):

        terms = self.engine.list_terms(
            2025
        )

        self.assertEqual(
            len(terms),
            24
        )

    def test_current_term(self):

        term = self.engine.get_current_term(
            2025,
            6,
            18
        )

        self.assertIsNotNone(term)


if __name__ == "__main__":
    unittest.main()
