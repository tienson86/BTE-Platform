from datetime import datetime


class JulianDay:
    """Chuyển đổi Gregorian ↔ Julian Day."""

    @staticmethod
    def from_gregorian(year: int, month: int, day: int) -> float:
        """
        Julian Date tại 00:00 UTC của ngày dân sự.

        Dùng cho timestamp lịch; Can Chi ngày nên dùng ``day_number``.
        """
        return datetime(year, month, day).toordinal() + 1721424.5

    @staticmethod
    def day_number(year: int, month: int, day: int) -> int:
        """
        Julian Day Number (mốc trưa, số nguyên) dùng cho Can Chi ngày.

        Tương đương công thức Hồ Ngọc Đức ``jdFromDate``.
        """
        return datetime(year, month, day).toordinal() + 1721425

    @staticmethod
    def to_gregorian(value: float) -> tuple[int, int, int]:
        dt = datetime.fromordinal(int(value - 1721424.5))
        return dt.year, dt.month, dt.day
