"""
Regression tests: solar → lunar must never equal solar Y/M/D copy.
"""

from __future__ import annotations

import unittest

from engines.calendar_engine.engine import CalendarEngine


class TestLunarRegressionCases(unittest.TestCase):
    """Minimum regression set from calendar bug investigation."""

    CASES = (
        (1987, 1, 21, 4, 30),
        (1990, 5, 15, 10, 0),
        (2000, 2, 5, 8, 0),
        (2026, 7, 26, 12, 0),
    )

    def setUp(self) -> None:
        self.engine = CalendarEngine()

    def test_solar_lunar_differ_and_print(self) -> None:
        for year, month, day, hour, minute in self.CASES:
            with self.subTest(solar=f"{year}-{month:02d}-{day:02d}"):
                result = self.engine.build(year, month, day, hour, minute)
                solar_ymd = (result.solar.year, result.solar.month, result.solar.day)
                lunar_ymd = (result.lunar.year, result.lunar.month, result.lunar.day)
                print(
                    f"Solar {day:02d}/{month:02d}/{year} {hour:02d}:{minute:02d}"
                    f" → Lunar {result.lunar.day:02d}/{result.lunar.month:02d}/"
                    f"{result.lunar.year} ({result.lunar.year_can_chi})"
                    f" leap={result.lunar.leap}"
                )
                self.assertNotEqual(solar_ymd, lunar_ymd)
                self.assertEqual(result.lunar_year, result.lunar.year)
                self.assertEqual(result.lunar_month, result.lunar.month)
                self.assertEqual(result.lunar_day, result.lunar.day)
                self.assertEqual(result.leap_month, result.lunar.leap)
                self.assertIsNotNone(result.solar_date)
                self.assertIsNotNone(result.lunar_date)
                self.assertNotEqual(result.solar_date, result.lunar_date)

    def test_known_1987_01_21(self) -> None:
        result = self.engine.build(1987, 1, 21, 4, 30)
        self.assertEqual(result.lunar_year, 1986)
        self.assertEqual(result.lunar_month, 12)
        self.assertEqual(result.lunar_day, 22)
        self.assertFalse(result.leap_month)
        self.assertEqual(result.lunar_date, "22/12/Bính Dần")
        self.assertEqual(result.solar_date, "21/01/1987")


if __name__ == "__main__":
    unittest.main()
