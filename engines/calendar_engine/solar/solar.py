from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, order=True, slots=True)
class SolarDate:
    year: int
    month: int
    day: int

    def __post_init__(self):
        datetime(self.year, self.month, self.day)

    def is_leap_year(self) -> bool:
        return self.year % 400 == 0 or (self.year % 4 == 0 and self.year % 100 != 0)

    def days_in_month(self) -> int:
        if self.month == 12:
            return 31
        return (datetime(self.year + (self.month == 12), self.month % 12 + 1, 1) - datetime(self.year, self.month, 1)).days

    def to_datetime(self) -> datetime:
        return datetime(self.year, self.month, self.day)

    def __str__(self) -> str:
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"
