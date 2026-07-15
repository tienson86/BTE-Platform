"""
Unit Test cho Solar Date.

Kiểm thử:

- Khởi tạo ngày dương
- Kiểm tra năm nhuận
- Kiểm tra số ngày trong tháng
- Chuyển sang datetime
- So sánh ngày
"""

import unittest
from datetime import datetime

from engines.calendar_engine.solar.solar import SolarDate


class TestSolarDate(unittest.TestCase):

    def test_create_date(self):
        """Khởi tạo ngày hợp lệ"""

        solar = SolarDate(
            year=2024,
            month=5,
            day=20
        )

        self.assertEqual(solar.year, 2024)
        self.assertEqual(solar.month, 5)
        self.assertEqual(solar.day, 20)

    def test_leap_year_true(self):
        """Năm nhuận"""

        solar = SolarDate(
            2024,
            1,
            1
        )

        self.assertTrue(
            solar.is_leap_year()
        )

    def test_leap_year_false(self):
        """Không phải năm nhuận"""

        solar = SolarDate(
            2023,
            1,
            1
        )

        self.assertFalse(
            solar.is_leap_year()
        )

    def test_days_in_month_31(self):
        """Tháng có 31 ngày"""

        solar = SolarDate(
            2025,
            1,
            1
        )

        self.assertEqual(
            solar.days_in_month(),
            31
        )

    def test_days_in_month_30(self):
        """Tháng có 30 ngày"""

        solar = SolarDate(
            2025,
            4,
            1
        )

        self.assertEqual(
            solar.days_in_month(),
            30
        )

    def test_days_in_february_leap(self):
        """Tháng 2 năm nhuận"""

        solar = SolarDate(
            2024,
            2,
            1
        )

        self.assertEqual(
            solar.days_in_month(),
            29
        )

    def test_days_in_february_normal(self):
        """Tháng 2 năm thường"""

        solar = SolarDate(
            2023,
            2,
            1
        )

        self.assertEqual(
            solar.days_in_month(),
            28
        )

    def test_to_datetime(self):
        """Chuyển sang datetime"""

        solar = SolarDate(
            2025,
            6,
            18
        )

        dt = solar.to_datetime()

        self.assertIsInstance(
            dt,
            datetime
        )

        self.assertEqual(
            dt.year,
            2025
        )

    def test_compare(self):
        """So sánh ngày"""

        a = SolarDate(
            2024,
            1,
            1
        )

        b = SolarDate(
            2025,
            1,
            1
        )

        self.assertTrue(a < b)
        self.assertTrue(b > a)

    def test_string(self):
        """Kiểm tra chuỗi"""

        solar = SolarDate(
            2025,
            12,
            31
        )

        self.assertEqual(
            str(solar),
            "2025-12-31"
        )


if __name__ == "__main__":

    unittest.main()
