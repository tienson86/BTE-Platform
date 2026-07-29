from dataclasses import dataclass
from typing import Any


@dataclass
class ScoreContext:
    """
    Dữ liệu đầu vào cho Score Engine.
    """

    bazi_chart: Any = None

    pattern_result: Any = None

    useful_god_result: Any = None

    shensha_result: Any = None

    luck_result: Any = None

    metadata: dict = None

    def validate(self):

        return True
