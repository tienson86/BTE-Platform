"""
Unit Test Julian Day.
"""

import unittest

from engines.calendar_engine.julian.julian import JulianDay


class TestJulianDay(unittest.TestCase):

    def test_from_gregorian(self):

        jd = JulianDay.from_gregorian(
            2025,
            6,
            18
        )

        self.assertIsInstance(jd, float)

    def test_to_gregorian(self):

        jd = JulianDay.from_gregorian(
            2025,
            6,
            18
        )

        year, month, day = JulianDay.to_gregorian(jd)

        self.assertEqual(year, 2025)
        self.assertEqual(month, 6)
        self.assertEqual(day, 18)

    def test_round_trip(self):

        jd = JulianDay.from_gregorian(
            2023,
            1,
            1
        )

        y, m, d = JulianDay.to_gregorian(jd)

        self.assertEqual((y, m, d), (2023, 1, 1))


if __name__ == "__main__":
    unittest.main()
