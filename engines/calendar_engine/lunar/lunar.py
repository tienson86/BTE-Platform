from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class LunarDate:
    year: int
    month: int
    day: int
    leap: bool = False

    def to_datetime(self) -> datetime:
        return datetime(self.year, self.month, self.day)
