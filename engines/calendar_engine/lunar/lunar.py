from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class LunarDate:
    year: int
    month: int
    day: int
    leap: bool = False
    year_can_chi: str | None = None

    def to_datetime(self) -> datetime:
        return datetime(self.year, self.month, self.day)

    def to_dict(self) -> dict[str, Any]:
        """Serialize lunar date for API / Portal."""
        data: dict[str, Any] = {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "leap": self.leap,
        }
        if self.year_can_chi:
            data["year_can_chi"] = self.year_can_chi
        return data
