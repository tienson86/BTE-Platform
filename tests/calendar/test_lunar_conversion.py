"""
Unit tests for Vietnamese lunar conversion and CalendarEngine lunar fields.
"""

from __future__ import annotations

import unittest

from engines.calendar_engine.engine import CalendarEngine
from engines.calendar_engine.lunar.converter import solar_to_lunar


class TestSolarToLunar(unittest.TestCase):
    """Known Vietnamese lunar dates (UTC+7)."""

    def test_golden_1987_01_21(self) -> None:
        # Golden snapshot case_0001: 21/01/1987 → 22/12/1986
        parts = solar_to_lunar(21, 1, 1987)
        self.assertEqual((parts.day, parts.month, parts.year, parts.leap), (22, 12, 1986, False))

    def test_year_start(self) -> None:
        # 01/01/2025 dương → âm cuối năm Giáp Thìn
        parts = solar_to_lunar(1, 1, 2025)
        self.assertNotEqual((parts.year, parts.month, parts.day), (2025, 1, 1))
        self.assertEqual(parts.year, 2024)
        self.assertEqual(parts.month, 12)
        self.assertGreaterEqual(parts.day, 1)

    def test_mid_year(self) -> None:
        parts = solar_to_lunar(15, 6, 2025)
        self.assertNotEqual((parts.year, parts.month, parts.day), (2025, 6, 15))
        self.assertEqual(parts.year, 2025)
        self.assertGreaterEqual(parts.month, 1)
        self.assertLessEqual(parts.month, 12)

    def test_year_end(self) -> None:
        parts = solar_to_lunar(31, 12, 2025)
        self.assertNotEqual((parts.year, parts.month, parts.day), (2025, 12, 31))
        self.assertEqual(parts.year, 2025)
        self.assertEqual(parts.month, 11)

    def test_tet_2024(self) -> None:
        # Tết Giáp Thìn: 10/02/2024 dương = 01/01/2024 âm
        parts = solar_to_lunar(10, 2, 2024)
        self.assertEqual((parts.day, parts.month, parts.year, parts.leap), (1, 1, 2024, False))

    def test_leap_month_2020(self) -> None:
        # 2020 có tháng 4 nhuận; 23/05/2020 ≈ mùng 1 tháng 4 nhuận
        parts = solar_to_lunar(23, 5, 2020)
        self.assertEqual(parts.month, 4)
        self.assertTrue(parts.leap)


class TestCalendarEngineLunar(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = CalendarEngine()

    def test_lunar_differs_from_solar(self) -> None:
        result = self.engine.build(1987, 1, 21, 4, 30)
        self.assertNotEqual(
            (result.lunar.year, result.lunar.month, result.lunar.day),
            (result.solar.year, result.solar.month, result.solar.day),
        )
        self.assertEqual(result.lunar_year, 1986)
        self.assertEqual(result.lunar_month, 12)
        self.assertEqual(result.lunar_day, 22)
        self.assertEqual(result.solar_date, "21/01/1987")
        self.assertEqual(result.lunar_date, "22/12/1986")
        self.assertEqual(result.lunar.year_can_chi, "Bính Dần")

    def test_api_flat_fields_year_edges(self) -> None:
        start = self.engine.build(2025, 1, 1)
        mid = self.engine.build(2025, 6, 15)
        end = self.engine.build(2025, 12, 31)
        for result in (start, mid, end):
            self.assertIsNotNone(result.lunar_year)
            self.assertIsNotNone(result.lunar_month)
            self.assertIsNotNone(result.lunar_day)
            self.assertIsNotNone(result.solar_date)
            self.assertIsNotNone(result.lunar_date)
            self.assertNotEqual(result.solar_date, result.lunar_date)


if __name__ == "__main__":
    unittest.main()
