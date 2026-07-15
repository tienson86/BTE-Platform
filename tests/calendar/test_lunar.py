"""
Unit Test cho LunarDate.
"""

import unittest
from datetime import datetime

from engines.calendar_engine.lunar.lunar import LunarDate


class TestLunarDate(unittest.TestCase):

    def test_create_lunar_date(self):
        lunar = LunarDate(
            year=2025,
            month=5,
            day=15,
            leap=False
        )

        self.assertEqual(lunar.year, 2025)
        self.assertEqual(lunar.month, 5)
        self.assertEqual(lunar.day, 15)
        self.assertFalse(lunar.leap)

    def test_leap_month(self):
        lunar = LunarDate(
            year=2025,
            month=6,
            day=1,
            leap=True
        )

        self.assertTrue(lunar.leap)

    def test_string(self):
        lunar = LunarDate(
            2025,
            5,
            15,
            False
        )

        self.assertIsInstance(str(lunar), str)

    def test_to_datetime(self):
        lunar = LunarDate(
            2025,
            5,
            15,
            False
        )

        dt = lunar.to_datetime()

        self.assertIsInstance(dt, datetime)


if __name__ == "__main__":
    unittest.main()
