from pathlib import Path

from .score_context import ScoreContext
from .score_engine import ScoreEngine
from .score_loader import ScoreLoader


class ScoreService:
    """
    API bên ngoài sử dụng.
    """

    def __init__(self, database_path):

        self.loader = ScoreLoader(database_path)

        self.engine = ScoreEngine(self.loader)

    def score(
        self,
        bazi_chart,
        pattern_result=None,
        useful_god_result=None,
        shensha_result=None,
        luck_result=None
    ):

        context = ScoreContext(
            bazi_chart=bazi_chart,
            pattern_result=pattern_result,
            useful_god_result=useful_god_result,
            shensha_result=shensha_result,
            luck_result=luck_result
        )

        return self.engine.calculate(context)
