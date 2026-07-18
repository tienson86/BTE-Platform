from .engine import PatternEngine


class PatternCalculator:
    def __init__(self):
        self.engine = PatternEngine()

    def calculate(self, context):
        return self.engine.calculate(context)
