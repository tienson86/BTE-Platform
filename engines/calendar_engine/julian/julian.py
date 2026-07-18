from datetime import datetime, timedelta


class JulianDay:
    @staticmethod
    def from_gregorian(year: int, month: int, day: int) -> float:
        return datetime(year, month, day).toordinal() + 1721424.5

    @staticmethod
    def to_gregorian(value: float) -> tuple[int, int, int]:
        dt = datetime.fromordinal(int(value - 1721424.5))
        return dt.year, dt.month, dt.day
