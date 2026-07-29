"""
Regression tests: Calendar Solar→Lunar + Bazi Tứ Trụ.

Critical case 1987-01-21 must match classical reference:
Âm lịch 22/12/1986, Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần.
"""

from __future__ import annotations

import unittest

from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.calendar_engine.julian.julian import JulianDay
from engines.calendar_engine.lunar.converter import solar_to_lunar
from engines.calendar_engine.solar_terms.engine import SolarTermEngine


class TestCriticalCase19870121(unittest.TestCase):
    """Blocker case from production audit."""

    def setUp(self) -> None:
        self.calendar = CalendarEngine()
        self.bazi = BaziEngine()
        self.terms = SolarTermEngine()

    def test_solar_to_lunar(self) -> None:
        parts = solar_to_lunar(21, 1, 1987)
        self.assertEqual(
            (parts.year, parts.month, parts.day, parts.leap),
            (1986, 12, 22, False),
        )

    def test_calendar_engine_lunar(self) -> None:
        result = self.calendar.build(1987, 1, 21, 3, 30)
        self.assertEqual(result.lunar_year, 1986)
        self.assertEqual(result.lunar_month, 12)
        self.assertEqual(result.lunar_day, 22)
        self.assertEqual(result.solar_term.name, "Đại Hàn")

    def test_four_pillars(self) -> None:
        chart = self.bazi.build(1987, 1, 21, 3, 30, gender="male")
        self.assertEqual(
            (chart.year_pillar.stem, chart.year_pillar.branch),
            ("Bính", "Dần"),
        )
        self.assertEqual(
            (chart.month_pillar.stem, chart.month_pillar.branch),
            ("Tân", "Sửu"),
        )
        self.assertEqual(
            (chart.day_pillar.stem, chart.day_pillar.branch),
            ("Canh", "Ngọ"),
        )
        self.assertEqual(
            (chart.hour_pillar.stem, chart.hour_pillar.branch),
            ("Mậu", "Dần"),
        )
        self.assertEqual(chart.day_master, "Canh")

    def test_four_pillars_hour_four_thirty(self) -> None:
        """Regression: 21/01/1987 04:30 — same hour pillar as 03:30."""
        chart = self.bazi.build(1987, 1, 21, 4, 30, gender="male")
        self.assertEqual(
            (chart.year_pillar.stem, chart.year_pillar.branch),
            ("Bính", "Dần"),
        )
        self.assertEqual(
            (chart.month_pillar.stem, chart.month_pillar.branch),
            ("Tân", "Sửu"),
        )
        self.assertEqual(
            (chart.day_pillar.stem, chart.day_pillar.branch),
            ("Canh", "Ngọ"),
        )
        self.assertEqual(
            (chart.hour_pillar.stem, chart.hour_pillar.branch),
            ("Mậu", "Dần"),
        )

    def test_ten_gods_are_not_stub(self) -> None:
        chart = self.bazi.build(1987, 1, 21, 3, 30, gender="male")
        self.assertEqual(chart.ten_gods[2], "Nhật Chủ")
        self.assertNotEqual(
            chart.ten_gods,
            ["Tỷ Kiên", "Tỷ Kiên", "Tỷ Kiên", "Tỷ Kiên"],
        )
        self.assertEqual(chart.ten_gods[3], "Thiên Ấn")

    def test_year_uses_li_chun_not_solar_year(self) -> None:
        """Trước Lập Xuân 1987 vẫn thuộc năm Bát Tự 1986."""
        self.assertFalse(self.terms.is_after_li_chun(1987, 1, 21))
        chart = self.bazi.build(1987, 1, 21, 3, 30)
        self.assertNotEqual(
            (chart.year_pillar.stem, chart.year_pillar.branch),
            ("Đinh", "Mão"),
        )

    def test_month_uses_solar_term_not_gregorian_month(self) -> None:
        month = self.terms.get_bazi_month(1987, 1, 21)
        self.assertEqual(month.branch, "Sửu")
        self.assertEqual(month.month_index, 12)

    def test_day_jdn(self) -> None:
        self.assertEqual(JulianDay.day_number(1987, 1, 21), 2446817)


