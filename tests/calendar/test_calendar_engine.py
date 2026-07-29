"""
Integration Test Calendar Engine.
"""

import unittest

from engines.calendar_engine.engine import CalendarEngine


class TestCalendarEngine(unittest.TestCase):

    def setUp(self):

        self.engine = CalendarEngine()

    def test_build_calendar(self):

        result = self.engine.build(
            year=2025,
            month=6,
            day=18,
            hour=10,
            minute=30
        )

        self.assertIsNotNone(result)

    def test_solar_date(self):

        result = self.engine.build(
            2025,
            6,
            18
        )

        self.assertIsNotNone(
            result.solar
        )

    def test_lunar_date(self):

        result = self.engine.build(
            2025,
            6,
            18
        )

        self.assertIsNotNone(
            result.lunar
        )

    def test_julian(self):

        result = self.engine.build(
            2025,
            6,
            18
        )

        self.assertIsNotNone(
            result.julian_day
        )

    def test_solar_term(self):

        result = self.engine.build(
            2025,
            6,
            18
        )

        self.assertIsNotNone(
            result.solar_term
        )


if __name__ == "__main__":
    unittest.main()
