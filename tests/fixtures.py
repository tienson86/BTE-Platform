"""
Dữ liệu mẫu dùng cho Test.
"""

from dataclasses import dataclass


@dataclass
class SampleContext:

    day_master: str = "Canh"

    month_branch: str = "Sửu"

    season: str = "Winter"

    strength: float = 72.0

    pattern: str = "ChinhQuan"

    useful_god: str = "Fire"

    luck_score: float = 80.0


def create_context():

    return SampleContext()
