from .score_result import ScoreResult


class ScoreEngine:

    def __init__(self, loader):

        self.loader = loader

    def calculate(self, context):

        context.validate()

        result = ScoreResult()

        #
        # các calculator sẽ bổ sung ở bước sau
        #

        return result