class TestBaziRegressionCases(unittest.TestCase):
    """Additional boundary / regression dates requested by audit."""

    CASES = (
        # solar Y,M,D,H,Mi → year, month, day, hour pillars
        (
            (1987, 1, 21, 3, 30),
            ("Bính", "Dần"),
            ("Tân", "Sửu"),
            ("Canh", "Ngọ"),
            ("Mậu", "Dần"),
            (1986, 12, 22),
        ),
        (
            (1986, 12, 30, 12, 0),
            ("Bính", "Dần"),
            ("Canh", "Tý"),
            ("Mậu", "Thân"),
            ("Mậu", "Ngọ"),
            (1986, 11, 30),
        ),
        (
            (1987, 2, 5, 12, 0),
            ("Đinh", "Mão"),
            ("Nhâm", "Dần"),
            ("Ất", "Dậu"),
            ("Nhâm", "Ngọ"),
            (1987, 1, 8),
        ),
        (
            (1988, 2, 17, 12, 0),
            ("Mậu", "Thìn"),
            ("Giáp", "Dần"),
            ("Nhâm", "Dần"),
            ("Bính", "Ngọ"),
            (1988, 1, 1),
        ),
        (
            (2000, 2, 4, 12, 0),
            ("Canh", "Thìn"),
            ("Mậu", "Dần"),
            ("Nhâm", "Thìn"),
            ("Bính", "Ngọ"),
            (1999, 12, 29),
        ),
        (
            (2024, 2, 10, 12, 0),
            ("Giáp", "Thìn"),
            ("Bính", "Dần"),
            ("Giáp", "Thìn"),
            ("Canh", "Ngọ"),
            (2024, 1, 1),
        ),
    )

    def setUp(self) -> None:
        self.bazi = BaziEngine()
        self.calendar = CalendarEngine()

    def test_all_cases(self) -> None:
        for solar, year_p, month_p, day_p, hour_p, lunar in self.CASES:
            with self.subTest(solar=solar):
                y, m, d, h, mi = solar
                chart = self.bazi.build(y, m, d, h, mi)
                cal = self.calendar.build(y, m, d, h, mi)
                self.assertEqual(
                    (chart.year_pillar.stem, chart.year_pillar.branch),
                    year_p,
                )
                self.assertEqual(
                    (chart.month_pillar.stem, chart.month_pillar.branch),
                    month_p,
                )
                self.assertEqual(
                    (chart.day_pillar.stem, chart.day_pillar.branch),
                    day_p,
                )
                self.assertEqual(
                    (chart.hour_pillar.stem, chart.hour_pillar.branch),
                    hour_p,
                )
                self.assertEqual(
                    (cal.lunar.year, cal.lunar.month, cal.lunar.day),
                    lunar,
                )


class TestLiChunYearBoundary(unittest.TestCase):
    """Năm Bát Tự đổi tại Lập Xuân, không đổi tại 01/01."""

    def setUp(self) -> None:
        self.bazi = BaziEngine()
        self.terms = SolarTermEngine()

    def test_before_and_after_li_chun_1987(self) -> None:
        before = self.bazi.build(1987, 2, 3, 12, 0)
        after = self.bazi.build(1987, 2, 4, 12, 0)
        self.assertEqual(
            (before.year_pillar.stem, before.year_pillar.branch),
            ("Bính", "Dần"),
        )
        self.assertEqual(
            (after.year_pillar.stem, after.year_pillar.branch),
            ("Đinh", "Mão"),
        )
        self.assertFalse(self.terms.is_after_li_chun(1987, 2, 3))
        self.assertTrue(self.terms.is_after_li_chun(1987, 2, 4))


if __name__ == "__main__":
    unittest.main()
